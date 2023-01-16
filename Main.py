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
        self.MAIN_STACK.setCurrentIndex(0)
        self.LOGIN_signal = False
        self.BT_setting()
        self.UserInfo = []
        self.MAIN_BT_loginout.clicked.connect(self.Move_LoginPage)
        self.MAIN_BT_seller_order.clicked.connect(self.Move_InventoryManagement)
        # self.MAIN_BT_test1.clicked.connect(self.Move_Store)
        self.inventory_management = InventoryManagement()

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
            self.MAIN_BT_loginout.setText('로그인')
            self.BT_setting()
            self.MAIN_LB_loginfo.clear()
            self.MAIN_LB_loginfo2.clear()
            self.UserInfo = []
            self.LOGIN_signal = False
        else:
            self.PAGE_Login = LoginPage(self)
        
    def Move_Store(self):
        self.MAIN_STACK.setCurrentIndex(1)
        #db에서 등록된 상품 정보 가져오기
        #
        #

    def Move_InventoryManagement(self):
        widget.setCurrentIndex(1)















if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    ex = MainPage()
    inventory_management = InventoryManagement()

    widget.addWidget(ex)
    widget.addWidget(inventory_management)
    widget.setGeometry(0, 0, 450, 660)
    widget.show()

    sys.exit(app.exec_())