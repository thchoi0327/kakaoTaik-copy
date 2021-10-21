import sys


from PyQt5 import QtWidgets, QtCore
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from kakaoLogin2 import Ui_LoginPage  # 수정부분
import requests
import json
import sys


class LoginPage(QMainWindow, Ui_LoginPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def login(self):
        userId = self.lineEdit_id.text()
        userPw = self.lineEdit_pw.text()
        if (userId == ''):
            QtWidgets.QMessageBox.about(self, 'kakao', '아이디를 입력해주세요.')
            return
        if (userPw == ''):
            QtWidgets.QMessageBox.about(self, 'kakao', '비밀번호를 입력해주세요.')
            return
        url = "http://192.168.2.85:8080/huefax/Chatting.do?cmd=ChattingLogin"
        loginData = {'userId': userId, 'userPw': userPw}
        try:
            req = requests.post(url, data=loginData)
        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.about(self, 'warning', '서버 점검 중입니다.')
            print('서버연결실패')
            return
        JSONdata = json.loads(str(req.text))
        data = JSONdata['result']
        if (data == 'SUCCESS'):
            self.lineEdit_id.setText('')
            self.lineEdit_pw.setText('')
            widget.setCurrentIndex(widget.currentIndex()+1)
            print('[메시지] 로그인 성공')
        else:
            self.label_FailPw.setVisible(True)
            self.textBrowser.setVisible(True)
            print('[메시지] 로그인 실패')


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("kakao_copy.ui", self)

    def openCaptureClass(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def login(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def buttonColor(self):
        print('btnColor2')

    def buttonColorPw(self):
        print('asdasd2')


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # 화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()

    # Widget 추가
    widget.addWidget(LoginPage())
    widget.addWidget(MainPage())
    # widget.addWidget(ScreenCaptureClass())

    # 프로그램 화면을 보여주는 코드
    widget.setFixedWidth(360)
    widget.setFixedHeight(589)

    widget.setStyleSheet("background-color:rgb(255,235,51);")
    widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    widget.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
