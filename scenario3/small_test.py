import numpy as np

max_amplitude=5
max_f=10
N = 10

def eval_wave(x, amplitude, frequency, offset=0, phase=0):
    return amplitude * np.sin(2*np.pi*frequency*x + phase) + offset

base = np.hstack((np.random.randint(0,max_amplitude, size=(N+1,1)),np.random.randint(0,max_f,size=(N+1,1)),np.zeros((N+1, 1))))

base_graph = np.array([[eval_wave(x, a, f)
                                    for x in np.linspace(0, 5, 1000)]
                                    for a, f, phase in base])

#print(base_graph)
a1,f1 = 1, 0.5
a2,f2 = 2, 2
state = np.array([[a1,f1],[a2,f2]])

two_graphs = np.array([[eval_wave(x,wave_params[0],wave_params[1]) 
                            for x in np.linspace(0, 5, 1000)]
                            for wave_params in state])
#print(two_graphs)
observation ={"target": np.sum(two_graphs,axis=0)}
print(np.sum(two_graphs,axis=0))

        #self.base_graph = np.array([[eval_wave(x, a, f)
         #                           for x in np.linspace(0, 5, 1000)]
          #                          for a, f, phase in base])
