import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class ChildOneWin(QWidget):
    def __init__(self, parent=None):
        super(ChildOneWin, self).__init__(parent)

        self.main_layout = QVBoxLayout()
        self.top_widget = QWidget()
        self.setLayout(self.main_layout)
        self.top_widget.setObjectName("ChildOneWin_wdt")
        self.top_widget.setStyleSheet("#ChildOneWin_wdt{background:rgb(255,255,255)}")
        self.main_layout.addWidget(self.top_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        top_widget_layout = QVBoxLayout()
        self.top_widget.setLayout(top_widget_layout)

        self.test_btn = QPushButton('窗口1')
        top_widget_layout.addStretch(1)
        top_widget_layout.addWidget(self.test_btn)


class ChildTwoWin(QWidget):
    def __init__(self, parent=None):
        super(ChildTwoWin, self).__init__(parent)

        self.main_layout = QVBoxLayout()

        self.top_widget = QWidget()
        self.setLayout(self.main_layout)
        self.top_widget.setObjectName("ChildTwoWin_wdt")
        self.top_widget.setStyleSheet("#ChildTwoWin_wdt{background:rgb(255,0,0)}")
        self.main_layout.addWidget(self.top_widget)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        top_widget_layout = QVBoxLayout()
        self.top_widget.setLayout(top_widget_layout)

        self.test_btn = QPushButton('窗口2')
        top_widget_layout.addStretch(1)
        top_widget_layout.addWidget(self.test_btn)
        top_widget_layout.addStretch(1)


class ChildThreeWin(QWidget):
    def __init__(self, parent=None):
        super(ChildThreeWin, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.BypassWindowManagerHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.wdt = QWidget()
        #self.wdt.setAttribute(Qt.WA_TranslucentBackground)
        self.wdt.setObjectName("tipWaitingWindow_back")
        self.wdt.setStyleSheet("#tipWaitingWindow_back{background:rgba(0,0,0,0.2)}")

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.wdt)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        main_layout = QVBoxLayout()

        self.wdt.setLayout(main_layout)

        self.test_btn = QPushButton('窗口3')
        main_layout.addWidget(self.test_btn)
        main_layout.addStretch(1)


class WinUIform(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('透明窗口测试')
        self.resize(330, 350)

        main_layout = QVBoxLayout()

        self.setLayout(main_layout)


        top_widget = QWidget()
        top_widget_layout = QHBoxLayout()


        top_widget.setLayout(top_widget_layout)

        self.test_btn = QPushButton('测试')
        self.test_btn.clicked.connect(self.call_back_test_btn)

        self.control_btn = QPushButton('控制')
        self.control_btn.clicked.connect(self.call_back_control_btn)

        self.show_btn = QPushButton('显示')
        self.show_btn.clicked.connect(self.call_back_show_btn)

        top_widget_layout.addWidget(self.test_btn)
        top_widget_layout.addStretch(1)
        top_widget_layout.addWidget(self.control_btn)
        top_widget_layout.addStretch(1)
        top_widget_layout.addWidget(self.show_btn)

        self.bottom_widget = QWidget()

        main_layout.addWidget(top_widget)
        main_layout.addWidget(self.bottom_widget)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 5)

        self.child_one_win = ChildOneWin()
        self.child_two_win = ChildTwoWin()
        self.child_three_win = ChildThreeWin()

        self.bottom_widget_layout = QHBoxLayout()

        self.bottom_widget.setLayout(self.bottom_widget_layout)
        self.bottom_widget_layout.addWidget(self.child_one_win)
        #self.bottom_widget_layout.addChildWidget(self.child_two_win)

        #self.child_two_win.setGeometry(50, 50, 200, 200)

    def call_back_show_btn(self):
        top_rect = self.bottom_widget.geometry()
        print(top_rect)
        self.bottom_widget_layout.addChildWidget(self.child_three_win)
        self.child_three_win.resize(top_rect.width(), top_rect.height())

    def call_back_test_btn(self):
        pass

    def call_back_control_btn(self):
        pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 下面两种方法都可以
    win = WinUIform()
    #win = Winform()
    win.show()
    sys.exit(app.exec_())