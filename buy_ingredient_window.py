import pymysql

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox


class BuyIngredient(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = ''
        self.c = ''

        self.title = QLabel(self)
        self.have = QLabel(self)
        self.have_quantity = QLabel(self)
        self.buy_quantity = QLabel(self)
        self.measurement = QLabel(self)

        self.esc = QPushButton(self)

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

        self.buy_quantity.setText('구매량')
        self.buy_quantity.setGeometry(160, 90, 40, 16)

        self.measurement.setGeometry(290, 90, 20, 16)

    def set_btn(self):
        self.esc.setText('닫기')
        self.esc.setGeometry(230, 10, 75, 23)
        self.esc.clicked.connect(self.esc_window)

    def set_combo(self):
        self.select_ingredient.setGeometry(20, 50, 90, 20)
        self.set_select_ingredient()

        self.select_quantity.setGeometry(210, 90, 71, 22)

    def set_ui(self):
        self.set_label()
        self.set_btn()
        self.set_combo()

        self.setFont(QtGui.QFont('D2Coding'))
        self.setGeometry(420, 200, 315, 160)

    def set_db(self):
        pass

    def esc_window(self):
        self.set_select_ingredient()
        self.close()

    def set_select_ingredient(self):
        conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                               db='project7smartstore')
        c = conn.cursor()

        c.execute('SELECT DISTINCT material_name from material_management')
        ingredient_list = c.fetchall()

        for ingredient in ingredient_list:
            self.select_ingredient.addItem(ingredient[0])

        c.close()
        conn.close()

    def set_select_quantity(self):
        pass
