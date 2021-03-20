# 图片显示空间封装
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, QPoint, QRect, QRectF, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QImage, QPixmap, QMovie
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem, QGraphicsTextItem, QLabel

from ImageWidget import ImageWidget


class ImageLabel(QGraphicsView):
    # 鼠标悬停像素的信号
    signal_pixel_selected = pyqtSignal(str, int)
    item: ImageWidget = None
    pixmap: QPixmap = None

    def __init__(self):
        super(ImageLabel, self).__init__()
        self.QImg = None
        self.image = None
        self.image_array = None
        self.background_color = QColor()
        self.background_color.setNamedColor('#ffffff')
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, self.background_color)
        self.__init_view()

    def __init_view(self):
        self.setAutoFillBackground(True)
        self.setPalette(self.palette)
        self.setAlignment(Qt.AlignCenter)
        self.v_width = self.width()
        self.v_height = self.height()
        self.scene = QGraphicsScene()  # 创建场景
        self.setSceneRect(QRectF(-(self.v_width / 2), -(self.v_height / 2), self.v_width - 10, self.v_height - 10))
        self.setScene(self.scene)

    # 显示整幅图像
    def showImage(self, image_array):
        self.scene.clear()
        height, width, bytesPerComponent = image_array.shape
        bytesPerLine = bytesPerComponent * width
        if bytesPerComponent == 1:
            # 显示灰度图像
            self.QImg = QImage(image_array.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)
        elif bytesPerComponent == 3:
            # 显示GGB图像
            self.QImg = QImage(image_array.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888)
        else:
            # 如果不符合就不显示
            return
        self.pixmap = QPixmap.fromImage(self.QImg)
        self.item = ImageWidget(self.pixmap, self.image, self.signal_pixel_selected)
        self.item.setQGraphicsViewWH(self.v_width, self.v_height)
        self.scene.addItem(self.item)
