import os
import sys

file_path = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # 根路径
sys.path.append(file_path)

from db.sift_img_db import *


def start():
    create_table_sift()  # 创建图像sift表
    creation_img_tag()  # 创建图像分类表
    create_table_path()  # 创建计算过目录表
    create_img_path_md5()  # 创建md5和路径表
