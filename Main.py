import sys

import pymysql
from PyQt5 import uic
from PyQt5.QtWidgets import *

from Login import LoginPage

MainUIset = uic.loadUiType("ui/main.ui")[0]
class MainPage(QWidget, MainUIset):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.MAIN_STACK.setCurrentIndex(0)

        self.MAIN_BT_loginout.clicked.connect(self.Move_LoginPage)
        self.MAIN_BT_test1.clicked.connect(self.Move_Store)


    def Move_LoginPage(self):
        self.PAGE_Login = LoginPage(self)
        
    def Move_Store(self):
        self.MAIN_STACK.setCurrentIndex(1)
        #db에서 등록된 상품 정보 가져오기
        #
        #
















if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPage()
    sys.exit(app.exec_())
