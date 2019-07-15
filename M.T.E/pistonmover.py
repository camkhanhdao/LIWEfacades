# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Created on Mon April 9

@author: Zachary Taylor and Cam Khanh Dao

This is a temporary script file.
"""
# gpio4 is to go forward 
# gpio5 is to move backwards

import os
import time
import readvoltbend
from time import sleep
timer = 5
timeread = 5 
i = 1
numofruns =4



voltage = []

def shutdown():
    os.system('echo in > /sys/class/gpio/gpio4/direction')
    os.system('echo out > /sys/class/gpio/gpio5/direction')
    sleep(timer)
    os.system('echo in > /sys/class/gpio/gpio5/direction')

def startup():
    os.system('echo 4 > /sys/class/gpio/export')
    os.system('echo 5 > /sys/class/gpio/export')
    main()
    
#def readit():
#    voltread.main()
#    c = voltread.main()
#    print(c)

def main():
    global i
    global timer
    global numofruns
    global voltage
#    
#    voltread.main()
#    c = voltread.main()

    if i <= numofruns: #later need to change to unlimited read
        try:
            os.system('echo out > /sys/class/gpio/gpio4/direction')
            time.sleep(timeread)
            readvoltbend.main()
            os.system('echo in > /sys/class/gpio/gpio4/direction')
            time.sleep(timeread)            
            readvoltbend.main()
            os.system('echo out > /sys/class/gpio/gpio5/direction')
            time.sleep(timeread)
            readvoltbend.main()
            os.system('echo in > /sys/class/gpio/gpio5/direction')
            time.sleep(timeread)
            readvoltbend.main()
            i += 1
            main()
        except:
            startup()
    else:
        shutdown()
        
 
if __name__=="__main__":   

    startup()
    try:
        main()
    except KeyboardInterrupt:
        shutdown()