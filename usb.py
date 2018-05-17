import os
import time
while True:
    disks=os.system("ls /dev") #checks /dev for a disk, the first disk is always listed as /sda and /sda1
    if "sda1" in disks:
        os.system("sh YOURPROGRAM.sh") #you can put whatever command/program you want it to execute when the drive it mounted here
    time.sleep(0.5) #waits half a second before beginning the n
