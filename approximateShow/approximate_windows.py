from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
import sys
from approximateShow.img_approximate_box import Approximate_img_list_Ui
from interface.image_frame import Ui_Form_img
from interface.file_list import File_list_Ui
from interface.setup import setupWindow



class ApproximateWindow(QMainWindow):
    # 声明无参数的信号
    # sig = pyqtSignal()

    def set_list_path(self, name, paths):
        # print(name)
        # print(paths)
        self.imgFrom.set_shujv(name, paths)
        self.showfilelist()

    def setUi(self, MainWindow, name="图像", paths=[]):
        # 设置窗口实现
        self.setup_win = None

        # 图像显示
        self.imgFrom = ImageFrame()

        self.name = name
        self.paths = paths

        # 文件目录
        self.filelistFrom = FileListFrom()

        MainWindow.setObjectName("Form")
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        body_width = int(screen.width() * 0.7)
        body_heigh = int(screen.height() * 0.8)

        # 窗体
        MainWindow.resize(body_width, body_heigh)
        MainWindow.setAutoFillBackground(True)

        # 内容主体
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.centralwidget.setStyleSheet("border:2px solid red;")
        MainWindow.setCentralWidget(self.centralwidget)

        # 显示图片布局
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(
            QtCore.QRect(int(screen.width() * 0.2 - 20), 20, int(screen.width() / 2), int(screen.height() * 0.6)))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setStyleSheet("border:2px solid #130c0e;")

        # 图片里面的布局
        self.MaingridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.MaingridLayout.setContentsMargins(0, 0, 0, 0)
        self.MaingridLayout.setObjectName("MaingridLayout")

        # 目录结构
        self.filelistLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.filelistLayoutWidget.setGeometry(QtCore.QRect(30, 20, int(screen.width() * 0.2 - 60),
                                                           int(screen.height() * 0.7) + 20))
        # self.filelistLayoutWidget.setStyleSheet("border:2px solid #130c0e;")
        self.filelistLayoutWidget.setObjectName("filelistLayoutWidget")

        self.filelistLayout = QtWidgets.QGridLayout(self.filelistLayoutWidget)
        self.filelistLayout.setContentsMargins(0, 0, 0, 0)
        self.filelistLayout.setObjectName("filelistLayout")

        self.retranslateUi(MainWindow)
        # self.showoperat()
        self.showfilelist_approximate()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "近似图像"))

    def showimage_approximate(self, img):
        self.MaingridLayout.addWidget(self.imgFrom)
        self.imgFrom.set_img(img)
        self.imgFrom.show()

    def showfilelist_approximate(self):  # 显示列表
        self.filelistLayout.addWidget(self.filelistFrom)
        self.filelistFrom.set_shujv(self)
        self.filelistFrom.set_filemodel()
        self.filelistFrom.show()


class ImageFrame(Ui_Form_img, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class FileListFrom(Approximate_img_list_Ui, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init()
        self.setupUi(self)


def start_widow_approximate(xx, paths_du):
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = ApproximateWindow()
    ui.setUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_widow_approximate("ss", "ss")
