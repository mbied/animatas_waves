import numpy as np
from gym import Env
from gym.spaces import Box, Tuple, Discrete, Dict
import yaml
from itertools import permutations



def eval_wave(x, amplitude, frequency, offset=0, phase=0):
    return amplitude * np.sin(2*np.pi*frequency*x + phase) + offset

def squared_loss(x, x_target):
    return -sum((x-x_target)**2)


class DiscreteWavesGridWorld(Env):
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
    #target_wave = np.array([[eval_wave(x,wave_params[0],wave_params[1]) 
                           # for x in np.linspace(0, 1, 1000)]
                           # for wave_params in target_state])
    

    def __init__(self, num_sum=2, target_state = np.array([2, 3, 5, 7]), discretization = 10):
        """

        """
        super().__init__()
        self.target_state = target_state
        self.num_sum = num_sum
        self.state = np.ones(2*num_sum, dtype=np.int64)    
        self.discretization = discretization
        
        
        # Set these in ALL subclasses
        self.action_space = Discrete(2*2*num_sum)
        self.action_availability = np.ones(2*2*num_sum,dtype=bool)
        #print(np.logical_and(self.action_availability, testarray))
        print("DiscreteWavesGridWorld initalized.")

            
        

    def step(self, action):
        """
        """
        if not self.action_availability[action]:
            raise Exception("Action %s is not in action space for this state." % action)


        self.state = self._calc_next_state(self, action)
        self.set_action_availabilty()
        observation = self.state
        reward = self._calc_reward()
        if reward == 0:
            done = True
        else:
            done = False
                
        return observation, reward, done, None

    def reset(self, task_params=None):
        """
        """
        self.state = np.zeros(2*self.num_sum, dtype=np.int64)
        self.set_action_availabilty()
        observation = self.state
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
    
    def set_action_availabilty(self):
        availability = np.ones(2*2*self.num_sum,dtype=bool)
        for s in range(0, len(self.state)):
            if self.state[s] == 0:
                availability[self.num_sum*s+1] = False
            if self.state[s] == 9:
                availability[self.num_sum*s] = False                      
        self.action_availability = availability
        return

    @property
    def unwrapped(self):
        return self

    def __str__(self):
        if self.spec is None:
            return '<{} instance>'.format(type(self).__name__)
        else:
            return '<{}<{}>>'.format(type(self).__name__, self.spec.id)
        
    def _calc_state_delta(self, action):
        state_delta = np.zeros(len(self.state))
        changed_param = action // self.num_sum
        
        if (action % self.num_sum) == 0:
            change_value = 1
        else:
            change_value = -1
            
        state_delta[changed_param] = change_value
        #print("State delta is: %s", state_delta)
        return state_delta
        

    def _calc_next_state(self, state, action):
        state_delta = self._calc_state_delta(action)
        next_state = self.state + state_delta
        #TODO check if next state is legal before returning
        #print("Next state is: %s", next_state)
        return next_state
        
    def _calc_reward(self):
        x = np.linspace(0, 1, 1000)
        #state_waves = np.array([[eval_wave(x,wave_params[0],wave_params[1]) 
                            #for x in np.linspace(0, 1, 1000)]
                            #for wave_params in self.state])   
        #reward = squared_loss(self.target_wave, state_waves)
        reward = squared_loss(self.target_state, self.state)
        return reward
        

        

if __name__ == "__main__":
    a = DiscreteWavesGridWorld()
    observation = a.reset()
    print(observation)
    observation, reward, done, _ = a.step(0)
    print(observation, reward)
    observation, reward, done, _ = a.step(1)
    print(observation, reward)
    observation, reward, done, _ = a.step(2)
    print(observation, reward)
