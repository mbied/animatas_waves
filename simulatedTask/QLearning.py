from DiscreteWavesGridWorld import DiscreteWavesGridWorld
import numpy as np
import matplotlib.pyplot as plt
import copy

class QLearning:
    
    def __init__(self,)
    
    
def chose_action(env, Q):
    
    r = np.random.rand()
    
    if r > 1:
        action_legit = False
        while not action_legit:
            action = np.random.randint(0, 8,size=1)[0]
            action_legit = env.action_availability[action]
            
    else:
        s = env.state
        #print(env.state)
        #print(s[0],s[1],s[2],s[3])
        Q_temp = Q[int(s[0]),int(s[1]),int(s[2]),int(s[3]),:]
        Q_fixed_s = copy.deepcopy(Q_temp)
        #insert NaN into not available actions
        Q_fixed_s[np.invert(env.action_availability)] = np.nan
        action = np.nanargmax(Q_fixed_s)
        
    return action
    
def update_Q_function(Q, state, next_state, action, reward, action_availability, alpha=.95, gamma=.7):
    Q_temp = Q[int(next_state[0]),int(next_state[1]),int(next_state[2]),int(next_state[3]),:]
    Q_next_state = copy.deepcopy(Q_temp)
    Q_next_state[np.invert(action_availability)] = np.nan
    max_arg_action = np.nanargmax(Q_next_state)
    Q_max = Q_next_state[max_arg_action]
    Q_d = Q
    Q_s_a = Q_d[int(state[0]),int(state[1]),int(state[2]),int(state[3]), action]
    Q_d[int(state[0]),int(state[1]),int(state[2]),int(state[3]), action] = Q_s_a + alpha*(reward + gamma* Q_max - Q_s_a)
    return Q_d

if __name__ == "__main__":
    # learning parameter
    gamma = 0.7
    Q = np.zeros([10,10,10,10,8])
    env = DiscreteWavesGridWorld()
    N = 1000
    
    for episode in range(0,N):
        state = env.reset()
        done = False
        i = 0
        cum_reward = 0    
        while not done:
            action = chose_action(env, Q)
            next_state, reward, done, _ = env.step(action)
            Q = update_Q_function(Q, state, next_state, action, reward, env.action_availability)
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
