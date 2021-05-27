# OpenMV Cam Ground Pin   ----> Arduino Ground
# OpenMV Cam UART3_TX(P4) ----> Arduino Uno UART_RX(0)
# OpenMV Cam UART3_RX(P5) ----> Arduino Uno UART_TX(1)

import time
from pyb import UART
import network
import sensor
import utime
import usocket

sensor.reset()
sensor.set_pixformat(sensor.JPEG)
sensor.set_quality(80)
sensor.set_framesize(sensor.SXGA)
sensor.skip_frames(time = 2000)

########################################################################

def MVread(str_in):     #READ CONFIG MESSAGE SENT BY PC
    X = ''
    Y = ''
    commaNum = 0
    for j in range (0, len(str_in)):
        if str_in[j] == ',':
            commaNum += 1
        else:
            if commaNum == 0:
                X += (str_in[j])
            if commaNum == 1:
               Y += (str_in[j])
            if commaNum == 2:
                break
    return int(X), int(Y)

########################################################################

uart = UART(3, 19200)

SSID ='TELUS3061'     # Network SSID
KEY  ='m2gbx75frq'     # Network key
print("Trying to connect... (may take a while)...")
wlan = network.WINC()
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)
print(wlan.ifconfig())

HOST = '192.168.1.69'
PORT1 = 5026
PORT2 = PORT1+1
s1 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
s2 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
s1.connect((HOST, PORT1))
s2.connect((HOST, PORT2))
s1.settimeout(1.0)   #0 is non-blocking, None is blocking
s2.settimeout(0.04)   #0 is non-blocking, None is blocking

NUM_IMAGES = 500

XX = 90
YY = 170
SetX = 90
SetY = 170

Bigstt = utime.ticks_ms()/1000

for i in range (0, NUM_IMAGES):
    T1 = utime.ticks_ms()/1000
    frame = sensor.snapshot()
    T2 = utime.ticks_ms()/1000
    frameSend = frame.compress(80).bytearray()
    T3 = utime.ticks_ms()/1000
    frameLen = str(len(frameSend))
    Send1 = str(0)
    Send2 = str(0)
    x0 = 4-len(Send1)
    y0 = 4-len(Send2)
    f0 = 6-len(frameLen)

    for q in range (0, x0):
        Send1 = "0"+Send1
    for q in range (0, y0):
        Send2 = "0"+Send2
    for q in range (0, f0):
        frameLen = "0"+frameLen

    dataSub = Send1.encode() + Send2.encode() + frameLen.encode()

    got = ""

    writeS =  utime.ticks_ms()/1000
    s1.write(dataSub+frameSend)
    recvS = utime.ticks_ms()/1000
    got = s2.recv(10)
    recvE = utime.ticks_ms()/1000

    if len(got) != 0:
        XX, YY = MVread(got.decode())

    SetX = XX
    SetY = YY

    str_SetX = str(SetX)
    str_SetY = str(SetY)

    if len(str_SetX) == 2:
        str_SetX = "0" + str_SetX
    if len(str_SetY) == 2:
        str_SetY = "0" + str_SetY
    if len(str_SetX) == 1:
        str_SetX = "00" + str_SetX
    if len(str_SetX) == 1:
        str_SetY = "00" + str_SetY

    if XX != 900:
        Settings = str_SetX + str_SetY + "Z"
        uart.write(Settings)
    #if (uart.any()):
    #    print(uart.read())
    #time.sleep(0.1)

Bigend = utime.ticks_ms()/1000

s1.close()
s2.close()
print("FPS: ", NUM_IMAGES/(Bigend-Bigstt))



