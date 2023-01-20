import random
import sys
import threading
import time
from threading import Thread

import pymysql
from PyQt5 import uic
from PyQt5.QtWidgets import *
import datetime

from Login import LoginPage
from buy_ingredient_window import Ingredient
from customer_service import CustomerService

MainUIset = uic.loadUiType("ui/main.ui")[0]


class MainPage(QWidget, MainUIset):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.MAIN_STACK.setCurrentIndex(0)
        self.LOGIN_signal = False
        self.th_siganl = False
        self.BT_setting()
        self.UserInfo = []
        self.material_db = ''
        self.table_data = []
        self.combobox = QComboBox()
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
        self.BT_toMain4.clicked.connect(self.move_main)
        self.BT_toBuy.clicked.connect(self.Check_order)
        self.MAIN_BT_seller_orderlist.clicked.connect(self.Move_selllist)
        self.MAIN_BT_seller_order.clicked.connect(self.move_to_bill_of_material)
        self.faq_management.clicked.connect(self.move_to_faq)
        self.ingredient_window = Ingredient()
        self.customer_service = ''
        auto_faq = threading.Thread(target=self.make_auto_faq, daemon=True)
        auto_faq.start()

        self.order_checked.clicked.connect(self.order_accept)
        self.BT_alert.clicked.connect(self.Move_selllist)
        self.BT_alert2.clicked.connect(self.Move_selllist)
        self.BT_alert3.clicked.connect(self.Move_selllist)
        # 012
        self.tete.clicked.connect(self.tttt)

    def tttt(self):
        auto_order = Thread(target=self.auto_ordering, args=())
        auto_order.daemon = True
        auto_order.start()

    def auto_ordering(self):
        while 1:
            print('구매중')
            db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM project7smartstore.product_info")
            product = cursor.fetchall()
            # print("상품",product)
            sell_product_info = product[random.randrange(0, len(product))]
            print("판매상품", sell_product_info)

            cursor.execute("SELECT * FROM project7smartstore.user_info INNER JOIN project7smartstore.product_info "
                           "ON project7smartstore.product_info.store_name = project7smartstore.user_info.store_name "
                           f"WHERE project7smartstore.product_info.store_name='{sell_product_info[2]}' and "
                           f"project7smartstore.product_info.product_name='{sell_product_info[1]}'")
            a = cursor.fetchall()
            print("a", a)
            cursor.execute(f'call project7smartstore.material_num_check("{sell_product_info[1]}")')
            num = cursor.fetchone()[0]
            if num == 0:
                print("구매불가 재고 부족")
                time.sleep(5)
                continue
            sellnum = random.randrange(num) // 7
            if sellnum != 0:
                cursor.execute("INSERT INTO project7smartstore.order_management "
                               f"(order_date,product_idx,product_name,product_quantity,"
                               f"customer_idx,seller_idx,store_name) "
                               f"values('{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}','{a[0][7]}','{a[0][8]}',"
                               f"'{sellnum}','3','{a[0][0]}','{a[0][9]}')")
                db.commit()
                db.close()
            time.sleep(5)

    def order_accept(self):
        select = self.MAIN_selllist.selectedItems()
        print("길이", len(select))
        for i in range(0, len(select), 6):
            db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
            cursor = db.cursor()
            a = cursor.execute("UPDATE project7smartstore.order_management SET checked=1 "
                               f"WHERE checked=0 and order_idx='{select[i].text()}'")
            db.commit()
            db.close()
        msg = QMessageBox.information(self, "알림", "주문확인")
        self.Move_selllist()

    def Move_selllist(self):
        self.MAIN_STACK.setCurrentIndex(6)

        db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
        cursor = db.cursor()
        a = cursor.execute("SELECT A.*,B.product_price FROM project7smartstore.order_management A "
                           "INNER JOIN project7smartstore.product_info B ON A.product_idx=B.product_idx "
                           f"WHERE A.seller_idx = '{self.UserInfo[0]}' and A.checked = '0'")
        print(a)
        if a == 0:
            self.MAIN_selllist.setRowCount(0)
            return
        Blist = cursor.fetchall()
        print("[", Blist)
        self.MAIN_selllist.setRowCount(a)
        self.MAIN_selllist.setColumnCount(6)
        for i in range(a):
            self.MAIN_selllist.setItem(i, 0, QTableWidgetItem(str(Blist[i][0])))
            self.MAIN_selllist.setItem(i, 1, QTableWidgetItem(str(Blist[i][1])))
            self.MAIN_selllist.setItem(i, 2, QTableWidgetItem(str(Blist[i][2])))
            self.MAIN_selllist.setItem(i, 3, QTableWidgetItem(str(Blist[i][4])))
            self.MAIN_selllist.setItem(i, 4, QTableWidgetItem(str(Blist[i][5])))
            self.MAIN_selllist.setItem(i, 5, QTableWidgetItem(str(Blist[i][5] * Blist[i][9])))

    def Move_buylist(self):
        self.MAIN_STACK.setCurrentIndex(7)
        db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
        cursor = db.cursor()
        a = cursor.execute("SELECT * "
                           "FROM project7smartstore.order_management INNER JOIN project7smartstore.product_info "
                           "ON project7smartstore.order_management.product_idx = "
                           "project7smartstore.product_info.product_idx "
                           f"WHERE project7smartstore.order_management.customer_idx = '{self.UserInfo[0]}'")
        print(a)
        if a == 0:
            return
        buylist = cursor.fetchall()
        print("[", buylist)
        self.MAIN_buylist.setRowCount(a)
        self.MAIN_buylist.setColumnCount(5)
        for i in range(a):
            self.MAIN_buylist.setItem(i, 0, QTableWidgetItem(str(buylist[i][4])))
            self.MAIN_buylist.setItem(i, 1, QTableWidgetItem(str(buylist[i][5])))
            self.MAIN_buylist.setItem(i, 2, QTableWidgetItem(str(buylist[i][12])))
            self.MAIN_buylist.setItem(i, 3, QTableWidgetItem(str(buylist[i][7])))
            if buylist[i][8] == 0:
                self.MAIN_buylist.setItem(i, 4, QTableWidgetItem('주문확인중'))
            else:
                self.MAIN_buylist.setItem(i, 4, QTableWidgetItem('주문확인완료'))

    def test_th(self):
        self.th_siganl = True
        thread_order = Thread(target=self.thread_act, args=())
        thread_order.daemon = True
        thread_order.start()

    def thread_act(self):
        bt = [self.BT_alert, self.BT_alert2, self.BT_alert3]
        if self.LOGIN_signal:
            while self.th_siganl:
                if not self.LOGIN_signal:
                    return
                db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
                cursor = db.cursor()
                a = cursor.execute("SELECT * FROM project7smartstore.order_management WHERE checked='0'")
                print("gg", a)
                cursor.close()
                if a > 0:
                    if self.MAIN_STACK.currentIndex() == 0:
                        temp = bt[0]
                    elif self.MAIN_STACK.currentIndex() == 1:
                        temp = bt[1]
                    elif self.MAIN_STACK.currentIndex() == 2:
                        temp = bt[2]
                    else:
                        time.sleep(2)
                        continue
                    temp.setText(f"새로운 주문도착 {a}건")
                    for i in range(30):
                        opacity_effect = QGraphicsOpacityEffect(temp)
                        opacity_effect.setOpacity(0.07 * i)
                        temp.setGraphicsEffect(opacity_effect)
                        time.sleep(0.02)
                    for j in range(40):
                        opacity_effect = QGraphicsOpacityEffect(temp)
                        opacity_effect.setOpacity(2 - (0.05 * j))
                        temp.setGraphicsEffect(opacity_effect)
                        time.sleep(0.02)
                else:
                    for temp in bt:
                        temp.setText(" ")
                    time.sleep(2)

    def Check_order(self):
        try:
            db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM project7smartstore.user_info INNER JOIN project7smartstore.product_info "
                           "ON project7smartstore.product_info.store_name = project7smartstore.user_info.store_name "
                           f"WHERE project7smartstore.product_info.store_name='{self.lb_storeName2.text()}' and "
                           f"project7smartstore.product_info.product_name='{self.lb_productname2.text()}'")
            a = cursor.fetchall()
            print("a", a)
            cursor.execute(f'call project7smartstore.material_num_check("{self.lb_productname2.text()}")')
            num = cursor.fetchone()[0]
            if num < int(self.le_sellnum.text()):
                QMessageBox.information(self, "알림", "구매 수량을 확인해주세요")
                return
            cursor.execute("INSERT INTO project7smartstore.order_management "
                           f"(order_date,product_idx,product_name,product_quantity,customer_idx,seller_idx,store_name) "
                           f"values('{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}','{a[0][7]}','{a[0][8]}',"
                           f"'{self.le_sellnum.text()}','{self.UserInfo[0]}','{a[0][0]}','{a[0][9]}')")
            db.commit()
            db.close()
            QMessageBox.information(self, "알림", "주문완료")
            self.le_sellnum.clear()
            self.Move_SellList()
        except pymysql.err.DataError:
            QMessageBox.information(self, "알림", "정보를 입력해주세요")
            return

    def move_main(self):
        self.MAIN_STACK.setCurrentIndex(0)

    def check_selllist(self, signal):
        if signal == 0:
            if self.MAIN_sellList.item(self.MAIN_sellList.currentRow(), 3).text() == "구매불가":
                QMessageBox.information(self, "알림", "구매할 수 없는 상품입니다.")
                return
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
            conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                                   db='project7smartstore')
            c = conn.cursor()
            # 재고확인해서 만들 수 있는 갯수 체크
            c.execute(f'call material_num_check("{str(sellList[i][8])}")')
            sellnum = c.fetchall()[0][0]
            if sellnum == 0 or sellnum is None:
                sellnum = '구매불가'
            self.MAIN_sellList.setItem(i, 3, QTableWidgetItem(str(sellnum)))
        self.frame.hide()

    def BT_setting(self):
        if not self.LOGIN_signal:
            self.frame_buyer.hide()
            self.frame_seller.hide()
            self.alert_frame.hide()
        else:
            if self.UserInfo[6] == 'True':
                self.frame_seller.show()
                self.alert_frame.show()
                self.test_th()
            else:
                self.frame_buyer.show()

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
    def rowplus(self, signal):
        if signal == 1:
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
            self.MAIN_strorelist.removeRow(self.MAIN_strorelist.rowCount() - 1)

    def datacheck(self):
        for i in range(self.MAIN_strorelist.rowCount()):
            for j in range(self.MAIN_strorelist.columnCount() - 1):
                try:
                    if self.MAIN_strorelist.item(i, j).text() is None or \
                            self.MAIN_strorelist.item(i, j).text() == "" or \
                            self.MAIN_strorelist.item(i, j).text() == " ":
                        QMessageBox.information(self, "알림", "정보를 입력해주세요")
                        return
                except AttributeError:
                    QMessageBox.information(self, "알림", "정보를 입력해주세요")
                    return

        try:
            if self.MAIN_LE_productName.text() is None or self.MAIN_LE_productName.text().strip() == "":
                QMessageBox.information(self, "알림", "정보를 입력해주세요")
                return
            db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
            cursor = db.cursor()
            # 제품명 존재하는지 체크
            test = cursor.execute("SELECT product_idx FROM project7smartstore.product_info "
                                  f"WHERE product_name='{self.MAIN_LE_productName.text()}'")
            print(test, "test")
            if test != 0:
                QMessageBox.information(self, "알림", "이미 존재합니다.")
                return
            cursor.execute("INSERT INTO project7smartstore.product_info "
                           f"(product_name,store_name,product_price) "
                           f"VALUES('{self.MAIN_LE_productName.text()}','{self.UserInfo[5]}',"
                           f"'{self.MAIN_LE_productPrice.text()}')")
            # db.commit()

            for i in range(self.MAIN_strorelist.rowCount()):
                cursor.execute("SELECT MAX(indexnum) FROM project7smartstore.bill_of_material")
                try:
                    temp = int(cursor.fetchone()[0]) + 1
                    print(temp)
                except TypeError:
                    temp = 1

                check = cursor.execute("SELECT material_idx FROM project7smartstore.bill_of_material "
                                       f"WHERE material_name = '{self.MAIN_strorelist.item(i, 0).text()}'")
                print("check", check)
                info = cursor.fetchall()

                cursor.execute("SELECT * FROM project7smartstore.product_info "
                               f"WHERE product_name='{self.MAIN_LE_productName.text()}' "
                               f"and store_name='{self.UserInfo[5]}'")
                temp2 = cursor.fetchall()
                if check == 0:
                    cursor.execute(f"call project7smartstore.BoM_insert('PJ{str(temp).zfill(4)}',"
                                   f"'{self.MAIN_strorelist.item(i, 0).text()}',"
                                   f"'{self.MAIN_strorelist.item(i, 1).text()}',"
                                   f"'{self.MAIN_strorelist.cellWidget(i, 2).currentText()}',"
                                   f"'{temp2[0][0]}','{temp2[0][1]}')")
                else:
                    cursor.execute(f"call project7smartstore.BoM_insert('{info[0][0]}',"
                                   f"'{self.MAIN_strorelist.item(i, 0).text()}',"
                                   f"'{self.MAIN_strorelist.item(i, 1).text()}',"
                                   f"'{self.MAIN_strorelist.cellWidget(i, 2).currentText()}',"
                                   f"'{temp2[0][0]}','{temp2[0][1]}')")

        except AttributeError:
            QMessageBox.information(self, "알림", "정보를 입력해주세요")
            return
        except pymysql.err.DataError:
            QMessageBox.information(self, "알림", "잘못된 정보입니다.")
            return
        except pymysql.err.OperationalError:
            QMessageBox.information(self, "알림", " operational Error")
            return
        db.commit()
        db.close()

# ===================================================== 재료 관리 =====================================================

    def set_material_db(self):
        sql = 'SELECT * FROM bill_of_material;'
        self.material_db = self.exe_db_smartstore(sql)
        # 0 = BoM idx, 1 = 재료 idx, 2 = 재료명, 3 = 재료 소모량, 4 = 계량 단위, 5 = 상품(사용처) idx, 6 = 상품명

    def set_bill_of_material_ui(self):
        self.set_material_db()
        # User_Info 0 = 유저 idx, 1 = 유저 id, 2 = 유저 pw, 3 = 유저명, 4 = 전화번호, 5 = 상호명, 6 = 유저 분류
        self.bom_store_name.setText(self.UserInfo[5])

        self.bom_go_back.clicked.connect(self.bom_to_main)
        self.buy_ingredient.clicked.connect(self.buy_ingredient_window)

        self.define_bom_combo_item()
        self.set_bom_table()

    def move_to_bill_of_material(self):
        self.set_bill_of_material_ui()
        self.MAIN_STACK.setCurrentIndex(1)

    def define_bom_combo_item(self):
        self.bom_select_menu.clear()
        # 기본값 전체 설정
        self.bom_select_menu.addItem('전체')
        self.fill_menu_list()

    def fill_menu_list(self):
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
        if len(self.bom_select_menu.currentText()) > 0:
            self.bom_select_menu.currentTextChanged.connect(self.menu_changed)

    def get_bom_table_db(self):
        sql = 'CALL group_product_by_material();'
        # 0 = 재료명(명칭과 계량 단위가 겹치지 않음), 1 = 보유 수량, 2 = 사용처 그룹
        self.table_data = self.exe_db_smartstore(sql)
        self.loop_put_all_data_in()

    def loop_put_all_data_in(self):
        # 툴팁과 데이터를 테이블에 삽입하기 위해 행 설정 및 반복문 실행
        self.bom_ingredient_table.setRowCount(len(self.table_data))

        for i in range(len(self.table_data)):
            for j in range(len(self.table_data[i])):
                self.set_bom_table_data_tooltip(i, j, i, j)

    def set_bom_table_data_tooltip(self, row, column, i, j):
        self.bom_ingredient_table.setItem(row, column, QTableWidgetItem(self.table_data[i][j]))
        self.bom_ingredient_table.item(row, column).setToolTip(self.table_data[i][j])

    def menu_changed(self):
        self.default_bom_table_and_label()
        self.set_bom_table_logic()
        self.set_bom_available()

    def default_bom_table_and_label(self):
        if self.bom_select_menu.currentText() == '전체':
            self.loop_put_all_data_in()
            self.bom_available.setText('')

    def set_bom_table_logic(self):
        # bom_table_row, bom_table_column은 set_bom_table_data_tooltip 함수에서 각각 row, column으로 사용함
        # 반복문에서의 i, j값과 별개로 데이터 축적시마다 1개씩 증가해 올바른 표의 행과 열에 삽입
        if self.bom_select_menu.currentText() != '전체' and len(self.bom_select_menu.currentText()) > 0:

            bom_table_row = 0
            self.bom_ingredient_table.setRowCount(bom_table_row)

            for i in range(len(self.table_data)):
                if self.bom_select_menu.currentText() in self.table_data[i][2]:
                    bom_table_row += 1
                    bom_table_column = 0

                    self.bom_ingredient_table.setRowCount(bom_table_row)

                    for j in range(len(self.table_data[i])):
                        self.set_bom_table_data_tooltip(bom_table_row - 1, bom_table_column, i, j)
                        bom_table_column += 1

    def set_bom_available(self):
        if self.bom_select_menu.currentText() != '전체':
            if len(self.bom_select_menu.currentText()) > 0:

                # 콤보박스에서 선택된 메뉴의 재료들 중 가장 작은 재료재고/재료소모량 값을 가져옴
                sql = f'CALL get_minimun_ingredient_left("{self.bom_select_menu.currentText()}");'
                producible = self.exe_db_smartstore(sql)[0][0]

                self.set_bom_available_text(producible)

    def change_bom_available_text_color(self, producible):
        if producible < 10:
            self.bom_available.setStyleSheet("Color: red")
        else:
            self.bom_available.setStyleSheet("Color: black")

    def set_bom_available_text(self, producible):
        self.change_bom_available_text_color(producible)
        self.bom_available.setText(f'{str(producible)}개 제작 가능')

    def buy_ingredient_window(self):
        self.ingredient_window.reset_items()
        self.ingredient_window.show()

    def bom_to_main(self):
        self.MAIN_STACK.setCurrentIndex(0)

# ===================================================== 문의 관리 =====================================================

    def move_to_faq(self):
        self.set_faq_page()
        self.MAIN_STACK.setCurrentIndex(4)

    def set_faq_page(self):
        self.set_faq_table()
        self.set_faq_btn()
        self.set_faq_label()

    def set_faq_table(self):
        faq_data = self.get_faq_data()
        store_faq_data = self.check_store_match_faq(faq_data)
        self.set_faq_table_rowcount(store_faq_data)
        self.faq_data_putin_table(store_faq_data)
        self.faq_table.clicked.connect(lambda: self.faq_detail(store_faq_data))

    def set_faq_btn(self):
        self.faq_go_back.clicked.connect(self.faq_to_bom)

    def set_faq_label(self):
        self.faq_store_name.setText(f'{self.UserInfo[5]}')

    @staticmethod
    def get_faq_data():
        conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                               db='project7smartstore')
        c = conn.cursor()

        c.execute('SELECT * FROM faq_management')
        faq_data = c.fetchall()

        c.close()
        conn.close()

        return faq_data

    def check_store_match_faq(self, faq_data):
        store_faq = []
        for i in range(len(faq_data)):
            if self.UserInfo[0] == faq_data[i][1]:
                store_faq.append(faq_data[i])

        return store_faq

    def set_faq_table_rowcount(self, store_faq_data):
        self.faq_table.setRowCount(len(store_faq_data))

    def faq_data_putin_table(self, store_faq_data):
        for i in range(len(store_faq_data)):
            self.faq_table.setItem(i, 0, QTableWidgetItem(store_faq_data[i][4]))
            self.faq_table.setItem(i, 1, QTableWidgetItem(str(store_faq_data[i][7])))
            self.faq_table.setItem(i, 2, QTableWidgetItem(store_faq_data[i][6]))
            self.faq_table.setItem(i, 3, QTableWidgetItem(self.faq_process_int_to_str(store_faq_data[i][9])))

    @staticmethod
    def faq_process_int_to_str(faq_process):
        if faq_process == 0:
            faq_process_text = '읽지 않음'

        elif faq_process == 1:
            faq_process_text = '읽음'

        else:
            faq_process_text = '답변 완료'

        return faq_process_text

    def comment(self):
        odered_comment = ['맛있어요.', '맛없어요.', '너무 매워요.', '너무 달아요.', '너무 써요', '너무 많아요.',
                          '너무 적어요.', '왜 팔아요?', '배달이 늦었어요.']
        not_odered_comment = ['맛있나요?', '맵나요?', '양 많은가요?', '왜 팔아요?']
        return odered_comment, not_odered_comment

    def get_faq_db(self):
        sql = 'SELECT product_name FROM product_info;'
        menu_db = self.exe_db_smartstore(sql)

        sql = 'CALL get_ordered_customer_db;'
        ordered_customer = self.exe_db_smartstore(sql)

        sql = 'CALL get_non_ordered_customer_db;'
        not_ordered_customer = self.exe_db_smartstore(sql)

        return menu_db, ordered_customer, not_ordered_customer

    def make_auto_faq(self):
        while True:
            if self.LOGIN_signal:
                time.sleep(15)
                menu = []
                faq_db = self.get_faq_db()
                comment = self.comment()

                for menu_name in faq_db[0]:
                    menu.append(menu_name[0])

                if random.randint(0, 1) == 1 and len(faq_db[1]) > 5:
                    faq_content = f'{menu[random.randint(0, len(menu) - 1)]} ' \
                                  f'{comment[0][random.randint(0, len(comment[0]) - 1)]}'

                    sql = f'''CALL comment_of_ordered_customer({self.UserInfo[0]}, "{self.UserInfo[3]}", 
                    {faq_db[1][0][0]}, "{faq_db[1][0][1]}", {faq_db[1][0][2]}, 
                    "{faq_db[1][0][3]}", {faq_db[1][0][4]}, "{faq_content}")'''
                    self.exe_db_smartstore(sql)

                time.sleep(285)

    def faq_detail(self, store_faq_data):
        self.customer_service = CustomerService(store_faq_data[self.faq_table.currentRow()])
        self.customer_service.show()

    def faq_to_bom(self):
        self.MAIN_STACK.setCurrentIndex(1)

    @staticmethod
    def exe_db_smartstore(sql):
        conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                               db='project7smartstore')
        c = conn.cursor()

        c.execute(sql)
        conn.commit()
        loaded = c.fetchall()

        c.close()
        conn.close()

        return loaded

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainPage()

    sys.exit(app.exec_())
