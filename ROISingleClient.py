#IROS_DEMO FILE

import sensor, image, utime, network, usocket, gc

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.SVGA)
#sensor.set_framesize(sensor.WQXGA2)
#sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW, (0,0,2592,1944))
#sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW, (0,0,1600,1200))
sensor.skip_frames(time = 2000)

gc.enable()

########################################################################

def MVread(str_in):     #READ CONFIG MESSAGE SENT BY PC
    offX = ''
    offY = ''
    commaNum = 0
    for j in range (0, len(str_in)):
        if str_in[j] == ',':
            commaNum += 1
        else:
            if commaNum == 0:
                offX += (str_in[j])
            if commaNum == 1:
                offY += (str_in[j])
            if commaNum == 2:
                break
    return int(offX), int(offY)

########################################################################

def mainf(PORT1):
    SSID ='TELUS3061'     # Network SSID
    KEY  ='m2gbx75frq'     # Network key


    wlan = network.WINC()
    wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)
    print(wlan.ifconfig())

    HOST = '192.168.1.67'  # The server's hostname or IP address
    #PORT1 = 5012      # The port used by the server
    #PORT2 = PORT1 + 1

    PORT2 = PORT1+1
    s1 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s2 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s1.connect((HOST, PORT1))
    s2.connect((HOST, PORT2))
    s1.settimeout(2.0)   #0 is non-blocking, None is blocking
    s2.settimeout(0.04)   #0 is non-blocking, None is blocking
    #0.04 -> 2 frames  (40 fps)

    OUT = []
    CAPT = []
    COMP = []
    TRAN = []
    RECV = []

    ########################################################################
    offx = 9000
    offy = 9000
    PREDoffx = 0
    PREDoffy = 0

    SCALE = 1
    ioctlW = int(800*SCALE)
    ioctlH = int(600*SCALE)

    cropW = int(400/SCALE)  #SETTING FOR DEMO
    cropH = int(150/SCALE)  #SETTING FOR DEMO

    #cropW = int(200/SCALE)  #SETTING FOR FIG1
    #cropH = int(150/SCALE)  #SETTING FOR FIG1

    LENGTH = 0.1
    NUM_IMAGES = 100
    configSize = 14

    ########################################################################

    for i in range (0, 10):
        count = 0
        start = utime.ticks_ms()/1000

        while count < NUM_IMAGES:
            gc.collect()

            #offx = 0
            #offy = 0

            if offx == 9000:
                #lastFrameFull = True
                sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW, (2592,1944))
                sensor.set_windowing((0,0,800,600))

            else: #####DO
                #lastFrameFull = False

                ioX = offx
                setX = 0
                ioY = offy
                setY = 0
                #'''
                if offx + ioctlW < 2592:
                    ioX = offx
                    setX = 0
                else:
                    ioX = 2592 - ioctlW   #992
                    setX = (offx - ioX)
                    setX = int(setX) - int(setX)%2

                if offy + ioctlH < 1944:
                    ioY = offy
                    setY = 0
                else:
                    ioY = 1944 - ioctlH   #744
                    setY = (offy - ioY)  #IF LAST IMAGE WAS FULL, /3.24, else /2
                    setY = int(setY) - int(setY)%2

                #print("SETTINGS", offx, offy, ioX, ioY, setX, setY)
                #out = sensor.ioctl(sensor.IOCTL_GET_READOUT_WINDOW)
                #print("IOCTL", out)

                sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW, (ioX,ioY,ioctlW,ioctlH))
                #sensor.set_windowing((0,0,cropW,cropH))
                sensor.set_windowing((setX,setY,cropW,cropH))
                sensor.skip_frames(1)

            STARTING = utime.ticks_ms()/1000
            CURRENT = 0
            print(["OUTSIDE", count])
            while True:

                if CURRENT - STARTING < LENGTH:
                    RESET = 0   #NO RESET
                else:
                    RESET = 1

                ###CAPTURE
                CURRENT = utime.ticks_ms()/1000

                T1 = utime.ticks_ms()/1000
                #frame = sensor.snapshot()
                frame = sensor.snapshot()
                #frame.crop((0,0,400,300))
                #data = frame.copy((0,0,400,300))#.bytearray()
                T2 = utime.ticks_ms()/1000
                #if lastFrameFull == True:
                #    frameSend = frame.compress(40).bytearray()
                #if lastFrameFull == False:
                frameSend = frame.compress(20).bytearray() #80
                #frameSend = frame.bytearray()
                T3 = utime.ticks_ms()/1000


                OFFXsend = str(offx)  #4 bytes
                OFFYsend = str(offy)  #4 bytes
                if offx < 0:
                    OFFXsend = str((-1)*offx+6000)
                if offy < 0:
                    OFFYsend = str((-1)*offy+6000)
                frameLen = str(len(frameSend))  #6 bytes

                x0 = 4-len(OFFXsend)
                y0 = 4-len(OFFYsend)
                f0 = 6-len(frameLen)

                for q in range (0, x0):
                    OFFXsend = "0"+OFFXsend
                for q in range (0, y0):
                    OFFYsend = "0"+OFFYsend
                for q in range (0, f0):
                    frameLen = "0"+frameLen

                dataSub = OFFXsend.encode() + OFFYsend.encode() + frameLen.encode()

                #dataAll = dataSub + frameSend

                writeS =  utime.ticks_ms()/1000
                #s1.write(dataAll)
                s1.write(dataSub)
                s1.write(frameSend)

                recvS = utime.ticks_ms()/1000
                got = s2.recv(10)
                recvE = utime.ticks_ms()/1000

                CAPT.append(T2-T1)
                COMP.append(T3-T2)
                TRAN.append(recvS-writeS)
                RECV.append(recvE-recvS)

                if len(got) != 0:
                    PREDoffx, PREDoffy = MVread(got.decode())

                if RESET == 1:
                    offx, offy = PREDoffx, PREDoffy
                    if offx >= 6000 and offx != 9000:
                        offx = (-1)*(offx-6000)
                    if offy >= 6000 and offx != 9000:
                        offy = (-1)*(offy-6000)
                    #print(offx, offy)

                count += 1
                print(count, got, "WRITE", recvS-writeS, "RECV", recvE-recvS, "LEN", frameLen)

                if count >= NUM_IMAGES or RESET == 1:
                    break



        end = utime.ticks_ms()/1000
        print("FPS: ", count/(end-start), count, end-start)
        print("TIME: ", end-start)
        OUT.append(count/(end-start))

    s1.close()
    s2.close()
    print(OUT)
    print(CAPT)
    print(COMP)
    print(TRAN)
    print(RECV)
    return end-start

PORT = 6000
mainf(PORT)
sensor.skip_frames(time = 5000)



