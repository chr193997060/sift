from PyQt5.QtWidgets import QMainWindow,QApplication,QHBoxLayout,QPushButton,QWidget
import sys

class WinForm(QMainWindow):

  def __init__(self,parent=None):
    super(WinForm, self).__init__(parent)

    self.setFixedSize(200,200)

    self.setWindowTitle('关闭主窗口的例子')
    #创建按钮实例，按钮名称：关闭主窗口
    self.button1=QPushButton('关闭主窗口')
    #按钮的clicked信号与onButtonClick槽函数关联起来
    self.button1.clicked.connect(self.onButtonClick)

    #水平布局
    layout=QHBoxLayout()
    #按钮加入水平布局中
    layout.addWidget(self.button1)

    #创建widget窗口实例
    main_frame=QWidget()
    #加载布局
    main_frame.setLayout(layout)
    #把widget窗口加载到主窗口的中央位置
    self.setCentralWidget(main_frame)
    main_frame.setFixedSize(150, 100)

  def onButtonClick(self):
    #sender是发送信号的对象，这里获得的是按钮的名称
    sender=self.sender()
    #以文本的行书输出按钮的名称
    print(sender.text() + ' 被按下了')
    #获取QApplication类的对象
    qApp=QApplication.instance()
    #退出
    qApp.quit()
if __name__ == '__main__':
  app=QApplication(sys.argv)
  win=WinForm()
  win.show()
  sys.exit(app.exec_())