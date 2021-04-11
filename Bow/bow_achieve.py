import time
import joblib
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from db.sift_img_db import select_row_1000, select_row_md_and_des_1000, insert_img_tag, select_img_tag, update_img_tag, \
    select_img_path_md5, select_img_des
from utilty.comsift import sift_img_match
from Bow.bow_dir import *


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
        insert_img_tag(des[0], int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]))


def load_kmeand():
    plk_path = modepath + "\\" + 'test.pkl'
    try:
        model = joblib.load(plk_path)
        return model
    except IOError:
        print(plk_path)
        return ""


def com_class():
    s = time.time()
    model = load_kmeand()
    MdAndDes = select_row_md_and_des_1000()
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
    if select_img_tag:
        update_img_tag(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), md5)
    else:
        insert_img_tag(md5, int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]))
    return a


def search_img_calss(md5, des):
    model = load_kmeand()
    if model == "":
        return
    tags = com_img_class(md5, des, model, 30)
    paths = select_img_path_md5("tag1", tags[0])

    print("一类的为")
    print(paths)
    print("-"*30)
    for path in paths:
        des2 = select_img_des(path[1])[0]
        if sift_img_match(des, des2) == 1:
            print(" %s 近似" % path[0])



