#!/usr/bin/env python3
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
from plotter import *
from DownloadFiles import *
import subprocess

### Constant Variables ###
path = "../data/"
### Constant Variables ###


simID = 6 
policy="Hybrid" 
algorithm="max-parking" 
zones=30
acs=4
tt=25
wt=1000000
utt=100
p=0

#file_name = downloadLog(simID, policy, algorithm, zones,acs,tt,wt,utt,p)
dataset = pd.read_csv(path+file_name, sep=";", skiprows=[0,1,2,3,4,5,6,7,8,9])
stationsID = downloadPlacementOrder(algorithm)[0:zones]
dataset = dataset[(dataset["Type"] == "e")
#                    &(dataset["ToRecharge"] == True)
                    &(dataset["Recharged"] == True)
                    ]
testSet = dataset.ZoneID.unique()



