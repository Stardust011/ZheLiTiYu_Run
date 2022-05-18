import random
from types import ClassMethodDescriptorType
from typing import cast
import geopy
import os
import webbrowser
from geopy import distance

if input("open browser?[o]")=="o":
    webbrowser.open(r'http://api.map.baidu.com/lbsapi/getpoint/')
f = open("gps.txt","w")
lin = input()
loc = lin.split(",")
lat1 = float(loc[1])
lon1 = float(loc[0])
f.write(str(lon1)+' '+str(lat1))
dis = 0
while True:
    lin = input()
    if lin == "":
        break
    loc = lin.split(",")
    lat2 = float(loc[1])
    lon2 = float(loc[0])
    d = distance.distance((lat1, lon1),(lat2, lon2)).meters
    c = d//10
    if c==0:
        lat1 = lat2
        lon1 = lon2
        continue
    lat_s = (lat2-lat1)/c
    lon_s = (lon2-lon1)/c
    i=0
    lastlat = lat1
    lastlon = lon1
    while i<c:
        latf = lat1 + lat_s * i + random.uniform(-0.00000500, 0.00000500)
        lonf = lon1 + lon_s * i + random.uniform(-0.00000500, 0.00000500)
        ds = distance.distance((latf, lonf),(lastlat, lastlon)).meters
        f.write('\n'+str(lonf) + ' ' + str(latf))
        dis = dis + ds
        lastlat = latf
        lastlon = lonf
        i = i+1
    lat1 = lat2
    lon1 = lon2
    print(dis)
f.close()