# Closed-loop Region of Interest Enabling High Spatial and Temporal Resolutions in Object Detection and Tracking via Wireless Camera

Journal Paper in IEEE Access, Volume #, 2021: LINK

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
9. B00PY3LQ2Y Adafruit Mini Pan-Tilt Kit 
10. TensorRT models (https://github.com/jkjung-avt/tensorrt_demos)

## Dependencies
1. Python-3.6
2. Nvidia-jetpack Version 4.4.1-b50
3. Opencv-3.4.6
4. Tensorflow-1.12.2
5. Protobuf-3.8.0
6. Imutils-0.5.3
7. Numpy-1.16.1
8. Pillow-8.0.1

## Notes

For the demos of streaming methods OpenMV scripts can be flashed directly onto the OpenMV (flashing instructions: ). 

For reproducing figures from the paper, the OpenMV must be wirelessly connected to the OpenMV on an external PC (connection instructions: ). Data for the figures is printed directly to the serial terminal and plotted.

After running a script once that requires a wireless connection, the TCP socket will be blocked. The socket can usually be cleared by running ClearSocket.py. If this does not work, the port numbers for the TCP socket must be changed inside the scripts.

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

## Figure Plotting

Blurb


