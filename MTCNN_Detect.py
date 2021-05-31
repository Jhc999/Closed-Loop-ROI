import cv2
import csv
import time
#from utils.mtcnn import TrtMtcnn
import numpy as np
import statistics

import pycuda.autoinit  # This is needed for initializing CUDA driver
from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO



file = open('Multi_Roi_Vals', 'w', newline = '')
with file:
    data = [["i", "left1", "top1", "right1", "bot1", "left2", "top2", "right2", "bot2"]]
    write = csv.writer(file)
    write.writerows(data)

#mtcnn = TrtMtcnn()
#minsize = 40

cls_dict = get_cls_dict(2)
h = w = 416
model = 'yolov4-416'
category_num = 2
letter_box = True 
conf_th = 0.5
trt_yolo = TrtYOLO(model, (h, w), category_num, letter_box)


for i in range (0, 350):
    print(i)
    img_bgr = cv2.imread('./ImuIms/'+str(i)+'.jpg')
    img = cv2.cvtColor(img_bgr, cv2.COLOR_RGB2BGR)
    #bbox, landmarks = mtcnn.detect(img, minsize=minsize)    
    
    box, confs, clss = trt_yolo.detect(img, conf_th)
    bbox = []
    if len(box) >= 2:
    #print(bbox,conf,clss) #clss 0 = face, clss 1 = person
        candidates = []
        for c in range (0, len(box)):
            if clss[c] == 0:
                candidates.append([box[c], confs[c]])
        results = sorted(candidates, key = lambda z: z[1], reverse = True)[:2]
        for res in range (0, len(results)):
            bbox.append(candidates[res][0])
                
                
    left1, top1, right1, bot1, left2, top2, right2, bot2 = -1, -1, -1, -1, -1, -1, -1, -1
    if len(bbox) == 1:
        left1, top1, right1, bot1 = bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3]
    if len(bbox) == 2:
        left2, top2, right2, bot2 = bbox[1][0], bbox[1][1], bbox[1][2], bbox[1][3]
    
    file = open('Multi_Roi_Vals', 'a', newline = '')
    with file:
        data = [[i, left1, top1, right1, bot1, left2, top2, right2, bot2]]
        write = csv.writer(file)
        write.writerows(data)
    
    for rr in range (0, len(bbox)):
        cv2.rectangle(img, (bbox[rr][0], bbox[rr][1]), (bbox[rr][2], bbox[rr][3]), (255,0,0), 2)
        cv2.imshow("", img)
        cv2.waitKey(1)


    
    

