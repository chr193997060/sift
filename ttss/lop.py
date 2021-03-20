from PyQt5.QtCore import QDir

from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication


class Main(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)
        model = QFileSystemModel()
        self.setModel(model)
        model.setRootPath(QDir.rootPath())
        self.setRootIndex(model.index("C:"))
        self.doubleClicked.connect(self.test)

    def test(self, signal):
        file_path = self.model().filePath(signal)
        print(file_path)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec_())
