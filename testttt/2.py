from PyQt5.QtWidgets import QApplication,QMainWindow,QAction
from PyQt5.QtGui import QIcon
#demo_7:菜单添加action以及状态栏显示消息
import sys
class Example(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.initUI()

    def initUI(self):
        action=QAction(QIcon('exit.png'),'&exit',self) #定义一个Action即动作
        action.setStatusTip('Exit application')#状态栏信息
        action.triggered.connect(self.app.quit) #触发事件动作为"关闭窗口"
        action.setShortcut('Ctrl+Q')#快捷键设置
        self.statusBar()#状态栏信

        menu=self.menuBar() #当前窗体创建menuBar
        fmenu=menu.addMenu('&file')

        menu2 = self.menuBar()
        fmenu2 = menu2.addMenu('&test') #再添加一个menuBar

        fmenu.addAction(action) #为第一级别menu添加动作
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Statusbar')
        self.show()

if __name__=='__main__':

    e=Example()
    sys.exit(e.app.exec())