from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '/')
from QGraphicsView import QGraphicsView_r

from abcde import ImageLabel


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.picshow = QGraphicsView_r(self.centralWidget)
        self.picshow.setObjectName("picshow")
        self.picshow.setStyleSheet("border:2px solid #130c0e;")

        # self.picshow.setHorizontalScrollBarPolicy(1)
        # self.picshow.setVerticalScrollBarPolicy(1)

        self.gridLayout.addWidget(self.picshow, 0, 1, 3, 1)

        self.zoomout = QtWidgets.QPushButton(self.centralWidget)
        self.zoomout.setObjectName("zoomout")
        self.gridLayout.addWidget(self.zoomout, 0, 0, 1, 1)
        self.zoomin = QtWidgets.QPushButton(self.centralWidget)
        self.zoomin.setObjectName("zoomin")
        self.gridLayout.addWidget(self.zoomin, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.zoomout.setText(_translate("MainWindow", "放大"))
        self.zoomin.setText(_translate("MainWindow", "缩小"))
