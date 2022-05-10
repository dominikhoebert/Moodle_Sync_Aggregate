from PyQt5.QtCore import QThread, pyqtSignal
from moodle_sync import MoodleSync
from pandas import DataFrame


class MoodleDownloaderCourses(QThread):
    taskFinished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def download(self, moodle: MoodleSync):
        self.moodle = moodle
        self.start()

    def run(self):
        try:
            courses = self.moodle.get_recent_courses()
        except Exception as e:
            self.error.emit("Failed to load courses. Please check Settings." + str(e))
        self.taskFinished.emit(courses)


class MoodleDownloaderStudentInfo(QThread):
    taskFinished = pyqtSignal(DataFrame)
    error = pyqtSignal(str)

    def download(self, moodle: MoodleSync, user_list: list):
        self.moodle = moodle
        self.user_list = user_list
        self.start()

    def run(self):
        try:
            user_info = self.moodle.get_student_info(userlist=self.user_list)
        except Exception as e:
            self.error.emit("Failed to load StudentInfo. " + str(e))
        self.taskFinished.emit(user_info)


class MoodleDownloaderGradeReport(QThread):
    taskFinished = pyqtSignal(DataFrame)
    error = pyqtSignal(str)

    def download(self, moodle: MoodleSync, course_id: str):
        self.moodle = moodle
        self.course_id = course_id
        self.start()

    def run(self):
        try:
            df = self.moodle.get_gradereport_of_course(self.course_id)
        except Exception as e:
            self.error.emit("Failed to load GradeReport. " + str(e))
        self.taskFinished.emit(df)
