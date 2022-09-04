#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QGridLayout, QDialog, QDialogButtonBox, QLineEdit, QCheckBox
from PyQt6.QtCore import Qt
#----------------------------------------------------------------------

    # Class
class QLoginResponse:
    def __init__(self, username = '', password = '', rememberChecked = None):
        self.username = username
        self.password = password
        if rememberChecked != None:
            if rememberChecked == Qt.CheckState.Checked: self.rememberChecked = True
            else: self.rememberChecked = False



class QLoginDialog(QDialog):
    def __init__(self, parent = None, langData = {'title': 'QLoginDialog', 'usernamePlaceholder': 'Username', 'passwordPlaceholder': 'Password', 'rememberText': 'Remember Me'}, username = '', rememberCheck = False, rememberChecked = False):
        super().__init__(parent)

        self.setWindowTitle(langData['title'])

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QGridLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText(langData['usernamePlaceholder'])
        self.username.setText(username)
        self.layout.addWidget(self.username, 0, 0)

        self.password = QLineEdit()
        self.password.setPlaceholderText(langData['passwordPlaceholder'])
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password, 1, 0)

        if rememberCheck:
            self.rememberCheckBox = QCheckBox()
            self.rememberCheckBox.setText(langData['rememberText'])
            if rememberChecked: self.rememberCheckBox.setCheckState(Qt.CheckState.Checked)
            else: self.rememberCheckBox.setCheckState(Qt.CheckState.Unchecked)
            self.layout.addWidget(self.rememberCheckBox, 2, 0)
        self.__rememberCheck__ = rememberCheck
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        if username:
            self.password.setFocus()


    def getText(self):
        if self.exec():
            if self.username.text == '' or self.password.text == '': return None
            if self.__rememberCheck__:
                return QLoginResponse(self.username.text(), self.password.text(), self.rememberCheckBox.checkState())
            return QLoginResponse(self.username.text(), self.password.text())
#----------------------------------------------------------------------
