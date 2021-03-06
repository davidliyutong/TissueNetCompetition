import glob
import cv2
import numpy as np
import json
import pandas as pd
import re
import time
from tqdm import tqdm

file_path_list = glob.glob("../data/annotations/jpg/*")
file_path_list.sort()


# pattern = re.compile(r'[^/]*\.jpeg')
metadata = pd.read_csv('../data/train_annotations_lbzOVuS.csv')

tif_name_list = []
annotation_id_list = []
annotation_class_list = []
for file_path in file_path_list:
    file_name = file_path.split('/')[-1]
    annotation_id = file_name.split('.')[0]

    entry = metadata[metadata['annotation_id'] == annotation_id]
    tif_name = entry['filename'].values[0]
    annotation_class = entry['annotation_class'].values[0]
    annotation_id_list.append(annotation_id)
    tif_name_list.append(tif_name)
    annotation_class_list.append(annotation_class)


file_name_df = pd.DataFrame({'annotation_id': annotation_id_list, 'filename': tif_name_list, 'file_path': file_path_list, 'annotation_class': annotation_class_list})

res_np = np.empty(shape=(len(annotation_id_list), 12))
for idx, (file_path, per) in enumerate(zip(file_path_list, tqdm(range(len(annotation_id_list))))):
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_avg, h_var = np.average(img[0]), np.var(img[0])
    h_max, h_min = np.max(img[0]), np.min(img[0])

    s_avg, s_var = np.average(img[1]), np.var(img[1])
    s_max, s_min = np.max(img[1]), np.min(img[1])

    v_avg, v_var = np.average(img[2]), np.var(img[2])
    v_max, v_min = np.max(img[2]), np.min(img[2])

    res_np[idx] = [h_avg, h_var, h_max, h_min, s_avg, s_var, s_max, s_min, v_avg, v_var, v_max, v_min]

res_df = pd.DataFrame(res_np, columns=["h_avg", "h_var", "h_max", "h_min", "s_avg", "s_var", "s_max", "s_min", "v_avg", "v_var", "v_max", "v_min"])

res = pd.concat([file_name_df, res_df], axis=1)
res.to_csv("statistic_annotations_{}.csv".format(len(file_path_list)))
print("Statistic saved")