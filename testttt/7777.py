# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'signal.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
class Ui_Form(object):
  def setupUi(self, Form):
    Form.setObjectName("Form")
    Form.resize(431, 166)
    self.pushButton = QtWidgets.QPushButton(Form)
    self.pushButton.setGeometry(QtCore.QRect(160, 50, 91, 41))
    font = QtGui.QFont()
    font.setFamily("YaHei Consolas Hybrid")
    font.setPointSize(14)
    self.pushButton.setFont(font)
    self.pushButton.setObjectName("pushButton")
    self.retranslateUi(Form)
    QtCore.QMetaObject.connectSlotsByName(Form)
  def retranslateUi(self, Form):
    _translate = QtCore.QCoreApplication.translate
    Form.setWindowTitle(_translate("Form", "信号与槽"))
    self.pushButton.setText(_translate("Form", "运行"))

class MyMainForm(QMainWindow, Ui_Form):
  def __init__(self, parent=None):
    super(MyMainForm, self).__init__(parent)
    self.setupUi(self)
    self.pushButton.clicked.connect(self.showMsg)
  def showMsg(self):
    QMessageBox.information(self, "信息提示框", "OK,内置信号与自定义槽函数！")

if __name__ == "__main__":
  app = QApplication(sys.argv)
  myWin = MyMainForm()
  myWin.show()
  sys.exit(app.exec_())