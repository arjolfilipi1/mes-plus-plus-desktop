from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys,os
from create_tables import User
from main_window import MainWindow

from PyQt5 import uic


class LoginWindow(QMainWindow):
    def __init__(self):
        self.my_user = None
        super().__init__()
        uic.loadUi("designer/login.ui", self)  # Load the .ui file
        self.LoginButton.clicked.connect(self.on_button_click)
        self.UserInput.returnPressed.connect(self.on_button_click)
        self.PasswordInput.returnPressed.connect(self.on_button_click)
        if os.path.exists('data.txt'):
            with open("data.txt","r") as file:
                data = file.read()
                if data:
                    username,password = (data).split(";;;;;")
                    self.UserInput.setText(username)
                    self.PasswordInput.setText(password)
    def accept(self):
        self.next = MainWindow(self.my_user)
        self.next.showMaximized()
        self.close()
    def on_button_click(self):
        username = self.UserInput.text()
        password = self.PasswordInput.text()
        qu = User.get_or_none(User.username == username)
        pw = ""
        if qu:
            pw = (qu.password)
            if(password == pw):
                self.my_user = qu
                with open("data.txt", "w") as file:
                    file.write(username+";;;;;"+password)
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Wrong Password')
        else:
            QMessageBox.warning(self, 'Error', 'User not registered')

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())