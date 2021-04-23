# -*- coding: utf-8 -*-
'''
Created on 2019年3月6日

@author: Administrator
'''
import sqlite3
import numpy as np
import io

def adapt_array(arr):

    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

# 创建数据库连接对象
conn = sqlite3.connect('sample_database.db', detect_types=sqlite3.PARSE_DECLTYPES)  # 连接到SQLite数据库
'''
sqlite3.PARSE_DECLTYPES
本常量使用在函数connect()里，设置在关键字参数detect_types上面。表示在返回一行值时，是否分析这列值的数据类型定义。如果设置了本参数，就进行分析数据表列的类型，并返回此类型的对象，并不是返回字符串的形式。

sqlite3.PARSE_COLNAMES 
本常量使用在函数connect()里，设置在关键字参数detect_types上面。表示在返回一行值时，是否分析这列值的名称。如果设置了本参数，就进行分析数据表列的名称，并返回此类型的名称
'''
# 参数:memory:来创建一个内存数据库
# conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)

# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)

x = np.arange(12).reshape(2, 6)

# conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()
# 创建数据库表
cursor.execute("create table test (arr array)")
# 插入一行数据
cursor.execute("insert into test (arr) values (?)", (x,))
# 提交
conn.commit()

cursor.execute("select arr from test")
data = cursor.fetchone()[0]

print(data)
'''
[[ 0  1  2  3  4  5]
 [ 6  7  8  9 10 11]]
'''
print(type(data))
'''
<class 'numpy.ndarray'>
'''
cursor.close()  # 关闭Cursor
conn.close()  # 关闭数据库

