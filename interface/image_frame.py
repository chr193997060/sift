import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from PyQt5.QtCore import Qt, QSize, pyqtSlot
import sys
import os
from PyQt5.QtWidgets import QDesktopWidget, QGraphicsPixmapItem, QGraphicsScene, QMessageBox

file_path = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # 根路径
sys.path.append(file_path)
from Refactor.QGraphicsView import QGraphicsView_r


class Ui_Form_img(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        # 获取屏幕坐标系
        self.screen = QDesktopWidget().screenGeometry()
        self.picshow = QGraphicsView_r(Form)
        self.picshow.setGeometry(QtCore.QRect(0, 0, int(self.screen.width() / 2), int(self.screen.height() * 0.6)))
        self.picshow.setObjectName("picshow")
        self.picshow.setStyleSheet("border:2px solid red;")

    def set_img(self, img_path):
        try:
            self.image = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.shape[1] * 3,
                                      QtGui.QImage.Format_RGB888).rgbSwapped()
            pix = QtGui.QPixmap.fromImage(self.image)
            self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
            self.scene = QGraphicsScene()  # 创建场景
            self.scene.addItem(self.item)
            self.picshow.setScene(self.scene)  # 将场景添加至视图
            self.zoomscale = 1  # 图片放缩尺度
            self.picshow.get_img_xx(self)  # 把数据打到QGraphicsView_r里
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '该位置没有图像请检查！！')
            msg_box.exec_()

    @pyqtSlot()
    def img_up(self):
        """
        点击放大图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale + 0.05
        if self.zoomscale >= 3:
            self.zoomscale = 3
        self.item.setScale(self.zoomscale)  # 放大图像

    @pyqtSlot()
    def img_down(self):
        """
            点击缩小图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale - 0.05
        if self.zoomscale <= 0.1:
            self.zoomscale = 0.1
        self.item.setScale(self.zoomscale)  # 缩小图像


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form_img()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
