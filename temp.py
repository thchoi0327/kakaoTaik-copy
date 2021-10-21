import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("kakao.ui", self)
        self.pushButton.clicked.connect(self.openCaptureClass)

    def openCaptureClass(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def login(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def buttonColor(self):
        print('btnColor')

    def buttonColorPw(self):
        print('asdasd')


class ScreenCaptureClass(QMainWindow):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # 화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()

    # Widget 추가
    widget.addWidget(MainWindow())
    widget.addWidget(ScreenCaptureClass())
    # widget.addWidget(ScreenCaptureClass())

    # 프로그램 화면을 보여주는 코드
    widget.setFixedWidth(360)
    widget.setFixedHeight(589)
    widget.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
