import PyQt5
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidget, QMessageBox, QApplication
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import uic

from socket import *
from select import select
import sys
from _socket import AF_INET, socket, SOCK_STREAM

ui_form = uic.loadUiType("ChattingPage.ui")[0]
HOST = 'localhost'
PORT = 3000
s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))


class ChatWindow(QMainWindow, ui_form):

    def __init__(self):
        super().__init__()
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
        self.inputText.setPlainText('')
        data = msg.encode()
        # 메시지 길이를 구한다.
        length = len(data)
        # server로 little 엔디언 형식으로 데이터 길이를 전송한다.
        s.sendall(length.to_bytes(4, byteorder="little"))
        # 데이터를 전송한다.
        s.sendall(data)
        self.showChat(msg)

    def showChat(self, msg):
        self.resultBrower.append("[나] %s" % msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = ChatWindow()
    myWindow.setWindowTitle('채팅 프로그램')
    myWindow.show()
    app.exec_()
