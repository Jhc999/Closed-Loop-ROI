#IROS_DEMO FILE

import sensor, image, utime, network, usocket, gc
'''
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.SVGA)   # Can edit firmware to make QVGA equal to anything
#sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW, (0,0,2592,1944))
#sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW, (0,0,1600,1200))
sensor.skip_frames(time = 2000)
'''
sensor.reset()
sensor.set_pixformat(sensor.JPEG)
sensor.set_quality(80)
#sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.WQXGA2)
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

    HOST = '192.168.1.65'  # The server's hostname or IP address
    #PORT1 = 5012      # The port used by the server
    #PORT2 = PORT1 + 1

    PORT2 = PORT1+1
    s1 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s2 = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s1.connect((HOST, PORT1))
    s2.connect((HOST, PORT2))
    s1.settimeout(None)   #0 is non-blocking, None is blocking
    s2.settimeout(0.04)   #0 is non-blocking, None is blocking
    #0.04 -> 2 frames  (40 fps)

    OUT = []
    CAPT = []
    COMP = []
    TRAN = []
    RECV = []

    for i in range (0, 1):
        ########################################################################
        NUM_IMAGES = 100
        count = 0
        OFFXsend = '1234'
        OFFYsend = '1234'
        configSize = 14

        start = utime.ticks_ms()/1000
        ########################################################################

        while count < NUM_IMAGES:
            gc.collect()

            T1 = utime.ticks_ms()/1000
            frame = sensor.snapshot()
            T2 = utime.ticks_ms()/1000
            #frameSend = frame.compress(80).bytearray()
            frameSend = frame.bytearray()
            T3 = utime.ticks_ms()/1000

            frameLen = str(len(frameSend))  #6 bytes
            OFFXsend = '9000'
            OFFYsend = '9000'
            f0 = 6-len(frameLen)
            for q in range (0, f0):
                frameLen = "0"+frameLen

            dataSub = OFFXsend.encode() + OFFYsend.encode() + frameLen.encode()

            writeS =  utime.ticks_ms()/1000
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

            count += 1
            print(count, got, "WRITE", recvS-writeS, "RECV", recvE-recvS, "LEN", frameLen)

            if count >= NUM_IMAGES:
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

timee = mainf(8000)
sensor.skip_frames(time = 5000)
#timee = mainf(5002)



