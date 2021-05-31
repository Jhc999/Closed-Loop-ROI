import socket, os, io, sys
import PIL
import PIL.Image as Image
import time
import numpy as np
import imutils
import threading, queue
import cv2
import statistics

import os
import signal
from subprocess import Popen, PIPE

#from __future__ import print_function
from config import *
from imutils import face_utils
import pdb
import csv
from FaceDetection import Detector
from imutils import face_utils

import pycuda.autoinit  # This is needed for initializing CUDA driver
from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
from utils.mtcnn import TrtMtcnn

from simple_pid import PID

#from utils.ssd_classes import get_cls_dict
#from utils.ssd import TrtSSD

#########################################################################
# PARAMETERS

HOST = '192.168.1.69'  # Standard loopback interface address (localhost)
PORT = 5000
NUM_IMAGES = 500
detector = "mtcnn"

#detector = "mobile"
#detector = "yolo"
#detector = "ssd"

#########################################################################
def PCread(str_in):     #READ CONFIG MESSAGE SENT BY OPENMV
    len1 = ''
    len2 = ''
    commaNum = 0
    for i in range (0, len(str_in)):
        if str_in[i] == ',':
            commaNum += 1
        else:
            if commaNum == 0:
                len1 += (str_in[i])
            if commaNum == 1:
                len2 += (str_in[i])
            if commaNum == 2:
                break
    #print("PCREADpart1", str_in)
    #print("PCREADpart2", len1, len2)
    return int(len1), int(len2)

def decodeRGB(bcolor, height, width):
    #print(bcolor[0:20])
    #print(bcolor[len(bcolor)-20:len(bcolor)])
    flag1 = time.time()
    MASK5 = 0b011111
    MASK6 = 0b111111
    im = np.empty([height,width], dtype=np.uint16)

    i = 0
    #flag2 = time.time()
    for y in range (0, height):
        for x in range (0, width):
            im[y,x] = int.from_bytes(bcolor[i+1:i+2]+bcolor[i:i+1], "little")
            i += 2
    #flag3 = time.time()
    b = (im & MASK5) << 3
    g = ((im >> 5) & MASK6) << 2
    r = ((im >> (5 + 6)) & MASK5) << 3
    bgr = np.dstack((b,g,r)).astype(np.uint8)
    flag4 = time.time()
    return bgr

#########################################################################

imgQ = queue.Queue()
paramsQ = queue.Queue()

#########################################################################

def main(PORT1, detector, resize, NUM_IMAGES, xP, xI, xD, yP, yI, yD):
    pidX = PID()
    pidX.sample_time = 0.1
    pidX.setpoint = 0
    pidX.tunings = (xP, xI, xD)
    
    pidY = PID()
    pidY.sample_time = 0.01
    pidY.setpoint = 0
    pidY.tunings = (yP, yI, yD)
    #current_value = 0
    #output = pid(current_value)
    XX = 90
    YY = 170
    errX = 0
    errY = 0

    
    FPS = []
    LocationX = []
    LocationY = []

    if detector == "mobile":
        face_detector = Detector(network_backbone = "mobile")
        face_detector.loadToDevice("cuda")

    if detector == "yolo":
        cls_dict = get_cls_dict(2)
        h = w = 416
        model = 'yolov4-416'
        category_num = 2
        letter_box = True 
        conf_th = 0.5
        trt_yolo = TrtYOLO(model, (h, w), category_num, letter_box)

    if detector == "mtcnn":
        mtcnn = TrtMtcnn()

    if detector == "ssd":
        model = 'ssd_mobilenet_v2_egohands'
        INPUT_HW = (300, 300)
        trt_ssd = TrtSSD(model, INPUT_HW)
        conf_th = 0.3

    print("READY")
    PORT2 = PORT1+1
    width = 2592
    height = 1944
    #CROPw = 200
    CROPw = 400
    CROPh = 150
    offx = 0
    offy = 0
    configSize = 14  #4,4,6
    lastFrameFull = True

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind((HOST, PORT1))
    s2.bind((HOST, PORT2))
    s1.listen()
    s2.listen()
    conn1, addr1 = s1.accept()    
    conn2, addr2 = s2.accept()

    print('Connect', addr1, addr2)

    START = time.time()

    for i in range (0, NUM_IMAGES): 
        #FRAMEstart = time.time()
        recvS = time.time()
        msgLen = 0
        buffer = b''
        firstMsg = True
        JPEGLEN = 10000

        while True:
            data = conn1.recv(min(1400, JPEGLEN+configSize-msgLen))
            msgLen += len(data)
            buffer += data

            if firstMsg == True:
                firstMsg = False
                lenCode = data[0:configSize]
                #print("FIRSTMSG", lenCode)
                OMVoffx = int(lenCode[0:4])
                OMVoffy = int(lenCode[4:8])
                JPEGLEN = int(lenCode[8:])

            if msgLen >= JPEGLEN+configSize:
                break

        if OMVoffx >= 6000 and OMVoffx != 9000:
            OMVoffx = (-1)*(OMVoffx-6000)
        if OMVoffy >= 6000 and OMVoffy != 9000:
            OMVoffy = (-1)*(OMVoffy-6000)

        recvE = time.time()

        #print("RECVtime", i, recvE-recvS)
        
        #DECODE
        jpegIMG = buffer[configSize:]

        F1 = time.time()
        image = Image.open(io.BytesIO(jpegIMG))
        
        F2 = time.time()
        #rgb_im = image.convert('RGB')
        F3 = time.time()
        #opencv_img = np.array(rgb_im)
        im_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        F4 = time.time()
        
        if resize == True:
            im_bgr = imutils.resize(im_bgr, width = 400)
        #raw = imutils.resize(opencv_img, width = 400)
        #cv2.imwrite(str(i)+".jpg", im_bgr)
        #cv2.imshow(opencv_img)
        #cv2.waitKey(1)
        
        print("IO", F2-F1, "RGB", F3-F2, "CV2", F4-F3)
        #gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
	    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #h, w, _ = opencv_img.shape
        
        
        if detector == "mobile":
            D1 = time.time()
            bbox = face_detector.forward(im_bgr)
            D2 = time.time()
            #bbox = face_detector.forward(opencv_img)
        
        if detector == "yolo":
            D1 = time.time()
            box, conf, clss = trt_yolo.detect(im_bgr, conf_th)
            D2 = time.time()
            bbox = []
            bestIndex = -1
            bestConf = 0
            for b in range (0, len(box)):
                if clss[b] == 0:
                    if conf[b] > bestConf:
                        bestConf = conf[b]
                        bestIndex = b
            if bestConf != 0:
                bbox.append(box[bestIndex])
            #print(bbox,conf,clss) #clss 0 = face, clss 1 = person
        
        if detector == "mtcnn":
            D1 = time.time()
            bbox, landmarks = mtcnn.detect(im_bgr, minsize=40)
            D2 = time.time()
	
        if detector == "ssd":
            D1 = time.time()
            box, conf, clss = trt_ssd.detect(im_bgr, conf_th)
            D2 = time.time()
            bbox = []
            bestIndex = -1
            bestConf = 0
            for b in range (0, len(box)):
                if clss[b] == 1:
                    if conf[b] > bestConf:
                        bestConf = conf[b]
                        bestIndex = b
            if bestConf != 0:
                bbox.append(box[bestIndex])
            #Class 1 = hands
        
        if len(bbox) == 0 :
            if i<10:
                XX = 90
                YY = 160
            
            '''
            DETECTION = "NO"
            offx = 9000
            offy = 9000
            LocationX.append(offx)
            LocationY.append(offy)
            '''

        else:
            midX = bbox[0][0] + (bbox[0][2] - bbox[0][0])/2
            midY = bbox[0][2]+ (bbox[0][3] - bbox[0][2])/2

            errX = midX - (1280/2) #(800/2) #(1280/2) #(1024/2)
            errY = midY - (1024/2) #(600/2) #(1024/2) #(768/2)

            XX += pidX(errX)
            YY -= pidY(errY)

            XX = int(XX)
            YY = int(YY)

            if XX < 0:
                XX = 0
            if XX > 180:
                XX = 180

            if YY < 0:
                YY = 0 
            if YY > 180:
                YY = 180
            
            '''
            DETECTION = "YES"
            Bleft, Btop, Bright, Bbot = bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3] 

            if OMVoffx == 9000:    #if 1 == 3
                SCALE = 2592/800
                width = (Bright - Bleft) * SCALE
                height= (Bbot - Btop) * SCALE
                offx = (Bleft) * SCALE - 896 - (CROPw - width)/2
                offy = (Btop) * SCALE  - 672 - (CROPh - height)/2
                                
            else:
                width = Bright - Bleft
                height = Bbot - Btop
                offx = OMVoffx + (Bleft - (CROPw - width)/2)
                offy = OMVoffy + (Btop  - (CROPh - height)/2)
                            
            offx = int(offx) - int(offx)%2
            offy = int(offy) - int(offy)%2
            
            LocationX.append(int(offx))
            LocationY.append(int(offy))
        
            if offx < 0:
                offx = (-1)*offx + 6000
            if offy < 0:
                offy = (-1)*offy + 6000 
                
            #INFO = [i, offx, offy, Bleft, Btop, Bright, Bbot, Bconf]
            #print(INFO)
            '''


        #offx = i #CHECK LAG
        #offy = 0
        confirm = str(XX)+","+str(YY)+","
        
        conn2.send(confirm.encode()+bytearray(10-len(confirm)))
        #print(i, DETECTION, D2-D1)
        print(i, errX, errY, XX, YY)
        #FRAMEend = time.time()
        #FPS.append(1/(FRAMEend-FRAMEstart))

    END = time.time()
    print("Time: ", END-START)
    #print("LOCATION")
    #print(LocationX)
    #print(LocationY)
    #print("RESULTS!!!")
    #print([np.average(FPS), statistics.stdev(FPS)])
    return(END-START)
    conn1.close()
    conn2.close()

resize = False
xP = 0.01
xI = 0.001
xD = 0.0005
yP = 0.025  
yI = 0.001
yD = 0.0005
main(PORT, detector, resize, NUM_IMAGES, xP, xI, xD, yP, yI, yD)

	

