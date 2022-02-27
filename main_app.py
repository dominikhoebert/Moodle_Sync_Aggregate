import sys
import datetime
from locale import atof, setlocale, LC_NUMERIC
import json

import pandas as pd
from openpyxl import Workbook, worksheet
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QCheckBox, QFileDialog
from PyQt5.QtCore import QSettings, QPoint, QSize

from main_window import Ui_MainWindow
from moodle_sync import MoodleSync
from settings_dialog import Ui_Dialog
from conditional_formating import custom_conditional_formatting


# Translate .ui to .py
# python -m PyQt5.uic.pyuic -x moodle_sync_aggregate.ui -o main_window.py (mac)
# pyuic5 -o main_window.py .\moodle_sync_aggregate.ui (win)
# pyuic5 -o settings_dialog.py .\settings.ui

# Pyinstaller
# pyinstaller -n Moodle_Sync_Aggregate --onefile --windowed main_app.py

def list_to_float(grade_list):
    return_list = []
    for item in grade_list:
        temp_item = item
        try:
            temp_item = float(atof(item))
        except (ValueError, TypeError):
            pass
        return_list.append(temp_item)
    return return_list


def filter_blank(grade_list):
    return_list = []
    for i, item in enumerate(grade_list):
        if item == '':
            return_list.append(f"Spalte{i}")
        else:
            return_list.append(item)
    return return_list


def get_column_for_module(ws, module):
    for cell in ws[1]:
        if module == cell.value:
            return cell.column_letter


def fail_to_load(message, error=None):
    print(message, error)
    msg_box = QMessageBox(QMessageBox.Information, "Fehler", message)
    msg_box.exec_()


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
        self.competences = None  # Dict competence number as string eg. '21' (for 2.1) to Module Names
        self.competence_helper = None  # Dict competence_name to competence number

        # Config
        self.settings = QSettings('TGM', 'Moodle_Sync_Grading')
        # self.settings.clear()
        self.resize(self.settings.value("size", QSize(1000, 800)))
        self.move(self.settings.value("pos", QPoint(50, 50)))
        if self.settings.contains('splitter'):
            self.splitter.restoreState(self.settings.value('splitter'))
        self.use_studentlist = self.settings.value("use_studentlist",  False)
        self.create_competence_columns = self.settings.value('create_competence_columns', True)
        self.mark_suggestion = self.settings.value('mark_suggestion', False)
        if self.use_studentlist == 'true' or self.use_studentlist == True:
            self.use_studentlist = True
        else:
            self.use_studentlist = False
        if self.create_competence_columns == 'true' or self.create_competence_columns == True:
            self.create_competence_columns = True
        else:
            self.create_competence_columns = False
        if self.mark_suggestion == 'true' or self.mark_suggestion == True:
            self.mark_suggestion = True
        else:
            self.mark_suggestion = False

        # Startup
        self.url = self.settings.value("url", "https://elearning.tgm.ac.at/")
        self.service = self.settings.value("service", "tgm_hoedmoodlesync")
        self.username = self.settings.value("username", None)
        self.password = self.settings.value("password", None)
        self.student_list_path = self.settings.value("studentlist",
                                                     "~/tgm - Die Schule der Technik/HIT - Abteilung für Informations"
                                                     "technologie - Dokumente/Organisation/Tools/studentlist.csv")
        self.moodle = None

        self.login()

    def login(self):
        if self.username and self.password:
            self.moodle = MoodleSync(self.url, self.username, self.password, self.service)
            self.download_courses()
        else:
            fail_to_load("Moodle Login not defined. Please check Settings.")

    def get_course_id(self, name):
        return self.courses[name]['id']

    def download_courses(self):
        if self.moodle:
            try:
                self.courses = self.moodle.get_recent_courses()
                self.set_courses()
                self.download_pushButton.setEnabled(self.all_none_checkBox.checkState())
            except Exception as e:
                fail_to_load("Failed to load courses. Please check Settings.", e)
        else:
            fail_to_load("Moodle URL/Key not defined. Please check Settings.")

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

        self.grades = self.grades.sort_values(by=['Gruppen', 'Schüler'])

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

        if self.create_competence_columns:
            self.competences = {}
            for module in list(self.grades.columns):
                if module not in ["Schüler", 'Klasse', 'Gruppen', 'Email']:
                    s = module.split(' ')[0].split('K')
                    if len(s) > 1:
                        module_type = s[0]
                        module_number = s[1]
                        if module_type in ['G', 'GE'] and len(module_number) >= 3:
                            competence_number = module_number[:2]
                            if competence_number in self.competences:
                                self.competences[competence_number].append(module)
                            else:
                                self.competences[competence_number] = [module]

            try:
                with open('modules.json', 'r') as f:
                    module_names = json.load(f)
            except FileNotFoundError:
                module_names = {}

            self.competence_helper = {}
            for competence_number, modules in self.competences.items():
                competence_name = f"{competence_number[0]}.{competence_number[1]} Grundkompetenz"
                if competence_number in module_names:
                    competence_name = module_names[competence_number]
                self.grades[competence_name] = '='
                self.competence_helper[competence_name] = competence_number

        if self.mark_suggestion:
            self.grades["Punkte"] = '='
            self.grades["Notenvorschlag"] = '='

        self.create_modules_list()

    def create_modules_list(self):
        self.checkboxes = []
        for i in reversed(range(self.tasks_verticalLayout.count())):
            self.tasks_verticalLayout.itemAt(i).widget().setParent(None)

        for module in list(self.grades.columns):
            if module not in ["Schüler", 'Klasse', 'Gruppen', 'Email', 'Punkte']:
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

        max_row = ws.max_row
        comp_dict = {'GK': [], 'GEK': [], 'EK': []}
        for cell in ws[1]:
            module = str(cell.value)
            cell_range = f"{cell.column_letter}2:{cell.column_letter}{max_row}"
            if module.startswith("GK"):
                custom_conditional_formatting(ws, cell_range, 'GK')
                comp_dict['GK'].append(cell.column_letter)
            elif module.startswith("EK"):
                custom_conditional_formatting(ws, cell_range, 'EK')
                comp_dict['EK'].append(cell.column_letter)
            elif module.startswith("GEK"):
                custom_conditional_formatting(ws, cell_range, 'GEK')
                comp_dict['GEK'].append(cell.column_letter)
            elif module.startswith("Wiederholung") or module.startswith("SMÜ"):
                for cx in ws[cell.column_letter]:
                    if cx.value == '-':
                        cx.value = 0.0
                custom_conditional_formatting(ws, cell_range, type='points',
                                              start=f'${cell.column_letter}${max_row + 2}',
                                              end=f'${cell.column_letter}${max_row + 3}')
                ws[f'A{max_row + 2}'].value = 'Bestehungsgrenze'
                ws[f'A{max_row + 2}'].font = Font(bold=True)
                ws[f'A{max_row + 3}'].value = 'Maximal erreichbar'
                ws[f'A{max_row + 3}'].font = Font(bold=True)
                ws[f'{cell.column_letter}{max_row + 2}'].value = 6
                ws[f'{cell.column_letter}{max_row + 3}'].value = 10
            elif module[1] == '.':  # if Kompetenz
                custom_conditional_formatting(ws, cell_range, 'K')
                for c_cell in ws[cell.column_letter]:
                    if c_cell.value == '=':
                        c_cell.value = '=' + ' & ";" & '.join(
                            [f"{get_column_for_module(ws, c)}{c_cell.row}" for c in
                             self.competences[self.competence_helper[module]]])
            elif module == 'Punkte' and self.mark_suggestion:
                for c_cell in ws[cell.column_letter]:
                    if c_cell.value == '=':
                        for module_type, module_letter_list in comp_dict.items():
                            for module_letter in module_letter_list:
                                affected_cell = f"SUMPRODUCT(--EXACT({module_letter}{c_cell.row}"
                                c_cell.value += f'{affected_cell},"GKü"))*-1+'
                                c_cell.value += f'{affected_cell},"EKü"))+'
                                c_cell.value += f'{affected_cell},"EKv"))*2+'
                                if module_type == 'GK':
                                    c_cell.value += f'{affected_cell},"ü"))*-1+'
                                elif module_type == 'GEK':
                                    c_cell.value += f'{affected_cell},"ü"))*-1+'
                                elif module_type == 'EK':
                                    c_cell.value += f'{affected_cell},"ü"))+'
                                    c_cell.value += f'{affected_cell},"v"))*2+'
                        c_cell.value = c_cell.value[:-1]
                custom_conditional_formatting(ws, cell_range, type='scale')
            elif module == 'Notenvorschlag' and self.mark_suggestion:
                sc = ws.max_column + 3  # start column

                marks_table = [['Note', 'Schlüssel', 'Anz.', 'P', '', 'Komp.', 'Anz.'],
                               [5, '', '', '', '', 'GK', len(comp_dict['GK'])],
                               [4, 'alle GK mind. ü', f'={get_column_letter(sc + 6)}2+{get_column_letter(sc + 6)}3',
                                f'={get_column_letter(sc + 2)}3*-1', '*', 'GEK', len(comp_dict['GEK'])],
                               [3, 'mind. GKv', 6, f'={get_column_letter(sc + 2)}4-{get_column_letter(sc + 2)}3', '',
                                'EK', len(comp_dict['EK'])],
                               [2, 'mind. EKü', 6, f'={get_column_letter(sc + 2)}5', '', '', ''],
                               [1, 'mind. EKv', 6, f'={get_column_letter(sc + 2)}6*2', '', '', '']]

                for row_number, rows in enumerate(marks_table):
                    for column_number, cell_value in enumerate(rows):
                        ws[f'{get_column_letter(sc + column_number)}{row_number + 1}'].value = cell_value

                tab = worksheet.table.Table(displayName="Table2",
                                            ref=f"{get_column_letter(sc)}1:{get_column_letter(sc + 3)}6")
                tab.tableStyleInfo = worksheet.table.TableStyleInfo(name="TableStyleMedium5", showRowStripes=False,
                                                                    showColumnStripes=False)
                ws.add_table(tab)

                tab = worksheet.table.Table(displayName="Table3",
                                            ref=f"{get_column_letter(sc + 5)}1:{get_column_letter(sc + 6)}4")
                tab.tableStyleInfo = worksheet.table.TableStyleInfo(name="TableStyleMedium6", showRowStripes=False,
                                                                    showColumnStripes=False)
                ws.add_table(tab)

                marks_table_column_dimensions = [8, 15, 8, 5, 5, 10, 8]
                for col, dim in enumerate(marks_table_column_dimensions):
                    ws.column_dimensions[get_column_letter(sc + col)].width = dim

                custom_conditional_formatting(ws, f'{get_column_letter(sc)}2:{get_column_letter(sc)}6', type='marks')

                mcl = f'${get_column_letter(sc)}$'  # mark_column_letter
                kpcl = f'${get_column_letter(sc + 3)}$'  # key_points_column_letter

                competences_letters_list = [*comp_dict['GK'], *comp_dict['GEK']]
                formular_string = '=_xlfn.IFS(SUMPRODUCT(--ISNUMBER(FIND({"n";"-"},'

                for c_cell in ws[cell.column_letter]:
                    if c_cell.value == '=':
                        c_cell.font = Font(bold=True)
                        pcc = f'{get_column_letter(c_cell.column - 1)}{c_cell.row}'  # points_cell_coordinate
                        cf = ' & '.join([f'{letter}{c_cell.row}' for letter in competences_letters_list])
                        c_cell.value = formular_string + cf + f')))>0,{mcl}2,{pcc}>={kpcl}6,{mcl}6,{pcc}>={kpcl}5,' \
                                                              f'{mcl}5,{pcc}>={kpcl}4,{mcl}4,{pcc}>={kpcl}3,{mcl}3)'
                custom_conditional_formatting(ws, cell_range, type='marks')

            elif module == 'Gruppen':
                custom_conditional_formatting(ws, cell_range, type='group')

        directory = self.settings.value('dir', "")
        ct = datetime.datetime.now()
        filename = f"{directory}/{ct.year}{str(ct.month).zfill(2)}{str(ct.day).zfill(2)}_{self.current_course}"

        file, _ = QFileDialog.getSaveFileName(self, "Export Grades", filename, "Excel files (*.xlsx)")
        if file:
            wb.save(file)
            self.settings.setValue("dir", file[:file.rfind("/")])

    def open_settings(self):
        settings = SettingsDlg(self.url, self.service, self.username, self.password, self.use_studentlist,
                               self.student_list_path, self.mark_suggestion, parent=self)
        if settings.exec():
            self.url = settings.ui.url_lineEdit.text()
            self.service = settings.ui.service_lineEdit.text()
            self.username = settings.ui.username_lineEdit.text()
            self.password = settings.ui.password_lineEdit.text()
            self.use_studentlist = settings.ui.checkBox.isChecked()
            self.student_list_path = settings.ui.studentlist_lineEdit.text()
            self.mark_suggestion = settings.ui.marksuggestion_checkBox.isChecked()

            self.settings.setValue("url", self.url)
            self.settings.setValue("service", self.service)
            self.settings.setValue("username", self.username)
            self.settings.setValue("password", self.password)
            self.settings.setValue("use_studentlist", self.use_studentlist)
            self.settings.setValue("studentlist", self.student_list_path)
            self.settings.setValue("mark_suggestion", self.mark_suggestion)
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
    def __init__(self, url, service, username, password, use_studentlist, studentlistpath, mark_suggestion,
                 parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.checkBox.setChecked(use_studentlist)
        self.ui.studentlist_lineEdit.setEnabled(use_studentlist)
        self.ui.marksuggestion_checkBox.setChecked(mark_suggestion)
        self.ui.checkBox.stateChanged.connect(self.checkbox_changed)
        self.ui.url_lineEdit.setText(url)
        self.ui.service_lineEdit.setText(service)
        self.ui.username_lineEdit.setText(username)
        self.ui.password_lineEdit.setText(password)
        self.ui.studentlist_lineEdit.setText(studentlistpath)

    def checkbox_changed(self):
        self.ui.studentlist_lineEdit.setEnabled(self.ui.checkBox.isChecked())


if __name__ == '__main__':
    setlocale(LC_NUMERIC, 'de_DE')
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
