from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class CollectionWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # 设置窗口标题和大小
        self.setWindowTitle('树控件')
        self.resize(380, 360)

        # 添加收藏夹，根节点的父是 QTreeWidget对象
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(['收藏夹'])  # 是表，则有表头

        self.tree.clicked.connect(self.onClicked)
        self.f_item = self.tree.headerItem()

        # 添加一个初始文件夹
        child = QTreeWidgetItem(self.tree)
        child.setText(0, '目录/跟节点')
        child.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

        # 以下是窗口的设置
        self.setCentralWidget(self.tree)

        addAction = QAction("添加新子节点", self)
        addAction.triggered.connect(self.addItem)
        addAction2 = QAction("添加新目录/根节点", self)
        addAction2.triggered.connect(self.addFolder)
        deleteAction = QAction("删除", self)
        deleteAction.triggered.connect(self.deleteItem)

        toolbar = self.addToolBar("")
        toolbar.addAction(addAction)
        toolbar.addAction(addAction2)
        toolbar.addAction(deleteAction)
        self.show()

    # 添加树控件子节点
    def addItem(self):
        currNode = self.tree.currentItem()
        addChild = QTreeWidgetItem()
        addChild.setText(0, "新子节点")
        currNode.addChild(addChild)

    # 添加根节点
    def addFolder(self):
        child = QTreeWidgetItem(self.tree)
        child.setText(0, '新目录/根节点')
        child.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

    # 删除控件树子节点/根节点
    def deleteItem(self):
        try:
            # 尝试删除子节点（通过其父节点，调用removeChild函数进行删除）
            currNode = self.tree.currentItem()
            parent1 = currNode.parent()
            parent1.removeChild(currNode)
        except Exception:
            # 遇到异常时删除根节点
            try:
                rootIndex = self.tree.indexOfTopLevelItem(currNode)
                self.tree.takeTopLevelItem(rootIndex)
            except Exception:
                print(Exception)

    def onClicked(self):
        # 将之前选中的子项目背景色还原
        self.f_item.setBackground(0, QColor(255, 255, 255))
        # 获取当前选中项
        item = self.tree.currentItem()
        # 设置当前选择项背景
        item.setBackground(0, QColor('#AFEEEE'))
        # 更新前选中项
        self.f_item = item


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CollectionWindow()
    window.show()
    sys.exit(app.exec_())
