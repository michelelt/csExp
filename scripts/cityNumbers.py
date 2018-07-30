#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 14:56:00 2018

@author: mc
"""

import pymongo
import ssl
from math import *
import sys
import os
import pandas as pd
import numpy as np
import random
import csv
import time
import datetime

def setup_mongodb(CollectionName):   
    """"Setup mongodb session """    
    try:        
        client = pymongo.MongoClient('bigdatadb.polito.it',
                                     27017,
                                     ssl=True,
                                     ssl_cert_reqs=ssl.CERT_NONE) # server.local_bind_port is assigned local port                #client = pymongo.MongoClient()
        client.server_info()        
        db = client['carsharing'] #Choose the DB to use     
        db.authenticate('ictts', 'Ictts16!')#, mechanism='MONGODB-CR') #authentication         #car2go_debug_info = db['DebugInfo'] #Collection for Car2Go watch
        Collection = db[CollectionName] #Collection for Enjoy watch   
    except pymongo.errors.ServerSelectionTimeoutError as err:        
        print(err)    
    return Collection

collection = "PermanentParkings"
collection_parkings = setup_mongodb(collection)

def timeStamp2date(ts):
        return datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d')

def averageFleet(df,it,ft):

    finalDF = pd.DataFrame(index=df.city.unique())
    
    df["dateDay"] =  df.apply(lambda x : timeStamp2date(x["init_time"]), axis=1)
    tmp = df.groupby(["city", "dateDay"], as_index=True).plate.nunique().reset_index()
    tmp = tmp.groupby("city").sum()
    finalDF["AFS"] = tmp["plate"].div(len(df.dateDay.unique()))
    
    finalDF["noBookings"] = pd.DataFrame(df.groupby(["city"], as_index=True).size(), columns=["noBooking"])
    
    return finalDF



#bookings = collection_parkings.find({"city": city,
#                                     "init_time": {"$gt": initDate, 
#                                                   "$lt": finalDate}
#                                     })

i = 2
initDate="2017-9-5T00:00:00"
#finalDate="2017-11-2T00:00:00"
finalDate = "2017-9-6T00:00:00"
initTime = int(time.mktime(datetime.datetime.strptime(initDate, "%Y-%m-%dT%H:%M:%S").timetuple()))
finalTime = int(time.mktime(datetime.datetime.strptime(finalDate, "%Y-%m-%dT%H:%M:%S").timetuple()))
print (finalTime-initTime)
#bookings = collection_parkings.find({
#                                     "init_time": {"$gt": initTime, 
#                                                   "$lt": finalTime}
#                                     })
#
#bookings_df = pd.DataFrame(list(bookings))
#bookings_df = pd.read_pickle("../data/bookings_df")
cities = sorted(list(bookings_df.city.unique()))
print("Start Average Fleet")
#
#bookings_df["duration"] = bookings_df["final_time"] - bookings_df["init_time"]
#bookings_df = bookings_df[
#          (bookings_df.duration >= 300) 
#        & (bookings_df.duration <= 7200)
#        ]
#bookings_df["dateDay"] =  bookings_df.apply(lambda x : timeStamp2date(x["init_time"]), axis=1)
stats ={}
for city in cities :
    madrid = bookings_df[bookings_df.city == city]
    tmp = pd.DataFrame(columns = ["bookingsNo", "city"])
    tmp["bookingsNo"] = madrid.groupby("dateDay").count()["_id"]
    tmp["city"] = [city]*59
    stats[city] = tmp
    print (city, len(madrid.dateDay.unique()))


#zzz = averageFleet(bookings_df, initTime, finalTime)
#
#print(zzz.sort_values("AFS").index)
#print(zzz.sort_values("noBookings").index)
#
#
#zzz.to_csv("statistcs_for_each_city.csv")





