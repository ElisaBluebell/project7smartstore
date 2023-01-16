#-*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton


# import

class InventoryManagement(QWidget):

    def __init__(self):
        super().__init__()
        self.title = QLabel(self)
        self.quit = QPushButton(self)
        self.set_ui()

    def set_label(self):
        self.title.setText('aa')
        self.title.setGeometry(20, 20, 20, 20)

        table_title = QLabel(self)

    def set_line(self):
        pass

    def set_btn(self):
        self.quit.setText('나가기')
        self.quit.setGeometry(40, 40, 40, 40)


    def set_combo(self):
        pass

    def set_table(self):
        pass

    def set_ui(self):
        self.set_label()
        self.set_line()
        self.set_btn()
        self.set_combo()
        self.set_table()

        self.setFont(QtGui.QFont('D2Coding'))

    def set_db(self):
        pass