import cv2
import time

import numpy as np
import statistics

from FaceDetection import Detector

face_detector = Detector(network_backbone = "mobile")
face_detector.loadToDevice("cuda")

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

RESULTS = []
for key in ResKey:
    TIME = []
    FPS = []
    resized = cv2.resize(img, (ResKey[key][0], ResKey[key][1]))
    
    for j in range (0,100):
        F1 = time.time()
        bbox = face_detector.forward(img)
        F2 = time.time()   
        TIME.append(F2-F1)
        FPS.append(1/(F2-F1))
        
    info = [key, np.average(FPS), statistics.stdev(FPS), np.average(TIME), statistics.stdev(TIME)]
    print(info)

    
    
    

