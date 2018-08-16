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
from plotter.header import*

from plotter.aggregateFleetPerDay import *         
from plotter.pdfChargingTimeVsAlgorithm import * 
from plotter.aggregatePerCityCDF import *           
from plotter.plotCDF import * 
from plotter.aggregateUtilizationPerHour import * 
from plotter.plotDeathProb import * 
from plotter.checkStartEndsAlternates import * 
from plotter.plotDeathsProb_policy import * 
from plotter.computeCDF import * 
from plotter.plotMetricVsTT_policy import * 
from plotter.aggregateMetricVsZones_city import * 
from plotter.maxTripCoordinates import * 
from plotter.plotMetricVsZones_policy import * 
from plotter.metricVaryingZonesAndACs_city import * 
from plotter.plotMetricVsZones_policy_p import *
from plotter.aggregateBookingsPerDay import *

from DownloadFiles import *
import subprocess
from DownloadFiles import Downloader

from hdfs import InsecureClient


'''
rnd dld
'''

def computeTravelWithPenlaty(df):
    k=150
    y = df["AvgWalkedDistance"]
    y = y.mul(df["ReroutePerc"])
    y = y + (df["AmountRechargePerc"] -  df["ReroutePerc"])*k
    y = y.div(100)
    return y
        
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
        print (city)
#       
#        dld.changeDstHome(city)
#        path = dld.dst_home
#        plt_home = dld.plt_home
#        mytt = 25
#        
##        if city == "Berlino":
##            mytt=50
#
#        dld.changeDstHome(city)
#        if c2id[city] <41: 
#            lastS, outFileName =dld.dowloadOutAnalysis(c2id[city])
#        else : 
#            lastS = c2id[city]
#            outFileName = "out_analysis_%s_cr.txt"%lastS
#
#        dict_df[city] = pd.read_csv(path+outFileName, sep=" ")
#        dict_df[city]["TravelWithPenlaty"] = computeTravelWithPenlaty(dict_df[city])
##       
#        if city in rnd2id.keys():
#            rndDf = pd.DataFrame()
#            for lastS_rnd in rnd2id[city]:
#                lastS_rnd, outFileName_rnd =dld.dowloadOutAnalysis(lastS_rnd)
#                tmp_rnd = pd.read_csv(path+outFileName_rnd, sep=" ")
#                tmp_rnd["TravelWithPenlaty"] = computeTravelWithPenlaty(tmp_rnd)
#                rndDf = tmp_rnd.append(tmp_rnd)
#                
#            df_rnd = rndDf
#            df_rnd = df_rnd[df_rnd["Policy"] == 'FreeFloating' ]
#            
#            
#            dfMean = df_rnd.groupby("Zones").mean()
#            dfMean["Provider"] = "car2go"
#            dfMean["Policy"] = "FreeFloating"
#            dfMean["Algorithm"] = "Mean Random"
#            dfMean = dfMean.reset_index()
#            dfMean = dfMean[dfMean.Zones.isin(dict_df[city].Zones)]
#        
##            return dfMean
##            dfMin = df_rnd.groupby("Zones").min()
##            dfMin["Provider"] = "car2go"
##            dfMin["Policy"] = "FreeFloating"
##            dfMin["Algorithm"] = "Mean Random"
##            dfMin = dfMin.reset_index()
##            dfMin = dfMin[dfMin.Zones.isin(dict_df[city].Zones)]
##
###            dict_df[city] = dict_df[city].append([dfMean], ignore_index=True)
#        print ("LS", lastS)
#        if lastS < 32:
#            if lastS < 17:
#                print ('dowload from server')
#                log0_name = dld.downloadLogHDFS(simID=lastS, policy = "Hybrid", algorithm="max-parking", 
#                            zones=22, acs=4, tt=25, wt=1000000, utt=100, p=0, city=city, fromSSD =False, kwh="")
#                print (log0_name)
#                
#            else:
#                log0_name = dld.downloadLogHDFS(simID=lastS, policy = "Hybrid", algorithm="max-parking", 
#                zones=20, acs=4, tt=25, wt=1000000, utt=100, p=0, city=city,  fromSSD =True, kwh=2)
#            
#            log_df[city] = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
#                                       skiprow=[0,1,2,3,4,5,6,7,8,9])
##        

#        dld.downloadBookingsPerHour(city)
        dld.downloadBookingsPerDay(city)
    
    return cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df, plt_home, path, mytt

def uploadFromSSDallStuff(c2id, rnd2id):
    dict_df={}
    log_df = {}
    cdfList_bdst = {}
    cdfList_bdur = {}
    cdfList_pdur = {}
    
    log0_name_dict={
            'Torino':    'car2go_Hybrid_max-parking_21_4_25_1000000_100_0.txt',
            'Berlino':   'car2go_Hybrid_max-parking_20_4_25_1000000_100_0.txt',
            'Milano':    'car2go_Hybrid_max-parking_20_4_25_1000000_100_0.txt',
            'Vancouver': 'car2go_Hybrid_max-parking_22_4_25_1000000_100_0.txt'
            }
    
    for city in c2id.keys():
        print (city)
        lastS = c2id[city]
        path='../data%s/'%city
        outFileName = "out_analysis_%s_cr.txt"%lastS

        dict_df[city] = pd.read_csv(path+outFileName, sep=" ")
        dict_df[city]["TravelWithPenlaty"] = computeTravelWithPenlaty(dict_df[city])
#       
        if city in rnd2id.keys():
            rndDf = pd.DataFrame()
            for lastS_rnd in rnd2id[city]:
                print('mount_rnd')
                outFileName_rnd = "out_analysis_%s_cr.txt"%lastS_rnd
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
            
            dict_df[city] = dict_df[city].append([dfMean], ignore_index=True)

            
        log0_name = log0_name_dict[city]
        
        log_df[city] = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
                                   skiprows=[0,1,2,3,4,5,6,7,8,9])
            
    mytt=25
            
    return cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df, mytt


#
c2id = {"Vancouver":8, "Berlino":7,"Milano":9, "Torino":6}
rnd2id = {"Torino":[11,12,13,14,15],
          "Vancouver":[17,18,19,20,21], 
          "Berlino":[22,23,24,25,26], 
          "Milano":[27,28,29,30,31]
          }
#rnd2id = {}


#c2id = {"Vancouver":8}

metrics = ["Deaths","AvgStationOccupancy", "AmountRechargePerc", "AvgSOC", 
           "ReroutePerc", "AvgWalkedDistance", "TravelWithPenlaty"]

metrics=['AmountRechargePerc','ReroutePerc', 'AvgWalkedDistance']

#
#cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df,\
#plt_home, path, mytt =  downloadAllStuff(c2id, rnd2id)
cdfList_bdst, cdfList_bdur, cdfList_pdur,\
 dict_df, log_df, mytt = uploadFromSSDallStuff(c2id, rnd2id)


#for city in c2id.keys():
#    
#    cdfList_bdst[city] = computeCDF(log_df[city], "RentalsDistance", city) 
#    cdfList_bdur[city] = computeCDF(log_df[city], "RentalsDuration", city)
#    cdfList_pdur[city] = computeCDF(log_df[city], "ParkingsDuration", city)
#    
#    plotDeathProb(dict_df[city], city=city, tt=25, acs=4, save=False, onlyFF=True, 
#                  path="../plot%s/"%city)
#
#    
#    plotMetricVsZones_policy(dict_df[city],city, acs=4, tt=mytt, utt=100, p=0,
#                                 metric='Deaths', save=False, freeFloating=True, k=250, 
#                                 path='../plot%s/'%city)
#
#    
#    for m in metrics:
#        print (m)
#        plotMetricVsZones_policy_p(init_df=dict_df[city], acs=4, tt=25, utt=100,
#                                        plist=[75,50,25,0],metric=m, city=city, save=False,
#                                        freeFloating=False, path="../plot"+city+"/cut_", ax="")
###        
####        
##
#aggreatePerCityCDF(cdfList_bdst, "RentalsDistance", save=True, path="../plotAggregated/", ax=None)
#aggreatePerCityCDF(cdfList_bdur, "RentalsDuration", save=True, path="../plotAggregated/", ax=None)
#aggreatePerCityCDF(cdfList_pdur, "ParkingsDuration", save=True, path="../plotAggregated/", ax=None)
#aggregateMetricVsZones_city(dict_df, save=True, path="../plotAggregated/")
#aggregateUtilizastionPerHour(['Vancouver', "Berlino", "Milano", "Torino"], 
#                             save=True, path='../plotAggregated/')

aggregateBookingsPerDay(save=True, path="../plotAggregated/")
aggregateFleetPerDay(save=True, path="../plotAggregated/")

  
    
c2id = {"Torino":41, "Berlino":42, "Milano":43, "Vancouver":44}
rnd2id={}
#cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df,\
#plt_home, path, mytt =  downloadAllStuff(c2id, rnd2id)
cdfList_bdst, cdfList_bdur, cdfList_pdur,\
dict_df, log_df, mytt = uploadFromSSDallStuff(c2id, rnd2id)

metricVaryingZonesAndAcs_city(dict_df, 'Deaths', save=False, path='../plotAggregated/50_')
#metricVaryingZonesAndAcs_city(dict_df, 'AvgTimeInStation', save=True, path='../plotAggregated/50_')
#metricVaryingZonesAndAcs_city(dict_df, 'ReroutePerc', save=True, path='../plotAggregated/50_')
#metricVaryingZonesAndAcs_city(dict_df, 'AvgWalkedDistance', save=True, path='../plotAggregated/50_')









        
        


    

    
    
    
    
    
    
    
    
    




