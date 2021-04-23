import multiprocessing
import struct


def func(mydict, mylist):
    mydict["index1"] = "aaaaaa"  # 子进程改变dict,主进程跟着改变
    mydict["index2"] = "bbbbbb"
    mylist.append(11)  # 子进程改变List,主进程跟着改变
    mylist.append(22)
    mylist.append(33)
    print(struct.calcsize("P"))
    print(mylist)


if __name__ == "__main__":
    with multiprocessing.Manager() as MG:  # 重命名
        mydict = multiprocessing.Manager().dict()  # 主进程与子进程共享这个字典
        mylist = multiprocessing.Manager().list([1])  # 主进程与子进程共享这个List

        p = multiprocessing.Process(target=func, args=(mydict, mylist))
        p2 = multiprocessing.Process(target=func, args=(mydict, [6, 1]))
        p.start()
        p2.start()
        p.join()
        p2.join()

        print(mylist)
        print(mydict)
