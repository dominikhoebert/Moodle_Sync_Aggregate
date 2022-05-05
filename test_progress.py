# Example 1 - Pulse ProgressBar:

# If minimum and maximum are both set to 0, the progressbar will show a busy indicator instead of a percentage of steps.
# https://stackoverflow.com/questions/19442443/busy-indication-with-pyqt-progress-bar


from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QCheckBox, QFileDialog, QScrollArea, QVBoxLayout, \
    QGroupBox
from PyQt5.QtCore import QSettings, QPoint, QSize, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import time



class MyCustomWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)

        # Create a progress bar and a button and add them to the main layout
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setRange(0, 1)
        layout.addWidget(self.progressBar)
        button = QtGui.QPushButton("Start", self)
        layout.addWidget(button)

        button.clicked.connect(self.onStart)

        self.myLongTask = TaskThread()
        self.myLongTask.taskFinished.connect(self.onFinished)

    def onStart(self):
        self.progressBar.setRange(0, 0)
        self.myLongTask.start()

    def onFinished(self):
        # Stop the pulsation
        self.progressBar.setRange(0, 1)


class TaskThread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()

    def run(self):
        time.sleep(3)
        self.taskFinished.emit()
