from multiprocessing.sharedctypes import Array
from multiprocessing import Process, Lock

def add_one(lock, arr):
    lock.acquire()
    for i in range(len(arr)):
        arr[i] += 1
    lock.release()
    print(arr[:])

if __name__ == '__main__':
    lock = Lock()
    arr = Array('i', range(10))
    print(arr[:])
    p1 = Process(target=add_one, args=(lock, arr))
    p2 = Process(target=add_one, args=(lock, arr))
    p1.start()
    p2.start()
