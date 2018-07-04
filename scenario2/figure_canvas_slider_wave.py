import sys
 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider, QGridLayout, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import numpy as np
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
 
import random

from ParametrizedWaves import ParametrizedWaves

class Backend:
    env = ParametrizedWaves()

    def __init__(self):
        self.observation = self.env.reset()

    def step(self, action):
        self.observation, self.reward, done, _ = self.env.step(action)
        
    def reset(self):
        self.observation = self.env.reset()
backend = Backend()

def eval_wave(x, amplitude, f, offset=0, phase=0):
    return amplitude * np.sin(2*np.pi*f*x + phase) + offset
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        
        self.slider_h = QSlider(Qt.Horizontal)
        self.slider_h.setMaximum(100)
        self.slider_h.setValue(10)
        layout.addWidget(self.slider_h, 1, 0)
        self.slider_h.valueChanged.connect(self.slider_changed)
        
        self.slider_v = QSlider(Qt.Vertical)
        self.slider_v.setMaximum(100)
        self.slider_v.setValue(50)
        layout.addWidget(self.slider_v, 0, 1)
        self.slider_v.valueChanged.connect(self.slider_changed)
        

        self.m = PlotCanvas(self, width=5, height=4)
        layout.addWidget(self.m, 0, 0)
        
        self.b1 = QPushButton("Step")
        layout.addWidget(self.b1,2,0)
        self.b1.setEnabled(False)
        self.label = QLabel()
        self.label.setText("Received Reward: no Step was made!")
        layout.addWidget(self.label,3,0)
        
        self.show()
        
    def slider_changed(self):
        amplitude = self.slider_v.value()/10
        f = self.slider_h.value()/10
        self.m.plot(amplitude,f)
        backend.step(np.array([amplitude, f]))
        #"Sammy has {} balloons.".format(5)
        s = "Received Reward: {:.4f}".format(backend.reward)
        self.label.setText(s)
 
 
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
        self.plot(5,1)
 
 
    def plot(self, amplitude, f):
        x = np.linspace(0, 1, 1000)
        data = eval_wave(x, amplitude, f)
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_ylim([-10,10])
        ax.plot(x, data)
        ax.plot(x, eval_wave(x, backend.observation[0], backend.observation[1]), 'g--')
        #ax.set_title('Scenario 2')
        self.draw()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    #ex.show()
    sys.exit(app.exec_())
