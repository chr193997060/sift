import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QPushButton, QHBoxLayout, QVBoxLayout, QWidget


class setupWindow(QWidget):
    def __init__(self, parent=None):
        super(setupWindow, self).__init__(parent)
        # 获取屏幕坐标系
        self.screen = QDesktopWidget().screenGeometry()
        self.setupUi()

    def setupUi(self):
        self.resize(int(self.screen.width() / 2), int(self.screen.height() / 2))
        self.setWindowTitle('设置')

        bt1 = QPushButton('应用设置', self)
        bt2 = QPushButton('恢复初始', self)
        bt3 = QPushButton('取消', self)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(bt1)
        hbox.addWidget(bt2)
        hbox.addWidget(bt3)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = setupWindow()
    ui.show()
    sys.exit(app.exec_())
