from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsView


class QGraphicsView_r(QtWidgets.QGraphicsView):
    # def __init__(self):
    #     self.left_flag = False
    #     self.right_flag = False

    leftMouseButtonPressed = pyqtSignal(float, float)
    leftMouseButtonReleased = pyqtSignal(float, float)

    def get_v(self, tt):  # 获取数据 and 初始化
        self.xx = tt

        self.canPan = True

        # self.left_flag = False
        # self.right_flag = False
        # self.label_x = 0  # label当前坐标
        # self.label_y = 0
        # self.mouse_mv_x = ""  # 鼠标移动上一次坐标
        # self.mouse_mv_y = ""
        # self.x1 = ""
        # self.y1 = ""

    # 鼠标滑动
    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        print(event.angleDelta())
        if event.angleDelta().y() < 0:
            self.xx.on_zoomin_clicked()
        elif event.angleDelta().y() > 0:
            self.xx.on_zoomout_clicked()

    # 鼠标点击事件
    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        if event.button() == QtCore.Qt.LeftButton:
            if self.canPan:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.leftMouseButtonPressed.emit(scenePos.x(), scenePos.y())
        QGraphicsView.mousePressEvent(self, event)

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):

        QGraphicsView.mouseReleaseEvent(self, event)
        scenePos = self.mapToScene(event.pos())
        if event.button() == QtCore.Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
            self.leftMouseButtonReleased.emit(scenePos.x(), scenePos.y())

    # # 鼠标移动事件
    # def mouseMoveEvent(self, event):
    #
    #     if self.left_flag:
    #         self.x1 = event.x()
    #         self.y1 = event.y()
    #
    #         if self.mouse_mv_x != "" and self.mouse_mv_y != "":
    #             self.label_x = self.label_x + (self.x1 - self.mouse_mv_x)
    #             self.label_y = self.label_y + (self.y1 - self.mouse_mv_y)
    #         self.mouse_mv_x = self.x1
    #         self.mouse_mv_y = self.y1
    #         print(self.label_x, self.label_y)
    #         print("-----")
