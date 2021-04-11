from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
import sys
from interface.image_frame import Ui_Form_img
from interface.file_list import File_list_Ui
from interface.setup import setupWindow
from interface.operating import Operating_Ui
from initialize.start import start

start()


class MainWindow(QMainWindow):
    # 声明无参数的信号
    sig = pyqtSignal()

    def setUi(self, MainWindow):

        # 设置窗口实现
        self.setup_win = None

        # 图像显示
        self.imgFrom = ImageFrame()
        # self.imgFrom.setStyleSheet("border:2px solid #181d4b;")

        # 图像下方按钮
        self.operatFrom = OperatFrom()

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

        # 菜单栏
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, body_width, 23))
        self.menubar.setObjectName("menubar")
        # self.menubar.setStyleSheet("border:2px solid red;")
        # 设置菜单栏
        MainWindow.setMenuBar(self.menubar)
        # 文件
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        # 设置
        self.setup = QtWidgets.QMenu(self.menubar)
        self.setup.setObjectName("setup")

        # 打开 --  文件
        self.open = QtWidgets.QAction("打开..", self)
        self.open.setStatusTip('打开图像')
        self.open.triggered.connect(self.open_image)
        self.menufile.addAction(self.open)
        # 添加图像目录  -- 文件
        self.directory = QAction('添加图像目录..', self)
        self.directory.setStatusTip('添加目录位置')
        self.menufile.addAction(self.directory)
        self.directory.triggered.connect(self.directory_open)

        # 设置
        self.setup_widow = QtWidgets.QAction("打开设计窗口", self)
        self.setup_widow.setStatusTip('打开图像')
        self.setup_widow.triggered.connect(self.open_set_widow)
        self.setup.addAction(self.setup_widow)

        self.sig.connect(self.call_back_sig)

        # 不能缺少  添加到菜单栏
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.setup.menuAction())

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

        # 左边按钮布局
        self.leftLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.leftLayoutWidget.setGeometry(QtCore.QRect(0, 0, 20, int(screen.height() * 0.8)))
        # self.leftLayoutWidget.setStyleSheet("border:2px solid #130c0e;")
        self.leftLayoutWidget.setObjectName("leftLayoutWidget")

        # 目录结构
        self.filelistLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.filelistLayoutWidget.setGeometry(QtCore.QRect(30, 20, int(screen.width() * 0.2 - 60),
                                                           int(screen.height() * 0.7) + 20))
        # self.filelistLayoutWidget.setStyleSheet("border:2px solid #130c0e;")
        self.filelistLayoutWidget.setObjectName("filelistLayoutWidget")

        self.filelistLayout = QtWidgets.QGridLayout(self.filelistLayoutWidget)
        self.filelistLayout.setContentsMargins(0, 0, 0, 0)
        self.filelistLayout.setObjectName("filelistLayout")

        # 图像下方
        self.operatLayouWidget = QtWidgets.QWidget(self.centralwidget)
        self.operatLayouWidget.setGeometry(
            QtCore.QRect(int(screen.width() * 0.2 - 20), int(screen.height() * 0.6) + 40, int(screen.width() / 2),
                         int(screen.height() * 0.1)))
        self.operatLayouWidget.setObjectName("operatLayouWidget")
        # self.operatLayouWidget.setStyleSheet("border:2px solid #130c0e;")

        self.operatLayout = QtWidgets.QGridLayout(self.operatLayouWidget)
        self.operatLayout.setContentsMargins(0, 0, 0, 0)
        self.operatLayout.setObjectName("operatLayout")

        # 底部
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        # self.statusbar.setStyleSheet("border:2px solid #181d4b;")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.showoperat()
        self.showfilelist()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "图像管理系统"))
        self.menufile.setTitle(_translate("MainWindow", "文件"))
        self.setup.setTitle(_translate("MainWindow", "设置"))

    def open_image(self):
        self.imgName, _ = QFileDialog.getOpenFileName(self, "openImage", "", "*.png *.jpg *.bmp;;All Files(*)")
        if self.imgName == '':
            return
        else:
            print(self.imgName)

        self.operatFrom.img = self.imgName
        self.showimage(self.imgName)

    def showimage(self, img):
        self.MaingridLayout.addWidget(self.imgFrom)
        self.imgFrom.set_img(img)
        self.imgFrom.show()

    def showoperat(self):
        self.operatLayout.addWidget(self.operatFrom)
        self.operatFrom.show()

    def showfilelist(self):
        self.filelistLayout.addWidget(self.filelistFrom)
        self.filelistFrom.get_shujv(self)
        self.filelistFrom.set_filemodel(self.filelistFrom.file_path)
        self.filelistFrom.show()

    def directory_open(self):
        m = QFileDialog.getExistingDirectory(self, "选取文件夹", "C:\\")  # 起始路径
        self.filelistFrom.file_path = m
        self.operatFrom.file_list = m
        self.showfilelist()

    def open_set_widow(self):
        self.sig.emit()

    def call_back_sig(self):
        if self.setup_win:
            print("++++++++++++++++++++++ call_back_sig first +++++++++++++++++++++")
            self.setup_win.show()
        else:
            self.setup_win = setupWindow()
            self.setup_win.show()
            # self.tick_win.move(200, 200)
            print("--------------------- call_back_sig second ----------------")


class ImageFrame(Ui_Form_img, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class OperatFrom(Operating_Ui, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.config()
        self.setupUi(self)


class FileListFrom(File_list_Ui, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init()
        self.setupUi(self)


def start_widow():
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
