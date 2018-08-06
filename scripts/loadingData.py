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
        
def downloadAllStuff(c2id,rnd2id) :
    
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
        
        if city in rnd2id.keys():
            rndDf = pd.DataFrame()
            for lastS_rnd in rnd2id[city]:
                lastS_rnd, outFileName_rnd =dld.dowloadOutAnalysis(lastS_rnd)
                tmp_rnd = pd.read_csv(path+outFileName_rnd, sep=" ")
                tmp_rnd["TravelWithPenlaty"] = computeTravelWithPenlaty(tmp_rnd)
                rndDf = tmp_rnd.append(tmp_rnd)
                
            df_rnd = rndDf
            df_rnd = df_rnd[df_rnd["Policy"] == 'FreeFloating' ]
            
            
            dfMean = df_rnd.groupby("Zones").mean()
            dfMean["Provider"] = "car2go"
            dfMean["Policy"] = "FreeFloating"
            dfMean["Algorithm"] = "Mean Random"
            dfMean = dfMean.reset_index()
            dfMean = dfMean[dfMean.Zones.isin(dict_df[city].Zones)]
        
    ##        return dfMean
    #        dfMin = df_rnd.groupby("Zones").min()
    #        dfMin["Provider"] = "car2go"
    #        dfMin["Policy"] = "FreeFloating"
    #        dfMin["Algorithm"] = "Mean Random"
    #        dfMin = dfMin.reset_index()
    #        dfMin = dfMin[dfMin.Zones.isin(dict_df[city].Zones)]
#
            dict_df[city] = dict_df[city].append([dfMean], ignore_index=True)
    
#        if lastS < 17:
#            log0_name = dld.downloadLogHDFS(simID=lastS, policy = "Hybrid", algorithm="max-parking", 
#                        zones=20, acs=4, tt=25, wt=1000000, utt=100, p=0, city=city, kwh="")
#        else:
#            log0_name = dld.downloadLogHDFS(simID=lastS, policy = "Hybrid", algorithm="max-parking", 
#            zones=20, acs=4, tt=25, wt=1000000, utt=100, p=0, city=city, kwh=2)
###        
###
#        log_df[city] = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
#                                   skiprows=[0,1,2,3,4,5,6,7,8,9])
        

#        dld.downloadBookingsPerHour(city)
#        dld.downloadFleetPerDayPickle(city)
#        dld.downloadBookingsInCsv(city)
        
    
    return cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df, plt_home, path, mytt

#
c2id = {"Vancouver":8, "Berlino":7,"Milano":9, "Torino":6}
rnd2id = {"Torino":[11,12,13,14,15],
          "Vancouver":[17,18,19,20,21], 
          "Berlino":[22,23,24,25,26], 
          "Milano":[27,29,30,31,32]
          }
 
metrics = ["Deaths", "AvgStationOccupancy", "AmountRechargePerc", "AvgSOC", 
           "ReroutePerc", "AvgWalkedDistance", "TravelWithPenlaty"]
metrics = ["AvgStationOccupancy", "AmountRechargePerc", "AvgSOC", 
           "ReroutePerc", "AvgWalkedDistance", "TravelWithPenlaty"]
metrics=["Deaths"]


#cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df,\
#plt_home, path, mytt =  downloadAllStuff(c2id, rnd2id)

#rnd = downloadAllStuff(c2id, rnd2id)


##x,y = metricVaryingZonesAndAcs(dict_df["Torino"], 25, [0,25,50,75], "Deaths")
#for city in c2id.keys():
#    
#    cdfList_bdst[city] = computeCDF(log_df[city], "RentalsDistance", city) 
#    cdfList_bdur[city] = computeCDF(log_df[city], "RentalsDuration", city)
#    cdfList_pdur[city] = computeCDF(log_df[city], "ParkingsDuration", city)

#    plotCDF(cdfList_bdst[city], "RentalsDistance", save=False, city=city, path=plt_home)
#    plotCDF(cdfList_bdur[city], "RentalsDuration", save=False, city=city, path=plt_home)
#    plotCDF(cdfList_pdur[city], "ParkingsDuration", save=False, city=city, path=plt_home)

#
#    plotDeathProb(init_df=dict_df[city], city=city, tt=mytt, acs=4,\
#                  save=True, onlyFF=True, path="../plot"+city+"/")
    
#    plotMetricVsZones_policy(dict_df[city],city, acs=4, tt=mytt, utt=100, p=0,
#                                 metric='Deaths', save=False, freeFloating=True, k=250, 
#                                 path='../plot%s/'%city)
        
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
        

#        
#    for m in metrics:
#        plotMetricVsZones_policy_p(init_df=dict_df[city], acs=4, tt=mytt, utt=100,
#                                        plist=[0,25,50,75],metric=m, city=city, save=False,
#                                        freeFloating=False, path="../plot"+city+"/cut_", ax="")
##        
###        
#
#aggreatePerCityCDF(cdfList_bdst, "RentalsDistance", save=True, path="../plotAggregated/", ax=None)
#aggreatePerCityCDF(cdfList_bdur, "RentalsDuration", save=True, path="../plotAggregated/", ax=None)
#aggreatePerCityCDF(cdfList_pdur, "ParkingsDuration", save=True, path="../plotAggregated/", ax=None)
#plotMetricVsZones_city(dict_df, save=True, path="../plotAggregated/")
#aggregateUtilizastionPerHour(['Vancouver', "Berlino", "Milano", "Torino"], save=True, path='../plotAggregated/')
#plotBookingsPerDay(save=True, path="../plotAggregated/")
#plotFleetPerDay(save=True, path="../plotAggregated/")

#os.system("copyFinalPlots.py")
#        
        
c2id = {"Vancouver":34, "Berlino":33,"Milano":35, "Torino":32}
rnd2id={}
cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df,\
plt_home, path, mytt =  downloadAllStuff(c2id, rnd2id)
metricVaryingZonesAndAcs(dict_df, "Deaths",save=True, path='../plotAggregated/')


        
        

    

    

    
    
    
    
    
    
    
    
    




