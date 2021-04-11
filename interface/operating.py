import copyreg
import os
import pickle
import sys

from Bow.bow_achieve import search_img_calss

file_path = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # 根路径
sys.path.append(file_path)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QGraphicsPixmapItem, QGraphicsScene, QPushButton, QWidget, QHBoxLayout, \
    QMessageBox
import multiprocessing
from multiprocessing import Process
from utilty.comsift import *
from db.sift_img_db import *


class Operating_Ui(object):

    def config(self):
        self.img = None
        self.img2 = None
        self.sift_img = None
        self.sift_img_list = {}
        self.file_list = file_path
        self.img_type = ["bmp", "jpg", "png", "webp", "PNG"]
        self.img_des_list = []
        self.sift_img_des = None
        self.sift_img_kp = None
        self.sift_img_1 = None
        self.imgs_name = []
        self.img_md5 = None
        self.Traverse_img_path()

    def setupUi(self, Form):

        self.Form = Form

        # 获取屏幕坐标系
        self.screen = QDesktopWidget().screenGeometry()

        self.opera_frame = QWidget(Form)
        self.opera_frame.setGeometry(QtCore.QRect(0, 0, int(self.screen.width() / 2),
                                                  int(self.screen.height() * 0.1)))
        # self.opera_frame.setStyleSheet("border:2px solid red;")

        opera_layout = QHBoxLayout()
        self.opera_frame.setLayout(opera_layout)

        self.SIFT_button = QPushButton("计算图像SIFT特征")
        opera_layout.addWidget(self.SIFT_button)
        self.SIFT_button.clicked.connect(self.com_sitf)

        self.Find_same_img_button = QPushButton("检索近相似图像")
        opera_layout.addWidget(self.Find_same_img_button)
        self.Find_same_img_button.clicked.connect(self.find_same_img)

        self.show_SITF_img = QPushButton("显示图像SITF特征")
        opera_layout.addWidget(self.show_SITF_img)
        self.show_SITF_img.clicked.connect(self.show_sitf_img)

        self.Start_SITF = QPushButton("开始计算目录中图像的SITF特征")
        opera_layout.addWidget(self.Start_SITF)
        self.Start_SITF.clicked.connect(self.Start_sitf_com)

        self.save_sift_img_b = QPushButton("保存图像SIFT特征图")
        opera_layout.addWidget(self.save_sift_img_b)
        self.save_sift_img_b.clicked.connect(self.save_sift_img)

        self.select_mulu = QPushButton("选择当前目录为比对目录")
        opera_layout.addWidget(self.select_mulu)
        self.select_mulu.clicked.connect(self.select_mulu_set)

        # self.select_mulu2 = QPushButton("选择当前目录为比对目录")
        # opera_layout.addWidget(self.select_mulu2)

    def com_sitf(self):
        print("com sitf")
        if self.img == None:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '图片还没有选择!!')
            msg_box.exec_()
            return
        else:
            print(self.img)
            if self.img2 is None:
                self.img2 = self.img
            elif self.img2 == self.img:
                msg_box = QMessageBox(QMessageBox.Warning, '提示', '已计算过,内存已保存数据！！！不做计算！！')
                msg_box.exec_()
                return
            s = time.time()
            self.img_md5, self.sift_img_list[
                self.img], self.sift_img_des, self.sift_img_kp, self.sift_img = sift_img_com(self.img)
            e = time.time()
            print(e - s)
            if self.sift_img is None:
                msg_box = QMessageBox(QMessageBox.Warning, '提示', '计算图像的sitf特征失败')
                msg_box.exec_()
            else:
                msg_box = QMessageBox(QMessageBox.Information, '提示', '计算图像的sitf特征成功')
                msg_box.exec_()

    def find_same_img(self):
        print("find same img")
        if self.img is None:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '图片还没有选择!!')
            msg_box.exec_()
            return
        s = time.time()
        print("和 %s 近似的有：" % self.img)
        imagesift = select_img_sift_db(self.img)
        if imagesift:
            des1 = imagesift[2]
            img_md5 = imagesift[0]
        else:
            img_md5, _, des1, _, _ = sift_img_com(self.img)

        search_img_calss(img_md5, des1)
        e = time.time()
        print(e - s)
        s = time.time()
        print("-"*30)
        self.imgs_name.clear()
        self.Traverse_img_path()
        for path2 in self.imgs_name:
            math_sift_des(des1, path2)
        e = time.time()
        print(e - s)

    def show_sitf_img(self):
        # print("show sitf img")
        if self.img is None:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '未选择图像')
            msg_box.exec_()
            return
        if self.sift_img_list.get(self.img) is None:
            img1, get_sift = select_img_sift_kp(self.img)
            if get_sift != "":
                img = cv2.drawKeypoints(img1, pickle.loads(get_sift), None)
                cv2.imshow("sift image", img)
            else:
                msg_box = QMessageBox(QMessageBox.Warning, '提示', '图像未计算sift特征，无法显示特征图像！')
                msg_box.exec_()
        else:
            s = time.time()
            cv2.imshow("sift image", self.sift_img_list.get(self.img))
            e = time.time()
            print(e - s)

    def Start_sitf_com(self):
        print("Start sitf")
        # print(self.file_list)
        if select_path(self.file_list):
            w = QWidget()
            msg_box = QMessageBox.question(w, '提示', '该目录已计算过！！！是否重新计算！！！',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if msg_box == QMessageBox.Yes:
                self.imgs_name.clear()
            else:
                return
        else:
            self.imgs_name.clear()
        self.Traverse_img_path()
        print(len(self.imgs_name))
        s = time.time()
        self.multi_process_com_sift()
        e = time.time()
        print(e - s)
        msg_box = QMessageBox(QMessageBox.Information, '提示', '计算完成！！！')
        msg_box.exec_()
        # 把目录保存到数据库
        insert_path_select(self.file_list)

    def Traverse_img_path(self):
        start = time.time()
        for root, dirs, files in os.walk(self.file_list):
            for fn in files:
                fn_ = fn.split(".")
                if fn_[-1] in self.img_type:
                    path = root + "\\" + fn
                    self.imgs_name.append(path)
        end = time.time()
        print(len(self.imgs_name))
        print("完毕！！！！共耗时%s s" % (end - start))

    def save_sift_img(self):
        # print("save sift img")
        if self.sift_img is None:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '还没有计算图像的sitf图像')
            msg_box.exec_()
            return
        else:
            img_name_list = self.img.split("/")
            img_name = img_name_list[-1]
            img_name_list_d = img_name.split(".")
            img_name_sift = mathimage_path() + "\\" + img_name_list_d[0] + "_sift." + img_name_list_d[1]
            print(img_name_sift)
            aa = "." + img_name_list_d[1]
            cv2.imencode(aa, self.sift_img)[1].tofile(img_name_sift)
            msg_box = QMessageBox(QMessageBox.Information, '提示', '保存成功！')
            msg_box.exec_()

    def select_mulu_set(self):
        self.Traverse_img_path()

    def multi_process_com_sift(self):
        # 开启多进程
        cpu_count = multiprocessing.cpu_count()
        if cpu_count > 10:
            cpu_count = cpu_count - 3
        elif cpu_count > 4:
            cpu_count = cpu_count - 2
        else:
            cpu_count = 1
        average_len = len(self.imgs_name) // cpu_count
        print(cpu_count)
        print(average_len)
        # p1 = Process(target=com_separate, args=(0, average_len, self.imgs_name, "ssss"))
        for i in range(cpu_count):
            exec('list{0}=self.imgs_name[{1}:{2}]'.format(i, i * average_len, (i + 1) * average_len))
            exec('p{0} = Process(target=com_separate, args=({1},{2},list{3}))'.format(i + 1, i, average_len, i))
        for i in range(cpu_count):
            exec('p{0}.start()'.format(i + 1))
        print("-"*50)
        for i in range(cpu_count):
            exec('p{0}.join()'.format(i + 1))
        for path in self.imgs_name[cpu_count * average_len:]:
            sift_img_insert_db(path)
        print("-"*50)


def com_separate(i, average_len, imgs_name):
    # print("com separate")
    for ii in range(average_len):
        cc = imgs_name[ii]
        # print(cc)
        sift_img_insert_db(cc)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Operating_Ui()
    ui.config()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
