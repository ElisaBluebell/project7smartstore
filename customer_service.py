import pymysql
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QTextBrowser, QWidget, QLineEdit, QMessageBox


class CustomerService(QWidget):
    def __init__(self, faq_db):
        super().__init__()
        self.faq_db = faq_db

        self.title = QLabel(self)
        self.customer_name = QLabel(self)
        self.answer = QLabel(self)

        self.close_btn = QPushButton(self)
        self.register = QPushButton(self)

        self.customer_cs_content = QTextBrowser(self)
        self.store_cs_content = QLineEdit(self)

        self.set_ui()

    def set_ui(self):
        self.set_window()
        self.set_text()

        self.set_geometry()
        self.set_connect()

        self.set_etc()

    def set_window(self):
        self.setWindowTitle('고객 문의')
        self.setGeometry(400, 200, 300, 390)
        self.setFont(QtGui.QFont('D2Coding'))

    def set_text(self):
        self.title.setText('고객 문의 상세')
        self.customer_name.setText(f'{self.faq_db[4]} 님의 문의입니다.')
        self.customer_cs_content.setText(f'{self.faq_db[8]}')
        self.answer.setText('답변하기')
        self.close_btn.setText('닫기')
        self.register.setText('등록')
        if self.faq_db[9] == 2:
            self.store_cs_content.setPlaceholderText(f'{self.faq_db[10]}')

    def set_geometry(self):
        self.title.setGeometry(0, 20, 300, 40)
        self.customer_name.setGeometry(20, 80, 260, 20)
        self.answer.setGeometry(20, 270, 100, 20)
        self.close_btn.setGeometry(220, 350, 60, 20)
        self.register.setGeometry(140, 350, 60, 20)
        self.customer_cs_content.setGeometry(20, 120, 260, 130)
        self.store_cs_content.setGeometry(20, 310, 260, 20)

    def set_connect(self):
        self.close_btn.clicked.connect(self.close_window)
        self.register.clicked.connect(self.register_cs_answer)
        self.store_cs_content.returnPressed.connect(self.register_cs_answer)

    def set_etc(self):
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QtGui.QFont('D2Coding', 14))
        self.change_faq_status_read()
        self.store_cs_content.setMaxLength(40)

    def register_cs_answer(self):
        sql = f'''CALL reply_faq("{self.store_cs_content.text()}", {self.faq_db[0]})'''
        self.exe_db_smartstore(sql)
        QMessageBox.information(self, '답변 등록 완료', '답변이 등록되었습니다.')

    def change_faq_status_read(self):
        sql = f'''UPDATE faq_management SET 
        faq_process=1 
        WHERE faq_idx={self.faq_db[0]}'''

        self.exe_db_smartstore(sql)

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

    def close_window(self):
        self.close()
