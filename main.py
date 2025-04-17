from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from create_tables import User
from insert import InsertDialog
my_user = None

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        self.setWindowIcon(QIcon('icon.jpeg'))
        file_menu = self.menuBar().addMenu("&Utility")

        self.setWindowTitle("MES++")
        adduser_action = QAction(QIcon("icon/add.png"),"Add user", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)
    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()
class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(120)
        self.setWindowIcon(QIcon('icon.jpeg'))

        layout = QVBoxLayout()
        self.userinput = QLineEdit()
        self.userinput.setPlaceholderText("user")
        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        # self.passinput.setText("123456")
        self.passinput.setPlaceholderText("Enter Password.")
        self.QBtn = QPushButton()
        self.QBtn.setText("Login")
        self.setWindowTitle('Login')
        self.QBtn.clicked.connect(self.login)

        title = QLabel("Login")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.userinput)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)
        

    def login(self):
        username = self.userinput.text()
        qu = User.get_or_none(User.username == username)
        # qu = User.select(User.username,User.operator_id,User.username,User.op_level).where(User.username == username)
        pw = ""
        if qu:
            pw = (qu.password)
            if(self.passinput.text() == pw):
                my_user = qu
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Wrong Password')
        else:
            QMessageBox.warning(self, 'Error', 'User not registered')
            
app = QApplication(sys.argv)
passdlg = LoginDialog()
if(passdlg.exec_() == QDialog.Accepted):
    window = MainWindow()
    window.showMaximized()
    window.show()
sys.exit(app.exec_())