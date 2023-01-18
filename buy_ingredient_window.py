import pymysql

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QMessageBox


class BuyIngredient(QWidget):
    def __init__(self):
        super().__init__()
        # self.i = 0
        self.ingredient_list = ''

        self.title = QLabel(self)
        self.have = QLabel(self)
        self.have_quantity = QLabel(self)
        self.buy_quantity = QLabel(self)
        self.measurement = QLabel(self)
        self.price_per_unit = QLabel(self)
        self.total_price = QLabel(self)

        self.esc = QPushButton(self)
        self.purchase = QPushButton(self)

        self.select_ingredient = QComboBox(self)
        self.select_quantity = QComboBox(self)

        self.set_ui()

    def set_label(self):
        self.title.setText('재료구매')
        self.title.setGeometry(0, 10, 220, 30)
        self.title.setFont(QtGui.QFont('D2Coding', 14))
        self.title.setAlignment(Qt.AlignCenter)

        self.have.setText('보유량')
        self.have.setGeometry(20, 90, 40, 16)

        self.have_quantity.setGeometry(70, 90, 70, 16)
        self.price_per_unit.setGeometry(20, 130, 90, 16)
        self.total_price.setGeometry(160, 130, 90, 16)

        self.buy_quantity.setText('구매량')
        self.buy_quantity.setGeometry(160, 90, 40, 16)

        self.measurement.setGeometry(290, 90, 20, 16)

    def set_btn(self):
        self.esc.setText('닫기')
        self.esc.setGeometry(230, 10, 75, 23)
        self.esc.clicked.connect(self.esc_window)

        self.purchase.setText('구매')
        self.purchase.setGeometry(230, 50, 75, 23)
        self.purchase.clicked.connect(self.purchase_ingredient)

    def set_combo(self):
        self.select_ingredient.setGeometry(20, 50, 90, 20)
        self.set_select_ingredient()

        self.select_quantity.setGeometry(210, 90, 71, 22)

    def set_ui(self):
        self.set_db()

        self.set_label()
        self.set_btn()
        self.set_combo()

        self.setFont(QtGui.QFont('D2Coding'))
        self.setGeometry(420, 200, 315, 160)

    def set_db(self):
        conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                               db='project7smartstore')
        c = conn.cursor()

        c.execute('''SELECT DISTINCT a.material_name, 
        a.buy_unit, 
        a.material_price, 
        a.inventory_quantity, 
        b.measure_unit 
        FROM material_management AS a 
        INNER JOIN bill_of_material AS b 
        ON a.material_name=b.material_name''')

        # 0 = 재료명, 1 = 재료구매단위, 2 = 재료가격, 3 = 재료재고, 4 = 계량단위
        self.ingredient_list = c.fetchall()

        c.close()
        conn.close()

    def esc_window(self):
        self.close()

    def set_select_ingredient(self):
        self.select_ingredient.clear()
        for ingredient in self.ingredient_list:
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
        while (self.ingredient_list[i][1] * j) + self.ingredient_list[i][3] <= self.ingredient_list[i][1] * 9:
            j += 1
            # 앞자리 수*구매단위(1*1000=1000, 8*10=80) 등으로 구매 단위에 맞춰 구매수량 추가
            self.select_quantity.addItem(str(j * self.ingredient_list[i][1])+self.ingredient_list[i][4])

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
            # 선택한 수량의 맨 앞자리 수(set_select_quantity 함수의 j값) * 단가
            self.total_price.setText(f'''합계: {int(self.select_quantity.currentText()[:1]) * 
                                          (int(self.price_per_unit.text()[4:-1]))}원''')

    def purchase_ingredient(self):
        if len(self.select_quantity.currentText()) != 0:
            conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                                   db='project7smartstore')
            c = conn.cursor()

            c.execute(f'''UPDATE material_management 
            SET inventory_quantity=inventory_quantity+(buy_unit*{int(self.select_quantity.currentText()[:1])}) 
            WHERE material_name="{self.select_ingredient.currentText()}"''')
            conn.commit()

            c.close()
            conn.close()

            # 변경된 DB를 다시 읽어 라벨과 체크박스 재설정
            self.set_db()
            self.set_select_quantity()

        else:
            QMessageBox.warning(self, '구매 불가', '더이상 구매할 수 없습니다.')
