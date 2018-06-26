import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication,
                             QLabel, QGridLayout, QSizePolicy,
                             QStatusBar, QStackedWidget, QPushButton,
                             QVBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QIcon, QFont, QDrag
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QEvent

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

class Task(QWidget):
    task_solved = pyqtSignal()

    def __init__(self, idx, status_bar=None):
        super(QWidget, self).__init__()

        self.preview = Preview(idx)

        self.back_button = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.back_button)
        self.setLayout(layout)


class TaskSelection(QWidget):
    def __init__(self, available_tasks):
        super(TaskSelection, self).__init__()

        layout = QGridLayout()
        for idx, task in enumerate(available_tasks):
            layout.addWidget(task.preview, idx // 4, idx % 4)

        self.setLayout(layout)

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        widget_selector = QStackedWidget()
        self.setCentralWidget(widget_selector)
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Please select a task to complete")

        available_tasks = [Task(idx, status_bar=self.status_bar) for idx in range(8)] # replace me with actual loading routine
        task_selection = TaskSelection(available_tasks)
        widget_selector.addWidget(task_selection)
        for task in available_tasks:
            task.task_solved.connect(self.backButtonClicked)
            widget_selector.addWidget(task)
            task.preview.clicked.connect(self.taskSelected)
            task.back_button.clicked.connect(self.backButtonClicked)

        widget_selector.setCurrentIndex(0)
        self.tasks = widget_selector

        self.setStatusBar(self.status_bar)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("ANIMATAS Waves Scenario 1")
        self.setWindowIcon(QIcon("wave.png"))

    def taskSelected(self, idx):
        self.status_bar.showMessage("You have selected on task %d" % idx)
        self.tasks.setCurrentIndex(idx+1)

    def backButtonClicked(self):
        self.status_bar.showMessage("Please select a task to complete")
        self.tasks.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Window()
    ex.show()

    sys.exit(app.exec_())
