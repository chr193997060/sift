import sys
from PyQt5.QtWidgets import QWidget, QApplication,QGraphicsScene,QGraphicsView
import time

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500,400)
        scene=QGraphicsScene(self)  #创建场景
        self.t=scene.addText("Hello, world!")  #在场景中添加文本
        view=QGraphicsView(scene,self)  #创建视图窗口
        view.move(10,10)
        view.show()  #显示

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())