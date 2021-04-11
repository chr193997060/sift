import os
import sqlite3
import sys
import time
import numpy as np
import io
import cv2
import hashlib
from db.db_dir import *

# file_path = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # 根路径
# sys.path.append(file_path)

db_path = db_path()
db_path = '{0}\\sift_img.db'.format(db_path)
con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)


def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)


def create_table_sift():
    # 创建表
    # 创建保存img的sift描述符和img  numpy数据及img的md5的数据库,如果存在就不创建
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS img_sift(
                img_md5 varchar(100)  PRIMARY KEY,
                image array,
                des array,
                kp mediumblob
            );
        """)


def creation_img_tag():
    # 建立图像分类标签表
    con.execute("""
                CREATE TABLE IF NOT EXISTS img_tag(
                    img_md5 varchar(100)  PRIMARY KEY,
                    tag1 Integer,
                    tag2 Integer,
                    tag3 Integer,
                    tag4 Integer,
                    tag5 Integer
                );
            """)


def create_table_path():
    # 创建表
    # 创建保存img的sift描述符和img  numpy数据及img的md5的数据库,如果存在就不创建
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS com_dir_path(
                path varchar(100)  PRIMARY KEY
            );
        """)


def create_img_path_md5():
    # 创建表
    # 创建保存img的md5描述符和路径
    with con:
        con.execute("""
                CREATE TABLE IF NOT EXISTS img_path_md5(
                    path_md5 varchar(100) PRIMARY KEY,
                    path varchar(100),
                    img_md5 varchar(100)
                );
            """)


# 插入数据
def insert_img_sift(img_md5, img=None, des=None, kp=None):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("insert into img_sift (img_md5,image,des,kp) values (?,?,?,?)", (img_md5, img, des, kp))
    con.commit()
    # print("插入成功！！！！")


def select_img_sift(img_md5):
    # print("select img sift")
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("select * from img_sift where img_md5=?", (img_md5,))
    data = cur.fetchall()
    return data


def select_img_des(img_md5):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("select des from img_sift where img_md5=?", (img_md5,))
    data = cur.fetchall()
    return data[0]


# select_img_des("bde65b507ba7d3263e1ab36d58c6e74d")

def select_img_kp(img_md5, select_name):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("select kp from img_sift where img_md5=?", (img_md5,))
    # cur.execute("select * from img_sift where img_md5=?", (img_md5,))
    data = cur.fetchall()
    return data


def _pickle_keypoint(keypoint):  # : cv2.KeyPoint
    return cv2.KeyPoint, (
        keypoint.pt[0],
        keypoint.pt[1],
        keypoint.size,
        keypoint.angle,
        keypoint.response,
        keypoint.octave,
        keypoint.class_id,
    )


def insert_path(path):
    # print("insert path")
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("insert into com_dir_path (path) values (?)", (path,))
    con.commit()
    # print("插入成功！！！！")


def select_path(path):
    # print("select path")
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("select * from com_dir_path where path=?", (path,))
    data = cur.fetchall()
    return data


def insert_path_select(path):
    # print("insert path select")
    if select_path(path):
        # print("已存在！！！")
        pass
    else:
        insert_path(path)


def select_row_1000():
    s = time.time()
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("select des from img_sift limit 1000")
    data = cur.fetchall()
    e = time.time()
    # print(data)
    # print(type(data))
    # print(len(data))
    print("select_row_1000", e - s)
    return data


def select_row_md_and_des_1000():
    s = time.time()
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("select img_md5,des from img_sift limit 1000")
    data = cur.fetchall()
    e = time.time()
    # print(data)
    # print(data[0])
    print(len(data))
    print("select_row_md_and_des_1000 time:%s s" % (e - s))
    return data


# select_row_md_and_des_1000()

# select_row_1000()


def set_null(md5):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.execute("VACUUM")


# set_null("ss")


def select_row_1000_2():
    s = time.time()
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    # cur.execute("select kp from img_sift where kp=null")
    cur.execute("select * from img_sift limit 100")
    data = cur.fetchall()
    e = time.time()
    print(data)
    print(type(data))
    print(len(data))
    print(e - s)
    # s = time.time()
    # for i in data:
    #     # print(i[0])
    #     set_null(i[0])
    # e = time.time()
    # print(e - s)


# select_row_1000_2()

def insert_img_tag(md5, tag1, tag2=None, tag3=None, tag4=None, tag5=None):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    # cur = con.cursor()
    con.execute("insert into img_tag (img_md5,tag1,tag2,tag3,tag4,tag5) values (?,?,?,?,?,?)",
                (md5, tag1, tag2, tag3, tag4, tag5))
    con.commit()


def select_img_tag(md5):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("select * from img_tag where img_md5=?", (md5,))
    data = cur.fetchall()
    return data


def update_img_tag(md5, tag1, tag2, tag3, tag4, tag5):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("update img_tag set tag1=?,tag2=?,tag3=?,tag4=?,tag5=? where img_md5=?",
                (tag1, tag2, tag3, tag4, tag5, md5))
    con.commit()


def select_img_path(path_md5):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("select * from img_path_md5 where path_md5=?",
                (path_md5,))
    data = cur.fetchall()
    return data



def insert_img_path_md5(path_md5, path, md5):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    # cur = con.cursor()
    con.execute("insert into img_path_md5 (path_md5,path,img_md5) values (?,?,?)",
                (path_md5, path, md5))
    con.commit()


def if_insert_update_img_path(path_md5, path, md5):
    a = select_img_path(path_md5)
    if a:
        pass
    else:
        insert_img_path_md5(path_md5, path, md5)



def select_img_path_md5(tag_index, tag):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    sql = """
            SELECT path,img_md5
            FROM img_path_md5 
            WHERE img_md5 IN 
            (SELECT img_md5 FROM img_tag WHERE {0}={1})
            ORDER BY path
        """.format(tag_index, tag)
    cur.execute(sql)
    date = cur.fetchall()
    return date

# select_img_path_md5('tag1', 16)

# select_img_tag("ss")
