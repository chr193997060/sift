import cv2
from PyQt5 import Qt, QtWidgets, QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QMainWindow
import numpy as np


class ImageBox(QWidget):
    def __init__(self):
        super(ImageBox, self).__init__()
        self.img = None
        self.scaled_img = None
        self.point = QPoint(0, 0)
        self.start_pos = None
        self.end_pos = None
        self.left_click = False
        self.scale = 0.5

    def init_ui(self):
        self.setWindowTitle("ImageBox")

    def set_image(self, img_path):
        """
        open image file
        :param img_path: image file path
        :return:
        """
        self.img = QPixmap(img_path)
        self.scaled_img = self.img.scaled(self.size())

    def paintEvent(self, e):
        """
        receive paint events
        :param e: QPaintEvent
        :return:
        """
        if self.scaled_img:
            painter = QPainter()
            painter.begin(self)
            painter.scale(self.scale, self.scale)
            painter.drawPixmap(self.point, self.scaled_img)
            painter.end()

    def mouseMoveEvent(self, e):
        """
        mouse move events for the widget
        :param e: QMouseEvent
        :return:
        """
        if self.left_click:
            self.end_pos = e.pos() - self.start_pos
            self.point = self.point + self.end_pos
            self.start_pos = e.pos()
            self.repaint()

    def mousePressEvent(self, e):
        """
        mouse press events for the widget
        :param e: QMouseEvent
        :return:
        """
        if e.button() == Qt.LeftButton:
            self.left_click = True
            self.start_pos = e.pos()

    def mouseReleaseEvent(self, e):
        """
        mouse release events for the widget
        :param e: QMouseEvent
        :return:
        """
        if e.button() == Qt.LeftButton:
            self.left_click = False


class body(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        # 初始化一个img的ndarry，用于存储图像
        pass



class imageBox(QWidget):
    def __init__(self, parent=None):
        super(imageBox, self).__init__(parent)

        self.image_frame = QtWidgets.QLabel()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)


        self.image_frame.setStyleSheet("border:2px solid red;")


    def set_img(self, img_path):
        self.image = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8),cv2.IMREAD_COLOR)
        #self.image = cv2.imread(img_path)
        self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(self.image))


    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        print("980")
        pass

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        print("845")

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        print("2456")