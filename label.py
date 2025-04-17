from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from create_tables import *
from PyQt5.QtCore import QDate


class label_opt():
    def label_setting(self,type_of_label):
        ui_file = "designer/label_edit.ui"
        while self.central_widget.count() > 0 :
            to_del = self.central_widget.widget(0)
            self.central_widget.removeWidget(to_del)
            to_del.deleteLater()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.ui_widget = uic.loadUi(ui_file)
        self.central_widget.addWidget(self.ui_widget)
        self.ui_widget.adjustSize()
        titleText = self.ui_widget.findChild(QLabel,'title')
        if type_of_label == 'CC':
            titleText.setText("C&C Label Settings")
        return None