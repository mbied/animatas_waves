import sys
from DiscreteWavesGridWorld import DiscreteWavesGridWorld
from QLearning import QLearning
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QPushButton, QDialog, QApplication, QVBoxLayout

class Form(QDialog):
    def __init__(self, qLearning, parent=None):
        super(Form, self).__init__(parent)
        
        self.qLearning = qLearning
        self.state = qLearning.env.state
        
        layout = QVBoxLayout()
        self.b1 = QPushButton("Button1")
        self.b1.clicked.connect(self.btnstate)
        layout.addWidget(self.b1)
        self.setLayout(layout)
        
    def btnstate(self):
        action = qLearning.chose_action()
        print(action)
        next_state, reward, done, _ = qLearning.env.step(action)
        qLearning.update_Q_function(self.state, next_state, action, reward)
        #cum_reward += reward            
        #i += 1
        self.state = next_state
        print(self.state)
        
        if done:
            print("finished")
            self.state = qLearning.env.reset()
            print(self.state)
      
            



if __name__ == "__main__":
    env = DiscreteWavesGridWorld()
    qLearning = QLearning(env)
    N = 400
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
   # plt.show()
    Q = qLearning.Q
    state = env.reset()
    app = QApplication(sys.argv)
    ex = Form(qLearning)
    ex.show()
    sys.exit(app.exec_())
