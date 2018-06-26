import sys
from DiscreteWaves import DiscreteWaves
import numpy as np
from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication,
                             QHBoxLayout, QVBoxLayout, QLabel, QGridLayout,
                             QGraphicsDropShadowEffect)
from PyQt5.QtGui import QDrag, QColor
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal

import json

from baseUI import Task as TaskStub
from baseUI import Window, Canvas
import baseUI

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

class WavesTask(TaskStub):
    task_solved = pyqtSignal()

    def __init__(self, idx, **kwargs):
        super(WavesTask, self).__init__(idx, **kwargs)

        N = 10  # number of waves in base set
        num_sum = 3  # maximum number of elements in sum of waves
        env = DiscreteWaves(N, num_sum)
        observation = env.reset()

        x = np.linspace(0, 5, 1000)
        task = Task(len(env.base_graph), num_sum, **kwargs)
        self.layout().addWidget(task)

        for slot in task.slot_list:
            slot.slot_changed.connect(self.on_slot_changed)

        # Set Task Preview
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0,0,255,128))
        shadow.setOffset(0,0)
        self.preview.setGraphicsEffect(shadow)
        self.preview.ax.plot(x, observation["target"])

        # Set Base Waves
        for wave, canvas in zip(observation["waves"], task.base_canvas_list):
            canvas.ax.plot(x, wave)

        task.result_canvas.ax.plot(x, observation["target"],"r")

        self.result_canvas = task.result_canvas
        self.slot_list = task.slot_list
        self.observation = observation
        self.env = env
        self.shadow = shadow

    def on_slot_changed(self, new_wave, slot_position):
        slot = self.slot_list[slot_position]
        result_canvas = self.result_canvas

        x = np.linspace(0, 5, 1000)
        observation, _, done, _ = self.env.step((new_wave, slot_position))

        slot.ax.cla()
        slot.ax.plot(x, observation["waves"][new_wave, :])
        slot.canvas.draw()

        result_canvas.ax.cla()
        result_canvas.ax.plot(x, observation["current"],"b")
        result_canvas.ax.plot(x, observation["target"],"r")
        result_canvas.canvas.draw()

        if done:
            self.done = True
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Task Solved")
            msg.setWindowTitle("Solved")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(self.taskComplete)
            self.shadow.setColor(QColor(0,255,0,200))
            msg.exec_()
        else:
            self.done = False
            self.shadow.setColor(QColor(255,0,0,200))


    def taskComplete(self, event):
        self.task_solved.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    baseUI.Task = WavesTask

    ex = Window()
    ex.show()

    sys.exit(app.exec_())