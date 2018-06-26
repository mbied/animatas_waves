import numpy as np
from gym import Env
from gym.spaces import Box, Tuple, Discrete, Dict
import yaml
from itertools import permutations

N = 10  # number of waves in base set
num_sum = 3  # maximum number of elements in sum of waves

def eval_wave(x, amplitude, frequency, offset=0, phase=0):
    return amplitude * np.sin(2*np.pi*frequency*x + phase) + offset


class DiscreteWaves(Env):
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
    reward_range = (-1, 1)
    spec = None

    def __init__(self, N=50, num_sum=3):
        """

        """

        super().__init__()

        self.state = np.zeros(3, dtype=np.int64)
        self.current_target = np.zeros(3, dtype=np.int64)
        base = np.hstack((np.ones((N+1,1)),np.random.randint(0,20,size=(N+1,1))/10,np.zeros((N+1, 1))))
        base[0,:] = 0
        self._set_base(base)
            
        

    def step(self, action):
        """Select a wave for a slot. Action is a 2-tuple of a base wave index
           and a slot. It returns the current observation, reward and if the
           environment has completed.

           Returns:
                observation: dict with keys "target", "current", "waves" where
                "target" is the wave to be created, "current" is the product of the
                currently selected waves and "waves" is a collection of 
                representations of the base wave
           
           Example: action=(5, 3)
           Meaning: Select base_wave[5] for the slot with index 3.

           Note: Slots can be deselected / emptied using (0,<slot_idx>) which
           is guaranteed to be a wave with amplitude 0.
        """
        if not self.action_space.contains(action):
            raise Exception("Action %s is not in action space." % action)

        self.state[action[1]] = action[0]
        observation = {
            "target": np.sum(self.base_graph[self.current_target, :], axis=0),
            "current": np.sum(self.base_graph[self.state, :], axis=0),
            "waves": self.base_graph
        }

        valid_combinations = np.array(list(permutations(self.current_target)))
        if np.any(np.all(valid_combinations == self.state, axis=1)):
            reward = 0
            done = True
            print("Done is True")
        else:
            reward = -1
            done = False

        return observation, reward, done, None

    def reset(self, task_params=None):
        """Choose a new target wave and reset the current state.
        """
        task_file = None
        if task_file is None:
            self.current_target = np.random.randint(0, self.base_graph.shape[0], size=3, dtype=np.int64)
            self.state = np.zeros(3, dtype=np.int64)
        else:
            self.current_target = task_params["target"]
            self.state = task_params["state"]
            self._set_base(task_params["base"])

        observation = {
            "target": np.sum(self.base_graph[self.current_target, :], axis=0),
            "current": np.sum(self.base_graph[self.state, :], axis=0),
            "waves": self.base_graph
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
        return

    @property
    def unwrapped(self):
        return self

    def __str__(self):
        if self.spec is None:
            return '<{} instance>'.format(type(self).__name__)
        else:
            return '<{}<{}>>'.format(type(self).__name__, self.spec.id)

    def _set_base(self, base):
        idx = np.lexsort((base[:,0],base[:,1]))
        base = base[idx,:]

        self.base_graph = np.array([[eval_wave(x, a, omega)
                                    for x in np.linspace(0, 5, 1000)]
                                    for a, omega, phase in base])

        # Set these in ALL subclasses
        wave_space = Box(low=-1e6*np.ones(1000), high=1e6*np.ones(1000))
        self.action_space = Tuple((Discrete(N+1), Discrete(num_sum)))
        self.observation_space = Dict({
                                "target": wave_space,
                                "current": wave_space,
                                "waves": Box(low=-1e2*np.ones((N+1, 1000)),
                                             high=1e2*np.ones((N+1, 1000)))})

if __name__ == "__main__":
    a = DiscreteWaves()
    a.reset()
    a.step((5, 0))
