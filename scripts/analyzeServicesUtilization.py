#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 14:32:27 2018

@author: mc
"""
import pandas as pd
import time

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return int(km*1000)

ssh_srvr = "d046373@polito.it@tlcdocker1.polito.it:"
src_path = "~/serviceUtilization/statistcs_for_each_city.csv"
dst_home = "~/Desktop/csExp/data/statistcs_for_each_city.csv"


def dowloadOutAnalysis():    
    src1 = ssh_srvr + src_path
    dst =  dst_home
    os.system('scp ' + src1 + dst)
    print ('scp ' + src1 + " " +dst)
    print ("File correctly downloaded")
    return

#dowloadOutAnalysis()
#stats = pd.read_csv(dst_home)
#stats = stats.rename( columns ={"Unnamed: 0":"city"})
#stats = stats.set_index("city")
##stats.to_csv("../data/AFS_boNumber.csv")
#
#print(stats.sort_values("AFS",ascending=False).iloc[0:5].index)
#print(stats.sort_values("noBookings",ascending=False).iloc[0:5].index)

a = time.time()
df = pd.read_pickle("/Users/mc/Desktop/csExp/dataVancouver/bookings_in_all_cities")
loading_time = time.time() - a
df = df[(df["city"] ==  "Vancouver")]
df["duration"] = df["final_time"] - df["init_time"]
df = df[(df["duration"] >= 120) & (df["duration"] <= 7200)]

df['coordinates'] = df.origin_destination.apply(lambda x : x['coordinates'])
df = df.drop('origin_destination',1)

df['start'] = df.coordinates.apply(lambda x : x[0])
df['end'] = df.coordinates.apply(lambda x : x[1])
df = df.drop('coordinates',1)

df['start_lon'] = df.start.apply(lambda x : float(x[0]) )
df['start_lat'] = df.start.apply(lambda x : float(x[1]) )
df = df.drop('start',1)

df['end_lon'] = df.end.apply(lambda x : float(x[0]) )
df['end_lat'] = df.end.apply(lambda x : float(x[1]) )
df = df.drop('end', 1)

df['distance'] = df.apply(lambda x : haversine(
        float(x['start_lon']),float(x['start_lat']),
        float(x['end_lon']), float(x['end_lat'])), axis=1
)
    
df = df[df["distance"] >= 500]



