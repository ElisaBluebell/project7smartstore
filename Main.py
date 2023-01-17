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
        self.MAIN_BT_seller_order.clicked.connect(self.move_to_bill_of_material)

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
        self.combobox.addItem('g')
        self.combobox.addItem('ml')
        self.combobox.addItem('개')
        self.MAIN_strorelist.insertRow(self.MAIN_strorelist.rowCount())  # 동적row 추가
        self.MAIN_strorelist.setCellWidget(self.MAIN_strorelist.rowCount() - 1, 2, self.combobox)
        self.MAIN_strorelist.scrollToBottom()

    def set_material_db(self):
        conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                               db='project7smartstore')
        c = conn.cursor()

        c. execute('SELECT * FROM `project7smartstore`.`bill_of_material`')
        self.material_db = c.fetchall()

        c.close()
        conn.close()

    def move_to_bill_of_material(self):
        self.set_material_db()

        self.bom_new_menu.clicked.connect(self.Move_test)
        self.bom_go_back.clicked.connect(self.bom_to_main)

        self.define_bom_combo_item()
        self.set_bom_table()

        self.MAIN_STACK.setCurrentIndex(2)

    def define_bom_combo_item(self):
        if not self.bom_select_menu.currentText():
            self.bom_select_menu.addItem('전체')
            menu = []
            for item in self.material_db:
                if item[6] not in menu:
                    menu.append(item[6])
            for item in menu:
                if item:
                    self.bom_select_menu.addItem(item)

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
                self.set_bom_table_data_tooltip(i, j)

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
                    self.bom_ingredient_table.setRowCount(bom_table_row)
                    for j in range(len(self.table_data[i])):
                        self.set_bom_table_data_tooltip(i, j)

    def set_bom_table_data_tooltip(self, row, column):
        self.bom_ingredient_table.setItem(row, column, QTableWidgetItem(self.table_data[row][column]))
        self.bom_ingredient_table.item(row, column).setToolTip(self.table_data[row][column])

    def bom_to_main(self):
        self.MAIN_STACK.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainPage()

    sys.exit(app.exec_())
