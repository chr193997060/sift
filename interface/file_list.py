import os

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
from PyQt5.QtCore import Qt, QSize, QDir

file_path = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # 根路径
sys.path.append(file_path)
from PyQt5.QtWidgets import QDesktopWidget, QFileSystemModel, QTreeView


class File_list_Ui(object):
    def get_shujv(self, xx):
        self.xx = xx

    def init(self):
        self.file_path = file_path
        # 获取屏幕坐标系
        self.screen = QDesktopWidget().screenGeometry()


    def setupUi(self, Form):


        print(self.file_path)


        self.filelist_frame = QtWidgets.QTreeView(Form)
        self.filelist_frame.setGeometry(QtCore.QRect(0, 0, int(self.screen.width() * 0.2 - 60),
                                                     int(self.screen.height() * 0.7) + 20))
        # self.filelist_frame.setStyleSheet("border:2px solid red;")

    def doubleck(self, Qmodelidx):
        img_type = ["bmp", "jpg", "png", "webp", "PNG"]
        d_filepath = self.filemodel.filePath(Qmodelidx)
        d_t = d_filepath.split("/")
        d_t2 = d_t[-1].split(".")
        if d_t2[-1] in img_type:
            if d_filepath == self.xx.operatFrom.img:
                return
            print(d_filepath)
            self.xx.showimage(d_filepath)
            self.xx.operatFrom.img = d_filepath
            self.xx.operatFrom.sift_img = None

    def set_filemodel(self, path):
        # 获取系统文件
        self.filemodel = QFileSystemModel()
        # 设置根目录
        self.filemodel.setRootPath(path)
        self.filelist_frame.setModel(self.filemodel)
        self.filelist_frame.setRootIndex(self.filemodel.index(path))
        for col in range(1, 4):
            self.filelist_frame.setColumnHidden(col, True)
        self.filelist_frame.doubleClicked.connect(self.doubleck)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = File_list_Ui()
    ui.init()
    ui.setupUi(widget)
    ui.set_filemodel(ui.file_path)
    widget.show()
    sys.exit(app.exec_())
