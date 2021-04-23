import hashlib
import os

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
from PyQt5.QtCore import Qt, QSize, QDir, QStringListModel

from db.sift_img_db import select_img_md5, delete_img_path, select_img_path_img_md5, delete_img_sift, delete_img_tag_
file_path = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # 根路径
sys.path.append(file_path)
from PyQt5.QtWidgets import QDesktopWidget, QFileSystemModel, QTreeView, QAbstractItemView, QMenu, QAction, QMessageBox, \
    QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor
from logo.logo_dir import logo_path


class Approximate_img_list_Ui(object):
    def set_shujv(self, obj):
        print("9" * 50)
        self.obj = obj
        self.name = obj.name
        self.aa = obj.paths
        # print(self.name)
        # print(self.aa)

    def init(self):
        self.file_path = file_path
        # 获取屏幕坐标系
        self.screen = QDesktopWidget().screenGeometry()
        self.aa = []
        self.name = "图像"
        self.last_path = ""
        # self.on = ""
        self.click_row = ""

    def setupUi(self, Form):

        print(self.file_path)

        self.filelist_frame = QtWidgets.QTreeView(Form)
        self.filelist_frame.setGeometry(QtCore.QRect(0, 0, int(self.screen.width() * 0.2 - 60),
                                                     int(self.screen.height() * 0.7) + 20))
        # self.filelist_frame.setStyleSheet("border:2px solid red;")

    def doubleck(self, Qmodelidx):
        # print("dddddd")
        img_type = ["bmp", "jpg", "png", "webp", "PNG"]
        if Qmodelidx.row() == 0:
            if Qmodelidx.data() is None:
                return
            else:
                if Qmodelidx.data() in "图像":
                    return
        data = self.aa[Qmodelidx.row()]
        # print(data)

        # d_t = data[0].split("\\")
        # print(d_t)
        # d_t2 = d_t[-1].split(".")
        # print(d_t2)
        if data[0][-3:] in img_type:
            path = data[0]
            # print(path)
            if path == self.last_path:
                return
            self.last_path = path
            self.click_row = Qmodelidx.row()
            self.obj.showimage_approximate(path)

    def set_filemodel(self):

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['图像位置', '近似度'])

        item = QStandardItem(self.name)
        model.appendRow(item)

        for i in self.aa:
            path = QStandardItem(str(i[0]))
            item.appendRow(path)
            item.setChild(path.index().row(), 1, QStandardItem(str(i[1])))

        self.filelist_frame.setModel(model)
        self.filelist_frame.header().resizeSection(0, int((self.screen.width() * 0.2 - 60) * 0.7))
        self.filelist_frame.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.filelist_frame.doubleClicked.connect(self.doubleck)
        self.filelist_frame.setContextMenuPolicy(Qt.CustomContextMenu)
        self.filelist_frame.customContextMenuRequested.connect(self.rightMenuShow)

    def rightMenuShow(self, e):
        # print(dir(e))
        # print(e)
        # print(e.y())
        # print(e.y())
        y_row = e.y() // 19
        # print("self.item_row", self.click_row)
        # print("y_row", y_row)
        # print("self.on", self.on)
        # if
        if e.y() < 20 or self.click_row == "":
            # 添加右键菜单
            self.popMenu = QMenu()
            del_img_all = self.popMenu.addAction(u'删除所有图像')
            del_img_all.triggered.connect(self.delete_img_all)
            self.popMenu.exec_(QCursor.pos())
        elif (self.click_row + 1) == y_row:
            # 添加右键菜单
            self.popMenu = QMenu()
            del_img = self.popMenu.addAction(u'删除图像')
            del_img.triggered.connect(self.delete_img)
            self.popMenu.exec_(QCursor.pos())
        else:
            return


    def delete_img(self):
        print("dfhjdjiofjfdfkodfjkgkldcf")
        print(self.last_path)

        w = QWidget()
        msg_box = QMessageBox.question(w, '提示', '是否要删除%s' % self.last_path,
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if msg_box == QMessageBox.Yes:
            pass
        else:
            return
        try:
            os.remove(self.last_path)
        except:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '删除失败！')
            msg_box.exec_()
            return
        del self.aa[self.click_row]

        msg_box = QMessageBox(QMessageBox.Information, '提示', '删除成功！')
        msg_box.exec_()
        logo_path_ = logo_path() + "\\img.jpg"
        self.set_filemodel()
        self.obj.showimage_approximate(logo_path_)

        path_md5 = hashlib.md5(self.last_path.encode('utf-8')).hexdigest()
        img_md5 = select_img_md5(path_md5)[0]
        print(img_md5)
        delete_img_path(self.last_path)
        if select_img_path_img_md5(img_md5) > 0:
            pass
        else:
            delete_img_sift(img_md5)
            delete_img_tag_(img_md5)

        self.click_row = ""
        self.last_path = ""

    def delete_img_all(self):
        print("delete_img_all")



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Approximate_img_list_Ui()
    ui.init()
    ui.setupUi(widget)
    ui.set_filemodel()
    widget.show()
    sys.exit(app.exec_())
