from DiscreteWavesGridWorld import DiscreteWavesGridWorld
import numpy as np
import matplotlib.pyplot as plt
import copy

def chose_action(env, Q):
    
    r = np.random.rand()
    
    if r > 0.1:
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
    
def update_Q_function(Q, alpha=.95, gamma=.7):
    #TODO implement me
    return Q

if __name__ == "__main__":
    # learning parameter
    gamma = 0.7
    Q = np.zeros([10,10,10,10,8])
    env = DiscreteWavesGridWorld()
    N = 5
    
    for episode in range(0,N):
        observed_state = env.reset()
        done = False
        i = 0
        cum_reward = 0    
        while not done:
            random_action = chose_action(env, Q)
            observation, reward, done, _ = env.step(random_action)
            Q = update_Q_function(Q)
            cum_reward += reward            
            i += 1

        if episode == 0:
            cum_rewards = np.array([cum_reward])
        else:
            cum_rewards = np.append(cum_rewards, np.array([cum_reward]))
            
        print("Episode {} done after {} steps".format(episode, i))

    
    plt.plot(cum_rewards)
    plt.show()
        
        
        

            
        
    
    #test_array = np.random.randint(0,100, size=100)
    #print(test_array)
    #plt.plot(test_array)
    #plt.ylabel('some numbers')
    #plt.show()
        
