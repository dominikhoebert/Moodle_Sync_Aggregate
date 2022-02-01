import sys
import datetime
from locale import atof, setlocale, LC_NUMERIC

import pandas as pd
from openpyxl import Workbook, worksheet
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl.formatting import Rule
from openpyxl.styles import Font, PatternFill, Border
from openpyxl.styles.differential import DifferentialStyle
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QCheckBox, QFileDialog
from PyQt5.QtCore import QSettings, QPoint, QSize

from main_window import Ui_MainWindow
from moodle_sync import MoodleSync
from settings_dialog import Ui_Dialog
from conditional_formating import conditional_formatting_GEK


# Translate .ui to .py
# python -m PyQt5.uic.pyuic -x moodle_sync_aggregate.ui -o main_window.py (mac)
# pyuic5 -o main_window.py .\moodle_sync_aggregate.ui (win)
# pyuic5 -o settings_dialog.py .\settings.ui

# Pyinstaller
# pyinstaller -n Moodle_Sync_Aggregate --onefile --windowed main_app.py

def list_to_float(list):
    return_list = []
    for item in list:
        temp_item = item
        try:
            temp_item = float(atof(item))
        except (ValueError, TypeError):
            pass
        return_list.append(temp_item)
    return return_list


def filter_blank(list):
    return_list = []
    for i, item in enumerate(list):
        if item == '':
            return_list.append(f"Spalte{i}")
        else:
            return_list.append(item)
    return return_list


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.export_pushButton.setEnabled(False)
        self.download_pushButton.setEnabled(False)

        # Event Handlers
        self.courselistWidget.currentItemChanged.connect(self.course_changed)
        self.download_pushButton.clicked.connect(self.download_grades)
        self.export_pushButton.clicked.connect(self.export_grades)
        self.reload_pushButton.clicked.connect(self.download_courses)
        self.actionSettings.triggered.connect(self.open_settings)
        self.all_none_checkBox.stateChanged.connect(self.all_none_checkbox_changed)

        # Data
        self.current_course = None  # Text
        self.courses = None  # Dict Course name:id
        self.grades = None  # Dataframe of Student name, Modules and Grades
        self.checkboxes = None  # List of Checkboxes for Modules
        self.student_list = None  # Dataframe Name Klasse

        # Config
        self.settings = QSettings('TGM', 'Moodle_Sync_Grading')
        # self.settings.clear()
        self.resize(self.settings.value("size", QSize(1000, 800)))
        self.move(self.settings.value("pos", QPoint(50, 50)))
        if self.settings.contains('splitter'):
            self.splitter.restoreState(self.settings.value('splitter'))
        self.use_studentlist = self.settings.value("use_studentlist", False) == 'true'

        # Startup
        self.url = self.settings.value("url", None)
        self.key = self.settings.value("key", None)
        self.student_list_path = self.settings.value("studentlist",
                                                     "~/tgm - Die Schule der Technik/HIT - Abteilung für Informations"
                                                     "technologie - Dokumente/Organisation/Tools/studentlist.csv")
        self.moodle = None

        self.login()

    def login(self):
        if self.url and self.key:
            self.moodle = MoodleSync(self.url, self.key)
            self.download_courses()
        else:
            self.fail_to_load("Moodle URL/Key not defined. Please check Settings.")

    def fail_to_load(self, message, error=None):
        print(message, error)
        msg_box = QMessageBox(QMessageBox.Information, "Fehler", message)
        msg_box.exec_()

    def get_course_id(self, name):
        return self.courses[name]['id']

    def download_courses(self):
        if self.moodle:
            try:
                self.courses = self.moodle.get_recent_courses()
                self.set_courses()
                self.download_pushButton.setEnabled(self.all_none_checkBox.checkState())
            except Exception as e:
                self.fail_to_load("Failed to load courses. Please check Settings.", e)
        else:
            self.fail_to_load("Moodle URL/Key not defined. Please check Settings.")

    def set_courses(self):
        self.courselistWidget.blockSignals(True)
        self.courselistWidget.clear()
        for c in self.courses.keys():
            self.courselistWidget.addItem(c)
        self.courselistWidget.blockSignals(False)

    def course_changed(self, course):
        self.current_course = course.text()

    def download_grades(self):
        if self.use_studentlist:
            try:
                self.student_list = pd.read_csv(self.student_list_path)
            except Exception as e:
                print("Failed to load Student List CSV. Please check Settings.", e)

        if self.current_course is None:
            self.courselistWidget.setCurrentRow(0)
        self.grades = self.moodle.get_gradereport_of_course(self.get_course_id(self.current_course))

        userlist = []
        for uid in self.grades.userid:
            userlist.append({"userid": uid, "courseid": self.get_course_id(self.current_course)})
        user_info = self.moodle.get_student_info(userlist=userlist)
        self.grades = self.grades.merge(user_info, how='left', left_on='userid', right_on='id')
        self.grades = self.grades.drop(['userid', 'id', 'fullname'], axis=1)
        self.grades = self.grades.rename(columns={'groups': 'Gruppen', 'email': 'Email'})

        self.grades = self.grades.replace("nicht erfüllt", "n")
        self.grades = self.grades.replace("Nicht erfüllt", "n")
        self.grades = self.grades.replace("GK vollständig", "GKv")
        self.grades = self.grades.replace("GK überwiegend", "GKü")
        self.grades = self.grades.replace("EK vollständig", "EKv")
        self.grades = self.grades.replace("EK überwiegend", "EKü")
        self.grades = self.grades.replace("vollständig erfüllt", "v")
        self.grades = self.grades.replace("überwiegend erfüllt", "ü")

        if self.student_list is not None:
            self.grades[['a', 'b', 'c']] = self.grades['Schüler'].str.lower().str.split(' ', 2, expand=True)
            self.grades['Name2'] = self.grades['a'] + ' ' + self.grades['b']
            self.student_list[['a', 'b', 'c']] = self.student_list['Name'].str.lower().str.split(' ', 2, expand=True)
            self.student_list['Name3'] = self.student_list['a'] + ' ' + self.student_list['b']
            self.grades = self.grades.merge(self.student_list, how='left', left_on='Name2', right_on='Name3')
            self.grades = self.grades.drop(['a_x', 'b_x', 'c_x', 'Name2', 'Name', 'a_y', 'b_y', 'c_y', 'Name3'], axis=1)
        else:
            self.grades["Klasse"] = ""

        self.grades.columns = filter_blank(self.grades.columns)
        self.grades = self.grades[["Schüler", "Klasse", "Gruppen", "Email"] + list(self.grades.columns)[1:-3]]
        self.create_modules_list()

    def create_modules_list(self):
        self.checkboxes = []
        for i in reversed(range(self.tasks_verticalLayout.count())):
            self.tasks_verticalLayout.itemAt(i).widget().setParent(None)

        for module in list(self.grades.columns):
            if module not in ["Schüler", 'Klasse', 'Gruppen', 'Email']:
                cb = QCheckBox(module, self)
                cb.setChecked(True)
                self.tasks_verticalLayout.addWidget(cb)
                self.checkboxes.append(cb)

        self.export_pushButton.setEnabled(True)

    def export_grades(self):
        wb = Workbook()
        ws = wb.active

        for row in dataframe_to_rows(self.grades, index=False, header=True):
            ws.append(list_to_float(row))

        for i, cb in enumerate(self.checkboxes):
            if cb.checkState() == 0:
                for cell in ws[1]:
                    if cell.value == cb.text():
                        ws.delete_cols(cell.column, 1)

        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 6
        ws.column_dimensions['C'].width = 8
        ws.column_dimensions['D'].width = 10
        ws.column_dimensions[get_column_letter(ws.max_column)].width = 5

        for i in range(5, ws.max_column):
            ws.column_dimensions[get_column_letter(i)].width = 4

        ws.freeze_panes = ws['B1']

        tab = worksheet.table.Table(displayName="Table1", ref=f"A1:{get_column_letter(ws.max_column)}{ws.max_row}")
        tab.tableStyleInfo = worksheet.table.TableStyleInfo(name="TableStyleMedium1", showRowStripes=True,
                                                            showColumnStripes=False)
        ws.add_table(tab)

        for cell in ws[1]:
            module = str(cell.value)
            if module.startswith("GK"):
                conditional_formatting_GEK(ws, f"{cell.column_letter}2:{cell.column_letter}{ws.max_row}", 'GK')
            elif module.startswith("EK"):
                conditional_formatting_GEK(ws, f"{cell.column_letter}2:{cell.column_letter}{ws.max_row}", 'EK')
            elif module.startswith("GEK"):
                conditional_formatting_GEK(ws, f"{cell.column_letter}2:{cell.column_letter}{ws.max_row}", 'GEK')
            elif module.startswith("Wiederholung") or module.startswith("SMÜ"):
                pass

        directory = self.settings.value('dir', "")
        ct = datetime.datetime.now()
        filename = f"{directory}/{ct.year}{str(ct.month).zfill(2)}{str(ct.day).zfill(2)}_{self.current_course}"

        file, _ = QFileDialog.getSaveFileName(self, "Export Grades", filename, "Excel files (*.xlsx)")
        if file:
            wb.save(file)
            self.settings.setValue("dir", file[:file.rfind("/")])  # TODO test on mac if sep is also "/" (maybe "\")

    def open_settings(self):
        settings = SettingsDlg(self, use_studentlist=self.use_studentlist, url=self.settings.value("url", ""),
                               key=self.settings.value("key", ""), studentlist=self.student_list_path)
        if settings.exec():
            self.url = settings.ui.url_lineEdit.text()
            self.key = settings.ui.key_lineEdit.text()
            self.student_list_path = settings.ui.studentlist_lineEdit.text()
            self.settings.setValue("url", self.url)
            self.settings.setValue("key", self.key)
            self.settings.setValue("studentlist", self.student_list_path)
            self.use_studentlist = settings.ui.checkBox.isChecked()
            self.settings.setValue("use_studentlist", self.use_studentlist)
        self.login()

    def all_none_checkbox_changed(self):
        for cb in self.checkboxes:
            cb.setChecked(self.all_none_checkBox.checkState())

    def closeEvent(self, e):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("splitter", self.splitter.saveState())
        e.accept()


class SettingsDlg(QDialog):
    def __init__(self, parent=None, url=None, key=None, studentlist=None, use_studentlist=False):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.checkBox.setChecked(use_studentlist)
        self.ui.studentlist_lineEdit.setEnabled(use_studentlist)
        self.ui.checkBox.stateChanged.connect(self.checkbox_changed)
        if url:
            self.ui.url_lineEdit.setText(url)
        if key:
            self.ui.key_lineEdit.setText(key)
        if studentlist:
            self.ui.studentlist_lineEdit.setText(studentlist)

    def checkbox_changed(self):
        self.ui.studentlist_lineEdit.setEnabled(self.ui.checkBox.isChecked())


if __name__ == '__main__':
    setlocale(LC_NUMERIC, '')
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
