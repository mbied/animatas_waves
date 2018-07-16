import numpy as np
import matplotlib.pyplot as plt
import copy

def chose_action(Q):
    # random for now
    #random_action_legit = False
    #while not random_action_legit:
    #    random_action = np.random.randint(0, 8,size=1)[0]
    #    random_action_legit = env.action_availability[random_action]
    
    s = np.zeros(4, dtype=np.int64)
    Q_temp = Q[s[0],s[1],s[2],s[3],:]
    Q_fixed_s = copy.deepcopy(Q_temp)
    #
    Q_fixed_s[0] = 1
    #
    action_availability = np.ones(8, dtype=bool)
    action_availability[0] = False
    print(action_availability)
    Q_fixed_s[np.invert(action_availability)] = np.nan
    print(np.nanargmax(Q_fixed_s))
    return

if __name__ == "__main__":
    Q = np.zeros([10,10,10,10,8])
    action = chose_action(Q)
    print(action)
