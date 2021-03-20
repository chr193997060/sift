import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Menu(QMainWindow):
    count=0
    def __init__(self):
        super(Menu,self).__init__()
        self.setWindowTitle('系统')
        self.resize(2600, 1000)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        bar = self.menuBar()  # 获取菜单栏

        file = bar.addMenu('文件')
        #新建菜单方式1
        new = QAction("新建", self)  # 也可以直接保存动作
        new.setShortcut("Ctrl+O")       # 快捷键
        file.addAction(new)
        #新建菜单2，加子菜单
        open = file.addMenu("打开")
        open.addAction('图片')            #添加“打开”子菜单
        #新建菜单3
        file.addAction('保存')            # 添加子菜单


        file.triggered.connect(self.windowaction)
        open.triggered.connect(self.openFile)  # 打开文件

    def openFile(self, q):
        self.imageLabel = QLabel()
        self.setCentralWidget(self.imageLabel)

        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', '图像文件(*.jpg *.png)')
        print(fname)

        self.imageLabel.setPixmap(QPixmap(fname))    #原图大小显示

        # png = QPixmap(fname).scaled(self.imageLabel.width(), self.imageLabel.height())  #按窗口大小显示
        # self.imageLabel.setPixmap(png)

    def windowaction(self, q):  # q:当前单击的菜单项
        print(q.text())
        if q.text() == "新建":
            Menu.count = Menu.count + 1
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("子窗口" + str(Menu.count))
            self.mdi.addSubWindow(sub)
            sub.show()
            self.mdi.tileSubWindows()       #平铺
            # self.mdi.cascadeSubWindows()   #级联排序

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('../Code/images/in.ico'))              #给标题添加图标
    main = Menu()
    main.show()
    sys.exit(app.exec_())
