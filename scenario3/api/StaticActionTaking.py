from DiscreteWavesGridWorld import DiscreteWavesGridWorld
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import copy

class StaticActionTaking:
    
    def __init__(self, env, alpha=.95, gamma=.7, epsilon=0, state_action_dimensions = np.array([10,10,10,10,8])):
        # the parameters are not used, they are only added for compatibility with QLearning
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = np.zeros(state_action_dimensions) 
        self.env = env
        self.givenFeedback = np.full(np.prod(state_action_dimensions), np.nan)
        self.state_action_dimensions = state_action_dimensions
        #print(state_action_dimensions)
        #print(state_action_dimensions.size)
        #self.givenFeedback = np.full(8000, np.nan)
        #np.reshape(self.givenFeedback, 8000)
        print(self.givenFeedback)
        print("StaticActionTaking initiated.")
        
    #def encode_action(state_delta):
    #    action = 0
        
    #    if 'wave2' in dict_guidance_action:
    #        action += 4
        
    #    wave = list(dict_guidance_action.keys())[0]
        
    #    if 'frequency' in dict_guidance_action[wave]:
    #        action += 2
            
    #    param = list(dict_guidance_action[wave].keys())[0]    
        #print(param)
        
    #    if dict_guidance_action[wave][param] == -1:
    #    action += 1
        #print(dict_guidance_action[wave])
        
    #    return action
    
    def _getIndex(self, state, action):
        multi_index = np.full((state.size+1,1), 1)
        for index, value in np.ndenumerate(state):
            multi_index[index][0] = value
        multi_index[-1][0] = action
        print(multi_index)
        #return 934
        ret_val = np.ravel_multi_index(multi_index, self.state_action_dimensions)
        print(ret_val)
        return ret_val
        
    def load_Q_table(self,file_path):
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        Q_new = json.loads(obj_text)
        self.Q = np.array(Q_new)
        
    def store_Q_table(self,file_path):
        Q_new = Q.tolist() # nested lists with same data, indices
        json.dump(Q_new, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
    
    def chose_action(self, guidance_feedback=None):     
        if guidance_feedback == None:
            # with probability p = epsilon a random 'wrong' action is selected
            r = np.random.rand()
            if r > 1 - self.epsilon:
                pass
            # chose step towards goal        
            else:
                action_availability = self.env.action_availability
                state_delta = self.env.target_state-self.env.state
                action_list = np.array(0)
                for i in range(4):
                    sub_state_delta = np.zeros(4)
                    if state_delta[i] > 0:
                        sub_state_delta[i] = 1
                    elif state_delta[i] < 0:
                        sub_state_delta[i] = -1
                    action = self.env.decode_state_delta(sub_state_delta)
                    action_list = np.append(action_list, action)
   
                action_list_backup = action_list
                remove_indices = np.array(0)
                
                for index, action in enumerate(action_list):
                    if self.givenFeedback[self._getIndex(self.env.state, action)] == -1:
                        remove_indices = np.append(remove_indices, action)
                        
                if len(action_list) > len(remove_indices):
                    action_list = np.delete(action_list, remove_indices)
                else:
                    action_list = np.delete(action_list, 0) 
                    
                print('action_list')
                print(action_list)
                    
                    
                    
                    
                action = action_list[randint(0, len(action_list)-1)]
                
        else:
            if self.env.action_availability[guidance_feedback]:
                action = guidance_feedback
            else:
                raise Exception('The guided action is not available in that state. The guiden action was: {}'.format(action))
            
        return action
        
    def update_Q_function(self,state, next_state, action, reward):
        index = self._getIndex(state, action)
        self.givenFeedback[index] = reward


if __name__ == "__main__":
    env = DiscreteWavesGridWorld()
    qLearning = QLearning(env)
    N = 1000
    
    for episode in range(0,N):
        state = env.reset()
        done = False
        i = 0
        cum_reward = 0    
        while not done:
            action = qLearning.chose_action()
            next_state, reward, done, _ = env.step(action)
            qLearning.update_Q_function(state, next_state, action, reward)
            cum_reward += reward            
            i += 1
            state = next_state

        if episode == 0:
            cum_rewards = np.array([cum_reward])
        else:
            cum_rewards = np.append(cum_rewards, np.array([cum_reward]))
            
        print("Episode {} done after {} steps".format(episode, i))

    
    plt.plot(cum_rewards)
    plt.show()
