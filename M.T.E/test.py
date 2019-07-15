# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Created on Sat April 21

@author: Cam Khanh Dao

"""
import volt_bending
import datetime
from time import sleep
precision = 2
timer = 1
list1 = []
i = 0
timer = 1

def voltbending():
    vb = volt_bending.main()
    if len(vb)>1:
        try:
            x = vb.strip('')
            list1.append(float(x))
            with open('/home/pi/Desktop/M.T.E. /rawdata/voltbendraw.txt','a+') as f:
                time = '{:%y-%d-%m %H:%M:%S}'.format(datetime.datetime.now())
                f.write(str(time+','+vb))
        except:
            voltbending()
def main():
    global list1
    global i
    voltbending()
    if i>=10:
        ave = sum(list1)/len(list1)
        time = '{:%y-%d-%m %H:%M:%S}'.format(datetime.datetime.now())
        f = open('/home/pi/Desktop/M.T.E. /Data.txt','a+')
        f.write(time+','+str(ave)+'\n')
        list1=[]
        i=0 
    else:
        i=i+1
    
if __name__=="__main__":   
    while True:
        main()
        sleep(timer)

