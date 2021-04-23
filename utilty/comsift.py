import copyreg
import hashlib
import pickle
import cv2
import time
import numpy as np
from db.sift_img_db import insert_img_sift, select_img_sift, _pickle_keypoint, select_img_kp, insert_img_path_md5, \
    if_insert_update_img_path
from mathimage.mathimage_dir import *

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
copyreg.pickle(cv2.KeyPoint().__class__, _pickle_keypoint)


def get_good_match(des1, des2):
    # print("get good match where comsift")

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # matchesMask = [[0, 0] for i in range(len(matches))]
    good = []
    # good_len = 0
    # matchRatio = 0
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
            # good_len += 1
    # matchRatio = len(good) * 100 / len(matches)
    return good, len(matches)


def sift_img_match(des1, des2, img1=None, kp1=None, img2=None, kp2=None):
    goodMatch, len_match = get_good_match(des1, des2)
    if len(goodMatch) > 15:
        return 1, goodMatch, len_match
    else:
        return 0, "", ""


# def math_sift(path1, path2, des1=None):
#     # 传进路径计算
#     if des1 is None:
#         # print("图像未计算")
#         sift1 = select_img_sift_db(path1)
#         if sift1:
#             img1 = sift1[1]
#             des1 = sift1[2]
#             kp1 = pickle.loads(sift1[3])
#         else:
#             _, _, des1, kp1, img1, img = sift_img_com(path1)
#     sift2 = select_img_sift_db(path2)
#     if sift2:
#         img2 = sift2[1]
#         des2 = sift2[2]
#         kp2 = pickle.loads(sift2[3])
#         if sift_img_match(des1, des2, img1, kp1, img2, kp2) == 1:
#             print("%s 和 %s 近似" % (path1, path2))
#     else:
#         print("%s 没有计算sift" % path2)


def save_sift_math_img(saveimg):
    name = hashlib.md5(saveimg).hexdigest()
    img_path = mathimage_path() + name + ".jpg"
    print(img_path)
    cv2.imencode(".jpg", saveimg)[1].tofile(img_path)


# def math_sift_des(des1, path2):
#     sift2 = select_img_sift_db(path2)
#     if sift2:
#         des2 = sift2[2]
#     else:
#         _, _, des2, _, _ = sift_img_com(path2)
#     mark, good, matchRatio = sift_img_match(des1, des2)
#     if mark == 1:
#         print(" %s 近似" % path2)


def show_match_sift(des1, des2, img1, img2, kp1, kp2):
    # print("show match sift for comsift")

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


def com_sift_des_kp(image_path=None, image=None):
    # print("com sift des kp for comsift")
    if image_path is None:
        pass
    else:
        img = cv2.imdecode(np.fromfile(image, dtype=np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图
        sift = cv2.SIFT_create()
        kp, des = sift.detectAndCompute(gray, None)
        kp_image = cv2.drawKeypoints(gray, kp, None)
        return kp_image, kp, des

    if image is None:
        pass
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰度图
        sift = cv2.SIFT_create()
        kp, des = sift.detectAndCompute(gray, None)
        kp_image = cv2.drawKeypoints(gray, kp, None)
        return kp_image, kp, des


# def sift_image_alignment(img1, img2):
#     # print("sift image alignment for comsift")
#     # 对准
#     _, kp1, des1 = com_sift_des_kp(image_path=img1)
#     _, kp2, des2 = com_sift_des_kp(image_path=img2)
#     goodmatch, len_match = get_good_match(des1, des2)
#     H = None
#     imgOut = None
#     status = None
#     if len(goodmatch) > 4:
#         ptsA = np.float32([kp1[m.queryIdx].pt for m in goodmatch]).reshape(-1, 1, 2)
#         ptsB = np.float32([kp2[m.trainIdx].pt for m in goodmatch]).reshape(-1, 1, 2)
#         ransacReprojThreshold = 4
#         H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, ransacReprojThreshold);
#         imgOut = cv2.warpPerspective(img2, H, (img1.shape[1], img1.shape[0]),
#                                      flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
#     return imgOut, H, status


def sift_img_insert_db(img_path):
    # print("sift img insert db")
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    img_md5 = hashlib.md5(img).hexdigest()
    img_path_md5 = hashlib.md5(img_path.encode('utf-8')).hexdigest()
    if_insert_update_img_path(img_path_md5, img_path, img_md5)
    if select_img_sift(img_md5):
        pass
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图
        # 创建SIFT特征检测器
        sift = cv2.SIFT_create()
        # 特征点提取与描述子生成
        kp, des = sift.detectAndCompute(gray, None)
        kp_pickle = pickle.dumps(kp)
        # 插入数据到数据库中
        insert_img_sift(img_md5, des=des, kp=kp_pickle)


def select_img_sift_db(img_path):
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    img_md5 = hashlib.md5(img).hexdigest()
    get_sift = select_img_sift(img_md5)
    if get_sift:
        return get_sift[0]
    return ""


def select_img_sift_kp(img_path):
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    img_md5 = hashlib.md5(img).hexdigest()
    get_kp = select_img_kp(img_md5, "kp")[0][0]
    if get_kp:
        return img, get_kp
    return "", ""


def sift_img_com(img_path):
    # 计算特征存入数据库，并返回
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    img_md5 = hashlib.md5(img).hexdigest()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图
    # 创建SIFT特征检测器
    sift = cv2.SIFT_create()
    # 特征点提取与描述子生成
    kp, des = sift.detectAndCompute(gray, None)
    sift_img = cv2.drawKeypoints(img, kp, None)  # 包含特征点图
    if select_img_sift(img_md5):
        pass
    else:
        kp_pickle = pickle.dumps(kp)
        # 插入数据到数据库中
        insert_img_sift(img_md5, des=des, kp=kp_pickle)
    return img_md5, sift_img, des, kp, sift_img, img


def sift_img_insert_db_(img, des, kp=None, img_md5=None):
    # print("sift img insett db - ")
    img_md5 = hashlib.md5(img).hexdigest()
    if select_img_sift(img_md5):
        # print("已存在于数据库中")
        pass
    else:
        insert_img_sift(img_md5, des=des)


def sift_img_insert_db_5(img, des, img_md5, kp=None):
    # print("sift img insett db - 5")
    if select_img_sift(img_md5):
        pass
    else:
        insert_img_sift(img_md5, des=des)


def show_match_sift_img(des1, des2, img1, img2, kp1, kp2):
    # print("show match sift img for comsift")
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
