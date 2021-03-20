#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from xiantao.imagebox import *
from image_frame import Ui_Form_img


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.img = np.ndarray(())
        self.initUI()


    def initUI(self):
        # 设置主窗口的标题
        self.setWindowTitle('图像管理系统')
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        self.body_width = int(screen.width() * 0.7)
        self.body_heigh = int(screen.height() * 0.8)
        # 设置窗口的尺寸
        self.resize(self.body_width, self.body_heigh)
        left = (screen.width() - self.body_width) / 2
        top = (screen.height() - self.body_heigh) / 2
        self.move(int(left), int(top))


        # 底部显示
        self.statusBar()

        # 设置菜单栏
        self.menubr = self.menuBar()
        self.file = self.menubr.addMenu('文件')
        # 打开
        self.open = QAction("打开..", self)
        self.open.setShortcut('Ctrl+O')
        self.open.setStatusTip('打开图像')
        self.open.triggered.connect(self.open_image)
        self.file.addAction(self.open)
        # 添加图像目录
        self.directory = QAction('添加图像目录..', self)
        self.directory.setStatusTip('添加目录位置')
        self.file.addAction(self.directory)

        # widget = QWidget()
        # gridLayout = QGridLayout(self)
        # widget.setLayout(gridLayout)
        # self.setCentralWidget(widget)
        #
        # self.imgbox = imageBox()
        #
        # self.imgbox.setGeometry(QtCore.QRect(60, 60, 500, 500))
        #
        # # self.setCentralWidget(self.imgbox)
        #
        #
        # gridLayout.addWidget(self.imgbox)




    def open_image(self):
        return
        imgName, _ = QFileDialog.getOpenFileName(self, "openImage", "", "*.png *.jpg *.bmp;;All Files(*)")
        if imgName == '':
            return
        print("1234")
        self.imgbox.set_img(imgName)


class img_open(Ui_Form_img, QtWidgets.QWidget):
    # 图像界面
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    # 显示在屏幕上
    main.show()
    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())
