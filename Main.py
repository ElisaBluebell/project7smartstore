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


        self.order_checked.clicked.connect(self.order_accept)
        self.BT_alert.clicked.connect(self.Move_selllist)
        self.BT_alert2.clicked.connect(self.Move_selllist)
        self.BT_alert3.clicked.connect(self.Move_selllist)

        auto_faq = threading.Thread(target=self.make_auto_faq, daemon=True)
        auto_faq.start()
        self.tete.clicked.connect(self.auto_ordering)
    # 자동주문 스레드 생성 메서드
    # auto_order 스레드를 생성하고 시작하는 메서드
    # 버튼클릭 시그널에 연결시킴. (로그인시 바로 동작해도 됨.)
    def auto_ordering(self):
        auto_order = Thread(target=self.thread_ordering, args=())
        auto_order.daemon = True
        auto_order.start()
    # 자동주문 스레드 메서드
    # 랜덤을 통해 판매중인 제품중에 재고에 맞춰 랜덤하게 주문하도록 구성.
    def thread_ordering(self):
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
            sellnum = random.randrange(num) // 5
            if sellnum != 0:
                cursor.execute("INSERT INTO project7smartstore.order_management "
                               f"(order_date,product_idx,product_name,product_quantity,customer_idx,seller_idx,store_name) "
                               f"values('{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}','{a[0][7]}','{a[0][8]}',"
                               f"'{sellnum}','3','{a[0][0]}','{a[0][9]}')")
                db.commit()
                db.close()
            time.sleep(5)
    # 주문확인 메서드
    # 판매자가 주문이 들어온 후 주문확인을 통해 구매자가 상태를 확인할 수 있게 함. (주문확인중 -> 주문확인완료)
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

    # 판매자의 판매리스트 메서드 어떤 상품이 팔렸는지 확인 하는 기능
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

    # 구매자의 구매리스트 메서드
    def Move_buylist(self):
        self.MAIN_STACK.setCurrentIndex(7)
        db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
        cursor = db.cursor()
        a = cursor.execute("SELECT * "
                           "FROM project7smartstore.order_management INNER JOIN project7smartstore.product_info "
                           "ON project7smartstore.order_management.product_idx = project7smartstore.product_info.product_idx "
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
    # 상품판매 알림 스레드 생성 메서드
    def test_th(self):
        self.th_siganl = True
        thread_order = Thread(target=self.thread_act, args=())
        thread_order.daemon = True
        thread_order.start()
    # 상품판매 스레드 메서드
    # 판매자가 확인하지 않은 주문건 수를 실시간으로 알려주는 기능.
    def thread_act(self):
        bt = [self.BT_alert, self.BT_alert2, self.BT_alert3]
        if self.LOGIN_signal == True:
            while self.th_siganl == True:
                if self.LOGIN_signal == False:
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

    # 상품 구매 메서드
    # 상품구매에 성공(조건 충족)하면 order 테이블에 데이터 insert 하는 기능.
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
                msg = QMessageBox.information(self, "알림", "구매 수량을 확인해주세요")
                return
            cursor.execute("INSERT INTO project7smartstore.order_management "
                           f"(order_date,product_idx,product_name,product_quantity,customer_idx,seller_idx,store_name) "
                           f"values('{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}','{a[0][7]}','{a[0][8]}',"
                           f"'{self.le_sellnum.text()}','{self.UserInfo[0]}','{a[0][0]}','{a[0][9]}')")
            db.commit()
            db.close()
            msg = QMessageBox.information(self, "알림", "주문완료")
            self.le_sellnum.clear()
            self.Move_SellList()
        except pymysql.err.DataError:
            msg = QMessageBox.information(self, "알림", "정보를 입력해주세요")
            return
        except ValueError:
            msg = QMessageBox.information(self, "알림", "수량을 입력해주세요")
            return


    def move_main(self):
        self.MAIN_STACK.setCurrentIndex(0)

    # 상품 선택 메서드
    # 제품 선택시 해당 제품에 대한 설명과 구매 정보 입력창이 출력 되는 기능.
    def check_selllist(self, signal):
        if signal == 0:
            if self.MAIN_sellList.item(self.MAIN_sellList.currentRow(), 3).text() == "구매불가":
                msg = QMessageBox.information(self, "알림", "구매할 수 없는 상품입니다.")
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
            except ValueError:
                self.lb_totalPrice.setText(" ")
                self.lb_totalPrice2.hide()

    # 메인에서 판매리스트로 이동
    # 판매 등록된 상품을 테이블위젯에 추가시키는 메서드
    # 재고와 연동해서 현재 보유중인 재고로 각 상품에 대해서 몇개를 구매 할 수 있는지 표현함. (여러종류를 한번에 구매는 못함)
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
            if sellnum == 0 or sellnum == None:
                sellnum = '구매불가'
            self.MAIN_sellList.setItem(i, 3, QTableWidgetItem(str(sellnum)))
        self.frame.hide()

    # 버튼 세팅 메서드
    # 프레임을 만들어서 판매자용 구매자용 버튼을 따로 지정해서 판매자로 로그인시 판매자용 버튼만 보이게,
    # 구매자로 로그인시 구매자용 버튼만 보이게 하는 기능.
    def BT_setting(self):
        if self.LOGIN_signal == False:
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

    # 로그인 페이지 이동 메서드
    # 버튼 클릭으로 연결해서 비로그인시엔 로그인창이 로그인시엔 로그아웃이 되도록 설정됨.
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

    # 페이지 이동시 이전 페이지의 데이터를 초기화 하는 메서드
    # 처음에는 다 설정 해 놓았다가 조금씩 코드 수정하면서 한 가지 경우로만 사용됨.
    def Move_reset(self, signal):
        if signal == 0:
            self.MAIN_STACK.setCurrentIndex(0)
            self.MAIN_LE_productName.clear()
            self.MAIN_LE_productPrice.clear()
            self.MAIN_strorelist.clearContents()
            self.MAIN_strorelist.setRowCount(0)


    # 판매상품 등록 페이지 이동 메서드
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

    # 판매상품 등록 페이지에서 +- 클릭이 동작하는 메서드
    # 테이블위젯의 행을 1개씩 추가하거나 제거하는 기능.
    def rowplus(self, signal):
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
            self.MAIN_strorelist.removeRow(self.MAIN_strorelist.rowCount() - 1)

    # 상품등록 메서드
    # 상품등록 확인 했을때 입력된 데이터들을 체크한 후 db에 insert 하는 기능.
    def datacheck(self):
        for i in range(self.MAIN_strorelist.rowCount()):
            for j in range(self.MAIN_strorelist.columnCount() - 1):
                try:
                    if self.MAIN_strorelist.item(i, j).text() == None or \
                            self.MAIN_strorelist.item(i, j).text() == "" or \
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
                    print(temp)
                except TypeError:
                    temp = 1

                check = cursor.execute("SELECT material_idx FROM project7smartstore.bill_of_material "
                                       f"WHERE material_name = '{self.MAIN_strorelist.item(i, 0).text()}'")
                print("check", check)
                info = cursor.fetchall()

                cursor.execute("SELECT * FROM project7smartstore.product_info "
                               f"WHERE product_name='{self.MAIN_LE_productName.text()}' and store_name='{self.UserInfo[5]}'")
                temp2 = cursor.fetchall()
                if check == 0:  # BoM_insert 프리시저 사용
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
            msg = QMessageBox.information(self, "알림", "정보를 입력해주세요")
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

        c.execute('SELECT * FROM `project7smartstore`.`bill_of_material`')
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
        self.bom_select_menu.clear()
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
        if len(self.bom_select_menu.currentText()) > 0:
            self.bom_select_menu.currentTextChanged.connect(self.menu_changed)

    def get_bom_table_db(self):
        sql = 'CALL group_product_by_material();'
        # 0 = 재료명(명칭과 계량 단위가 겹치지 않음), 1 = 보유 수량, 2 = 사용처 그룹
        self.table_data = self.exe_db_smartstore(sql)
        # self.loop_put_all_data_in()


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
            if len(self.bom_select_menu.currentText()) > 0:
                # bom_table_row, bom_table_column은 set_bom_table_data_tooltip 함수에서 각각 row, column으로 사용함
                # 반복문에서의 i, j값과 별개로 데이터 축적시마다 1개씩 증가해 올바른 표의 행과 열에 들어감
                bom_table_row = 0
                self.bom_ingredient_table.setRowCount(bom_table_row)

                for i in range(len(self.table_data)):
                    # self.table_data =
                    # [material_name, material_quantity+measure_unit, product_name GROUP BY material_name]
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
            if len(self.bom_select_menu.currentText()) > 0:
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
        self.ingredient_window.reset_items()
        self.ingredient_window.show()

    def bom_to_main(self):
        self.MAIN_STACK.setCurrentIndex(0)

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
        self.put_faq_data_in_table(store_faq_data)
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

    def put_faq_data_in_table(self, store_faq_data):
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

    def make_auto_faq(self):
        while True:
            if self.LOGIN_signal == True:
                time.sleep(15)
                menu = []
                conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', db='project7smartstore')
                c = conn.cursor()

                c.execute('SELECT product_name FROM product_info')
                menu_db = c.fetchall()

                c.execute('''SELECT DISTINCT c.user_idx, c.user_name, a.product_idx, a.product_name, a.order_idx
                FROM order_management AS a
                INNER JOIN faq_management AS b
                INNER JOIN user_info AS c
                ON a.customer_idx = c.user_idx
                WHERE a.order_idx NOT IN (
                SELECT order_idx
                FROM faq_management
                );''')
                ordered_customer = c.fetchall()

                c.execute('''SELECT * FROM user_info AS a 
                JOIN product_info AS b 
                WHERE a.user_type NOT IN(
                SELECT user_type FROM user_info 
                WHERE store_name=FALSE
                )''')
                not_ordered_customer = c.fetchall()
                for menu_name in menu_db:
                    menu.append(menu_name[0])

                odered_comment = ['맛있어요.', '맛없어요.', '너무 매워요.', '너무 달아요.', '너무 써요', '너무 많아요.', '너무 적어요.', '왜 팔아요?', '배달이 늦었어요.']
                not_odered_comment = ['맛있나요?', '맵나요?', '양 많은가요?', '왜 팔아요?']
                if random.randint(0, 1) == 1:
                    if len(ordered_customer) > 5:
                        if random.randint(0, 1) == 1:
                            faq_content = f'{menu[random.randint(0, len(menu) - 1)]} ' \
                                         f'{odered_comment[random.randint(0, len(odered_comment) - 1)]}'
                            c.execute(f'''INSERT INTO faq_management
                            (seller_idx, seller_name, buyer_idx, buyer_name, product_idx, product_name, order_idx, 
                            faq_content) VALUES({self.UserInfo[0]}, '{self.UserInfo[3]}', {ordered_customer[0][0]}, 
                            '{ordered_customer[0][1]}', {ordered_customer[0][2]}, '{ordered_customer[0][3]}', 
                            {ordered_customer[0][4]}, '{faq_content}')''')
                            conn.commit()

                    else:
                        faq_content = f'{menu[random.randint(0, len(menu) - 1)]} ' \
                                      f'{not_odered_comment[random.randint(0, len(not_odered_comment) - 1)]}'
                        c.execute(f'''INSERT INTO faq_management
                        (seller_idx, seller_name, buyer_idx, buyer_name, product_idx, product_name, faq_content) 
                        VALUES({self.UserInfo[0]}, '{self.UserInfo[3]}', {not_ordered_customer[0][0]}, 
                        '{not_ordered_customer[0][1]}', {not_ordered_customer[0][2]}, '{not_ordered_customer[0][3]}', 
                        '{faq_content}')''')
                        conn.commit()

                c.close()
                conn.close()

                time.sleep(285)

    def faq_detail(self, store_faq_data):
        self.customer_service = CustomerService(store_faq_data[self.faq_table.currentRow()])
        self.customer_service.show()

    def faq_to_bom(self):
        self.MAIN_STACK.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainPage()

    sys.exit(app.exec_())
