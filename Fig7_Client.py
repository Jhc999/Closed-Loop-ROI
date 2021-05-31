import sensor, image, utime, network, usocket, omv
sensor.reset()

#RGB
#sensor.set_pixformat(sensor.RGB565)

#JPEG
sensor.set_pixformat(sensor.JPEG)
sensor.set_quality(85) #85, 90, 95

SSID =''     # Network SSID
KEY  =''     # Network key
HOST = '192.168.1.71'
PORT1 = 9003
testnum = 100

########################################################################
ResKey = {}
ResKey["QQVGA"] = [sensor.QQVGA ,160,120]
ResKey["HQVGA"] = [sensor.HQVGA ,240,160]
ResKey["QVGA"]  = [sensor.QVGA ,320,240]
ResKey["VGA"]   = [sensor.VGA ,640,480]
ResKey["SVGA"]  = [sensor.SVGA ,800,600]
ResKey["XGA"]   = [sensor.XGA ,1024,768]
ResKey["SXGA"]  = [sensor.SXGA ,1280,1024]
ResKey["UXGA"]  = [sensor.UXGA ,1600,1200]
ResKey["HD"]    = [sensor.HD ,1280,720]
ResKey["FHD"]   = [sensor.FHD ,1920,1080]
ResKey["QHD"]   = [sensor.QHD ,2560,1440]
ResKey["QXGA"]  = [sensor.QXGA ,2048,1536]
ResKey["WQXGA"] = [sensor.WQXGA ,2560,1600]
ResKey["WQXGA2"]= [sensor.WQXGA2 ,2592,1944]

########################################################################

omv.disable_fb()

wlan = network.WINC()
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)
print(wlan.ifconfig())

s1 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
s1.connect((HOST, PORT1))
s1.settimeout(1.0)

########################################################################


for key in ResKey:
    s_format, W, H = ResKey[key][0], ResKey[key][1], ResKey[key][2]
    sensor.set_framesize(s_format)

    OUT=[key, W*H]
    accum = 0

    frame = sensor.snapshot().bytearray()
    for i in range (0,testnum):
        F1 = utime.ticks_ms()/1000
        s1.write(frame)
        F2 = utime.ticks_ms()/1000
        accum += (F2-F1)
    OUT.append(accum/testnum)
    print(OUT)

s1.close()

