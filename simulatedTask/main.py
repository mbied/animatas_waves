from DiscreteWavesGridWorld import DiscreteWavesGridWorld
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    env = DiscreteWavesGridWorld()
    observation = env.reset()
    done = False
    i = 0
    cum_reward = 0
    while not done:
        random_action_legit = False
        while not random_action_legit:
            random_action = np.random.randint(0, 8,size=1)[0]
            random_action_legit = env.action_availability[random_action]
            
        observation, reward, done, _ = env.step(random_action)
        cum_reward += reward
        i += 1
    
    test_array = np.random.randint(0,100, size=100)
    print(test_array)
    plt.plot(test_array)
    plt.ylabel('some numbers')
    plt.show()
        
    print("Finished after %s steps." % i)
