import sys
from DiscreteWaves import DiscreteWaves
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QMessageBox, QApplication,
QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QFont, QDrag
from PyQt5.QtCore import Qt, QMimeData

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json

N = 10  # number of waves in base set
num_sum = 3  # maximum number of elements in sum of waves

backend = DiscreteWaves(N, num_sum)

class WavePlotCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, data, parent=None, width=50, height=40, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.random = np.random.rand()

        x = np.linspace(0,5,1000)
        self.axes.plot(x, data)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        self.data = data

        super().__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)      

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()
        mimeData.setText(json.dumps(self.data.tolist()))

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        drag.exec_(Qt.MoveAction)

class BaseWaveSlot(FigureCanvas):
    def __init__(self, data, parent=None, width=50, height=40, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.random = np.random.rand()

        x = np.linspace(0,5,1000)
        self.axes.plot(x, data)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        self.x = x

        super().__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()
        

    def dropEvent(self, e):
        self.axes.cla()
        data = np.array(json.loads(e.mimeData().text()))
        self.axes.plot(self.x, data)
        self.draw()

        e.setDropAction(Qt.MoveAction)
        e.accept()


class Example(QWidget):
    def __init__(self):
        super().__init__()

        # Overall Layout
        overall = QVBoxLayout()

        sum_display = QHBoxLayout()
        sum_display.addWidget(BaseWaveSlot(np.zeros(1000), self))
        sum_display.addWidget(QLabel("+", self))
        sum_display.addWidget(BaseWaveSlot(np.zeros(1000), self))
        sum_display.addWidget(QLabel("+", self))
        sum_display.addWidget(BaseWaveSlot(np.zeros(1000), self))
        sum_display.addWidget(QLabel("=", self))
        sum_display.addWidget(BaseWaveSlot(np.zeros(1000), self))
        overall.addLayout(sum_display)

        base_wave_matrix = QGridLayout()
        base_waves = np.zeros(N+1)
        for idx, wave in enumerate(backend.base_wave_representations):
            pos = np.unravel_index(idx, (int(np.ceil((N+1)/4)), 4))
            widget = WavePlotCanvas(wave, self)
            base_wave_matrix.addWidget(widget, *pos)

        overall.addLayout(base_wave_matrix)
        
        self.setLayout(overall)
        #self.statusBar().showMessage("I am fully charged")
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("ANIMATAS Waves Scenario 1")
        self.setWindowIcon(QIcon("wave.png"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ex = Example()
    ex.show()

    sys.exit(app.exec_())