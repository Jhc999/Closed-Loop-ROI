#IROS_DEMO FILE

import sensor, image, utime, network, usocket, gc

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.SVGA)
sensor.skip_frames(time = 2000)

gc.enable()

########################################################################

def MVread(str_in):     #READ CONFIG MESSAGE SENT BY PC
    offX1 = ''
    offY1 = ''
    offX2 = ''
    offY2 = ''
    commaNum = 0
    for j in range (0, len(str_in)):
        if str_in[j] == ',':
            commaNum += 1
        else:
            if commaNum == 0:
                offX1 += (str_in[j])
            if commaNum == 1:
                offY1 += (str_in[j])
            if commaNum == 2:
                offX2 += (str_in[j])
            if commaNum == 3:
                offY2 += (str_in[j])
            if commaNum == 4:
                break
    return int(offX1), int(offY1), int(offX2), int(offY2)

########################################################################

def main(PORT1):
    SSID ='TELUS3061'     # Network SSID
    KEY  ='m2gbx75frq'     # Network key


    wlan = network.WINC()
    wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)
    print(wlan.ifconfig())

    HOST = '192.168.1.73'

    PORT2 = PORT1+1
    #PORT3 = PORT2+1
    #PORT4 = PORT3+1
    s1 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s2 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    #s3 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    #s4 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)

    s1.connect((HOST, PORT1))
    s2.connect((HOST, PORT2))
    #s3.connect((HOST, PORT3))
    #s4.connect((HOST, PORT4))

    s1.settimeout(2.0)   #0 is non-blocking, None is blocking
    s2.settimeout(0.04)   #0 is non-blocking, None is blocking
    #s3.settimeout(2.0)   #0 is non-blocking, None is blocking
    #s4.settimeout(0.04)   #0 is non-blocking, None is blocking

    OUT = []
    CAPT = []
    COMP = []
    TRAN = []
    RECV = []

    ########################################################################
    offx = 9000
    offy = 9000

    offx1 = 9000
    offy1 = 9000
    PREDoffx1 = 0
    PREDoffy1 = 0

    offx2 = 9000
    offy2 = 9000
    PREDoffx2 = 0
    PREDoffy2 = 0

    ioctlW = int(800)
    ioctlH = int(600)
    cropW = int(400)
    cropH = int(150)

    LENGTH = 0.1
    NUM_IMAGES = 100
    configSize = 14
    LEN_NUM = 3

    person = 1

    ########################################################################

    for i in range (0, 10):
        count = 0
        start = utime.ticks_ms()/1000

        while count < NUM_IMAGES:
            gc.collect()

            #offx1 = 9000
            #offy = 0

            if offx1 == 9000 or offx2 == 9000:
                #lastFrameFull = True
                sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW, (2592,1944))
                sensor.set_windowing((0,0,800,600))

            else: #####DO
                #lastFrameFull = False

                if person == 1:
                    offx, offy = offx1, offy1
                else:
                    offx, offy = offx2, offy2

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

                #print("SETTINGS", person, offx, offy, ioX, ioY, setX, setY)
                print("PERSON#", person, "OFFSET1", offx1, offx2, "OFFSET2", offx1, offx2)

                #out = sensor.ioctl(sensor.IOCTL_GET_READOUT_WINDOW)
                #print("IOCTL", out)

                sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW, (ioX,ioY,ioctlW,ioctlH))
                #sensor.set_windowing((0,0,cropW,cropH))
                sensor.set_windowing((setX,setY,cropW,cropH))
                sensor.skip_frames(1)

            STARTING = utime.ticks_ms()/1000
            CURRENT = 0
            START_NUM = 0
            CURR_NUM = 0
            #print(["OUTSIDE", count])
            while True:

                #if CURRENT - STARTING < LENGTH:
                if CURR_NUM - START_NUM < LEN_NUM:
                    RESET = 0   #NO RESET
                else:
                    RESET = 1

                ###CAPTURE
                CURRENT = utime.ticks_ms()/1000
                CURR_NUM += 1

                T1 = utime.ticks_ms()/1000
                #frame = sensor.snapshot()
                frame = sensor.snapshot()
                #frame.crop((0,0,400,300))
                #data = frame.copy((0,0,400,300))#.bytearray()
                T2 = utime.ticks_ms()/1000
                #if lastFrameFull == True:
                #    frameSend = frame.compress(40).bytearray()
                #if lastFrameFull == False:
                frameSend = frame.compress(80).bytearray() #80
                #frameSend = frame.bytearray()
                T3 = utime.ticks_ms()/1000


                OFFXsend1 = str(offx1)  #4 bytes
                OFFYsend1 = str(offy1)  #4 bytes
                if offx1 < 0:
                    OFFXsend1 = str((-1)*offx1+6000)
                if offy1 < 0:
                    OFFYsend1 = str((-1)*offy1+6000)

                frameLen = str(len(frameSend))  #6 bytes

                OFFXsend2 = str(offx2)  #4 bytes
                OFFYsend2 = str(offy2)  #4 bytes
                if offx2 < 0:
                    OFFXsend2 = str((-1)*offx2+6000)
                if offy2 < 0:
                    OFFYsend2 = str((-1)*offy2+6000)

                x01 = 4-len(OFFXsend1)
                y01 = 4-len(OFFYsend1)
                f0 = 6-len(frameLen)
                x02 = 4-len(OFFXsend2)
                y02 = 4-len(OFFYsend2)

                for q in range (0, x01):
                    OFFXsend1 = "0"+OFFXsend1
                for q in range (0, y01):
                    OFFYsend1 = "0"+OFFYsend1
                for q in range (0, f0):
                    frameLen = "0"+frameLen
                for q in range (0, x02):
                    OFFXsend2 = "0"+OFFXsend2
                for q in range (0, y02):
                    OFFYsend2 = "0"+OFFYsend2

                dataSub = OFFXsend1.encode() + OFFYsend1.encode() + frameLen.encode() + str(person).encode() + OFFXsend2.encode() + OFFYsend2.encode()

                #dataAll = dataSub + frameSend

                writeS =  utime.ticks_ms()/1000
                #s1.write(dataAll)
                s1.write(dataSub)
                s1.write(frameSend)

                recvS = utime.ticks_ms()/1000
                got = s2.recv(24)
                recvE = utime.ticks_ms()/1000

                CAPT.append(T2-T1)
                COMP.append(T3-T2)
                TRAN.append(recvS-writeS)
                RECV.append(recvE-recvS)

                if len(got) != 0:
                    PREDoffx1, PREDoffy1, PREDoffx2, PREDoffy2 = MVread(got.decode())

                if RESET == 1:
                    offx1, offy1 = PREDoffx1, PREDoffy1
                    if offx1 >= 6000 and offx1 != 9000:
                        offx1 = (-1)*(offx1-6000)
                    if offy1 >= 6000 and offx1 != 9000:
                        offy1 = (-1)*(offy1-6000)

                    offx2, offy2 = PREDoffx2, PREDoffy2
                    if offx2 >= 6000 and offx2 != 9000:
                        offx2 = (-1)*(offx2-6000)
                    if offy2 >= 6000 and offx2 != 9000:
                        offy2 = (-1)*(offy2-6000)
                    #print(offx, offy)

                count += 1
                #print(count, got, "WRITE", recvS-writeS, "RECV", recvE-recvS, "LEN", frameLen)

                if count >= NUM_IMAGES or RESET == 1:
                    if person == 1:
                        person = 2
                    else:
                        person = 1
                    break



        end = utime.ticks_ms()/1000
        print("FPS: ", count/(end-start), count, end-start)
        print("TIME: ", end-start)
        OUT.append(count/(end-start))

    s1.close()
    s2.close()
    return end-start

main(8000)
