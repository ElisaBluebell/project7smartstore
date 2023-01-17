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
        self.LOGIN_signal = False
        self.BT_setting()
        self.UserInfo = []
        self.MAIN_BT_loginout.clicked.connect(self.Move_LoginPage)
        self.MAIN_BT_seller_insert.clicked.connect(self.Move_test)
        self.MAIN_BT_plus.clicked.connect(self.rowplus)
        self.MAIN_listcheck.clicked.connect(self.datacheck)
        self.MAIN_BT_buyer_buy.clicked.connect(self.Move_SellList)

        self.MAIN_sellList.doubleClicked.connect(lambda: self.check_SellList(0))
        self.le_sellnum.textChanged.connect(lambda: self.check_SellList(1))
        self.BT_toMain.clicked.connect(self.Move_Main)
        self.BT_toMain2.clicked.connect(self.Move_Main)
        self.BT_toBuy.clicked.connect(self.Check_order)



    def Check_order(self):
        db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM project7smartstore.user_info INNER JOIN project7smartstore.product_info "
                       "ON project7smartstore.product_info.store_name = project7smartstore.user_info.store_name "
                       f"WHERE project7smartstore.product_info.store_name='{self.lb_storeName2.text()}' and "
                       f"project7smartstore.product_info.product_name='{self.lb_productname2.text()}'")
        a = cursor.fetchall()
        print(a)
        cursor.execute("INSERT INTO project7smartstore.order_management "
                       f"(product_idx,product_name,product_quantity,customer_idx,customer_name,seller_idx,seller_name,store_name) "
                       f"values('{a[0][7]}','{a[0][8]}','{self.le_sellnum.text()}','{self.UserInfo[0]}','{self.UserInfo[3]}',"
                       f"'{a[0][0]}','{a[0][1]}','{a[0][9]}')")
        db.commit()
        db.close()


    def Move_Main(self):
        self.MAIN_STACK.setCurrentIndex(0)


    def check_SellList(self, signal):
        if signal == 0:
            self.frame.show()
            self.le_sellnum.clear()
            self.lb_productname2.setText(self.MAIN_sellList.item(self.MAIN_sellList.currentRow(), 0).text())
            self.lb_storeName2.setText(self.MAIN_sellList.item(self.MAIN_sellList.currentRow(), 1).text())
            self.lb_price2.setText(self.MAIN_sellList.item(self.MAIN_sellList.currentRow(), 2).text())
        elif signal == 1:
            try:
                self.lb_totalPrice2.show()
                self.lb_totalPrice.setText(f"{int(self.le_sellnum.text())*int(self.lb_price2.text())}")
            except:
                self.lb_totalPrice.setText(" ")
                self.lb_totalPrice2.hide()

    def Move_SellList(self):
        self.MAIN_STACK.setCurrentIndex(3)
        self.le_sellnum.clear()
        #판매리스트 세팅
        db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
        cursor = db.cursor()
        num = cursor.execute("SELECT * FROM project7smartstore.user_info inner JOIN project7smartstore.product_info "
                             "on project7smartstore.product_info.store_name = project7smartstore.user_info.store_name")
        sellList = cursor.fetchall()
        print(sellList)
        self.MAIN_sellList.setRowCount(num)
        self.MAIN_sellList.setColumnCount(4)
        for i in range(num):
            self.MAIN_sellList.setItem(i, 0, QTableWidgetItem(str(sellList[i][8])))
            self.MAIN_sellList.setItem(i, 1, QTableWidgetItem(str(sellList[i][9])))
            self.MAIN_sellList.setItem(i, 2, QTableWidgetItem(str(sellList[i][10])))
        self.frame.hide()

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


    def Move_reset(self,signal):
        if signal == 0:
            self.MAIN_STACK.setCurrentIndex(0)
            self.MAIN_name.clear()
            self.MAIN_strorelist.clearContents()
            self.MAIN_strorelist.setRowCount(0)

    def Move_test(self):
        self.MAIN_STACK.setCurrentIndex(1)

        self.MAIN_listcl.clicked.connect(lambda: self.Move_reset(0))

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
        self.combobox.addItem('g')
        self.combobox.addItem('mg')
        self.combobox.addItem('ml')
        self.combobox.addItem('개')
        self.MAIN_strorelist.insertRow(self.MAIN_strorelist.rowCount())  # 동적row 추가
        self.MAIN_strorelist.setCellWidget(self.MAIN_strorelist.rowCount() - 1, 2, self.combobox)
        self.MAIN_strorelist.scrollToBottom()

    def move_to_bill_of_material(self):
        self.MAIN_STACK.setCurrentIndex(2)
        self.bom_go_back.clicked.connect(self.bom_to_main)

    def datacheck(self):
        for i in range(self.MAIN_strorelist.rowCount()):
            for j in range(self.MAIN_strorelist.columnCount()-1):
                try:
                    if self.MAIN_strorelist.item(i, j).text() == None or self.MAIN_strorelist.item(i, j).text() == "" or self.MAIN_strorelist.item(i, j).text() == " ":
                        msg = QMessageBox.information(self, "알림", "정보를 입력해주세요")
                        return
                except:
                    msg = QMessageBox.information(self, "알림", "정보를 입력해주세요")
                    return

        db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
        cursor = db.cursor()
        for i in range(self.MAIN_strorelist.rowCount()):
            cursor.execute("SELECT MAX(indexnum) FROM project7smartstore.bill_of_material")
            try:
                temp = int(cursor.fetchone()[0])+1
            except:
                temp = 1
            try:
                cursor.execute("insert into project7smartstore.bill_of_material "
                               "(material_idx,material_name,material_quantity,measure_unit) "
                               f"VALUES('PJ{str(temp).zfill(6)}',"
                               f"'{self.MAIN_strorelist.item(i, 0).text()}',"
                               f"'{self.MAIN_strorelist.item(i, 1).text()}',"
                               f"'{self.MAIN_strorelist.cellWidget(i, 2).currentText()}')")
            except:
                msg = QMessageBox.information(self, "알림", "잘못된 정보입니다. 확인해주세요.")
                return
        db.commit()
        db.close()

    def bom_to_main(self):
        self.MAIN_STACK.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainPage()

    sys.exit(app.exec_())
