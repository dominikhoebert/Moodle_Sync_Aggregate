from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QRadioButton


class ImportDialog(QDialog):
    def __init__(self, sheets: list):
        super().__init__()

        self.setWindowTitle("Choose Sheet to Import")
        self.btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.label = QLabel("Choose Sheet to Import:")
        self.layout.addWidget(self.label)
        self.radio_buttons = []
        for sheet in sheets:
            rb = QRadioButton(sheet)
            self.radio_buttons.append(rb)
            self.layout.addWidget(rb)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_selected_sheet(self):
        for button in self.radio_buttons:
            if button.isChecked():
                return button.text()
