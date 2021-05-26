import os
import signal
from subprocess import Popen, PIPE

Plist = []

START = 8000
END = 8050

print("Clearing ports "+str(START)+" to "+str(END))

for j in range (START, END):
    Plist.append(j)

for i in range (0, len(Plist)):
    port = Plist[i]
    process = Popen(["lsof", "-i", ":{0}".format(port)], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    for process in str(stdout.decode("utf-8")).split("\n")[1:]:       
        data = [x for x in process.split(" ") if x != '']
        if (len(data) <= 1):
            continue

        os.kill(int(data[1]), signal.SIGKILL)
