# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QPoint, QRectF, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStyleOptionGraphicsItem, QWidget, QGraphicsItem

# from util.ImageUtil import MyImage


class ImageWidget(QGraphicsPixmapItem):
    # 影像在横轴偏移量
    w_offset = 0
    # 影像在纵轴的偏移量
    h_offset = 0
    # 鼠标当前所在的像素位置
    w_cur_pos = 0
    h_cur_pos = 0

    def __init__(self, pixmap: QPixmap, signal_pixel_selected):
        super(ImageWidget, self).__init__(pixmap)
        self.pixmap = pixmap
        self.setAcceptDrops(True)
        self.m_scaleValue = 1
        self.m_scaleDafault = 1
        self.m_isMove = False
        self.m_startPos = None
        self.setAcceptHoverEvents(True)
        self.signal_pixel_selected = signal_pixel_selected

    def boundingRect(self):
        self.w_offset = int(self.pixmap.width() / 2)
        self.h_offset = int(self.pixmap.height() / 2)
        return QRectF(-self.w_offset, -self.h_offset,
                      self.pixmap.width(), self.pixmap.height())

    def paint(self, painter: QPainter, const: QStyleOptionGraphicsItem, widget: QWidget):
        self.setOffset(-self.w_offset, -self.h_offset)
        painter.drawPixmap(-self.w_offset, -self.h_offset, self.pixmap)

    # 将主界面的控件QGraphicsView的width和height传进本类中，并根据图像的长宽和控件的长宽的比例来使图片缩放到适合控件的大小
    def setQGraphicsViewWH(self, nwidth: int, nheight: int):
        nImgWidth = self.pixmap.width()
        nImgHeight = self.pixmap.height()
        t_width = nwidth * 1.0 / nImgWidth
        t_height = nheight * 1.0 / nImgHeight
        if t_width > t_height:
            self.m_scaleDafault = t_height
        else:
            self.m_scaleDafault = t_width
        self.setScale(self.m_scaleDafault)
        self.m_scaleValue = self.m_scaleDafault

    # 重置图片大小
    def resetItemPos(self):
        #  缩放比例回到一开始的自适应比例
        self.m_scaleValue = self.m_scaleDafault
        # 缩放到一开始的自适应大小
        self.setScale(self.m_scaleDafault)
        self.setPos(0, 0)

    def getScaleValue(self):
        return self.m_scaleValue

    # 鼠标点击事件
    def mousePressEvent(self, event):
        print("鼠标点击事件 x=%d y=%d" % (event.pos().x(), event.pos().y()))
        if event.buttons() == Qt.LeftButton:  # 左键按下
            self.m_startPos = event.pos()
            self.m_isMove = True
        elif event.buttons() == Qt.RightButton:  # 右键按下
            print("单击鼠标右键")
        elif event.buttons() == Qt.MidButton:  # 中键按下
            print("单击鼠标中键")

    '''滚轮滚动事件'''

    def wheelEvent(self, event):
        if event.delta() > 0 and self.m_scaleValue >= 1000:
            return
        elif event.delta() < 0 and self.m_scaleValue <= 0.01:
            return
        else:
            angle = event.delta()
            # 获取当前鼠标相对于view的位置
            pos = event.pos()
            qrealOriginScale = self.m_scaleValue
            if angle > 0:
                self.m_scaleValue *= 1.1
            else:  # 滚轮下滚
                self.m_scaleValue *= 0.9
            self.setScale(self.m_scaleValue)
            # 使图片缩放的效果看起来像是以鼠标所在点为中心进行缩放的
            if angle > 0:
                self.moveBy(-pos.x() * qrealOriginScale * 0.1, -pos.y() * qrealOriginScale * 0.1)
            else:  # 滚轮下滚
                self.moveBy(pos.x() * qrealOriginScale * 0.1, pos.y() * qrealOriginScale * 0.1)

    '''鼠标双击事件(单击)'''

    def mouseDoubleClickEvent(self, event):
        self.resetItemPos()

    '''鼠标键释放事件'''

    def mouseReleaseEvent(self, event):
        self.m_isMove = False

    '''鼠标移动事件'''

    def mouseMoveEvent(self, event):
        if self.m_isMove:
            point: QPoint = (event.pos() - self.m_startPos) * self.m_scaleValue
            self.moveBy(point.x(), point.y())
