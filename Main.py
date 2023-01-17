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
        self.material_db = ''
        self.table_data = []
        self.MAIN_BT_loginout.clicked.connect(self.Move_LoginPage)
        self.MAIN_BT_seller_insert.clicked.connect(self.Move_test)
        self.MAIN_BT_plus.clicked.connect(lambda: self.rowplus(1))
        self.MAIN_BT_minus.clicked.connect(lambda: self.rowplus(0))
        self.MAIN_listcheck.clicked.connect(self.datacheck)
        self.MAIN_BT_buyer_buy.clicked.connect(self.Move_SellList)

        self.MAIN_sellList.doubleClicked.connect(lambda: self.check_selllist(0))
        self.le_sellnum.textChanged.connect(lambda: self.check_selllist(1))
        self.BT_toMain.clicked.connect(self.move_main)
        self.BT_toMain2.clicked.connect(self.move_main)
        self.BT_toBuy.clicked.connect(self.Check_order)

    def Check_order(self):
        try:
            db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM project7smartstore.user_info INNER JOIN project7smartstore.product_info "
                           "ON project7smartstore.product_info.store_name = project7smartstore.user_info.store_name "
                           f"WHERE project7smartstore.product_info.store_name='{self.lb_storeName2.text()}' and "
                           f"project7smartstore.product_info.product_name='{self.lb_productname2.text()}'")
            a = cursor.fetchall()
            print(a)
            cursor.execute("INSERT INTO project7smartstore.order_management "
                           f"(product_idx,product_name,product_quantity,customer_idx,seller_idx,store_name) "
                           f"values('{a[0][7]}','{a[0][8]}','{self.le_sellnum.text()}','{self.UserInfo[0]}',"
                           f"'{a[0][7]}','{a[0][9]}')")
            db.commit()
            db.close()
            msg = QMessageBox.information(self, "알림", "주문완료")
            self.le_sellnum.clear()
            self.Move_SellList()
        except pymysql.err.DataError:
            msg = QMessageBox.information(self, "알림", "정보를 입력해주세요")
            return

    def move_main(self):
        self.MAIN_STACK.setCurrentIndex(0)

    def check_selllist(self, signal):
        if signal == 0:
            self.frame.show()
            self.le_sellnum.clear()
            self.lb_productname2.setText(self.MAIN_sellList.item(self.MAIN_sellList.currentRow(), 0).text())
            self.lb_storeName2.setText(self.MAIN_sellList.item(self.MAIN_sellList.currentRow(), 1).text())
            self.lb_price2.setText(self.MAIN_sellList.item(self.MAIN_sellList.currentRow(), 2).text())
        elif signal == 1:
            try:
                self.lb_totalPrice2.show()
                self.lb_totalPrice.setText(f"{int(self.le_sellnum.text()) * int(self.lb_price2.text())}")
            except:
                self.lb_totalPrice.setText(" ")
                self.lb_totalPrice2.hide()

    def Move_SellList(self):
        self.MAIN_STACK.setCurrentIndex(3)
        self.le_sellnum.clear()
        # 판매리스트 세팅
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

    def Move_reset(self, signal):
        if signal == 0:
            self.MAIN_STACK.setCurrentIndex(0)
            self.MAIN_LE_productName.clear()
            self.MAIN_LE_productPrice.clear()
            self.MAIN_strorelist.clearContents()
            self.MAIN_strorelist.setRowCount(0)

    def Move_test(self):
        self.MAIN_STACK.setCurrentIndex(2)

        self.MAIN_listcl.clicked.connect(lambda: self.Move_reset(0))

        self.MAIN_strorelist.setColumnCount(3)  # 열추가
        # 헤더 크기조절
        header = self.MAIN_strorelist.horizontalHeader()
        header.resizeSection(0, 285)
        header.resizeSection(1, 50)
        header.resizeSection(2, 50)
        self.rowplus(1)

    # 동적 행 추가
    def rowplus(self,signal):
        if signal == 1:
            self.combobox = QComboBox()
            self.combobox.addItem('g')
            self.combobox.addItem('mg')
            self.combobox.addItem('ml')
            self.combobox.addItem('개')
            self.MAIN_strorelist.insertRow(self.MAIN_strorelist.rowCount())  # 동적row 추가
            self.MAIN_strorelist.setCellWidget(self.MAIN_strorelist.rowCount() - 1, 2, self.combobox)
            self.MAIN_strorelist.scrollToBottom()
        elif signal == 0:
            if self.MAIN_strorelist.rowCount() < 2:
                return
            self.MAIN_strorelist.removeRow(self.MAIN_strorelist.rowCount()-1)

    def move_to_bill_of_material(self):
        self.set_material_db()

    def datacheck(self):
        for i in range(self.MAIN_strorelist.rowCount()):
            for j in range(self.MAIN_strorelist.columnCount() - 1):
                try:
                    if self.MAIN_strorelist.item(i, j).text() == None or \
                            self.MAIN_strorelist.item(i,j).text() == "" or \
                            self.MAIN_strorelist.item(i, j).text() == " ":
                        msg = QMessageBox.information(self, "알림", "정보를 입력해주세요")
                        return
                except AttributeError:
                    msg = QMessageBox.information(self, "알림", "정보를 입력해주세요")
                    return

        try:
            db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
            cursor = db.cursor()
            # 제품명 존재하는지 체크
            test = cursor.execute("SELECT product_idx FROM project7smartstore.product_info "
                                  f"WHERE product_name='{self.MAIN_LE_productName.text()}'")
            print(test, "test")
            if test != 0:
                msg = QMessageBox.information(self, "알림", "이미 존재합니다.")
                return
            cursor.execute("INSERT INTO project7smartstore.product_info "
                           f"(product_name,store_name,product_price) "
                           f"VALUES('{self.MAIN_LE_productName.text()}','{self.UserInfo[5]}','{self.MAIN_LE_productPrice.text()}')")
            # db.commit()

            for i in range(self.MAIN_strorelist.rowCount()):
                cursor.execute("SELECT MAX(indexnum) FROM project7smartstore.bill_of_material")
                try:
                    temp = int(cursor.fetchone()[0]) + 1
                except TypeError:
                    temp = 1

                check = cursor.execute("SELECT material_idx FROM project7smartstore.bill_of_material "
                                       f"WHERE material_name = '{self.MAIN_strorelist.item(i, 0).text()}'")
                info = cursor.fetchall()

                cursor.execute("SELECT * FROM project7smartstore.product_info "
                               f"WHERE product_name='{self.MAIN_LE_productName.text()}' and store_name='{self.UserInfo[5]}'")
                temp2 = cursor.fetchall()
                if check == 0 :
                    cursor.execute("INSERT INTO project7smartstore.bill_of_material "
                                   "(material_idx,material_name,material_quantity,measure_unit,product_idx,product_name) "
                                   f"VALUES('PJ{str(temp).zfill(4)}',"
                                   f"'{self.MAIN_strorelist.item(i, 0).text()}',"
                                   f"'{self.MAIN_strorelist.item(i, 1).text()}',"
                                   f"'{self.MAIN_strorelist.cellWidget(i, 2).currentText()}',"
                                   f"'{temp2[0][0]}','{temp2[0][1]}')")
                else:
                    cursor.execute("insert into project7smartstore.bill_of_material "
                                   "(material_idx,material_name,material_quantity,measure_unit,product_idx,product_name) "
                                   f"VALUES('{info[0][0]}',"
                                   f"'{self.MAIN_strorelist.item(i, 0).text()}',"
                                   f"'{self.MAIN_strorelist.item(i, 1).text()}',"
                                   f"'{self.MAIN_strorelist.cellWidget(i, 2).currentText()}',"
                                   f"'{temp2[0][0]}','{temp2[0][1]}')")
                    
        except AttributeError:
            msg = QMessageBox.information(self, "알림", "잘못된 정보입니다. 확인해주세요.")
            return
        db.commit()
        db.close()

    def set_bom_table(self):
        self.bom_ingredient_table.verticalHeader().setVisible(False)
        self.bom_ingredient_table.setColumnWidth(0, 72)
        self.bom_ingredient_table.setColumnWidth(1, 60)
        self.bom_ingredient_table.setColumnWidth(2, 240)

        self.get_bom_table_db()

        self.bom_select_menu.currentTextChanged.connect(self.set_bom_table_logic)

    def get_bom_table_db(self):

        conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                               db='project7smartstore')
        c = conn.cursor()

        # material_name에 따라 product_name을 묶어주기 위한 view 생성
        c.execute('''CREATE OR REPLACE VIEW product_group 
        AS SELECT any_value(material_idx) AS material_idx, 
        group_concat(product_name) AS product_name 
        FROM bill_of_material 
        GROUP BY material_name;''')

        # 재료의 수량과 단위를 하나의 값으로 묶고 view, material_name 값을 함께 갖는 데이터 추출
        c.execute('''SELECT DISTINCT b.material_name, 
        (SELECT CONCAT(cast(b.inventory_quantity AS CHAR), a.measure_unit)) AS material_quantity, 
        c.product_name 
        FROM bill_of_material AS a 
        LEFT JOIN material_management AS b 
        ON b.material_name=a.material_name 
        INNER JOIN product_group AS c 
        ON c.material_idx=a.material_idx;''')

        self.table_data = c.fetchall()
        self.bom_table_default_data()

    def bom_table_default_data(self):
        self.bom_ingredient_table.setRowCount(len(self.table_data))
        for i in range(len(self.table_data)):
            for j in range(len(self.table_data[i])):
                self.set_bom_table_data_tooltip(i, j, i, j)

    def set_bom_table_logic(self):
        if self.bom_select_menu.currentText() == '전체':
            self.bom_table_default_data()

        else:
            bom_table_row = 0
            self.bom_ingredient_table.setRowCount(bom_table_row)
            for i in range(len(self.table_data)):
                # self.table_data = [material_name, material_quantity+measure_unit, product_name GROUP BY material_name]
                if self.bom_select_menu.currentText() in self.table_data[i][2]:
                    bom_table_row += 1
                    bom_table_column = 0
                    self.bom_ingredient_table.setRowCount(bom_table_row)
                    for j in range(len(self.table_data[i])):
                        self.set_bom_table_data_tooltip(bom_table_row - 1, bom_table_column, i, j)
                        bom_table_column += 1

    def set_bom_table_data_tooltip(self, row, column, i, j):
        self.bom_ingredient_table.setItem(row, column, QTableWidgetItem(self.table_data[i][j]))
        self.bom_ingredient_table.item(row, column).setToolTip(self.table_data[i][j])

    def bom_to_main(self):
        self.MAIN_STACK.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainPage()

    sys.exit(app.exec_())
