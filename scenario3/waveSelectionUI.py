import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication,
                             QLabel, QGridLayout, QSizePolicy,
                             QStatusBar, QStackedWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QIcon, QFont, QDrag
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QEvent

import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json

import time

class Canvas(QWidget):
    def __init__(self, width=2, height=3):
        super(Canvas, self).__init__()
        self.setStyleSheet("border:1px solid rgb(0, 0, 0);")

        canvas = FigureCanvas(Figure(figsize=(width, height)))
        ax = canvas.figure.subplots()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        
        self.ax = ax
        self.canvas = canvas

        # this widget overlays matplotlib to catch mouse clicks
        invis = QWidget()
        invis.setStyleSheet("background-color: rgba(255,0,0,0);")
        self.invis = invis

        layout = QVBoxLayout()
        layout.addWidget(canvas)
        layout.addWidget(invis)
        self.setLayout(layout)

    def paintEvent(self, event):
        x, y, w, h = self.canvas.x(), self.canvas.y(), self.canvas.width(), self.canvas.height()
        self.invis.setGeometry(x, y, w, h)

class Preview(Canvas):
    clicked = pyqtSignal(int)

    def __init__(self, idx, *args, **kwargs):
        super(Preview, self).__init__(*args, **kwargs)
        self.idx = idx

    def mousePressEvent(self, event):
        if event.type() == QEvent.MouseButtonPress:
            self.clicked.emit(self.idx)

        #    i = obj.property("index") 
        #    self.clicked.emit(i)
        #return QWidget.eventFilter(self, obj, event)
        
def print_clicked():
    print("clicked")
    
class WavePlotCanvas(Canvas):
    def __init__(self, idx):
        super(WavePlotCanvas, self).__init__(width=3, height=2)
        self.idx = idx

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()
        mimeData.setText(str(self.idx))

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        drag.exec_(Qt.MoveAction)

class BaseWaveSlot(Canvas):
    slot_changed = pyqtSignal(int, int)

    def __init__(self, slot_position):
        super(BaseWaveSlot, self).__init__(width=5, height=5)

        self.slot_position = slot_position
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        idx = int(e.mimeData().text())
        self.slot_changed.emit(idx, self.slot_position)

        e.setDropAction(Qt.MoveAction)
        e.accept()

class Task(QWidget):
    def __init__(self, num_bases, num_slots, **kwargs):
        super(Task, self).__init__()

        # Slots and Result
        sum_display = QHBoxLayout()
        #result = ResultWave()
        signs = ["+"] * (num_slots - 1) + ["="]
        slot_list = list()
        for idx, sign in enumerate(signs):
            slot = BaseWaveSlot(idx)
            slot_list.append(slot)
            sum_display.addWidget(slot)
            sum_display.addWidget(QLabel(sign, self))
        #sum_display.addWidget(result)

        # Pool of Base Waves
        bases = list()
        base_wave_matrix = QGridLayout()
        for idx in range(num_bases):
            pos = np.unravel_index(idx, (int(np.ceil((num_bases+1)/4)), 4))
            widget = WavePlotCanvas(idx)
            base_wave_matrix.addWidget(widget, *pos)
            bases.append(widget)

        layout = QVBoxLayout()
        layout.addLayout(sum_display)
        layout.addLayout(base_wave_matrix)
        self.setLayout(layout)

        #self.result_canvas = result
        self.base_canvas_list = bases
        self.slot_list = slot_list

class waveSelect(QWidget):
    def __init__(self):
        print("waveSelect init.")

        
    def choose_waves(self, base_graph):
        #print(base_graph)   
        
        x = np.linspace(0, 5, 1000)
        task = Task(len(base_graph), 2)
        
        # Set Base Waves
        for wave, canvas in zip(base_graph, task.base_canvas_list):
            canvas.ax.plot(x, wave)


        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Preview(0)
    ex.show()
    #print_clicked()

    sys.exit(app.exec_())        
