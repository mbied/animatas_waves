import numpy as np
from gym import Env
from gym.spaces import Box, Tuple, Discrete, Dict

import waveSelectionUI as ws

def eval_wave(x, amplitude, frequency, offset=0, phase=0):
    return amplitude * np.sin(2*np.pi*frequency*x + phase) + offset

class InteractiveWaves(object):
    """The main OpenAI Gym class. It encapsulates an environment with
    arbitrary behind-the-scenes dynamics. An environment can be
    partially or fully observed.
    The main API methods that users of this class need to know are:
        step
        reset
        render
        close
        seed
    And set the following attributes:
        action_space: The Space object corresponding to valid actions
        observation_space: The Space object corresponding to valid observations
        reward_range: A tuple corresponding to the min and max possible rewards
    Note: a default reward range set to [-inf,+inf] already exists. Set it if you want a narrower range.
    The methods are accessed publicly as "step", "reset", etc.. The
    non-underscored versions are wrapper methods to which we may add
    functionality over time.
    """

    # Set this in SOME subclasses
    metadata = {'render.modes': []}
    reward_range = (-float('inf'), float('inf'))
    spec = None

    # Set these in ALL subclasses
    action_space = None
    observation_space = None
    
    def __init__(self, N=10, num_sum=2, max_amplitude=5, max_f=10, ):
        """

        """

        super().__init__()
        self.N = N
        self.num_sum = num_sum
        self.max_amplitude = max_amplitude
        self.max_f = max_f


        self.state = np.zeros(4, dtype=np.int64)
        self.idx_chosen_waves = np.zeros(2, dtype=np.int64)
        # [amplitude, frequency, phaseshift]
        base = np.hstack((np.random.randint(0,max_amplitude, size=(N+1,1)),np.random.randint(0,max_f,size=(N+1,1)),np.zeros((N+1, 1))))
        base[0,:] = 0
        self._set_base(base)
        
        self.wave_select = ws.waveSelect()

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).
        Args:
            action (object): an action provided by the environment
        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        
        self.state = action

        action_graphs = np.array([[eval_wave(x,wave_params[0],wave_params[1]) 
                            for x in np.linspace(0, 5, 1000)]
                            for wave_params in self.state])
        
        observation = {
            "target": np.sum(self.base_graph[self.idx_chosen_waves, :], axis=0),
            "current": np.sum(action_graphs,axis=0)
        }
        
        done = False # when to end interaction?
        
        reward = 0 # request from user
        
        return observation, reward, done, None

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns: observation (object): the initial observation of the
            space.
        """
        idx1, idx2 = 1, 2 # = request_target(self.base_graph)        
        self.idx_chosen_waves = np.array([idx1, idx2])
        
        # just some random chosen hard copied values for a start, decide later how to set them properly
        a1,f1 = 1, 0.5
        a2,f2 = 2, 2
        self.state = np.array([[a1,f1],[a2,f2]])

        action_graphs = np.array([[eval_wave(x,wave_params[0],wave_params[1]) 
                            for x in np.linspace(0, 5, 1000)]
                            for wave_params in self.state])
        
        self.wave_select.choose_waves(self.base_graph)

        observation = {
            "target": np.sum(self.base_graph[self.idx_chosen_waves, :], axis=0),
            "current": np.sum(action_graphs,axis=0)
        }
        
        
        
        
        return observation

    def render(self, mode='human'):
        """Renders the environment.
        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).
        Note:
            Make sure that your class's metadata 'render.modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.
        Args:
            mode (str): the mode to render with
            close (bool): close all open renderings
        Example:
        class MyEnv(Env):
            metadata = {'render.modes': ['human', 'rgb_array']}
            def render(self, mode='human'):
                if mode == 'rgb_array':
                    return np.array(...) # return RGB frame suitable for video
                elif mode is 'human':
                    ... # pop up a window and render
                else:
                    super(MyEnv, self).render(mode=mode) # just raise an exception
        """
        raise NotImplementedError

    def close(self):
        """Override _close in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        return

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).
        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.
        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        logger.warn("Could not seed environment %s", self)
        return

    @property
    def unwrapped(self):
        """Completely unwrap this env.
        Returns:
            gym.Env: The base non-wrapped gym.Env instance
        """
        return self

    def __str__(self):
        if self.spec is None:
            return '<{} instance>'.format(type(self).__name__)
        else:
            return '<{}<{}>>'.format(type(self).__name__, self.spec.id)
        
    def _set_base(self, base):
        idx = np.lexsort((base[:,0],base[:,1]))
        base = base[idx,:]

        self.base_graph = np.array([[eval_wave(x, a, f)
                                    for x in np.linspace(0, 5, 1000)]
                                    for a, f, phase in base])

        # Set these in ALL subclasses
        wave_space = Box(low=-1e6*np.ones(1000), high=1e6*np.ones(1000))
       
        #self.action_space = Tuple((Discrete(self.N+1), Discrete(self.num_sum)))
        # implement more generic
        self.action_space= Box(low=np.zeros(2*self.num_sum), high=np.array([self.max_amplitude, self.max_f, self.max_amplitude, self.max_f]))
        self.observation_space = Dict({
                                "target": wave_space,
                                "current": wave_space})


if __name__ == "__main__":
    pass
