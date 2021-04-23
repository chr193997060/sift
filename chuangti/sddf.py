# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class FirstWindow(QMainWindow):
    sig = pyqtSignal()

    def __init__(self, parent=None):
        super(FirstWindow, self).__init__(parent)
        self.tick_win = None
        self.btn = QPushButton(self)
        self.hide_btn = QPushButton(self)
        self.init_ui()

    def init_ui(self):

        self.resize(200, 200)
        self.setWindowTitle('FirstWindow')

        self.btn.setText('Emit')
        self.btn.setGeometry(30, 40, 60, 40)
        self.btn.clicked.connect(self.call_back_btn)
        self.sig.connect(self.call_back_sig)

        self.hide_btn.setText('hide')
        self.hide_btn.setGeometry(30, 120, 60, 40)

        self.hide_btn.clicked.connect(self.call_back_hide)

    def call_back_btn(self):
        self.sig.emit()

    def call_back_sig(self):

        if self.tick_win:
            print("++++++++++++++++++++++ call_back_sig first +++++++++++++++++++++")
            self.tick_win.show()
        else:
            self.tick_win = SecondWindow()
            self.tick_win.show()
            #self.tick_win.move(200, 200)
            print("--------------------- call_back_sig second ----------------")

    def call_back_hide(self):
        if self.tick_win:
            self.tick_win.hide()


class SecondWindow(QMainWindow):

    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.resize(200, 100)
        self.setWindowTitle('SecondWindow')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FirstWindow()
    w.show()
    sys.exit(app.exec_())
