# Closed-loop Region of Interest Enabling High Spatial and Temporal Resolutions in Object Detection and Tracking via Wireless Camera

Journal Paper in IEEE Access, Volume #, 2021: LINK

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

* For reproducing figures from the paper, the serial port should be connected to the OpenMV IDE on an external PC. Data for the figures is printed directly to the serial port and read by the IDE to later be plotted. 
* For the demos of streaming methods OpenMV, the serial port connection is not necessary, and scripts can be flashed directly onto the OpenMV. However, the serial port connection will display the captured images in the OpenMV IDE without the need to save the images (which reduces the FPS).
* After running a script once that requires a wireless connection, the TCP socket will be blocked. The socket can usually be cleared by running ClearPort.py. If this does not work, the port numbers for the TCP socket must be changed inside the scripts.
* The model weights for YoloV4 (256 MB) are available upon request. Downlaod and place into `/Closed-Loop-ROI/Yolo/`

## Default Streaming Method

* Enter the SSID, password, and IP address of the Jetson to `DefaultServer.py`. 
* Run `DefaultServer.py` first, then run `DefaultClient.py` either by flashing directly to the OpenMV or by connecting the OpenMV to the IDE.
* Note that displaying the video stream on `ROISingleServer.py` will reduce the FPS of the video.

## Pan & Tilt Method

* Upload `ServoControl.ino` to the Arduino Uno. Connect pins between the OpenMV and Arduino listed in `PanTiltClient.py`. 
* Enter the SSID, password, and IP address of the Jetson to `PanTiltServer.py`. 
* Run `PanTiltClient.py` first, then run `PanTiltServer.py` either by flashing directly to the OpenMV or by connecting the OpenMV to the IDE. 
* Note that displaying the video stream on `PanTiltServer.py` will reduce the FPS of the video.

## Closed-Loop ROI for Single Object

* Enter the SSID, password, and IP address of the Jetson to `ROISingleServer.py`. 
* Run `ROISingleClient.py` first, then run `ROISingleServer.py` either by flashing directly to the OpenMV or by connecting the OpenMV to the IDE. 
* Note that displaying the video stream on `ROISingleServer.py` will reduce the FPS of the video.

## Closed-Loop ROI for Multiple Objects

* Enter the SSID, password, and IP address of the Jetson to `ROIMultiServer.py`. 
* Run `ROIMultiClient.py` first, then run `ROIMultiServer.py` either by flashing directly to the OpenMV or by connecting the OpenMV to the IDE. 
* Note that displaying the video stream on `ROIMultiServer.py` will reduce the FPS of the video.

## Figure 1

* Figure 1 is generated using the demo codes for Default Streaming Method and for Closed-Loop ROI for Single Object. 
* The ROI dimensions should be changed to 200x150 pixels and a face or picture of a face should remain within the camera's field of view at all times.

## Figure 4

* Histogram values are obtained from scripts for Figure 6, Figure 7, and Figure 8.

## Figure 5

* Connect the OpenMV to the OpenMV IDE over serial.
* Run `Fig5_Part1.py` (for resolultions below SVGA) and `Fig5_Part2.py` (for resolutions above SVGA) to generate data to be plotted.

## Figure 6 

* Connect the OpenMV to the OpenMV IDE over serial. 
* Run `Fig6.py` to generate data to be plotted.

## Figure 7

* For Wifi data transmission, enter the SSID, password, and IP address of the Jetson or external PC to `Fig7_Server.py`. Set the JPEG quality factor. Run `Fig7_Server.py` first. Then, run `Fig7_Client.py` either by flashing directly to the OpenMV or by connecting the OpenMV to the IDE. 
* For USB data transmission, use the `USB_vcp.py` script from the OpenMV. However, use the `utime` module instead of the `time` module.

## Figure 8

* For face detection with MobileNet, run `Fig8_MobileNet.py` on the Jetson. 
* For face detection with MTCNN, run `Fig8_MTCNN.py` on the Jetson. 
* For face detection with YoloV4, run `Fig8_YoloV4.py` on the Jetson. 

## Figure 9

* For the ground truth, record the video of the full frame with the OpenMV IDE at VGA.
* For the default method, follow the same steps as the default demo. However, use `DefaultClient.py` with `Color_Server_Default.py`.
* For the ROI method, follow the same steps as the single ROI demo. However, change the ROI dimension in `ROISingleClient.py` from 400x150 pixels to 200x200 and  use with `ROISingleServer.py`. 
* Process the videos using `Fig9_Processing.py`.

## Helper Scripts

* `ClearPorts.py` clears an open port. Ports may be blocked after running a script that opens a TCP connection.
* `Convert_frames_to_video.py` converts frames saved by demo files into videos.
