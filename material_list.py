import sys

import pymysql
from PyQt5 import uic
from PyQt5.QtWidgets import *

from Login import LoginPage
from buy_ingredient_window import BuyIngredient



materialUI = uic.loadUiType("ui/material_list.ui")[0]

class material(QWidget, materialUI):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.show()

        self.material_close.clicked.connect(lambda: self.close())
        self.material_check.clicked.connect(self.data_insert)


    def data_insert(self):
        self.material_name.text()
        self.material_price.text()
        self.material_unit.text()

        db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
        cursor = db.cursor()
        cursor.execute("SELECT MAX(IDX) FROM project7smartstore.material_management")
        temp = cursor.fetchone()[0]
        print(temp, "dasd")
        a = cursor.execute("INSERT INTO project7smartstore.material_management "
                           "(material_idx, material_name, inventory_quantity, buy_unit, material_price) "
                           f"values('{}','{}','{}','{}','{}','{}')")