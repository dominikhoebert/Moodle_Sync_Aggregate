from PyQt5.QtCore import QThread, pyqtSignal


class TaskThread(QThread):
    taskFinished = pyqtSignal()

    def run(self):
        # something long here
        self.taskFinished.emit()
