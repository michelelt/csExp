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
from plotter import *
from DownloadFiles import *
import subprocess
from DownloadFiles import Downloader

from hdfs import InsecureClient


'''
rnd dld
'''
        
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
        
def downloadAllStuff(c2id) :
    
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
        lastS, outFileName =dld.dowloadOutAnalysis(c2id[city])
##
        dict_df[city] = pd.read_csv(path+outFileName, sep=" ")
        dict_df[city]["TravelWithPenlaty"] = computeTravelWithPenlaty(dict_df[city])
        log0_name = dld.downloadLogHDFS(simID=lastS, policy = "Hybrid", algorithm="max-parking", 
                    zones=20, acs=4, tt=25, wt=1000000, utt=100, p=0, city=city, kwh="")
##        
##
        log_df[city] = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
                                   skiprows=[0,1,2,3,4,5,6,7,8,9])
        

        dld.downloadBookingsPerHour(city)
        dld.downloadFleetPerDayPickle(city)
        dld.downloadBookingsInCsv(city)
        
    
    return cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df, plt_home, path, mytt

#
c2id = {"Torino":6, "Berlino":7, "Vancouver":8, "Milano":9}
#c2id = {"Torino":6}


metrics = ["Deaths", "AvgStationOccupancy", "AmountRechargePerc", "AvgSOC", 
           "ReroutePerc", "AvgWalkedDistance", "TravelWithPenlaty"]
metrics = ["AvgStationOccupancy", "AmountRechargePerc", "AvgSOC", 
           "ReroutePerc", "AvgWalkedDistance", "TravelWithPenlaty"]


#cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df,\
#plt_home, path, mytt =  downloadAllStuff(c2id)


#x,y = metricVaryingZonesAndAcs(dict_df["Torino"], 25, [0,25,50,75], "Deaths")
for city in c2id.keys():
#    mytt=25
    
#    cdfList_bdst[city] = computeCDF(log_df[city], "RentalsDistance", city) 
#    cdfList_bdur[city] = computeCDF(log_df[city], "RentalsDuration", city)
#    cdfList_pdur[city] = computeCDF(log_df[city], "ParkingsDuration", city)

#    plotCDF(cdfList_bdst[city], "RentalsDistance", save=False, city=city, path=plt_home)
#    plotCDF(cdfList_bdur[city], "RentalsDuration", save=False, city=city, path=plt_home)
#    plotCDF(cdfList_pdur[city], "ParkingsDuration", save=False, city=city, path=plt_home)

#
    plotDeathProb(init_df=dict_df[city], city=city, tt=mytt, acs=4,\
                  save=True, onlyFF=True, path="../plot"+city+"/")
#    
    plotMetricVsZones_policy(dict_df[city],city, acs=4, tt=mytt, utt=100, p=0,
                                 metric='Deaths', save=True, freeFloating=True, k=250, 
                                 path='../plot%s/'%city)
        
#        metricVsZones_kwhSupplied(dict_df['Torino'],
#                          city='Torino', 
#                          algorithm='max-parking',
#                          policy= 'Needed',
#                          metric=m,
#                          save=False, path='./../plotTorino/')
#   
#        metricVsZones_kwhSupplied(dict_df['Torino'],
#                          city='Torino', 
#                          algorithm='max-parking',
#                          policy= 'Hybrid',
#                          metric=m,
#                          save=False, path='./../plotTorino/')
#
#        metricVsZones_kwhSupplied(dict_df['Torino'],
#                          city='Torino', 
#                          algorithm='max-parking',
#                          policy= 'FreeFloating',
#                          metric=m,
#                          save=False, path='./../plotTorino/')
        

        
    for m in metrics:
        plotMetricVsZones_policy_p(init_df=dict_df[city], acs=4, tt=mytt, utt=100,
                                        plist=[0,25,50,75],metric=m, city=city, save=False,
                                        freeFloating=False, path="../plot"+city+"/cut_", ax="")
#        
##        

#fig, ax = plt.subplots(3,1, figsize=(36,6))
aggreatePerCityCDF(cdfList_bdst, "RentalsDistance", save=False, path="../plotAggregated/", ax=None)
aggreatePerCityCDF(cdfList_bdur, "RentalsDuration", save=False, path="../plotAggregated/", ax=None)
aggreatePerCityCDF(cdfList_pdur, "ParkingsDuration", save=False, path="../plotAggregated/", ax=None)
plotMetricVsZones_city(dict_df, False, path="../plotAggregated/")

#plt.savefig("../plotAggregated/CDF_1fig.pdf", bbox_inches = 'tight', format='pdf')


df = aggregateUtilizastionPerHour(['Vancouver', "Berlino", "Milano", "Torino"], save=False, 
                                   path='../plotAggregated/')
plotBookingsPerDay(save=False, path="../plotAggregated/")
        
plotFleetPerDay(save=False, path="../plotAggregated/")    
        
        

        
        
        

    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




