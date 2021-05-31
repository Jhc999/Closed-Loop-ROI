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

from config import *
from imutils import face_utils
import pdb
import csv
from FaceDetection import Detector
from imutils import face_utils

import pycuda.autoinit 
from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
from utils.mtcnn import TrtMtcnn

#########################################################################
#CONFIGURE THESE VALUES
#########################################################################

HOST = '192.168.1.67'  # Standard loopback interface address (localhost)
PORT = 8000	       # Port Number   	
resize = False
NUM_IMAGES = 1000
disp = False
save = False

#########################################################################

file = open('Multi_Roi_Vals', 'w', newline = '')
with file:
    data = [["i", "Offx1", "Offy1", "Offx2", "Offy2", "Person"]]
    write = csv.writer(file)
    write.writerows(data)

def main(PORT1, resize, NUM_IMAGES, disp, save):
    FPS = []
    LocationX = []
    LocationY = []
    PersonList = []
    Locations = []

    #minsize = 40
    #mtcnn = TrtMtcnn()
    
    cls_dict = get_cls_dict(2)
    h = w = 416
    model = 'yolov4-416'
    category_num = 2
    letter_box = True 
    conf_th = 0.5
    trt_yolo = TrtYOLO(model, (h, w), category_num, letter_box)
    
    print("READY")
    
    PORT2 = PORT1+1
    width = 2592
    height = 1944
    CROPw = 400
    CROPh = 150

    configSize = 23  #4,4,6,1,4,4

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind((HOST, PORT1))
    s2.bind((HOST, PORT2))
    s1.listen()
    s2.listen()
    conn1, addr1 = s1.accept()    
    conn2, addr2 = s2.accept()

    person1 = [-1, -1]
    person2 = [-1, -1]

    print('Connect', addr1, addr2)

    START = time.time()

    for i in range (0, NUM_IMAGES): 
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
                OMVoffx1 = int(lenCode[0:4])
                OMVoffy1 = int(lenCode[4:8])
                JPEGLEN = int(lenCode[8:14])
                person  = int(lenCode[14:15])
                OMVoffx2 = int(lenCode[15:19])
                OMVoffy2 = int(lenCode[19:23])
                
            if msgLen >= JPEGLEN+configSize:
                break

        if OMVoffx1 >= 6000 and OMVoffx1 != 9000:
            OMVoffx1 = (-1)*(OMVoffx1-6000)
        if OMVoffy1 >= 6000 and OMVoffy1 != 9000:
            OMVoffy1 = (-1)*(OMVoffy1-6000)

        if OMVoffx2 >= 6000 and OMVoffx2 != 9000:
            OMVoffx2 = (-1)*(OMVoffx2-6000)
        if OMVoffy2 >= 6000 and OMVoffy2 != 9000:
            OMVoffy2 = (-1)*(OMVoffy2-6000)
        
        #DECODE
        jpegIMG = buffer[configSize:]
        image = Image.open(io.BytesIO(jpegIMG))
        im_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        #cv2.imwrite("temp.jpg", im_bgrR)
        #im_bgr = cv2.imread("temp.jpg")       
        #print("IMAGE")
        #print(im_bgr[10])
        #print(im_bgr[100])
           
        hIM, wIM, _, = im_bgr.shape
            
        try:       
            if hIM == 600:
                #print("YOLO Detect")
                box, conf, clss = trt_yolo.detect(im_bgr, conf_th)
                bbox = []
                
                print(box)
                if len(box) >= 2:
                    #print(bbox,conf,clss) #clss 0 = face, clss 1 = person
                    candidates = []
                    for c in range (0, len(box)):
                        if clss[c] == 0:
                            candidates.append([box[c], conf[c]])
                    results = sorted(candidates, key = lambda z: z[1], reverse = True)[:2]
                    for res in range (0, len(results)):
                        bbox.append(candidates[res][0])
                    
            else:
                #print("MTCNN Detect")
                #bbox, landmarks = mtcnn.detect(im_bgr, minsize=minsize)
                
                #print("YOLO Detect")
                box, conf, clss = trt_yolo.detect(im_bgr, conf_th)
                bbox = []
                
                print(box)
                if len(box) >= 1:
                    #print(bbox,conf,clss) #clss 0 = face, clss 1 = person
                    candidates = []
                    for c in range (0, len(box)):
                        if clss[c] == 0:
                            candidates.append([box[c], conf[c]])
                    results = sorted(candidates, key = lambda z: z[1], reverse = True)[:1]
                    for res in range (0, len(results)):
                        bbox.append(candidates[res][0])
        except:
            bbox = []
            print("------FAILED DETECT------")
            continue

        #for rr in range (0, len(bbox)):
        #    cv2.rectangle(im_bgr, (bbox[rr][0], bbox[rr][1]), (bbox[rr][2], bbox[rr][3]), (255,0,0), 2)
            
        #Locations.append([i, OMVoffx1, OMVoffy1, OMVoffx2, OMVoffy2, person])
        cv2.imwrite("./multi_images/"+str(i)+".jpg", im_bgr)
        file = open('Multi_Roi_Vals', 'a', newline = '')
        with file:
            data = [[i, OMVoffx1, OMVoffy1, OMVoffx2, OMVoffy2, person]]
            write = csv.writer(file)
            write.writerows(data)

        if disp == True:                 
            cv2.imshow("", im_bgr)
            cv2.waitKey(1)
        
        if (len(bbox) == 0):
            print("------no detections------")
            LocationX.append(9000)
            LocationY.append(9000)
            PersonList.append(0)
            offx1, offy1, offx2, offy2 = 9000, 9000, 9000, 9000
            person1 = [offx1, offy1]
            person2 = [offx2, offy2]  
              
        elif (OMVoffx1 == 9000 and len(bbox) == 1) or (OMVoffx2 == 9000 and len(bbox) == 1):
            print("------1 detection------")
            print(bbox)
            LocationX.append(9000)
            LocationY.append(9000)
            PersonList.append(0)
            offx1, offy1, offx2, offy2 = 9000, 9000, 9000, 9000
            person1 = [offx1, offy1]
            person2 = [offx2, offy2]  
                             
        else:                     
            if (OMVoffx1 == 9000 and len(bbox) == 2) or (OMVoffx2 == 9000 and len(bbox) == 2):                
                print("------2 detections------")
                
                SCALE = 2592/800
                
                Bleft, Btop, Bright, Bbot = bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3] 
                width = (Bright - Bleft) * SCALE
                height= (Bbot - Btop) * SCALE
                offx1 = (Bleft) * SCALE - 896 - (CROPw - width)/2
                offy1 = (Btop) * SCALE  - 672 - (CROPh - height)/2
                person1 = [offx1, offy1]
                
                Bleft, Btop, Bright, Bbot = bbox[1][0], bbox[1][1], bbox[1][2], bbox[1][3]
                width = (Bright - Bleft) * SCALE
                height= (Bbot - Btop) * SCALE
                offx2 = (Bleft) * SCALE - 896 - (CROPw - width)/2
                offy2 = (Btop) * SCALE  - 672 - (CROPh - height)/2
                person2 = [offx2, offy2]
                                
            else:
                print("------roi detection------")
                
                Bleft, Btop, Bright, Bbot = bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3] 
                width = Bright - Bleft
                height = Bbot - Btop
                if person == 1:
                    offxT = OMVoffx1 + (Bleft - (CROPw - width)/2)
                    offyT = OMVoffy1 + (Btop  - (CROPh - height)/2)
                    person1 = [offxT, offyT]
                if person == 2:
                    offxT = OMVoffx2 + (Bleft - (CROPw - width)/2)
                    offyT = OMVoffy2 + (Btop  - (CROPh - height)/2)
                    person2 = [offxT, offyT]
            
            offx1, offy1, offx2, offy2 = person1[0], person1[1], person2[0], person2[1]
                                            
            offx1 = int(offx1) - int(offx1)%2
            offy1 = int(offy1) - int(offy1)%2
            
            offx2 = int(offx2) - int(offx2)%2
            offy2 = int(offy2) - int(offy2)%2
            
            if person == 1:
                LocationX.append(int(offx1))
                LocationY.append(int(offy1))
                PersonList.append(1)
            if person == 2:
                LocationX.append(int(offx2))
                LocationY.append(int(offy2))
                PersonList.append(2)            
        
            if offx1 < 0:
                offx1 = (-1)*offx1 + 6000
            if offy1 < 0:
                offy1 = (-1)*offy1 + 6000 
            if offx2 < 0:
                offx2 = (-1)*offx2 + 6000
            if offy2 < 0:
                offy2 = (-1)*offy2 + 6000 
                
            #INFO = [i, offx, offy, Bleft, Btop, Bright, Bbot, Bconf]
            #print(INFO)


        #offx = i #CHECK LAG
        #offy = 0
        confirm = str(offx1)+","+str(offy1)+","+str(offx2)+","+str(offy2)+","
        
        #print("CONFIRM", confirm, len(confirm))
        conn2.send(confirm.encode()+bytearray(24-len(confirm)))
        #FRAMEend = time.time()
        #FPS.append(1/(FRAMEend-FRAMEstart))
        if (i % 100) == 0:
            #print(LocationX)
            #print(LocationY)
            print(Locations)

    END = time.time()
    print("Time: ", END-START)
    print("LOCATION")
    #print(LocationX)
    #print(LocationY)
    #print(PersonList)
    print(Locations)
    #print("RESULTS!!!")
    print([np.average(FPS), statistics.stdev(FPS)])
    return(END-START)
    conn1.close()
    conn2.close()

main(PORT, resize, NUM_IMAGES, disp, save)





