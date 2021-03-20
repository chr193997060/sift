import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtWidgets import QDesktopWidget

class Left_Ui(object):
    def setupUi(self, Form):
        # 获取屏幕坐标系
        self.screen = QDesktopWidget().screenGeometry()

        self.left_frame = QtWidgets.QLabel(Form)
        self.left_frame.setGeometry(QtCore.QRect(0, 0, 20, int(self.screen.height() * 0.8)))
        self.left_frame.setStyleSheet("border:2px solid red;")





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Left_Ui()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())