from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from create_tables import *
from machine_tables import *
from masters import masters
from qa_tables import *
from label import *
class MainWindow(QMainWindow,masters,label_opt):
    def __init__(self,my_user):
        self.my_user = my_user
        
    def load_users(self):
        all_users = User.select()
        for u in all_users:
            #delete 
            cell_widget_delete = QWidget()
            layout = QHBoxLayout(cell_widget_delete)

            deleteBtn = QPushButton(self.ui_widget.user_tableWidget)
            deleteBtn.setIcon(QIcon("icons/trash.png"))
            deleteBtn.setFixedWidth(50)

            deleteBtn.clicked.connect(lambda _, user_id=u.id: self.delete_user(user_id))
            
            layout.addWidget(deleteBtn)

            layout.setContentsMargins(0, 0, 0, 0)  # Optional: adjust spacing as needed
            cell_widget_delete.setLayout(layout)
            
            #edit 
            cell_widget_edit = QWidget()
            layout = QHBoxLayout(cell_widget_edit)

            editBtn = QPushButton(self.ui_widget.user_tableWidget)
            editBtn.setIcon(QIcon("icons/info.png"))
            editBtn.setFixedWidth(50)

            editBtn.clicked.connect(lambda _, user_id=u.id: self.navigate('edit_user',user_id= user_id))

            layout.addWidget(editBtn)

            layout.setContentsMargins(0, 0, 0, 0)  # Optional: adjust spacing as needed
            cell_widget_edit.setLayout(layout)

            rowPosition = self.ui_widget.user_tableWidget.rowCount()
            self.ui_widget.user_tableWidget.insertRow(rowPosition)
            self.ui_widget.user_tableWidget.setItem(rowPosition , 0, QTableWidgetItem(u.username))
            self.ui_widget.user_tableWidget.setItem(rowPosition , 1, QTableWidgetItem(u.operator_id))
            self.ui_widget.user_tableWidget.setItem(rowPosition , 2, QTableWidgetItem('******'))
            self.ui_widget.user_tableWidget.setItem(rowPosition , 3, QTableWidgetItem(u.op_level.name))
            self.ui_widget.user_tableWidget.setCellWidget(rowPosition , 4, cell_widget_delete)
            self.ui_widget.user_tableWidget.setCellWidget(rowPosition , 5, cell_widget_edit)
        pass                                                                                  
    def load_user_level(self):
        
        for l in UserLevel.select():
            if l.rank == self.my_user.op_level.rank or l.rank > self.my_user.op_level.rank:
                self.ui_widget.Level.addItem(l.name)
        pass
    def load_user(self,user_id):
        print(user_id)
        qu = User.get_or_none(User.id == str(user_id))
        if qu:
            self.ui_widget.usernameEdit.setText(qu.username)
            self.ui_widget.idEdit.setText(qu.operator_id)
            self.ui_widget.passwordEdit.setText(qu.password)
            self.ui_widget.Level.addItem(qu.op_level.name)
    def delete_user(self,user_id):
        error_dialog = QMessageBox()
        error_dialog.setWindowIcon(QIcon('ico.jpeg'))
        error_dialog.setWindowTitle('Confirm')
        error_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        error_dialog.setText('Please confirm. Deleting a User can delete many other rows of data')
        res = error_dialog.exec()
        if res :
            User.delete
            query = User.delete().where(User.id == user_id)
            query.execute()
            self.navigate('actionUser_Manager')
    def update_user(self,user_id):
        username = self.ui_widget.usernameEdit.text()
        operator_id = self.ui_widget.idEdit.text()
        password = self.ui_widget.passwordEdit.text()
        op_level = self.ui_widget.Level.currentText()
        try:
            q = User.update(username = username , operator_id = operator_id, password = password,op_level = op_level).where(User.id == user_id)
            q.execute()
            return True
        except Exception as e:
            self.error_dialog = QMessageBox()
            self.error_dialog.setWindowIcon(QIcon('ico.jpeg'))
            self.error_dialog.setWindowTitle('An error was found')
            self.error_dialog.setText(str(e))
            self.error_dialog.exec()
            return False
        
    def save_user(self):
        username = self.ui_widget.usernameEdit.text()
        operator_id = self.ui_widget.idEdit.text()
        password = self.ui_widget.passwordEdit.text()
        op_level = self.ui_widget.Level.currentText()
        try:
            q = User.insert(username = username , operator_id = operator_id, password = password,op_level = op_level)
            q.execute()
            return True
        except Exception as e:
            self.error_dialog = QMessageBox()
            self.error_dialog.setWindowIcon(QIcon('ico.jpeg'))
            self.error_dialog.setWindowTitle('An error was found')
            self.error_dialog.setText(str(e))
            self.error_dialog.exec()
            return False
        pass
    def update_user_and_return(self,user_id):
        r =  self.update_user(user_id)
        if r:
            self.navigate('actionUser_Manager')
    def save_user_and_return(self):
        r =  self.save_user()
        if r:
            self.navigate('actionUser_Manager')
        
    def save_user_and_stay(self):
        r =  self.save_user()
        if r:
            self.navigate('add_new_user')
        
    #returns the qaction name, so we can navigate pages dynamicly
    def return_name(self):
        use = self.sender().objectName()
        self.navigate(use)
    def __init__(self,user):
        self.ui_widget = None
        self.my_user = user
        super().__init__()
        uic.loadUi("designer/main.ui", self)  # Load the .ui file
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        for menu in self.menuBar().findChildren(QMenu):
            for action in  menu.actions():
                action.triggered.connect( self.return_name)
    def navigate(self,use,user_id = None):
        #cental widget holder
        ui_file = ""
        match(use):
            case 'actionC_C_LABEL':
                self.label_setting('CC')
            case 'actionMachine_Types':
                self.open(Machine_type)
            case 'actionTestModelMaster':
                self.open(TestModel)
            case 'actionMachine':
                self.open(Machine)
            case 'actionPartNumberMaster':
                self.open(Part_nr)
            case 'actionPartCategoryMaster':
                self.open(Category)
            case 'actionApplicatorMaster':
                self.open(Applicator)
            case 'actionApplicatorCA':
                self.open(ApplicatorDieType)
            case 'actionSpare_part_Master':
                self.open(SparePart)
            case 'actionTestMaster':
                self.open(Test)
            case 'actionUser_Manager':
                ui_file = "designer/user_manager.ui"
            case 'add_new_user':
                ui_file = "designer/add_new_user.ui"
            case 'edit_user':
                ui_file = "designer/edit_user.ui"
            case 'actionCuttingList':
                self.open(CuttingList)
        if ui_file:
            while self.central_widget.count() > 0 :
                to_del = self.central_widget.widget(0)
                self.central_widget.removeWidget(to_del)
                to_del.deleteLater()
            self.central_widget = QStackedWidget()
            self.setCentralWidget(self.central_widget)
            self.ui_widget = myWidget(ui_file)
            self.central_widget.addWidget(self.ui_widget)

        match(use):
            case 'edit_user':
                self.load_user(user_id= user_id)
                self.load_user_level()
                #connect(lambda _, user_id=u.id: self.navigate('edit_user',user_id= user_id))
                self.ui_widget.Confirm.clicked.connect(self.update_user_and_return)
                self.central_widget.setCurrentIndex(1)
            case 'actionUser_Manager':
                self.load_users()
                self.ui_widget.add_new_user.clicked.connect(self.return_name)
            case 'add_new_user':
                self.load_user_level()
                self.ui_widget.Confirm.clicked.connect(self.save_user_and_return)
                self.ui_widget.Add.clicked.connect(self.save_user_and_stay)
                self.central_widget.setCurrentIndex(1)
        return False
class myWidget(QWidget):
    def __init__(self,ui_file):
        QWidget.__init__(self)
        uic.loadUi(ui_file, self)