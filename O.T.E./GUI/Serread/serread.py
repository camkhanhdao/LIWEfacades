#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 09:41:28 2017
Editted on Tue May 8 
@author: Zachary Taylor
@editor: Cam Khanh Dao
"""
import pandas as pd
import VoltTemp
import Humidity
import Irradiance
import datetime
from time import sleep
import upload_to_drive
import upload_to_drive_rawdata
import credentialsPi
import sys
sys.path.append(credentialsPi.get_path("sys"))


precision = 2 # how many decimal places you want in the readings
timer = 1  # reading delay

Cell1List = []
Cell2List = []
Cell3List = []
Cell4List = []
TempList  = []
HumList   = []
IrrList   = []
i = 0
Wattsum = 0

         
def voltchop():
    
    vt = VoltTemp.main()
    if len(vt) > 1:
        try:
            f = open(credentialsPi.get_path("voltchop"), 'a+')
            #time = '{:%y-%d-%m %H:%M:%S}'.format(datetime.datetime.now())  
            time = pd.Timestamp.now()
            #data = str(time+', '+vt)
            f.write(str(time))
            f.write(vt+'\n')
            upload_to_drive_rawdata.main()
            x, y, w, z, t= vt.split(',')
            Cell1List.append(float(x))
            Cell2List.append(float(y))
            Cell3List.append(float(w))
            Cell4List.append(float(z))
            TempList.append(float(t))
        except:
            voltchop()
                    
def humchop():

    hum = Humidity.main() 

    if len(hum) > 1:
        try:
            f = open(credentialsPi.get_path("humchop"), 'a+')
            time = pd.Timestamp.now()
            #time = '{:%y-%d-%m %H:%M:%S}'.format(datetime.datetime.now())  
            #data = str(time+', '+hum)
            data = str(hum)
            f.write(str(time))
            f.write(data+'\n')
            upload_to_drive_rawdata.main()
            x = hum[:-8]
            HumList.append(float(x))
        except:
            humchop()
        
def irrchop():
    
    irr = Irradiance.main()
    
    if len(irr)>1:
         try:
            f = open(credentialsPi.get_path("irrchop"), 'a+')
            #time = '{:%y-%d-%m %H:%M:%S}'.format(datetime.datetime.now())  
            time = pd.Timestamp.now()
            #data = str(time+', '+irr)
            data = str(irr)
            f.write(str(time))
            f.write(data+'\n')
            upload_to_drive_rawdata.main()
            irrchopped = irr[:-10]
            IrrList.append(float(irrchopped))       
         except Exception:
            irrchop()

                
def main():
    global Cell1List
    global Cell2List
    global Cell3List
    global Cell4List
    global TempList
    global HumList
    global IrrList
    global i
    global Wattsum
    
    voltchop()
    humchop()
    irrchop()
    
    if i >= 10:
   
        cell1ave = sum(Cell1List)/len(Cell1List)
        cell1ave = round(cell1ave, precision)
        cell2ave = sum(Cell2List)/len(Cell2List)
        cell2ave = round(cell2ave, precision)
        cell3ave = sum(Cell3List)/len(Cell3List)
        cell3ave = round(cell3ave, precision)
        cell4ave = sum(Cell4List)/len(Cell4List)
        cell4ave = round(cell4ave, precision)
        tempave = sum(TempList)/len(TempList)
        tempave = round(tempave, precision)
        humave = sum(HumList)/len(HumList)
        humave = round(humave, precision)
        irrave = sum(IrrList)/len(IrrList)
        irrave = round(irrave, precision)
        Wattsum += irrave
        #time = '{:%y-%d-%m %H:%M:%S}'.format(datetime.datetime.now())
        time = pd.Timestamp.now()
        c = str([cell1ave, cell2ave, cell3ave, cell4ave, tempave, humave, irrave, Wattsum])
        c = c[1:-1]
        f = open(credentialsPi.get_path("data"), 'a+')
        f.write(str(time))
        #f.write(time+','+c+"\n")
        f.write(c+'\n')
        Cell1List = []
        Cell2List = []
        Cell3List = []
        Cell4List = []
        TempList  = []
        HumList   = []
        IrrList   = []
        i = 0
        upload_to_drive.main()
        
    else:
        i += 1


if __name__ == "__main__":
    while True:
        main()
        sleep(timer)
