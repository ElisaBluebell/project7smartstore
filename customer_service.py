from PyQt5.QtWidgets import QLabel, QPushButton, QTextBrowser, QWidget


class CustomerService(QWidget):
    def __init__(self, faq_db):
        super().__init__()
        self.faq_db = faq_db

        self.title = QLabel(self)
        self.close = QPushButton(self)
        self.customer_cs_content = QTextBrowser(self)
        self.store_cs_content = QTextBrowser(self)

        self.set_ui()

    def set_ui(self):
        self.set_window()
        self.set_text()

        self.set_geometry()
        self.set_connect()

        self.set_etc()

    def set_window(self):
        pass

    def set_text(self):
        self.setWindowTitle('고객 문의')
        self.title.setText('고객 문의 상세')
        self.close.setText('닫기')

    def set_geometry(self):
        self.setGeometry(400, 200, 300, 500)
        self.close.setGeometry(220, 460, 60, 20)

    def set_connect(self):
        self.close.clicked.connect(self.close_window)

    def set_etc(self):
        pass

    def close_window(self):
        print(self.faq_db)
