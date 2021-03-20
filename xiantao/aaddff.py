from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap
import cv2
from Ui_picshow import Ui_MainWindow


class picturezoom(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(picturezoom, self).__init__(parent)
        self.setupUi(self)
        img = cv2.imread(r"C:\Users\chen\Desktop\PythonCode-master\ImageBox\images\wallhaven-d5qy5m.jpg")  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        # self.item.setScale(self.zoomscale)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)

        self.picshow.setScene(self.scene)  # 将场景添加至视图

        self.picshow.get_v(self)

        # self.picshow.setGeometry(QtCore.QRect(30, 30, 400, 400))

        # print(self.zooms)

        self.picshow.centerOn(100, 200)

    @pyqtSlot()
    def on_zoomin_clicked(self):
        """
        点击缩小图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale - 0.05
        if self.zoomscale <= 0:
            self.zoomscale = 0.2
        self.item.setScale(self.zoomscale)  # 缩小图像

    @pyqtSlot()
    def on_zoomout_clicked(self):
        """
        点击方法图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale + 0.05
        if self.zoomscale >= 1.2:
            self.zoomscale = 1.2
        self.item.setScale(self.zoomscale)  # 放大图像

    def xy_mobile(self):
        pass


def main():
    import sys
    app = QApplication(sys.argv)
    piczoom = picturezoom()
    piczoom.show()
    app.exec_()


if __name__ == '__main__':
    main()
