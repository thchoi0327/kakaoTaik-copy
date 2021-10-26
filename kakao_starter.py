import sys


from PyQt5 import QtWidgets, QtCore
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from kakaoLogin import Ui_LoginPage  # 수정부분
from PyQt5 import uic
from _socket import AF_INET, socket, SOCK_STREAM
import requests
import json
import sys

USER_NAME = ""
ChattingPage = uic.loadUiType("ChattingPage.ui")[0]


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
            self.MainPage = MainPage(self)
            self.hide()
            self.MainPage.show()
            print('서버연결실패')
            return
        JSONdata = json.loads(str(req.text))
        data = JSONdata['result']
        if (data == 'SUCCESS'):
            self.lineEdit_id.setText('')
            self.lineEdit_pw.setText('')
            # widget.setCurrentIndex(widget.currentIndex()+1)

            print('[메시지] 로그인 성공')
        else:
            self.label_FailPw.setVisible(True)
            self.textBrowser.setVisible(True)
            print('[메시지] 로그인 실패')

    def main_close(self):
        sys.exit()

    def minimize(self):
        self.showMinimized()

    def maximize(self):
        self.showMaximized()


class MainPage(QMainWindow, ChattingPage):
    HOST = 'localhost'
    PORT = 3000
    s = socket(AF_INET, SOCK_STREAM)

    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.s.connect((self.HOST, self.PORT))
        self.setupUi(self)

        self.inputButton.clicked.connect(self.send_message)
        self.inputText.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.inputText:
            if event.key() == QtCore.Qt.Key_Return and self.inputText.hasFocus():
                self.send_message()
        return super().eventFilter(obj, event)

    def send_message(self):
        QtWidgets.qApp.processEvents()
        msg = self.inputText.toPlainText()
        if (msg == ''):
            return

        self.inputText.clear()
        self.inputText.setPlainText("\n")
        data = msg.encode()
        # 메시지 길이를 구한다.
        length = len(data)
        # server로 little 엔디언 형식으로 데이터 길이를 전송한다.
        self.s.sendall(length.to_bytes(4, byteorder="little"))
        # 데이터를 전송한다.
        self.s.sendall(data)
        self.showChat(msg)

    def showChat(self, msg):
        self.resultBrower.append("[나] %s" % msg)


app = QApplication(sys.argv)
kakao = LoginPage()
kakao.show()
app.exec_()

# QApplication : 프로그램을 실행시켜주는 클래스
# app = QApplication(sys.argv)

# # 화면 전환용 Widget 설정
# widget = QtWidgets.QStackedWidget()

# # Widget 추가
# widget.addWidget(LoginPage())
# widget.addWidget(ChatWindow())
# # widget.addWidget(ScreenCaptureClass())

# # 프로그램 화면을 보여주는 코드
# widget.setObjectName("kakaoFrame")
# widget.setFixedWidth(360)
# widget.setFixedHeight(589)
# widget.setStyleSheet(
#     "#kakaoFrame {background-color:rgb(255,235,51); border:1px solid rgb(123,113,21)}")
# widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
# widget.show()

# # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
# app.exec_()
