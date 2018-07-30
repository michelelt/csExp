#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 10:49:33 2018

@author: mc
"""
#
import sys
import os
import subprocess
import time
p = os.path.abspath('..')
sys.path.append(p+"/")
sys.path.append(p+"/Simulator/")

import datetime as datetime
import pickle
import multiprocessing
from multiprocessing import Process
import subprocess


def validSimulation(BestEffort, tankThreshold_valid, upperTankThreshold_valid, pThresholdCheck) :
          
   #Station Based and IMP2
    if tankThreshold_valid == 100:
        return False
        
    #IMP1
    if BestEffort==False and tankThreshold_valid==-1 :
        return False

    #Needed only p = 0, utt=100
    if BestEffort == False \
        and tankThreshold_valid >= 0 \
        and tankThreshold_valid < 100 \
        and (pThresholdCheck != 0.0 or upperTankThreshold_valid != 100) :
        #print(BestEffort, tankThreshold, p, upperTankThreshold)
        return False
    
    ##free Floating only utt=100 and p=0
    if BestEffort == True \
        and tankThreshold_valid == -1 \
        and (upperTankThreshold_valid != 100 or pThresholdCheck != 0.0) :
        #print(BestEffort, tankThreshold, p, upperTankThreshold)
        return False

    return True



f1 = open("/Users/mc/Desktop/csExp/data/packets.txt", 'r')
f2 = open("/Users/mc/Desktop/csExp/data/packets2.txt", 'w')
for line in f1:
     line2=[]
     line = line.split("\t")
     for i in line:
         if len(i) > 1 :
            line2.append(i)
            line2.append(";")
     line2 = line2[:-1]
     myStr=""
     for element in line2:
         myStr = myStr + element
     print (myStr)
     f2.write(myStr)
f1.close()
f2.close()

df = pd.read_csv("/Users/mc/Desktop/csExp/data/packets2.txt", sep=";")


