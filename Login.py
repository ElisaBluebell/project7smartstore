import pymysql
from PyQt5 import uic
from PyQt5.QtWidgets import *



LoginUIset = uic.loadUiType("ui/login.ui")[0]
class LoginPage(QWidget, LoginUIset):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.show()
        self.LOGIN_stack.setCurrentIndex(0)

        self.LOGIN_BT_regist.clicked.connect(self.Page_regist)


    def GO_main(self, check):
        if check:
            if self.signal_id:
                if self.signal_pass :
                    if len(self.REGIST_name.text()) != 0:
                        if len(self.REGIST_number.text()) != 0:
                            # db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
                            # cursor = db.cursor()
                            # cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                            #                "WHERE TABLE_NAME  = 'regist_list' ")
                            # temp = cursor.fetchall()
                            # listcount = cursor.execute("select count(*) from biconn.regist_list")
                            print("1")
                            print(self.REGIST_id.text())
                            print(self.REGIST_pass.text())
                            print(self.REGIST_name.text())
                            print("2")
                            colunms = ()
                            # for i in temp:
                            #     colunms = colunms + i
                            # cursor.execute(f"insert into biconn.regist_list (ID,PASS,NAME,PHONE,SEPT) "
                            #                f"values('{self.REGIST_id.text()}','{self.REGIST_pass.text()}','{self.REGIST_name.text()}','{self.REGIST_number.text()}','{self.REGIST_radio2.isChecked()}')")
                            # db.commit()
                            # db.close()
                            self.datareset('registsignal')
                            QMessageBox.information(self, "알림", "회원가입 완료")
                            self.LOGIN_stack.setCurrentIndex(0)
                        else:
                            QMessageBox.information(self, "알림", "번호를 입력해주세요")
                    else:
                        QMessageBox.information(self, "알림", "이름을 입력해주세요")
                else:
                    QMessageBox.information(self, "알림", "비밀번호를 확인해주세요")
            else:
                QMessageBox.information(self, "알림", "중복확인하세요")
        else:
            self.LOGIN_stack.setCurrentIndex(0)
            self.datareset('registsignal')
    #초기화 함수
    def datareset(self, signal):
        if signal == 'mainsignal':
            self.signal_id = False  # id pass check유무
            self.signal_pass = False
            self.LOGIN_stack.setCurrentIndex(1)
            self.LOGINMAIN_id.clear()
            self.LOGINMAIN_pass.clear()
        elif signal == 'registsignal':
            self.REGIST_id.clear()
            self.REGIST_pass.clear()
            self.REGIST_pass2.clear()
            self.REGIST_name.clear()
            self.REGIST_number.clear()
            self.REGIST_idcheck.clear()
            self.REGIST_LB_passcheck.clear()
            self.REGIST_radio2.setChecked(True)
            self.REGIST_adminnumber.clear()
            self.regist_adminchecker()
            self.signal_id = False
            self.signal_pass = False
        elif signal == 'passsignal':
            self.signal_pass = False
        elif signal == 'idsignal':
            self.signal_id = False

    def Page_regist(self):
        self.datareset('mainsignal')
        self.REGIST_radio.toggled.connect(self.regist_adminchecker)
        self.REGIST_BT_cancel.clicked.connect(lambda: self.GO_main(False))
        self.REGIST_BT_ok.clicked.connect(lambda: self.GO_main(True))
        self.REGIST_id.textChanged.connect(lambda: self.datareset('idsignal'))
        self.REGIST_pass.textChanged.connect(lambda: self.datareset('passsignal'))
        self.REGIST_pass2.textChanged.connect(self.regist_pass_check)
        self.REGIST_BT_idcheck.clicked.connect(self.regist_id_check)

    def regist_id_check(self):
        if len(self.REGIST_id.text()) == 0:
            QMessageBox.information(self, "알림", "아이디를 입력해주세요")
            return

        self.REGIST_idcheck.setStyleSheet("Color : red")  # 글자색 변환
        # db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r', charset='utf8')
        # cursor = db.cursor()
        # cursor.execute('select * from biconn.regist_list where ID = %s', self.REGIST_id.text())
        if 1==2:
            self.REGIST_idcheck.setText('이미 존재하는 아이디입니다.')
            self.signal_id = False
        else:
            self.REGIST_idcheck.setText('사용 가능한 아이디입니다.')
            self.signal_id = True

    def regist_pass_check(self):
        self.REGIST_LB_passcheck.setStyleSheet("Color : red")  # 글자색 변환
        if self.REGIST_pass.text() == self.REGIST_pass2.text():
            self.REGIST_LB_passcheck.setText('비밀번호 확인.')
            self.signal_pass = True
        else:
            self.REGIST_LB_passcheck.setText('비밀번호가 일치하지 않습니다.')
            self.signal_pass = False
    def regist_adminchecker(self):
        if self.REGIST_radio.isChecked() == True:
            self.REGIST_adminnumber.setEnabled(True)
        else:
            self.REGIST_adminnumber.setEnabled(False)

    def exestart(self):
        self.show()