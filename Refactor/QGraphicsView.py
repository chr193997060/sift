from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsView


class QGraphicsView_r(QtWidgets.QGraphicsView):

    leftMouseButtonPressed = pyqtSignal(float, float)
    leftMouseButtonReleased = pyqtSignal(float, float)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        # 鼠标滑轮
        if event.angleDelta().y() < 0:
            self.img_frame_.img_down()
        elif event.angleDelta().y() > 0:
            self.img_frame_.img_up()

    def get_img_xx(self, tt):
        self.img_frame_ = tt
        self.canPan = True


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
