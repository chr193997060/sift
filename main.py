import os
import sys
file_path = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # 根路径
sys.path.append(file_path)
print(file_path)
from main_dir import *
sys.path.append(app_path())
from interface.MainWidow import start_widow

if __name__ == '__main__':
    start_widow()