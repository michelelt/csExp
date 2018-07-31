#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:41:21 2018

@author: mc
"""

from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd

with open ("../data/bookingsPerCity.raw", "r") as myfile:
    data=myfile.readlines()
    
for i in range(len(data)):
    if "/*" in data[i]:
        data[i]= ","
data[0] = "["
data.append("]")

f = open("../data/bookingsPerCity.json", "w")
for cell in data:
    f.write(cell)
f.close()
    
    
with open("../data/bookingsPerCity.json") as f:
    data = json.load(f)
    
cities = {}
for i in range(len(data)):
    cities[data[i]["_id"]] = data[i]['noBookings']
    
df = pd.DataFrame(index=cities.keys(), columns=["nob"])
for city in cities.keys():
    df.loc[city] = cities[city]
pd.set_option('display.float_format', '{:.2E}'.format)

x = range(len(data))
y = df["nob"]

fig, ax = plt.subplots()
ax.grid()
ax.bar(x,y)
ax.set_xticks(x)
ax.set_xticklabels(df.index, rotation='vertical')
ax.set_ylabel("Number of Bookings in one year")

plt.show()
plt.savefig("../plotAggregated/bookings_per_city.pdf", 
            format='pdf', bbox_inches = 'tight')