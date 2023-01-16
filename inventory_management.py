#-*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton


class InventoryManagement(QWidget):

    def __init__(self):
        super().__init__()
        self.quit = QPushButton(self)
        self.set_ui()

    def set_label(self):
        title = QLabel(self)
        title.setFont(QtGui.QFont('D2Coding', 20))
        title.setAlignment(Qt.AlignCenter)
        title.setText('재 고 관 리 ')
        title.setGeometry(0, 20, 450, 40)

        table_title = QLabel(self)
        table_title.setAlignment(Qt.AlignCenter)
        table_title.setText('재고 보유 현황표')
        table_title.setGeometry(0, 120, 450, 20)

    def set_btn(self):
        self.quit.setText('나가기')
        self.quit.setGeometry(370, 600, 60, 30)
        self.quit.clicked.connect(self.go_main)

    def set_ui(self):
        self.set_label()
        self.set_line()
        self.set_btn()

        self.setFont(QtGui.QFont('D2Coding'))

    def set_db(self):
        pass

    def go_main(self):
        print(self.user_info)
        self.parent().setCurrentIndex(0)