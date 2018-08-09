import sys
from DiscreteWavesGridWorld import DiscreteWavesGridWorld
from QLearning import QLearning
import numpy as np

from PyQt5.QtWidgets import QPushButton, QDialog, QApplication, QVBoxLayout, QSizePolicy
#from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider, QGridLayout, QLabel)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def eval_wave(x, amplitude, f, offset=0, phase=0):
    return amplitude * np.sin(2*np.pi*f*x + phase) + offset

class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #self.plot(5,1)
 
 
    def plot(self, amplitude, f, amplitude2, f2,):
        x = np.linspace(0, 1, 1000)
        data1 = eval_wave(x, amplitude, f)
        data2 = eval_wave(x, amplitude2, f2)
        data = data1 + data2
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_ylim([-10,10])
        ax.plot(x, data)
        data = eval_wave(x, 2, 3) + eval_wave(x, 5, 7)
        ax.plot(x,data)
        #ax.plot(x, eval_wave(x, backend.observation[0], backend.observation[1]), 'g--')
        #ax.set_title('Scenario 2')
        self.draw()

class Form(QDialog):
    def __init__(self, qLearning, parent=None):
        super(Form, self).__init__(parent)
        
        #just for testing
        self.guidance = [6, 6, 4, 6, 6, 4, 4, 6, 2, 0, 4, 2, 6, 0, 2, 4, 6]
        self.i = 0
        
        self.qLearning = qLearning
        self.state = qLearning.env.state
        
        layout = QVBoxLayout()
        self.b1 = QPushButton("Button1")
        self.b1.clicked.connect(self.btnstate)
        layout.addWidget(self.b1)
        self.canvas = PlotCanvas(self, width=5, height=4)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
    def btnstate(self):
        action = qLearning.chose_action(self.guidance[self.i])
        #action = qLearning.chose_action()
        self.i += 1
        print(action)
        next_state, reward, done, _ = qLearning.env.step(action)
        qLearning.update_Q_function(self.state, next_state, action, reward)
        #cum_reward += reward            
        #i += 1
        self.state = next_state
        self.canvas.plot(self.state[0],self.state[1],self.state[2],self.state[3])
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
