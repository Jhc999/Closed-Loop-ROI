# Python code for Multiple Color Detection 
  
import numpy as np 
import cv2 
import imutils
  
webcam = cv2.VideoCapture("Video.mp4") 
  
LocationX = []
LocationY = []

LASTX = -1
LASTY = -1
while(1): 
      
    # Reading the video from the 
    # webcam in image frames 
    _, imageFrame = webcam.read()
    imageFrame = imutils.resize(imageFrame, width = 2592)
  
    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 
  
    # Set range for red color and  
    # define mask
    #red_lower = np.array([140, 87, 111], np.uint8) 
    red_lower = np.array([136, 87, 111], np.uint8) 
    red_upper = np.array([180, 255, 255], np.uint8) 
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 
    '''
    # Set range for green color and  
    # define mask 
    green_lower = np.array([25, 52, 72], np.uint8) 
    green_upper = np.array([102, 255, 255], np.uint8) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 
  
    # Set range for blue color and 
    # define mask 
    blue_lower = np.array([94, 80, 2], np.uint8) 
    blue_upper = np.array([120, 255, 255], np.uint8) 
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 
    '''     
    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernal = np.ones((5, 5), "uint8") 
      
    # For red color 
    red_mask = cv2.dilate(red_mask, kernal) 
    res_red = cv2.bitwise_and(imageFrame, imageFrame,  
                              mask = red_mask) 
    '''  
    # For green color 
    green_mask = cv2.dilate(green_mask, kernal) 
    res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = green_mask) 
      
    # For blue color 
    blue_mask = cv2.dilate(blue_mask, kernal) 
    res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
                               mask = blue_mask) 
    '''
    # Creating contour to track red color 
    contours, hierarchy = cv2.findContours(red_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
      
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour)

        x, y, w, h = cv2.boundingRect(contour)
        if(area > 100) and x > 750:  #WQXGA2
            x, y, w, h = cv2.boundingRect(contour) 
            imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                       (x + w, y + h),  
                                       (0, 0, 255), 2) 
              
            cv2.putText(imageFrame, "Red Colour", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                        (0, 0, 255))
            bbox = [[x, y, x+w, y+h]]

            if len(bbox) != 1:
                print(len(bbox))

            Bleft, Btop, Bright, Bbot = bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3] 

            #scale = 2592/640
            scale = 1

            if Bleft != LASTX and Btop != LASTY:
                L = Bleft*scale
                T = Btop*scale
                W = w*scale
                H = h*scale
                #LocationX.append(int(Bleft*scale))
                #LocationY.append(int(Btop*scale))
                LocationX.append(int(L-(200-W)/2))
                LocationY.append(int(T-(200-H)/2))
            LASTX = Bleft
            LASTY = Btop
            '''
            #SCALE = 2592/640
            SCALE = 2592/1340
            Bleft*=SCALE
            Bright*=SCALE
            Btop*=SCALE
            Bbot*=SCALE

            width = Bright - Bleft
            height = Bbot - Btop
            CROPw = 170
            CROPh = 170
            offx = (Bleft - (CROPw - width)/2)
            offy = (Btop  - (CROPh - height)/2)
                            
            offx = int(offx) - int(offx)%2
            offy = int(offy) - int(offy)%2

            LocationX.append(int(offx))
            LocationY.append(int(offy))
            '''
    '''
    # Creating contour to track green color 
    contours, hierarchy = cv2.findContours(green_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
      
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        if(area > 300): 
            x, y, w, h = cv2.boundingRect(contour) 
            imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                       (x + w, y + h), 
                                       (0, 255, 0), 2) 
              
            cv2.putText(imageFrame, "Green Colour", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX,  
                        1.0, (0, 255, 0)) 
  
    # Creating contour to track blue color 
    contours, hierarchy = cv2.findContours(blue_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        if(area > 300): 
            x, y, w, h = cv2.boundingRect(contour) 
            imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                       (x + w, y + h), 
                                       (255, 0, 0), 2) 
              
            cv2.putText(imageFrame, "Blue Colour", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1.0, (255, 0, 0)) 
    '''
              
    # Program Termination 
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    #print(LocationX)
    #print(LocationY)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print(LocationX)
        print(LocationY)
        cap.release() 
        cv2.destroyAllWindows() 
        break










