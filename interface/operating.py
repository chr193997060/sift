import os
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
from PyQt5.QtCore import Qt, QSize
import matplotlib.pyplot as plt
import time
file_path = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # 根路径
sys.path.append(file_path)
from PyQt5.QtWidgets import QDesktopWidget, QGraphicsPixmapItem, QGraphicsScene, QPushButton, QWidget, QHBoxLayout, \
    QMessageBox


class Operating_Ui(object):

    def config(self):
        self.img = None
        self.sift_img = None
        self.sift_img_list = {}
        self.file_list = file_path
        self.img_type = ["bmp", "jpg", "png", "webp", "PNG"]
        self.img_des_list = {}
        self.sift_img_des = None
        self.sift_img_kp = None
        self.sift_img_1 = None

    def setupUi(self, Form):
        # 获取屏幕坐标系

        self.Form = Form

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

    def com_sitf(self):
        print("com sitf")
        if self.img == None:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '图片还没有选择!!')
            msg_box.exec_()
            return
        else:
            print(self.img)
            img = cv2.imdecode(np.fromfile(self.img, dtype=np.uint8), cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图

            # cv2.imshow("box", img)
            # cv2.imshow("gray", gray)

            # 创建SIFT特征检测器
            sift = cv2.SIFT_create()

            # 特征点提取与描述子生成
            kp1, des1 = sift.detectAndCompute(gray, None)
            # print(des1)
            # 把特征点加载到图像上
            self.sift_img = cv2.drawKeypoints(img, kp1, self.sift_img)

            self.sift_img_des = des1
            self.sift_img_kp = kp1
            self.sift_img_1 = img

            self.sift_img_list[self.img] = self.sift_img

            # cv2.imshow("img", img)
            # cv2.imshow("sssss", self.sift_img)
            if self.sift_img is None:
                msg_box = QMessageBox(QMessageBox.Warning, '提示', '计算图像的sitf特征失败')
                msg_box.exec_()
            else:
                msg_box = QMessageBox(QMessageBox.Information, '提示', '计算图像的sitf特征成功')
                msg_box.exec_()

    def find_same_img(self):
        print("find same img")
        self.find_sitf_img()

    def show_sitf_img(self):
        print("show sitf img")
        if self.sift_img_list.get(self.img) is None:
            print("rrrrrr")
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '图像未计算sift特征，无法显示特征图像！')
            msg_box.exec_()
        else:
            print("aaaaa")
            cv2.imshow("sift image", self.sift_img_list.get(self.img))
        # if self.sift_img is None:
        #     msg_box = QMessageBox(QMessageBox.Warning, '提示', '图像未计算sift特征，无法显示特征图像！')
        #     msg_box.exec_()
        # else:
        #     cv2.imshow("sift image", self.sift_img)

    def Start_sitf_com(self):
        print("Start sitf")
        print(self.file_list)
        start = time.time()
        for root, dirs, files in os.walk(self.file_list):
            for fn in files:
                # print(root, fn)
                # print(root + fn)
                fn_ = fn.split(".")
                if fn_[-1] in self.img_type:
                    # print(root + )
                    path = root + "/" + fn
                    self.sift_imglist_com(path)
        end = time.time()
        print("完毕！！！！共耗时%s s" % (end-start))

    def find_sitf_img(self):
        if self.sift_img_1 is None or self.sift_img_kp is None or self.sift_img_des is None or self.img_des_list == {}:
            print("dddddd")
            return
        else:
            print("aaa")
            # print(self.sift_img_1, self.sift_img_kp, self.sift_img_des, self.img_des_list)
            for i in self.img_des_list:
                self.match_sift(self.sift_img_des, self.img_des_list.get(i).get("des"),
                                self.sift_img_1, self.img_des_list.get(i).get("img"),
                                self.sift_img_kp, self.img_des_list.get(i).get("kp"))

    def sift_imglist_com(self, img_path):

        # img_path = img_path.replace("\\", "/")
        print(img_path)

        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)

        # cv2.imshow(img_path, img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图
        # 创建SIFT特征检测器
        sift = cv2.SIFT_create()
        # 特征点提取与描述子生成
        kp1, des1 = sift.detectAndCompute(gray, None)
        # 把特征点加载到图像上
        # sift_img = cv2.drawKeypoints(img, kp1, None)
        # cv2.imshow(img_path, sift_img)
        a = {
            "des": des1,
            "img": img,
            "kp": kp1
        }
        self.img_des_list[img_path] = a

    def save_sift_img(self):
        print("save sift img")
        if self.sift_img is None:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '还没有计算图像的sitf图像')
            msg_box.exec_()
            return
        else:
            img_name_list = self.img.split("/")
            img_name = img_name_list[-1]
            img_name_list_d = img_name.split(".")
            img_name_sift = file_path + "\\SaveImg\\" + img_name_list_d[0] + "_sift." + img_name_list_d[1]
            print(img_name_sift)
            aa = "." + img_name_list_d[1]
            # img_name_sift = img_name_sift.replace('\\', '/')
            # print(img_name_sift)
            cv2.imencode(aa, self.sift_img)[1].tofile(img_name_sift)
            msg_box = QMessageBox(QMessageBox.Information, '提示', '保存成功！')
            msg_box.exec_()

    def match_sift(self, des1, des2, img1, img2, kp1, kp2):
        print("match_sift")
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        matchesMask = [[0, 0] for i in range(len(matches))]

        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                matchesMask[i] = [1, 0]

        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=(255, 0, 0),
                           matchesMask=matchesMask,
                           flags=cv2.DrawMatchesFlags_DEFAULT)

        img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
        cv2.imshow(str(time.time()), img3)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Operating_Ui()
    ui.config()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
