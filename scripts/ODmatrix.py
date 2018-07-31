#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import pandas as pd
from DownloadFiles import Downloader

maxLon = 13.54876
maxLat = 52.576763
minLat = 52.388954
minLon = 13.181448

shiftLat500m = 0.0045
shiftLon500m = 0.00637

Ncolumns = 58
Nrows = 42
def coordinates_to_index(coords):
    
    lon = coords[0]
    lat = coords[1]
    
    ind = int((lat - minLat) / ShiftLat) * NColumns + \
          int((lon - minLon) / ShiftLon)
    if(ind<=GlobalVar.MaxIndex): 
        return int(ind)

    return -1



def zonesID(city):
#    c2id={"Vancouver":510, "Torino":261, "Berlino":833, "Milano":549}
#    if city in c2id.keys():
#        return c2id[city]
    

#    command = 'ssh -t d046373@polito.it@tlcdocker1.polito.it wc -l %s_sim3.0/input/car2go_ValidZones.csv' % city
    command = "ssh -t d046373@polito.it@tlcdocker1.polito.it \"awk -F\',\' \'{if (\\$1) print \\$1}\' Berlino_sim3.0/input/car2go_ValidZones.csv\""
    zones = str(subprocess.check_output(command, shell=True))[6:].replace("\\", "").replace("'", "")
    zones = zones.split("n")[0:-1]
    zones = list(map(int, zones))
    
    
    return zones

zones = zonesID("Berlino")
ODmatrix = pd.DataFrame(columns=zones, index=zones)
ODmatrix[:] = 0

lastS = 10
dld = Downloader("Berlino")
#log0_name = dld.downloadLog(lastS, "FreeFloating", "max-parking", 25,4,-1, 1000000,100,0)
df = pd.read_csv(dld.dst_home+log0_name, sep=";", skiprows=[0,1,2,3,4,5,6,7,8,9])

df = df.sort_values(by=["ID", "Stamp"]).iloc[:].reset_index()
org = df[df["Type"] == "s"].reset_index()
dst = df[df["Type"] == "e"].reset_index()
couple = pd.DataFrame()
couple["O"] = org.ZoneID
couple["D"] = dst.ZoneID
couple["OD"] =  org.ZoneID.astype(str) + "," +dst.ZoneID.astype(str)
count = couple.OD.value_counts()
count = pd.DataFrame(count).reset_index().rename(columns={"index":"COD"})
count.COD.astype(str)
count["O"] = count.COD.str.split(",", expand=True)[0].astype(int)
count["D"] = count.COD.str.split(",", expand=True)[1].astype(int)

ODmatrix.loc[count.O, count.D] = count.OD











