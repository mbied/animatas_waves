import sys
from DiscreteWaves import DiscreteWaves
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QMessageBox, QApplication,
                             QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, 
                             QSizePolicy)
from PyQt5.QtGui import QIcon, QFont, QDrag
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json

N = 10  # number of waves in base set
num_sum = 3  # maximum number of elements in sum of waves


class Backend:
    env = DiscreteWaves(N, num_sum)

    def __init__(self):
        self.observation = self.env.reset()

    def step(self, action):
        self.observation, reward, done, _ = self.env.step(action)
backend = Backend()


class WavePlotCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, idx, parent=None, width=3, height=2, dpi=100):
        self.idx = idx
        x = np.linspace(0, 5, 1000)
        data = backend.observation["waves"][idx, :]

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.plot(x, data)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

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
        mimeData.setText(str(self.idx))

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        drag.exec_(Qt.MoveAction)


class BaseWaveSlot(FigureCanvas):
    slot_changed = pyqtSignal(int)

    def __init__(self, slot_position, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.slot_position = slot_position

        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        self.x = np.linspace(0, 5, 1000)

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
        idx = int(e.mimeData().text())
        self.axes.plot(self.x, backend.observation["waves"][idx, :])
        self.draw()

        backend.step((idx, self.slot_position))
        self.slot_changed.emit(idx)

        e.setDropAction(Qt.MoveAction)
        e.accept()


class ResultWave(FigureCanvas):
    observation_changed = pyqtSignal()

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        x = np.linspace(0, 5, 1000)
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        self.axes.plot(x, backend.observation["current"])
        self.axes.plot(x, backend.observation["target"])
        self.x = x

        super().__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def on_slot_changed(self, idx):
        self.axes.cla()
        self.axes.plot(self.x, backend.observation["current"])
        self.axes.plot(self.x, backend.observation["target"])
        self.draw()


class DiscreteWavesGame(QWidget):
    def __init__(self):
        super().__init__()

        # Overall Layout
        overall = QVBoxLayout()

        result = ResultWave(parent=self)
        sum_display = QHBoxLayout()
        signs = ["+"] * (num_sum - 1) + ["="]

        for idx, sign in enumerate(signs):
            slot = BaseWaveSlot(idx, self)
            slot.slot_changed.connect(result.on_slot_changed)
            sum_display.addWidget(slot)
            sum_display.addWidget(QLabel(sign, self))
        sum_display.addWidget(result)
        overall.addLayout(sum_display)

        base_wave_matrix = QGridLayout()
        base_waves = np.zeros(N+1)
        for idx, wave in enumerate(backend.env.base_graph):
            pos = np.unravel_index(idx, (int(np.ceil((N+1)/4)), 4))
            widget = WavePlotCanvas(idx, self)
            base_wave_matrix.addWidget(widget, *pos)

        overall.addLayout(base_wave_matrix)

        self.setLayout(overall)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("ANIMATAS Waves Scenario 1")
        self.setWindowIcon(QIcon("wave.png"))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = DiscreteWavesGame()
    ex.show()

    sys.exit(app.exec_())
