import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication,
                             QLabel, QGridLayout, QSizePolicy,
                             QStatusBar, QStackedWidget, QPushButton)
from PyQt5.QtGui import QIcon, QFont, QDrag
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QEvent

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json

class Preview(QLabel):
    clicked = pyqtSignal()
    def eventFilter(self, obj, event):
        print("something")
        if isinstance(obj, QLabel) and event.type() == QEvent.MouseButtonPress:
            i = obj.property("index") 
            self.clicked.emit(i)
        return QWidget.eventFilter(self, obj, event)

class Task(QWidget):
    def __init__(self, idx, status_bar=None):
        super(Task, self).__init__()

        self.preview = Preview("Preview %d" % idx)
        self.preview.setStyleSheet("border:2px solid rgb(0, 0, 0);")

        foo = QGridLayout()
        foo.addWidget(QLabel(str(idx)))
        self.setLayout(foo)


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
        self.status_bar.showMessage("Done")

        available_tasks = [Task(idx, self.status_bar) for idx in range(10)] # replace me with actual loading routine
        task_selection = TaskSelection(available_tasks)
        widget_selector.addWidget(task_selection)
        for task in available_tasks:
            widget_selector.addWidget(task)
            task.preview.clicked.connect(self.foo)

        widget_selector.setCurrentIndex(0)

        self.setStatusBar(self.status_bar)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("ANIMATAS Waves Scenario 1")
        self.setWindowIcon(QIcon("wave.png"))

    def foo(self):
        self.status_bar.showMessage("Something happned")#. %s" % str(value))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Window()
    ex.show()

    sys.exit(app.exec_())
