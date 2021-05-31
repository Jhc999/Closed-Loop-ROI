import cv2
import numpy as np
import os
from os.path import isfile, join
pathIn  = './Multi_Win2/'
pathOut = 'WIN2.mp4'
fps = 70
files = []
frame_array = []

for i in range(0, 900):
    files.append(str(i)+'.jpg')

for i in range(len(files)):
    filename=pathIn + files[i]
    #reading each files
    img = cv2.imread(filename)
    print(filename)
    height, width, layers = img.shape
    size = (width,height)
    
    #inserting the frames into an image array
    frame_array.append(img)
out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
out.release()
