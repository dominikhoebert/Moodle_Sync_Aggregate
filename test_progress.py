# Example 1 - Pulse ProgressBar:

# If minimum and maximum are both set to 0, the progressbar will show a busy indicator instead of a percentage of steps.
# https://stackoverflow.com/questions/19442443/busy-indication-with-pyqt-progress-bar


from PyQt5.QtWidgets import QApplication, QVBoxLayout, QProgressBar, QPushButton
from PyQt5 import QtCore, QtWidgets
import time
import sys


class MyCustomWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Create a progress bar and a button and add them to the main layout
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 1)
        layout.addWidget(self.progressBar)
        button = QPushButton("Start", self)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyCustomWidget()
    win.show()
    sys.exit(app.exec())
