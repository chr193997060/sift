import hashlib
import multiprocessing
import pickle
import time
from multiprocessing import Process

import cv2
import numpy as np

from db.sift_img_db import select_img_des, select_img_md5, select_img_des_kp
from mathimage.mathimage_dir import mathimage_path
from utilty.comsift import sift_img_match
from collections import Counter


def com_approximate_img(core, des, paths, kp, img):
    average_len_img = int(len(paths) / core)

    num = multiprocessing.Manager().list()
    print(num)

    for i in range(core):
        exec('list{0}=paths[{1}:{2}]'.format(i, i * average_len_img, (i + 1) * average_len_img))

    if average_len_img:
        remaining_path_len = len(paths[core * average_len_img:])

        remaining_path_groups = remaining_path_len // average_len_img

        for i in range(remaining_path_groups):
            exec('list{0}=paths[{1}:{2}]'.format(core + i, (core + i) * average_len_img,
                                                 (core + i + 1) * average_len_img))
        exec('list{0}=paths[{1}:]'.format(core + remaining_path_groups,
                                          (core + remaining_path_groups) * average_len_img))
        for i in range(core):
            exec('p{0} = Process(target=com_img_match_core, args=({1},list{2},num,kp,img))'.format(i, "des", i))
        for i in range(core):
            exec('p{0}.start()'.format(i))
        for i in range(core):
            exec('p{0}.join()'.format(i))

        for i in range(remaining_path_groups):
            exec('p{0} = Process(target=com_img_match_core, args=({1},list{2},num,kp,img))'.format(core + i, "des",
                                                                                                   (core + i)))
        for i in range(remaining_path_groups):
            exec('p{0}.start()'.format(core + i))
        for i in range(remaining_path_groups):
            exec('p{0}.join()'.format(core + i))

        exec('p{0} = Process(target=com_img_match_core, args=({1},list{2},num,kp,img))'.format(
            core + remaining_path_groups, "des", (core + remaining_path_groups)))
        exec('p{0}.start()'.format(core + remaining_path_groups))
        exec('p{0}.join()'.format(core + remaining_path_groups))
    else:
        print("*" * 30)
        com_img_match_core(des, paths, num)
    return list(num)


def com_img_match_core(des, paths, retu_list=[], kp1=[], img=[]):
    for path in paths:
        des_kp = select_img_des_kp(path[1])
        des2 = des_kp[0]
        kp2 = pickle.loads(des_kp[1])
        mark, good, len_match = sift_img_match(des, des2)
        if mark == 1:
            matchRatio = len(good) * 100 / len_match
            if matchRatio < 5. or matchRatio > 99.:
                continue
            s = time.time()
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            # findHomography 函数是计算变换矩阵
            # 参数cv2.RANSAC是使用RANSAC算法寻找一个最佳单应性矩阵H，即返回值M
            # 返回值：M 为变换矩阵，mask是掩模
            M, mask2 = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            # ravel方法将数据降维处理，最后并转换成列表格式
            matchesMask = mask2.ravel().tolist()
            e = time.time()
            print(e - s)
            # 获取img1的图像尺寸
            # h, w, dim = img.shape
            # pts是图像img1的四个顶点
            # pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            # 计算变换后的四个顶点坐标位置
            print("RANSAC 前的good数为：%s/n后的 good 数为 %s" % (len(good), Counter(matchesMask)))
            ccc = Counter(matchesMask)
            if ccc.get(1) < 15:
                continue
            # print(type(ccc.get(1)))
            matchRatio = ccc.get(1) * 100 / len_match
            print("-" * 30)
            if matchRatio < 2.:
                continue
            # try:
            #     dst = cv2.perspectiveTransform(pts, M)
            #     img2 = cv2.imdecode(np.fromfile(path[0], dtype=np.uint8), cv2.IMREAD_COLOR)
            #     # 根据四个顶点坐标位置在img2图像画出变换后的边框
            #     img2 = cv2.polylines(img2, [np.int32(dst)], True, (0, 0, 255), 3, cv2.LINE_AA)
            #     # cv2.imshow(path[0], img2)
            #     s = time.time()
            #     img_name_list = path[0].split("\\")
            #     img_name = img_name_list[-1]
            #     img_name_list_d = img_name.split(".")
            #     img_name_sift = mathimage_path() + "\\" + img_name_list_d[0] + "_sift." + img_name_list_d[1]
            #     cv2.imencode(".jpg", img2)[1].tofile(img_name_sift)
            #     e = time.time()
            #     print(e - s)
            #     draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
            #                        singlePointColor=None,
            #                        matchesMask=matchesMask,  # draw only inliers
            #                        flags=2)
            #
            #     img3 = cv2.drawMatches(img, kp1, img2, kp2, good, None, **draw_params)
            #     img_name_sift2 = mathimage_path() + "\\" + img_name_list_d[0] + "_sift2." + img_name_list_d[1]
            #     cv2.imencode(".jpg", img3)[1].tofile(img_name_sift2)
            # except:
            #     print("发生异常")
            #     print(path[0])

            retu_list.append((path[0], matchRatio))

            # print(" %s 近似" % path[0])


if __name__ == '__main__':
    arr = [i for i in range(44)]
    com_approximate_img(10, None, arr)
