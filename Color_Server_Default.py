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
from imutils import face_utils

#########################################################################
#MODIFY PARAMETERS

HOST = '192.168.1.65'  # Standard loopback interface address (localhost)
PORTNUM = 8000

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

def main(PORT1, detector, resize, NUM_IMAGES):

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

    if detector == "color":
        red_lower = np.array([136, 87, 111], np.uint8) 
        red_upper = np.array([180, 255, 255], np.uint8)
        kernal = np.ones((5, 5), "uint8") 

    print("READY")
    PORT2 = PORT1+1
    width = 2592
    height = 1944
    #CROPw = 200
    CROPw = 200
    CROPh = 200
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

        if detector == "color":
            bbox = []
            D1 = time.time()
            hsvFrame = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2HSV)
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
            red_mask = cv2.dilate(red_mask, kernal) 
            res_red = cv2.bitwise_and(im_bgr, im_bgr, mask = red_mask)
            contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 
                if(area > 100): #300
                    x, y, w, h = cv2.boundingRect(contour)
                    bbox = [[x, y, x+w, y+h]]
            D2 = time.time()

        if detector == "blank":
            bbox = []
            D1 = 0
            D2 = 0
        
        if len(bbox) == 0 :
            DETECTION = "NO"
            offx = 9000
            offy = 9000
                 
        else:
            DETECTION = "YES"
            Bleft, Btop, Bright, Bbot = bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3] 

            LocationX.append(int(Bleft)*800/2592)   
            LocationY.append(int(Btop)*800/2592)    
        
            if offx < 0:
                offx = (-1)*offx + 6000
            if offy < 0:
                offy = (-1)*offy + 6000 
                
        confirm = str(offx)+","+str(offy)+","
        
        conn2.send(confirm.encode()+bytearray(10-len(confirm)))
        print(i, DETECTION, D2-D1)
        print(LocationX)
        print(LocationY)

    END = time.time()
    print("Time: ", END-START)
    print("LOCATION")
    print(LocationX)
    print(LocationY)
    conn1.close()
    conn2.close()
    return(END-START)

detector = "color"
resize = False
NUM_IMAGES = 100 
main(PORTNUM, detector, resize, NUM_IMAGES)



