import sys

import pymysql
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *

from Login import LoginPage
from inventory_management import InventoryManagement

MainUIset = uic.loadUiType("ui/main.ui")[0]
class MainPage(QWidget, MainUIset):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.MAIN_STACK.setCurrentIndex(0)
        self.LOGIN_signal = False
        self.BT_setting()
        self.UserInfo = []
        self.MAIN_BT_loginout.clicked.connect(self.Move_LoginPage)
        self.MAIN_BT_seller_insert.clicked.connect(self.Move_test)

    def BT_setting(self):
        if self.LOGIN_signal == False:
            self.MAIN_BT_seller_insert.hide()
            self.MAIN_BT_seller_order.hide()
            self.MAIN_BT_buyer_buy.hide()
            self.MAIN_BT_buyer_orderlist.hide()
        else:
            if self.UserInfo[6] == 'True':
                self.MAIN_BT_seller_insert.show()
                self.MAIN_BT_seller_order.show()
            else:
                self.MAIN_BT_buyer_buy.show()
                self.MAIN_BT_buyer_orderlist.show()


    def Move_LoginPage(self):
        if self.LOGIN_signal:
            # 로그아웃시 초기화
            self.LOGIN_signal = False
            self.MAIN_BT_loginout.setText('로그인')
            self.BT_setting()
            self.MAIN_LB_loginfo.clear()
            self.MAIN_LB_loginfo2.clear()
            self.UserInfo = []

        else:
            self.PAGE_Login = LoginPage(self)

    def Move_test(self):
        self.MAIN_STACK.setCurrentIndex(1)
        self.MAIN_strorelist.setColumnCount(3)  # 열추가
        #헤더 크기조절
        header = self.MAIN_strorelist.horizontalHeader()
        header.resizeSection(0, 285)
        header.resizeSection(1, 50)
        header.resizeSection(2, 50)
        self.rowplus()
        self.MAIN_BT_plus.clicked.connect(self.rowplus)

    # 동적 행 추가
    def rowplus(self):
        self.combobox = QComboBox()
        self.combobox.addItem('mg')
        self.combobox.addItem('ml')
        self.combobox.addItem('개')
        self.MAIN_strorelist.insertRow(self.MAIN_strorelist.rowCount())  # 동적row 추가
        self.MAIN_strorelist.setCellWidget(self.MAIN_strorelist.rowCount() - 1, 2, self.combobox)
        self.MAIN_strorelist.scrollToBottom()








if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainPage()

    sys.exit(app.exec_())
