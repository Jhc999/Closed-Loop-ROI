import sensor, image, utime

NUM_IMAGES = 100

settings = [[100,100], [200,150], [300, 224], [400,300], [500, 374], [600,450], [700, 524], [800, 600]]

for j in range (0, len(settings)):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)

    sensor.set_framesize(sensor.SVGA)
    sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW,(0,0,800,600))
    sensor.skip_frames(time = 2000)

    W = settings[j][0]
    H = settings[j][1]
    OUT = [W*H]

    for i in range (0, NUM_IMAGES+2):
        F1 = utime.ticks_ms()/1000
        sensor.ioctl(sensor.IOCTL_SET_READOUT_WINDOW,(0,0,800,600))
        sensor.set_windowing((0,0,W,H))
        sensor.skip_frames(1)

        F2 = utime.ticks_ms()/1000
        img = sensor.snapshot()

        F3 = utime.ticks_ms()/1000
        send = img.compress(quality=80).bytearray()

        F4 = utime.ticks_ms()/1000
        sensor.skip_frames(1)

        if i >= 1:
            OUT.append([F2-F1, F3-F2, F4-F3])

    print(OUT)
