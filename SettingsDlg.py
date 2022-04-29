from datetime import datetime
import os

from PyQt5.QtWidgets import QDialog, QFileDialog

from settings_dialog import Ui_Dialog
from ldap_download import ldap_studenlist_download


class SettingsDlg(QDialog):
    def __init__(self, url, service, username, password, use_studentlist, studentlistpath, mark_suggestion,
                 username_extension, cancle_number, filename="ldap_studentlist.csv", parent=None):
        super().__init__(parent)
        self.filename = filename
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
        self.ui.extension_lineEdit.setText(username_extension)
        self.ui.studentlist_lineEdit.setText(studentlistpath)
        self.ui.open_pushButton.clicked.connect(self.open_dialog)
        self.ui.download_pushButton.clicked.connect(self.download)
        self.ui.cancle_number_spinBox.setValue(cancle_number)
        self.update_studentlistlabel()

    def checkbox_changed(self):
        self.ui.studentlist_lineEdit.setEnabled(self.ui.checkBox.isChecked())

    def open_dialog(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Studentlist", self.ui.studentlist_lineEdit.text(),
                                              "CSV files (*.csv)")
        if file:
            self.ui.studentlist_lineEdit.setText(file)

    def download(self):
        ldap_studenlist_download(self.ui.username_lineEdit.text() + self.ui.extension_lineEdit.text(),
                                 self.ui.password_lineEdit.text(), self.filename)
        self.update_studentlistlabel()

    def update_studentlistlabel(self):
        try:
            time = datetime.fromtimestamp(os.path.getmtime(self.filename))
            time = time.strftime('%Y-%m-%d %H:%M')
        except FileNotFoundError:
            time = "File not found!"
        self.ui.last_download_label.setText("last download: " + time)
