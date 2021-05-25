# Closed-loop Region of Interest Enabling High Spatial and Temporal Resolutions in Object Detection and Tracking via Wireless Camera

Journal Paper in JOURNAL NAME, Volume #, 2021: https://google.com

Authors: Jack Chen<sup>*1,2</sup>, Hen-Wei Huang<sup>*1,3,4</sup>, Philipp Rupp<sup>1,5</sup>, Anjali Sinha<sup>4</sup>, Claas Ehmke<sup>3</sup>, and Giovanni Traverso<sup>1,4</sup>

*<sup>1</sup> Division of Gastroenterology, Brigham & Women’s Hospital, Harvard Medical School*  
*<sup>2</sup> Department of Engineering Science, University of Toronto*  
*<sup>3</sup> The Koch Institute for Integrative Cancer Research, MIT*  
*<sup>4</sup> Department of Mechanical Engineering, MIT*  
*<sup>5</sup> Department of Information Technology and Electrical Engineering, ETH Zürich*   
_<sup>*</sup> These authors contributed equally._

Supplementary Video: https://youtu.be/OYW2WF3mKDA

This repository provides the code to replicate all the demos and figures in the paper.

## Setup
1. Nvidia Jetson AGX Xavier
2. PC with OpenMV IDE
3. OpenMV H7 Plus camera 
4. OpenMV Wifi shield 
5. OpenMV firmware version 3.9 
6. M25156H14 140° lens
7. M25360H06 60° lens
8. Arduino Uno
9. Adafruit Mini Pan-Tilt Kit 
10. TensorRT models (https://github.com/jkjung-avt/tensorrt_demos)

## Dependencies
1. Python-3.6
2. Nvidia-jetpack-4.4.1-b50
3. Opencv-3.4.6
4. Tensorflow-1.12.2
5. Protobuf-3.8.0
6. Imutils-0.5.3
7. Numpy-1.16.1
8. Pillow-8.0.1

## Notes

* For the demos of streaming methods OpenMV scripts should be flashed directly onto the OpenMV. 
* For reproducing figures from the paper, the serial port should be connected to the OpenMV IDE on an external PC. Data for the figures is printed directly to the serial port and read by the IDE to later be plotted.
* After running a script once that requires a wireless connection, the TCP socket will be blocked. The socket can usually be cleared by running ClearSocket.py. If this does not work, the port numbers for the TCP socket must be changed inside the scripts.

## Default Streaming Method

Blurb

## Pan & Tilt Method

Blurb

## Closed-Loop ROI for Single Object

Blurb

## Closed-Loop ROI for Multiple Objects

Blurb

## Figure 1

Blurb

## Figure 4

Blurb

## Figure 5

Blurb

## Figure 6 

Blurb

## Figure 7

Blurb

## Figure 8

Blurb

## Figure 9

Blurb


