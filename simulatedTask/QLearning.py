from DiscreteWavesGridWorld import DiscreteWavesGridWorld
import numpy as np
import matplotlib.pyplot as plt
import copy

class QLearning:
    
    def __init__(self, env, alpha=.95, gamma=.7, epsilon=0, state_action_dimensions = [10,10,10,10,8]):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = np.zeros(state_action_dimensions) 
        self.env = env
    
    def load_Q_table(self,file_path):
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        Q_new = json.loads(obj_text)
        self.Q = np.array(Q_new)
        
    
    def chose_action(self, guidance_feedback=None):     
        if guidance_feedback == None:
            # with probability p = epsilon a random action is selected
            r = np.random.rand()
            if r > 1 - self.epsilon:
                action_legit = False
                while not action_legit:
                    action = np.random.randint(0, 8,size=1)[0]
                    action_legit = self.env.action_availability[action]
                    
            else:
                s = self.env.state
                #print(env.state)
                #print(s[0],s[1],s[2],s[3])
                Q_temp = self.Q[int(s[0]),int(s[1]),int(s[2]),int(s[3]),:] # TODO: change to generic implementation
                Q_fixed_s = copy.deepcopy(Q_temp)
                #insert NaN into not available actions
                Q_fixed_s[np.invert(self.env.action_availability)] = np.nan
                action = np.nanargmax(Q_fixed_s)
        else:
            if self.env.action_availability[guidance_feedback]:
                action = guidance_feedback
            else:
                raise Exception('The guided action is not available in that state. The guiden action was: {}'.format(action))
            
        return action
        
    def update_Q_function(self,state, next_state, action, reward):
        action_availability =  self.env.action_availability
        # TODO change to generic implementation (regarding state_action_dimensions)
        Q_temp = self.Q[int(next_state[0]),int(next_state[1]),int(next_state[2]),int(next_state[3]),:]
        Q_next_state = copy.deepcopy(Q_temp)
        Q_next_state[np.invert(action_availability)] = np.nan
        max_arg_action = np.nanargmax(Q_next_state)
        Q_max = Q_next_state[max_arg_action]
        Q_s_a = self.Q[int(state[0]),int(state[1]),int(state[2]),int(state[3]), action]
        self.Q[int(state[0]),int(state[1]),int(state[2]),int(state[3]), action] = Q_s_a + self.alpha*(reward + self.gamma* Q_max - Q_s_a)


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
