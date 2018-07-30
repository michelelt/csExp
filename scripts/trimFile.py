#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 16:17:24 2018

@author: mc
"""

import pandas as pd

cities = ["Berlino", "Vancouver", "Milano"]

for c in cities:
    zzz = pd.read_csv("../../"+c+".csv")
    zzz = zzz.sort_values(by="NParkings", ascending=False)
    zzz = zzz.iloc[0:round(len(zzz)*0.3)]
    print (c, zzz.NParkings.max(), zzz.NParkings.min())
