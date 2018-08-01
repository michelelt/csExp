#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 17:18:37 2018

@author: mc
"""

import os
path = '../plotToExport/'
#print(os.listdir(path))

plotNames = ['cut_Vancouver_AvgWalkedDistanceVsZones_Policy_44_tt-25_100_4.pdf', 
             'BerlinoMaxParking.pdf', '.DS_Store', 'VancouverAvgParking.pdf', 
             'BerlinoAvgTime.pdf', 'CDF_aggregate_RentalsDistance.pdf', 
             'bookings_per_day.pdf', 'Torino_zonesVsDeaths_algorithms_acs-4_tt-25_policy-FreeFloating.pdf', 
             'DeathsVsZones_city.pdf', 'Berlino_zonesVsDeaths_algorithms_acs-4_tt-25_policy-FreeFloating.pdf', 
             'cut_Berlino_AmountRechargePercVsZones_Policy_44_tt-25_100_4.pdf', 'aggBookginfsPerHour.pdf', 
             'VancouverMaxParking.pdf', 'Milano_zonesVsDeaths_algorithms_acs-4_tt-25_policy-FreeFloating.pdf', 
             'cut_Milano_AmountRechargePercVsZones_Policy_44_tt-25_100_4.pdf', 
             'Berlino_DeathsVsZones_Policy_44_tt-25_100_4.pdf', 'CDF_aggregate_RentalsDuration.pdf', 
             'cut_Torino_AmountRechargePercVsZones_Policy_44_tt-25_100_4.pdf',
             'Vancouver_zonesVsDeaths_algorithms_acs-4_tt-25_policy-FreeFloating.pdf', 
             'CDF_aggregate_ParkingsDuration.pdf', 'cut_Torino_ReroutePercVsZones_Policy_44_tt-25_100_4.pdf', 
             'cut_Berlino_AvgWalkedDistanceVsZones_Policy_44_tt-25_100_4.pdf', 
             'Vancouver_DeathsVsZones_Policy_44_tt-25_100_4.pdf', 'fleet_per_day.pdf', 
             'cut_Milano_AvgWalkedDistanceVsZones_Policy_44_tt-25_100_4.pdf', 
             'cut_Vancouver_TravelWithPenlatyVsZones_Policy_44_tt-25_100_4.pdf', 
             'cut_Torino_AvgWalkedDistanceVsZones_Policy_44_tt-25_100_4.pdf', 
             'cut_Milano_ReroutePercVsZones_Policy_44_tt-25_100_4.pdf', 
             'cut_Vancouver_AvgSOCVsZones_Policy_44_tt-25_100_4.pdf', 
             'cut_Vancouver_AmountRechargePercVsZones_Policy_44_tt-25_100_4.pdf', 
             'cut_Berlino_ReroutePercVsZones_Policy_44_tt-25_100_4.pdf', 
             'cut_Vancouver_ReroutePercVsZones_Policy_44_tt-25_100_4.pdf']

dirList = ['plotAggregated/', 'plotTorino/', 'plotBerlino/', 'plotMilano/', 'plotVancouver/']

for myDir in dirList:
    plotInDir = os.listdir("../"+myDir)
    for plot in plotNames:
        if plot in plotInDir:
            os.system("cp %s %s"%( "../"+myDir+plot, path+plot))
        
