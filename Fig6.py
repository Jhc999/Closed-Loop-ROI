import sensor, image, utime

#Every period: reconfigure subwindow and reconfigure ioctl

ResKey = {}
ResKey["SVGA"]  = [sensor.SVGA ,800, 600]
ResKey["XGA"]   = [sensor.XGA ,1024, 768]
ResKey["SXGA"]  = [sensor.SXGA ,1280, 1024]
ResKey["UXGA"]  = [sensor.UXGA ,1600, 1200]
ResKey["HD"]    = [sensor.HD ,1280, 720]
ResKey["FHD"]   = [sensor.FHD ,1920, 1080]
ResKey["QHD"]   = [sensor.QHD ,2560, 1440]
ResKey["QXGA"]  = [sensor.QXGA ,2048, 1536]
ResKey["WQXGA"] = [sensor.WQXGA ,2560, 1600]
ResKey["WQXGA2"]= [sensor.WQXGA2 ,2592, 1944]

period = [float("inf"), 0.5, 0.1, 0.01]
#period = [0.01]

NUM_IMAGES = 100
NUM_TESTS = 2

for key in ResKey:
    s_format, W, H = ResKey[key][0], ResKey[key][1], ResKey[key][2]
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(s_format)
    sensor.skip_frames(time = 2000)

    for p in range (0, len(period)):
        LENGTH = period[p]

        OUT = [LENGTH, key, ResKey[key][1]*ResKey[key][2]]

        for t in range (0, NUM_TESTS):
            BIGSTART = utime.ticks_ms()/1000

            count = 0
            while count < NUM_IMAGES:
                sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW, (count, count, W-count-2, H-count-2))
                sensor.set_windowing((count,count, W-count-2, H-count-2))
                sensor.skip_frames(1)

                STARTING = utime.ticks_ms()/1000
                CURRENT = 0
                while True:
                    if CURRENT - STARTING > LENGTH:
                        break
                    CURRENT = utime.ticks_ms()/1000
                    frame = sensor.snapshot()
                    count += 1

                    if count >= NUM_IMAGES:
                        break

            BIGEND = utime.ticks_ms()/1000

            OUT.append(BIGEND-BIGSTART)
        print(OUT)

#ResKey["QQVGA"] = [sensor.QQVGA ,160, 120]
#ResKey["HQVGA"] = [sensor.HQVGA ,240, 160]
#ResKey["QVGA"]  = [sensor.QVGA ,320, 240]
#ResKey["VGA"]   = [sensor.VGA ,640, 480]
