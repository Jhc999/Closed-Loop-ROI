import cv2
import time
from utils.mtcnn import TrtMtcnn
import numpy as np
import statistics


def show_faces(img, boxes, landmarks):
    BBOX_COLOR = (0, 255, 0)
    for bb, ll in zip(boxes, landmarks):
        x1, y1, x2, y2 = int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])
        cv2.rectangle(img, (x1, y1), (x2, y2), BBOX_COLOR, 2)
        for j in range(0,5):
            cv2.circle(img, (int(ll[j]), int(ll[j+5])), 2, BBOX_COLOR, 2)
    return img

def randImg(w,h):
    np.random.seed(2)
    return np.random.randint(255, size=(w,h,3),dtype=np.uint8)

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
mtcnn = TrtMtcnn()
minsize = 40

#FIRST 100 DETECTIONS ARE SLOWER, SKIP
temp = cv2.resize(img, (160, 120))
for i in range (0,100):
    F1 = time.time()
    dets, landmarks = mtcnn.detect(temp, minsize=minsize)
    F2 = time.time()

RESULTS = []
for key in ResKey:
    TIME = []
    FPS = []
    resized = cv2.resize(img, (ResKey[key][0], ResKey[key][1]))
    #resized = randImg(ResKey[key][0], ResKey[key][1])

    for j in range (0,100):
        F1 = time.time()
        dets, landmarks = mtcnn.detect(resized, minsize=minsize)
        F2 = time.time()   
        TIME.append(F2-F1)
        FPS.append(1/(F2-F1))
        
    info = [key, np.average(FPS), statistics.stdev(FPS), np.average(TIME), statistics.stdev(TIME)]
    print(info)

    
    
    

