import pymysql

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QMessageBox, QTabWidget, QLineEdit


class Ingredient(QTabWidget):
    def __init__(self):
        super().__init__()
        self.buy_ingredient = BuyIngredient()
        self.manage_ingredient = ManageIngredient()

        self.addTab(self.buy_ingredient, '재료 구매')
        self.addTab(self.manage_ingredient, '재료 관리')
        self.set_ui()

    def set_ui(self):
        self.setFont(QtGui.QFont('D2Coding'))
        self.setGeometry(420, 200, 315, 200)

    def reset_items(self):
        self.buy_ingredient.set_db()
        self.manage_ingredient.reset_select_name_item()


class BuyIngredient(QWidget):
    def __init__(self):
        super().__init__()
        self.ingredient_list = ''

        self.title = QLabel(self)
        self.have = QLabel(self)
        self.have_quantity = QLabel(self)
        self.buy_quantity = QLabel(self)
        self.measurement = QLabel(self)
        self.price_per_unit = QLabel(self)
        self.total_price = QLabel(self)

        self.purchase = QPushButton(self)

        self.select_ingredient = QComboBox(self)
        self.select_quantity = QComboBox(self)

        self.set_ui()

    def set_label(self):
        self.title.setText('재료 구매')
        self.title.setGeometry(0, 10, 315, 30)
        self.title.setFont(QtGui.QFont('D2Coding', 14))
        self.title.setAlignment(Qt.AlignCenter)

        self.have.setText('보유량')
        self.have.setGeometry(20, 90, 40, 16)

        self.have_quantity.setGeometry(70, 90, 70, 16)
        self.price_per_unit.setGeometry(20, 130, 90, 16)
        self.total_price.setGeometry(160, 90, 90, 16)

        self.buy_quantity.setText('구매량')
        self.buy_quantity.setGeometry(160, 50, 40, 16)

        self.measurement.setGeometry(290, 90, 20, 16)

    def set_btn(self):
        self.purchase.setText('구매')
        self.purchase.setGeometry(160, 130, 75, 23)
        self.purchase.clicked.connect(self.purchase_ingredient)

    def set_combo(self):
        self.select_ingredient.setGeometry(20, 50, 90, 20)
        self.set_select_ingredient()

        self.select_quantity.setGeometry(210, 50, 71, 22)

    def set_ui(self):
        self.set_db()

        self.set_label()
        self.set_btn()
        self.set_combo()

    def set_db(self):
        conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                               db='project7smartstore')
        c = conn.cursor()

        # 0재료명 1구매단위 2단위가격 3재고수량 4계량단위
        c.execute('''CALL get_ingredient_db()''')
        self.ingredient_list = c.fetchall()

        c.close()
        conn.close()

    def set_select_ingredient(self):
        self.select_ingredient.clear()
        # 받아온 DB의 길이만큼 재료명 추가
        for ingredient in self.ingredient_list:
            if ingredient[1] != 0:
                self.select_ingredient.addItem(ingredient[0])

        self.set_select_quantity()
        self.select_ingredient.currentTextChanged.connect(self.set_select_quantity)

    def set_select_quantity(self):
        self.select_quantity.clear()
        i = 0
        j = 0
        # 콤보박스에 해당하는 재료명 탐색, 찾으면 탐색 멈춤, i값을 인덱스로 설정
        for i in range(len(self.ingredient_list)):
            if self.ingredient_list[i][0] == self.select_ingredient.currentText():
                break

        # 구매 단위의 9배수까지 반복해서 앞자리 수를 추가함
        while (self.ingredient_list[i][1] * j) + self.ingredient_list[i][3] <= self.ingredient_list[i][1] * 8:
            j += 1
            # 앞자리 수*구매단위(1*1000=1000, 8*10=80) 등으로 구매 단위에 맞춰 구매수량 추가
            self.select_quantity.addItem(str(j * self.ingredient_list[i][1]) + self.ingredient_list[i][4])

        # 해당 재료에 맞춰 라벨값 반응
        self.set_responsive_label_text(i)

    def set_responsive_label_text(self, i):
        # 현재 보유량 = 보유수량 + 계량단위
        self.have_quantity.setText(f'{self.ingredient_list[i][3]}{self.ingredient_list[i][4]}')
        self.price_per_unit.setText(f'단가: {str(self.ingredient_list[i][2])}원')

        self.select_quantity.currentTextChanged.connect(self.calculate_total_price)
        self.calculate_total_price()

    def calculate_total_price(self):
        # 수량이 빈 값이 아닌 경우(초기화로 인해 비는 경우를 제외)
        if len(self.select_quantity.currentText()) != 0:
            # 선택한 수량의 맨 앞자리 수(set_select_quantity 함수의 j값) * 단가q
            self.total_price.setText(f'''합계: {int(self.select_quantity.currentText()[:1]) *
                                              (int(self.price_per_unit.text()[4:-1]))}원''')
        else:
            self.total_price.setText('')

    def purchase_ingredient(self):
        if len(self.select_quantity.currentText()) != 0:
            conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                                   db='project7smartstore')
            c = conn.cursor()

            # 재고 수량 = 재고 수량 + (구매 단위 * 선택 수량 맨 앞자리수)
            c.execute(f'''CALL purchase_ingredient({int(self.select_quantity.currentText()[:1])}, 
            "{self.select_ingredient.currentText()}")''')
            conn.commit()

            c.close()
            conn.close()

            # 변경된 DB를 다시 읽어 라벨과 체크박스 재설정
            self.set_db()
            self.set_select_quantity()

        else:
            QMessageBox.warning(self, '구매 불가', '더이상 구매할 수 없습니다.')


class ManageIngredient(QWidget):
    def __init__(self):
        super().__init__()

        self.title = QLabel(self)
        self.name = QLabel(self)
        self.price = QLabel(self)
        self.bundle = QLabel(self)
        self.measurement = QLabel(self)

        self.input_price = QLineEdit(self)

        self.modify = QPushButton(self)

        self.select_name = QComboBox(self)
        self.select_bundle = QComboBox(self)
        self.select_measurement = QComboBox(self)

        self.set_page()

    def set_page(self):
        self.set_ui()

    def set_ui(self):
        self.set_text()
        self.set_geometry()
        self.set_connect()
        self.set_combo_item()
        self.set_etc()

        self.set_select_name_item()

    def set_text(self):
        self.title.setText('재료 관리')
        self.name.setText('이름')
        self.price.setText('가격')
        self.bundle.setText('수량')
        self.measurement.setText('단위')

        self.modify.setText('수정')

    def set_geometry(self):
        self.title.setGeometry(0, 10, 315, 30)
        self.name.setGeometry(20, 50, 40, 20)
        self.price.setGeometry(20, 90, 40, 20)
        self.bundle.setGeometry(160, 50, 40, 20)
        self.measurement.setGeometry(160, 90, 40, 20)

        self.input_price.setGeometry(60, 90, 80, 20)
        self.modify.setGeometry(220, 130, 75, 23)

        self.select_name.setGeometry(60, 50, 80, 20)
        self.select_bundle.setGeometry(200, 50, 95, 20)
        self.select_measurement.setGeometry(200, 90, 95, 20)

    def set_connect(self):
        self.modify.clicked.connect(self.modify_ingredient)

    def set_etc(self):
        self.title.setFont(QtGui.QFont('D2Coding', 14))
        self.title.setAlignment(Qt.AlignCenter)

    def set_combo_item(self):
        self.set_select_name_item()
        self.set_select_bundle_item()
        self.set_select_measurement_item()

    def set_select_name_item(self):
        self.select_name.clear()

        sql = f'''SELECT material_name, 
        buy_unit 
        FROM material_management'''
        name_and_unit = self.exe_db_smartstore(sql)

        self.put_item_in_select_name(name_and_unit)

    def set_select_bundle_item(self):
        for i in range(1, 5):
            self.select_bundle.addItem(str(1) + i * str(0), int(str(1) + i * str(0)))

    def set_select_measurement_item(self):
        measurement = ['개', 'g', 'ml']
        for i in range(len(measurement)):
            self.select_measurement.addItem(measurement[i])

    def modify_ingredient(self):
        try:
            if type(int(self.input_price.text())) == int:
                name = self.check_if_new_name()

                sql = f'''CALL modify_ingredient_data({int(self.input_price.text())}, {self.select_bundle.currentData()}
                , "{self.select_measurement.currentText()}", "{name}")'''
                self.exe_db_smartstore(sql)

                QMessageBox.information(self, '수정', '수정되었습니다.')
                self.reset_select_name_item()

        except ValueError:
            QMessageBox.warning(self, '입력 오류', '가격은 숫자로 입력해주세요.')

    def check_if_new_name(self):
        if '*' in self.select_name.currentText():
            name = self.select_name.currentText()[:-1]
        else:
            name = self.select_name.currentText()
        return name

    def reset_select_name_item(self):
        self.select_name.clear()
        self.set_select_name_item()

    def put_item_in_select_name(self, name_and_unit):
        self.give_tooltip_to_new_item(name_and_unit)
        self.append_star_to_new_ingredient(name_and_unit)

    def give_tooltip_to_new_item(self, name_and_unit):
        new_item_tooltip = ''

        for item in name_and_unit:
            if item[1] == 0:
                # 툴팁으로 등록하기 위해 텍스트 더함
                new_item_tooltip += f'{item[0]} '

        self.select_name.setToolTip(f'{new_item_tooltip}등록 필요')

    def append_star_to_new_ingredient(self, name_and_unit):
        for item in name_and_unit:
            if item[1] == 0:
                # 등록 필요한 신규 아이템 구별을 위한 *표
                self.select_name.addItem(f'{item[0]}*')

            else:
                self.select_name.addItem(f'{item[0]}')

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
