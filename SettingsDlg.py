from datetime import datetime
import os

from PyQt5.QtWidgets import QDialog, QFileDialog

from settings_dialog import Ui_Dialog
from ldap_download import ldap_studenlist_download


class SettingsDlg(QDialog):
    def __init__(self, username, password, use_studentlist, studentlistpath, cancel_number, ldap_url,
                 filename, ldap_extension, config_text="", parent=None):
        super().__init__(parent)
        self.filename = filename
        self.ldap_url = ldap_url
        self.ldap_extension = ldap_extension
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.checkBox.setChecked(use_studentlist)
        self.ui.studentlist_lineEdit.setEnabled(use_studentlist)
        self.ui.checkBox.stateChanged.connect(self.checkbox_changed)
        self.ui.username_lineEdit.setText(username)
        self.ui.password_lineEdit.setText(password)
        self.ui.studentlist_lineEdit.setText(studentlistpath)
        self.ui.open_pushButton.clicked.connect(self.open_dialog)
        self.ui.download_pushButton.clicked.connect(self.download)
        self.ui.cancle_number_spinBox.setValue(cancel_number)
        self.ui.config_label.setText(config_text)
        self.update_studentlistlabel()

    def checkbox_changed(self):
        self.ui.studentlist_lineEdit.setEnabled(self.ui.checkBox.isChecked())

    def open_dialog(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Studentlist", self.ui.studentlist_lineEdit.text(),
                                              "CSV files (*.csv)")
        if file:
            self.ui.studentlist_lineEdit.setText(file)

    def download(self):
        try:
            ldap_studenlist_download(self.ldap_url, self.ui.username_lineEdit.text() + self.ldap_extension,
                                     self.ui.password_lineEdit.text(), self.filename)
            self.update_studentlistlabel()
        except Exception as e:
            self.ui.last_download_label.setText("Error: " + str(e))

    def update_studentlistlabel(self):
        try:
            time = datetime.fromtimestamp(os.path.getmtime(self.filename))
            time = time.strftime('%Y-%m-%d %H:%M')
        except FileNotFoundError:
            time = "File not found!"
        self.ui.last_download_label.setText("last download: " + time)
