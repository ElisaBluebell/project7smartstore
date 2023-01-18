import sys

import pymysql
from PyQt5 import uic
from PyQt5.QtWidgets import *

from Login import LoginPage
from buy_ingredient_window import Ingredient

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
        self.MAIN_BT_buyer_orderlist.clicked.connect(self.Move_buylist)
        self.MAIN_sellList.doubleClicked.connect(lambda: self.check_selllist(0))
        self.le_sellnum.textChanged.connect(lambda: self.check_selllist(1))
        self.BT_toMain.clicked.connect(self.move_main)
        self.BT_toMain2.clicked.connect(self.move_main)
        self.BT_toMain3.clicked.connect(self.move_main)
        self.BT_toBuy.clicked.connect(self.Check_order)

        self.MAIN_BT_seller_order.clicked.connect(self.move_to_bill_of_material)
        self.ingredient_window = Ingredient()



    def Move_buylist(self):
        self.MAIN_STACK.setCurrentIndex(4)
        db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
        cursor = db.cursor()
        a = cursor.execute("SELECT * "
                           "FROM project7smartstore.order_management INNER JOIN project7smartstore.product_info "
                           "ON project7smartstore.order_management.product_idx = project7smartstore.product_info.product_idx "
                           f"WHERE project7smartstore.order_management.customer_idx = '{self.UserInfo[0]}'")
        print(a)
        if a == 0 :
            return
        buylist = cursor.fetchall()
        print("[",buylist)
        self.MAIN_buylist.setRowCount(a)
        self.MAIN_buylist.setColumnCount(4)
        for i in range(a):
            self.MAIN_buylist.setItem(i, 0, QTableWidgetItem(str(buylist[i][3])))
            self.MAIN_buylist.setItem(i, 1, QTableWidgetItem(str(buylist[i][4])))
            self.MAIN_buylist.setItem(i, 2, QTableWidgetItem(str(buylist[i][11])))
            self.MAIN_buylist.setItem(i, 3, QTableWidgetItem(str(buylist[i][6])))




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
            msg = QMessageBox.information(self, "알림", "정보를 확인해주세요")
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
            if self.MAIN_LE_productName.text() == None or self.MAIN_LE_productName.text().strip() == "":
                msg = QMessageBox.information(self, "알림", "정보를 입력해주세요")
                return
            db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
            cursor = db.cursor()
            # 제품명 존재하는지 체크
            test = cursor.execute("SELECT product_idx FROM project7smartstore.product_info "
                                  f"WHERE product_name='{self.MAIN_LE_productName.text()}'")

            print(test, "test")
            if test != 0:
                msg = QMessageBox.information(self, "알림", "이미 존재하는 상품명입니다.")
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
                    cursor.execute(f"call project7smartstore.BoM_insert('PJ{str(temp).zfill(4)}','{self.MAIN_strorelist.item(i, 0).text()}',"
                                   f"'{self.MAIN_strorelist.item(i, 1).text()}',"
                                   f"'{self.MAIN_strorelist.cellWidget(i, 2).currentText()}',"
                                   f"'{temp2[0][0]}','{temp2[0][1]}')")
                else:
                    cursor.execute(f"call project7smartstore.BoM_insert('{info[0][0]}','{self.MAIN_strorelist.item(i, 0).text()}',"
                                   f"'{self.MAIN_strorelist.item(i, 1).text()}',"
                                   f"'{self.MAIN_strorelist.cellWidget(i, 2).currentText()}',"
                                   f"'{temp2[0][0]}','{temp2[0][1]}')")
                    
        except AttributeError:
            msg = QMessageBox.information(self, "알림", "정보를 입력해주세요.")
            return
        except pymysql.err.DataError:
            msg = QMessageBox.information(self, "알림", "잘못된 정보입니다.")
            return
        except pymysql.err.OperationalError:
            msg = QMessageBox.information(self, "알림", " operational Error")
            return
        db.commit()
        db.close()

    def set_material_db(self):
        conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                               db='project7smartstore')
        c = conn.cursor()

        c. execute('SELECT * FROM `project7smartstore`.`bill_of_material`')
        # 0 = BoM idx, 1 = 재료 idx, 2 = 재료명, 3 = 재료 소모량, 4 = 계량 단위, 5 = 상품(사용처) idx, 6 = 상품명
        self.material_db = c.fetchall()

        c.close()
        conn.close()

    def move_to_bill_of_material(self):
        self.set_material_db()
        # User_Info 0 = 유저 idx, 1 = 유저 id, 2 = 유저 pw, 3 = 유저명, 4 = 전화번호, 5 = 상호명, 6 = 유저 분류
        self.bom_store_name.setText(self.UserInfo[5])

        self.bom_go_back.clicked.connect(self.bom_to_main)
        self.buy_ingredient.clicked.connect(self.buy_ingredient_window)

        self.define_bom_combo_item()
        self.set_bom_table()

        self.MAIN_STACK.setCurrentIndex(1)

    def define_bom_combo_item(self):
        if not self.bom_select_menu.currentText():
            # 기본값 전체 설정
            self.bom_select_menu.addItem('전체')
            menu = []
            # DB상 상품명을 중복되지 않게 메뉴 리스트에 삽입
            for item in self.material_db:
                if item[6] not in menu:
                    menu.append(item[6])
            # 메뉴 선택 콤보박스에 추가
            for item in menu:
                if item:
                    self.bom_select_menu.addItem(item)

    def set_bom_table(self):
        self.bom_ingredient_table.verticalHeader().setVisible(False)
        self.bom_ingredient_table.setColumnWidth(0, 72)
        self.bom_ingredient_table.setColumnWidth(1, 60)
        self.bom_ingredient_table.setColumnWidth(2, 240)

        self.get_bom_table_db()
        self.bom_select_menu.currentTextChanged.connect(self.menu_changed)

    def get_bom_table_db(self):

        conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                               db='project7smartstore')
        c = conn.cursor()

        c.execute('call project7smartstore.group_product_by_material();')

        # 프로시저 호출을 통해 받아온 DB값, 0 = 재료명(명칭과 계량 단위가 겹치지 않음), 1 = 보유 수량, 2 = 사용처 그룹
        self.table_data = c.fetchall()
        self.bom_table_default_data()

        c.close()
        conn.close()

    def bom_table_default_data(self):
        # 프로시저를 통해 받아온 DB의 요소 수만큼 반복함
        self.bom_ingredient_table.setRowCount(len(self.table_data))

        for i in range(len(self.table_data)):
            for j in range(len(self.table_data[i])):
                self.set_bom_table_data_tooltip(i, j, i, j)

    def set_bom_table_data_tooltip(self, row, column, i, j):
        self.bom_ingredient_table.setItem(row, column, QTableWidgetItem(self.table_data[i][j]))
        self.bom_ingredient_table.item(row, column).setToolTip(self.table_data[i][j])

    def menu_changed(self):
        self.set_bom_table_logic()
        self.set_bom_available()

    def set_bom_table_logic(self):
        if self.bom_select_menu.currentText() == '전체':
            self.bom_table_default_data()

        else:
            # bom_table_row, bom_table_column은 set_bom_table_data_tooltip 함수에서 각각 row, column으로 사용함
            # 반복문에서의 i, j값과 별개로 데이터 축적시마다 1개씩 증가해 올바른 표의 행과 열에 들어감
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

    def set_bom_available(self):
        if self.bom_select_menu.currentText() == '전체':
            self.bom_available.setText('')

        else:
            conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                                   db='project7smartstore')
            c = conn.cursor()

            # 콤보박스에서 선택된 메뉴의 재료들 중 가장 작은 재료재고/재료소모량 값을 가져옴
            c.execute(f'''SELECT min(b.inventory_quantity DIV a.material_quantity) AS produce_available 
            FROM bill_of_material AS a 
            INNER JOIN material_management AS b 
            ON a.material_name=b.material_name 
            WHERE a.product_name="{self.bom_select_menu.currentText()}"''')

            producible = c.fetchall()[0][0]

            if producible < 10:
                self.bom_available.setStyleSheet("Color: red")
            else:
                self.bom_available.setStyleSheet("Color: black")

            self.bom_available.setText(f'{str(producible)}개 제작 가능')

    def buy_ingredient_window(self):
        self.ingredient_window.show()

    def bom_to_main(self):
        self.MAIN_STACK.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainPage()

    sys.exit(app.exec_())
