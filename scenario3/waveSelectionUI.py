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
        
class ResultWave(Canvas):
    def __init__(self):
        super().__init__(width=5, height=5)        

class Task(QWidget):
    def __init__(self, num_bases, num_slots, **kwargs):
        super(Task, self).__init__()

        # Slots and Result
        sum_display = QHBoxLayout()
        result = ResultWave()
        signs = ["+"] * (num_slots - 1) + ["="]
        slot_list = list()
        for idx, sign in enumerate(signs):
            slot = BaseWaveSlot(idx)
            slot_list.append(slot)
            sum_display.addWidget(slot)
            sum_display.addWidget(QLabel(sign, self))
        sum_display.addWidget(result)

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

        self.result_canvas = result
        self.base_canvas_list = bases
        self.slot_list = slot_list

class WaveSelect(QWidget):
    def __init__(self,interactive_waves_env, num_sum=2):
        QWidget.__init__(self)
        self.num_sum = num_sum
        self.interactive_waves_env = interactive_waves_env
        base_graph = interactive_waves_env.base_graph
        self.selected_waves = np.tile(np.zeros(1000), (num_sum,1)) 
        self.selected_waves_idx = -1*np.ones(num_sum)
        x = np.linspace(0, 5, 1000)
        task = Task(len(base_graph), 2)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.layout().addWidget(task)
        self.b1 = QPushButton("Button1")
        layout.addWidget(self.b1)
        self.b1.clicked.connect(self.btn_press)
        
        for slot in task.slot_list:
            slot.slot_changed.connect(self.on_slot_changed)
        
        # Set Base Waves
        for wave, canvas in zip(base_graph, task.base_canvas_list):
            canvas.ax.plot(x, wave)
            
        self.result_canvas = task.result_canvas
        self.slot_list = task.slot_list
        self.base_graph = base_graph
        self.show()

            
    def on_slot_changed(self, new_wave, slot_position):
            slot = self.slot_list[slot_position]
            result_canvas = self.result_canvas

            x = np.linspace(0, 5, 1000)

            slot.ax.cla()
            wave = self.base_graph[new_wave, :] 
            slot.ax.plot(x, wave)
            slot.canvas.draw()
            self.selected_waves[slot_position] = wave
            self.selected_waves_idx = slot_position
            added_wave = np.sum(self.selected_waves,axis=0)

            result_canvas.ax.cla()
            result_canvas.ax.plot(x, added_wave,"b")
            #result_canvas.ax.plot(x, observation["target"],"r")
            result_canvas.canvas.draw()
            
    def btn_press(self, b):
        # add check if waves were selected
        self.interactive_waves_env.reset(self.selected_waves_idx)



        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Preview(0)
    ex.show()
    #print_clicked()

    sys.exit(app.exec_())        
