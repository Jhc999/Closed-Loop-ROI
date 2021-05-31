import time
import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver
from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
import numpy as np
import statistics

ResKey = {}
ResKey["QQQVGA"]= [80,60]
ResKey["QQVGA"] = [160,120]
ResKey["HQVGA"] = [240,160]
ResKey["QVGA"]  = [320,240]
ResKey["VGA"]   = [640,480]
ResKey["SVGA"]  = [800,600]

ResKey["XGA"]   = [1024,768]
ResKey["SXGA"]  = [1280,1024]
ResKey["UXGA"]  = [1600,1200]
ResKey["QXGA"]  = [2048,1536]
ResKey["WQXGA"] = [2560,1600]
ResKey["WQXGA2"]= [2592,1944]

ResKey["HD"]    = [1280,720 ]
ResKey["FHD"]   = [1920,1080]
ResKey["QHD"]   = [2560,1440]

img = cv2.imread("sample.jpg")

cls_dict = get_cls_dict(2)
h = w = 416
model = 'yolov4-416'
category_num = 2
letter_box = True 
conf_th = 0.5
trt_yolo = TrtYOLO(model, (h, w), category_num, letter_box)

#FIRST 100 DETECTIONS ARE SLOWER, SKIP
for i in range (0,100):
    F1 = time.time()
    boxes, confs, clss = trt_yolo.detect(img, conf_th)
    F2 = time.time()
    #print("FPS: ", 1/(F2-F1))

RESULTS = []
for key in ResKey:
    TIME = []
    FPS = []
    resized = cv2.resize(img, (ResKey[key][0], ResKey[key][1]))
    
    for j in range (0,100):
        F1 = time.time()
        boxes, confs, clss = trt_yolo.detect(img, conf_th)
        F2 = time.time()   
        TIME.append(F2-F1)
        FPS.append(1/(F2-F1))
        
    info = [key, np.average(FPS), statistics.stdev(FPS), np.average(TIME), statistics.stdev(TIME)]
    print(info)



