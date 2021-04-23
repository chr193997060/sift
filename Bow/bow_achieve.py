import time

import cv2
import joblib
import numpy as np
from PyQt5 import QtWidgets
from sklearn.cluster import MiniBatchKMeans
import pickle

from approximateShow.approximate_windows import start_widow_approximate, ApproximateWindow
from db.sift_img_db import select_row_1000, select_row_md_and_des_1000, insert_img_tag, select_img_tag, update_img_tag, \
    select_img_path_md5, select_img_des, select_row_md_and_des_all, select_img_des_kp
from mathimage.mathimage_dir import mathimage_path
from multiProgress.progress import com_approximate_img
from utilty.comsift import sift_img_match
from Bow.bow_dir import *
from collections import Counter

modepath = bow_path()


def clusterize(sift_keypoints, num_cluster):
    sift_keypoints = np.asarray(sift_keypoints)
    sift_keypoints = np.concatenate(sift_keypoints, axis=0)
    print(sift_keypoints)
    print("Training kmeans")
    s = time.time()
    kmeans = MiniBatchKMeans(n_clusters=num_cluster, random_state=0).fit(sift_keypoints)
    e = time.time()
    print("clusterize", e - s)
    # visual_words = kmeans.cluster_centers_
    # print(kmeans)
    return kmeans


def sift_features_asarray_mad(MdAndDes):
    sift_keypoints = []
    for i in MdAndDes:
        sift_keypoints.append(i[1])
    return sift_keypoints


def calculate_centroids_histogram_mad_and_insert(model, MdAndDes, num_cluster):
    # feature_vectors = []
    for des in MdAndDes:
        predict_kmeans = model.predict(des[1])
        hist, bin_edges = np.histogram(predict_kmeans, num_cluster)
        # feature_vectors.append(hist)
        hist2 = np.asarray(hist)
        a = hist2.argsort()[-5:][::-1]
        if select_img_tag(des[0]):
            update_img_tag(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), des[0])
        else:
            insert_img_tag(des[0], int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]))


def calculate_centroids_histogram_mad_and_insert_all(model, MdAndDes, num_cluster):
    for des in MdAndDes:
        predict_kmeans = model.predict(des[1])
        hist, bin_edges = np.histogram(predict_kmeans, num_cluster)
        hist2 = np.asarray(hist)
        a = hist2.argsort()[-5:][::-1]
        insert_img_tag(des[0], int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]))


def com_db_img_class():
    MdAndDes = select_row_md_and_des_all()
    s = time.time()
    model = load_kmeand()
    if model == "":
        sift_keypoints = sift_features_asarray_mad(MdAndDes)
        model = clusterize(sift_keypoints, 30)
        joblib.dump(model, modepath + "\\" + 'test.pkl')
    e = time.time()
    print(e - s)
    s = time.time()
    calculate_centroids_histogram_mad_and_insert(model, MdAndDes, 30)
    e = time.time()
    print(e - s)


def load_kmeand():
    plk_path = modepath + "\\" + 'test.pkl'
    try:
        model = joblib.load(plk_path)
        return model
    except IOError:
        print(plk_path)
        return ""


def com_class():
    MdAndDes = select_row_md_and_des_1000()
    s = time.time()
    model = load_kmeand()
    if model == "":
        sift_keypoints = sift_features_asarray_mad(MdAndDes)
        model = clusterize(sift_keypoints, 30)
        joblib.dump(model, modepath + "\\" + 'test.pkl')
    e = time.time()
    print(e - s)
    s = time.time()
    calculate_centroids_histogram_mad_and_insert(model, MdAndDes, 30)
    e = time.time()
    print(e - s)


# com_class()


def com_img_class(md5, des, model, num_cluster):
    predict_kmeans = model.predict(des)
    hist, bin_edges = np.histogram(predict_kmeans, num_cluster)
    hist2 = np.asarray(hist)
    a = hist2.argsort()[-5:][::-1]
    if select_img_tag(md5):
        update_img_tag(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), md5)
    else:
        insert_img_tag(md5, int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]))
    return a


def search_img_calss(md5, des, kp1, img):
    model = load_kmeand()
    if model == "":
        return
    tags = com_img_class(md5, des, model, 30)

    # paths = select_img_path_md5("tag1", tags[0])

    # print(paths)
    paths = []
    for i in range(1, 6):
        for j in range(5):
            paths.extend(select_img_path_md5("tag{0}".format(i), tags[j]))
        # paths.extend(select_img_path_md5("tag{0}".format(i), tags[1]))
        # paths.extend(select_img_path_md5("tag{0}".format(i), tags[2]))
        # paths.extend(select_img_path_md5("tag{0}".format(i), tags[3]))
        # paths.extend(select_img_path_md5("tag{0}".format(i), tags[4]))

    paths = list(set(paths))
    print(len(paths))
    if len(paths) > 40:
        return com_approximate_img(4, des, paths, kp1, img)
    else:
        approximate_path = []
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
                e = time.time()
                print(e - s)
                # ravel方法将数据降维处理，最后并转换成列表格式
                matchesMask = mask2.ravel().tolist()
                # 获取img1的图像尺寸
                # h, w, dim = img.shape
                # pts是图像img1的四个顶点
                # pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                # 计算变换后的四个顶点坐标位置
                print("RANSAC 前的good数为：%s/n后的 good 数为 %s" % (len(good), Counter(matchesMask)))
                ccc = Counter(matchesMask)
                if ccc.get(1) < 15:
                    continue
                matchRatio = int(ccc.get(1)) * 100 / len_match
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
                #     img3 = cv2.drawMatches(img, kp1, img2, kp2, good, None, **draw_params)
                #     img_name_sift2 = mathimage_path() + "\\" + img_name_list_d[0] + "_sift2." + img_name_list_d[1]
                #     cv2.imencode(".jpg", img3)[1].tofile(img_name_sift2)
                # except:
                #     print("发生异常")
                #     print(path[0])
                approximate_path.append((path[0], matchRatio))

        return approximate_path
