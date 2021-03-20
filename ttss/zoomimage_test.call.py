#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：mgboy time:2020/6/25
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget

from zoomimage_test import Ui_Form


class Myfolder(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Myfolder, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_1)

    def button_1(self):
        print('点击pushbutton')
        # 方法1：完美显示图片，并自适应大小
        pix = QtGui.QPixmap(r"C:\Users\chen\Desktop\图像管理\image\cccc.jpg")
        self.label.setPixmap(pix)
        self.label.setStyleSheet("border: 2px solid blue")
        self.label.setScaledContents(True)
        # 方法2：这个会使图片显示模糊
        # jpg = QtGui.QPixmap("D:/PixivWallpaper/catavento.png").scaled(self.label.width(), self.label.height())
        # self.label.setPixmap(jpg)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = Myfolder()
    myWin.show()
    sys.exit(app.exec_())