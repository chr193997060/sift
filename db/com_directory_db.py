import os
import sqlite3
import sys
import numpy as np
import io
import cv2

file_path = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # 根路径
sys.path.append(file_path)

db_path = '{0}\\db\\sift_img.db'.format(file_path)

print(db_path)

con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)



# create_table_path()





