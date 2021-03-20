# if __name__ == "__main__":
#     while True:
#         pass

#
# import _thread
# import time
#
#
# # 为线程定义一个函数
# def print_time(threadName, delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print("%s: %s" % (threadName, time.ctime(time.time())))
#
#
# # 创建两个线程
# try:
#     _thread.start_new_thread(print_time, ("Thread-1", 2,))
#     _thread.start_new_thread(print_time, ("Thread-2", 4,))
# except:
#     print("Error: 无法启动线程")
#
# while 1:
#     pass

#coding=utf-8
from multiprocessing import Pool
from threading import Thread

from multiprocessing import Process


def loop():
    while True:
        pass

if __name__ == '__main__':

    for i in range(9):
        t = Process(target=loop)
        t.start()

    while True:
        pass

