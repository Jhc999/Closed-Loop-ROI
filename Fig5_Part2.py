import sensor, image, utime

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

NUM_IMAGES = 100

for key in ResKey:
    s_format, W, H = ResKey[key][0], ResKey[key][1], ResKey[key][2]
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(s_format)
    sensor.skip_frames(time = 2000)

    OUT = [key, W*H]

    for i in range (0, NUM_IMAGES+1):
        F1 = utime.ticks_ms()/1000
        sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW,(0,0,W,H))
        sensor.skip_frames(1)

        F2 = utime.ticks_ms()/1000
        img = sensor.snapshot()

        F3 = utime.ticks_ms()/1000
        send = img.compress(quality=80).bytearray()

        F4 = utime.ticks_ms()/1000
        if i != 0:
            #OUT.append([F2-F1, F3-F2, F4-F3])
            OUT.append([1/(F2-F1), 1/(F3-F2), 1/(F4-F3)])
    print(OUT)
