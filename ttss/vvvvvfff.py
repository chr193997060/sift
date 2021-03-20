import sys
import os

from PyQt5.Qt import *  # noqa


class DirectoryTreeWidget(QTreeView):

    def __init__(self, path=QDir.currentPath(), *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.init_model(path)
        self.expandsOnDoubleClick = False
        self.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.setAutoScroll(True)

    def init_model(self, path):
        self.extensions = ["*.*"]
        self.path = path
        model = QFileSystemModel(self)
        model.setRootPath(QDir.rootPath())
        model.setReadOnly(False)
        model.setFilter(QDir.AllDirs | QDir.NoDot | QDir.AllEntries)
        self.setModel(model)
        self.set_path(path)

    def set_path(self, path):
        self.path = path
        model = self.model()
        index = model.index(str(self.path))

        if os.path.isfile(path):
            self.setRootIndex(model.index(
                os.path.dirname(str(self.path))))
            self.scrollTo(index)
            self.setCurrentIndex(index)
        else:
            self.setRootIndex(index)


class Foo(QWidget):

    def __init__(self, path):
        super().__init__()

        self.path = path

        self.tree_view = DirectoryTreeWidget(path=".")
        self.tree_view.show()
        bt = QPushButton(f"Update {path}")
        bt.pressed.connect(self.update_file)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)
        layout.addWidget(bt)

        self.setLayout(layout)

        # New file will automatically refresh QFileSystemModel
        self.create_file()

    def create_file(self):
        with open(self.path, "w") as f:
            data = "This new file contains xx bytes"
            f.write(data.replace("xx", str(len(data))))

    def update_file(self):
        model = self.tree_view.model()

        # Updating a file won't refresh QFileSystemModel, the question is,
        # how can we update that particular item to be refreshed?
        data = "The file updated is much larger, it contains xx bytes"
        with open(self.path, "w") as f:
            f.write(data.replace("xx", str(len(data))))

        # file_info = self.obj.model.fileInfo(index)
        # file_info.refresh()
        index = model.index(self.path)
        model.setData(index, model.data(index))
        QMessageBox.about(None, "Info", f"{self.path} updated, new size is {len(data)}")


def main():
    app = QApplication(sys.argv)
    foo = Foo("foo.txt")
    foo.setMinimumSize(640, 480)
    foo.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()