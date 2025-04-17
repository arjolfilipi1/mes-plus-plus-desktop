from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from create_tables import *
from PyQt5.QtCore import QDate

#get all rel_model rows
def get_all_related_rows(foreign_key_field):
    related_model = foreign_key_field.rel_model
    return related_model.select()

# Function to get the value of a field dynamically
def get_field_value(instance, field_name):
    try:
        if hasattr(instance, field_name):  # Check if the field exists
            return getattr(instance, field_name)
        else:
            raise AttributeError(f"Field '{field_name}' does not exist in the model.")
    except Exception as e:
        pass
        print(instance,field_name,e,'end')
class myWidget(QWidget):
    def __init__(self,ui_file):
        QWidget.__init__(self)
        uic.loadUi(ui_file, self)
def get_field_types(model):
    f_t ={}
    for f_n,f_o in model._meta.fields.items():
        rel_model = None
        if isinstance( f_o,ForeignKeyField):
            rel_model = f_o.rel_model.select()
        f_t[f_n] = [type(f_o).__name__,rel_model]
    return f_t

class masters():
    def on_row_click(self,row,col):
        self.selected = True
        self.row = row
        for index,name in enumerate(self.field_names):
            val = self.tableWidget.item(row,index).text()
            target = name
            le = self.ui_widget.findChild(QLineEdit,target)
            if le:
                le.setText(val)
                
            sb = self.ui_widget.findChild(QSpinBox,target)
            if sb:
                try:
                    sb.setValue(int(val))
                except:
                    sb.setValue(0)
                
            dsb = self.ui_widget.findChild(QDoubleSpinBox,target)
            if dsb:
                try:
                    dsb.setValue(float(val))
                except:
                    dsb.setValue(0)
            cb = self.ui_widget.findChild(QCheckBox,target)
            if cb:
                v = True if val=='True' else False
                cb.setChecked( v )
            #default %Y-%m-%d
            de = self.ui_widget.findChild(QDateEdit,target)
            if de and val != 'None' and val:
                sval = (val).split("-")
                try:
                    d = QDate(int(sval[0]), int(sval[1]), int(sval[2]))
                    de.setDate(d)
                except Exception as e:
                    e = "Date format is not correct. \n Please repair"
                    self.error_dialog = QMessageBox()
                    self.error_dialog.setWindowIcon(QIcon('ico.jpeg'))
                    self.error_dialog.setWindowTitle('An error was found')
                    self.error_dialog.setText((e))
                    self.error_dialog.exec()
                    
            fk = self.ui_widget.findChild(QComboBox,target)
            if fk:
                ind = fk.findText(val)
                if ind:
                    fk.setCurrentIndex( ind )
                else:
                    fk.setCurrentIndex(0)
        return row,col
    def save_new(self):
        save_data ={}
        for index,name in enumerate(self.field_names):
            le = self.ui_widget.findChild(QLineEdit,name)
            if le:
                save_data[name] = le.text()
                
            sb = self.ui_widget.findChild(QSpinBox,name)
            if sb:
                save_data[name] = sb.value()
                
            dsb = self.ui_widget.findChild(QDoubleSpinBox,name)
            if dsb:
                save_data[name] = dsb.value()

            cb = self.ui_widget.findChild(QCheckBox,name)
            if cb:
                v = 'True' if cb.isChecked() else 'False'
                save_data[name] = v
                
            #default %Y-%m-%d
            de = self.ui_widget.findChild(QDateEdit,name)
            if de:
                save_data[name] = de.date().toString()
            fk = self.ui_widget.findChild(QComboBox,name)
            if fk:
                save_data[name] = fk.currentText()
            pass
        
        try:
            new = self.model.create(**save_data)
            new.save()
            self.open(self.model)
        except Exception as e:
            self.error_dialog = QMessageBox()
            self.error_dialog.setWindowIcon(QIcon('ico.jpeg'))
            self.error_dialog.setWindowTitle('An error was found')
            self.error_dialog.setText(str(e))
            self.error_dialog.exec()

    def delete_row(self):
        if self.selected:
            
            try:
                to_del = self.data[self.row]
                to_del.delete_instance()
                self.open(self.model)
            except Exception as e:
                e = str(e)
                if 'matching query does not exist' in e:
                    e = "Data was not found in the database. \n Make sure data was not changed"
                self.error_dialog = QMessageBox()
                self.error_dialog.setWindowIcon(QIcon('ico.jpeg'))
                self.error_dialog.setWindowTitle('An error was found')
                self.error_dialog.setText((e))
                self.error_dialog.exec()
    def update_row(self):
        if self.selected != None:
            original_data = self.data[self.row]
            save_data = {}
            for index,name in enumerate(self.field_names):
                le = self.ui_widget.findChild(QLineEdit,name)
                if le:
                    data = le.text()
                    
                sb = self.ui_widget.findChild(QSpinBox,name)
                if sb:
                    data = int(sb.value())
                    
                dsb = self.ui_widget.findChild(QDoubleSpinBox,name)
                if dsb:
                    data = float(dsb.value())

                cb = self.ui_widget.findChild(QCheckBox,name)
                if cb:
                    v = True if cb.isChecked() else False
                    data = v
                    
                #default %Y-%m-%d
                de = self.ui_widget.findChild(QDateEdit,name)
                if de:
                    data = de.date().toPyDate()
                fk = self.ui_widget.findChild(QComboBox,name)
                if fk:
                    data = fk.currentText() if fk.currentText() else None
                # save_data[name] = data
                setattr(original_data, name, data)
            try:

                original_data.save()
                self.open(self.model)
            
            except Exception as e:
                e = str(e)
                if 'matching query does not exist' in e:
                    e = "Data was not found in the database. \n Make sure data was not changed"
                self.error_dialog = QMessageBox()
                self.error_dialog.setWindowIcon(QIcon('ico.jpeg'))
                self.error_dialog.setWindowTitle('An error was found')
                self.error_dialog.setText((e))
                self.error_dialog.exec()
        pass
        
    def open(self,model):
        self.data = []
        self.model = model
        self.selected = False
        ui_file = "designer/master.ui"
        while self.central_widget.count() > 0 :
            to_del = self.central_widget.widget(0)
            self.central_widget.removeWidget(to_del)
            to_del.deleteLater()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.ui_widget = uic.loadUi(ui_file)
        self.central_widget.addWidget(self.ui_widget)
        self.ui_widget.adjustSize()
        layout = QGridLayout()
        fields = get_field_types(model)
        r =0
        c = 0
        self.field_names =[]
        for f,td in fields.items():
            t = td[0]
            self.field_names.append(f)
            label = QLabel(f)
            layout.addWidget(label,r,c)
            if t == 'CharField':
                inputwidget = QLineEdit( objectName = f )
            elif t =='BooleanField':
                inputwidget = QCheckBox( objectName = f )
            elif t =='DateField':
                inputwidget = QDateEdit( objectName = f )
                inputwidget.setDisplayFormat("d-MM-yyyy")
            elif t =='IntegerField':
                inputwidget = QSpinBox( objectName = f )
                inputwidget.setRange(1000000000)
            elif t =='FloatField':
                inputwidget = QDoubleSpinBox( objectName = f )
                inputwidget.setMinimum(0)
                inputwidget.setMaximum(100000)
            elif t =='ForeignKeyField':
                inputwidget = QComboBox( objectName = f )
                inputwidget.addItem(None)
                # '''
                opt = td[1]
                for o in opt:
                    str_opt = str(o)
                    inputwidget.addItem(str_opt)
                # '''
            else:
                inputwidget = QWidget()
            inputwidget.setFixedHeight(50)
            layout.addWidget(inputwidget,r,c+1)
            c +=2
            if c == 4:
                c = 0
                r +=1
        #c u d buttons
        separator = QWidget()
        separator.setFixedHeight(10)
        layout.addWidget(separator,r+1,c)
        c = 0
        r +=2
        addButton = QPushButton('Add data', self)
        addButton.clicked.connect(self.save_new)
        addButton.setStyleSheet("background-color : green") 
        layout.addWidget(addButton,r,c)
        
        deleteButton = QPushButton('Delete data', self)
        deleteButton.clicked.connect(self.delete_row)
        deleteButton.setStyleSheet("background-color : red") 
        layout.addWidget(deleteButton,r,c+1)
        
        updateButton = QPushButton('Update data', self)
        updateButton.clicked.connect(self.update_row)
        updateButton.setStyleSheet("background-color : blue") 
        layout.addWidget(updateButton,r,c+2)
        layout.addWidget(separator,r+1,c)
        r += 2
        self.tableWidget = QTableWidget()
        #load table headers
        
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(len(self.field_names))
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)  # Disable stretching for manual width
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(( f for f in self.field_names ))
        
        #load data
        rows_data = model.select()
        tr = 0
        self.data = rows_data
        for row in rows_data:
            self.tableWidget.insertRow(tr)
            tc = 0
            for name in self.field_names:
                res = get_field_value(row,name)
                
                self.tableWidget.setItem(tr, tc, QTableWidgetItem(str(res)))
                tc += 1
            tr +=1
        self.tableWidget.setFixedHeight(50*tr)
        self.tableWidget.cellClicked.connect(self.on_row_click)
        layout.addWidget(self.tableWidget,r,0,1,4)
        
        container = QFrame()
        container.setLayout(layout)
        
        s_a = QScrollArea()
        s_a.setWidget(container)
        s_a.setWidgetResizable(True)
        self.ui_widget.verticalLayout.addWidget(s_a)