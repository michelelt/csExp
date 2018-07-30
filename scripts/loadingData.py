  # -*- coding: utf-8 -*-
import numpy as np
import pickle
import sys
import os

p = os.path.abspath('..')
sys.path.append(p+"/")

import time
import datetime
import pandas as pd

import matplotlib.pyplot as plt
from plotter.header import *
from plotter.plotter import *
from DownloadFiles import *
import subprocess
from DownloadFiles import Downloader

from hdfs import InsecureClient




def downloadAllStuff(c2id, fromSSD) :
    
    dict_df={}
    log_df = {}
    dld = Downloader("Berlino")
    cdfList_bdst = {}
    cdfList_bdur = {}
    cdfList_pdur = {}
    
    for city in c2id.keys():
        
        dld.changeDstHome(city)
        path = dld.dst_home
        plt_home = dld.plt_home
        mytt = 25
        
        if city == "Berlino":
            mytt=50

        dld.changeDstHome(city)
        if fromSSD == False:
            lastS, outFileName = dld.dowloadOutAnalysis(c2id[city])
        else:
            lastS = c2id[city]
            outFileName = "out_analysis_%d_cr.txt"% lastS

        dict_df[city] = pd.read_csv(path+outFileName, sep=" ")
#        dict_df[city]["TravelWithPenlaty"] = computeTravelWithPenlaty(dict_df[city])
        
#        log0_name = dld.downloadLogHDFS(simID=lastS, policy = "FreeFloating", algorithm="max-parking", 
#                    zones=21, acs=4, tt=-1, wt=1000000, utt=100, p=0, city=city)

#        log_df[city] = pd.read_csv(path+log0_name, sep=";", skiprows=[0,1,2,3,4,5,6,7,8,9])
#        dld.downloadBookingsPerHour()
        
    
    return cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df, plt_home, path, mytt


c2id = {"Torino":6, "Berlino":7, "Vancouver":8, "Milano": 9}
#c2id = {"Milano":9}



metrics = ["Deaths", "AvgStationOccupancy", "AmountRechargePerc", "AvgSOC", 
           "ReroutePerc", "AvgWalkedDistance", "TravelWithPenlaty"]
#metrics = ["Deaths"]

#
cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df,\
plt_home, path, mytt =  downloadAllStuff(c2id, True)
#

#x,y = metricVaryingZonesAndAcs(dict_df["Torino"], 25, [0,25,50,75], "Deaths")
for city in c2id.keys():
#    
##    if city != "Torino":
##        mytt = 25
#
#    cdfList_bdst[city] = computeCDF(log_df[city], "RentalsDistance", city) 
#    cdfList_bdur[city] = computeCDF(log_df[city], "RentalsDuration", city)
#    cdfList_pdur[city] = computeCDF(log_df[city], "ParkingsDuration", city)
#
#    plotCDF(cdfList_bdst[city], "RentalsDistance", save=False, city=city, path=plt_home)
#    plotCDF(cdfList_bdur[city], "RentalsDuration", save=False, city=city, path=plt_home)
#    plotCDF(cdfList_pdur[city], "ParkingsDuration", save=False, city=city, path=plt_home)
#
#
#    plotDeathProb(init_df=dict_df[city], city=city, tt=mytt, acs=4, 
#                  save=False, onlyFF=True)
#    
#    zzz = plotMetricVsZones_policy(init_df=dict_df[city], city=city,
#                             acs=4, tt=mytt, utt=100, p=[0, 25, 50,75],
#                             metric="Deaths", save=False, freeFloating=True, k=125, path="")
    for m in metrics :
#        
#        metricVaryingZonesAndAcs(dict_df2[city], 72, 25, [0,25,50,75], m, ax[1])
        plotMetricVsZones_policy_p(init_df=dict_df[city], acs=4, tt=mytt, utt=100, 
                                   plist=[0,25,50,75], metric=m, city=city, save=False, 
                                   freeFloating=False, path=plt_home, ax=None)
#        
##        

#aggreatePerCityCDF(cdfList_bdst, "RentalsDistance", save=True, path="/Users/mc/Desktop/csExp/plotAggregated/")
#aggreatePerCityCDF(cdfList_bdur, "RentalsDuration", save=True, path="/Users/mc/Desktop/csExp/plotAggregated/")
#aggreatePerCityCDF(cdfList_pdur, "ParkingsDuration", save=True, path="/Users/mc/Desktop/csExp/plotAggregated/")
#df = aggregateUtilizastionPerHour(list(c2id.keys()), save=True, path="")




#rndDf = pd.DataFrame()
#for lastS in [11,12,13, 14, 15]:
#    c2id2 = {"Torino":lastS}
#    cdfList_bdst2, cdfList_bdur2, cdfList_pdur2, dict_df2, log_df2,\
#    plt_home2, path2, mytt2 =  downloadAllStuff(c2id2)
#    rndDf = rndDf.append(dict_df["Torino"])
#cdfList_bdst2, cdfList_bdur2, cdfList_pdur2, dict_df2, log_df2, plt_home2, path2, mytt2 =  downloadAllStuff(c2id2)

#validZones =str(list( dict_df["Torino"].Zones.unique()))

#df = rndDf
#df = df[df["Policy"] == 'FreeFloating' ]
#
#dfMean = df.groupby("Zones").mean()
#dfMean["Provider"] = "car2go"
#dfMean["Policy"] = "FreeFloating"
#dfMean["Algorithm"] = "Mean Random"
#dfMean = dfMean.reset_index()
#
#dfMin = df.groupby("Zones").min()
#dfMin["Provider"] = "car2go"
#dfMin["Policy"] = "FreeFloating"
#dfMin["Algorithm"] = "Min Random"
#dfMin = dfMin.reset_index()
#
#
#
#q1 = dfFFmp["Deaths"] 
#q2 = dfMin["Deaths"]
#
#
#dict_df["Torino"] = dict_df["Torino"].append([dfMean], ignore_index=True)
#df = dict_df["Torino"]
#
#df = df [df["Policy"]!= "max-time"]
#zzz = plotDeathProb(init_df=df, city="Torino", tt=mytt, acs=4, 
#              save=True, onlyFF=True, path=plt_home)
