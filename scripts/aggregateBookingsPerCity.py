#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 18:58:40 2018

@author: mc
"""

import pandas as pd
import pymongo
import ssl
import datetime
import time
from math import radians, cos, sin, asin, sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib




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


def query_bookings(city, start, end):
    car2goBookings = setup_mongodb("PermanentBookings")

    return car2goBookings.find(
            {'init_date':
                           {
                               '$gt': start,
                               '$lt': end
                           },
            'city' : city,
#            "driving.distance" : {"$ne":-1} 
            }).sort([("_id", 1)]) 
  
        
def query_bookings_df(city, start, end):
        books_cursor = query_bookings(city, start, end)
        if books_cursor         == "err from cursor": return "err"
        if books_cursor.count() == 0                : return "Query Empty!"
        else :
#            print books_cursor.count()
#            bookings_df = pd.DataFrame(columns = pd.Series(books_cursor.next()).index)
            print (1)
            bookings_df = pd.DataFrame(list(books_cursor))
            
            print (2)
            bookings_df['duration_dr'] = bookings_df.driving.apply(lambda x: float(x['duration']/60))
            bookings_df['distance_dr'] = bookings_df.driving.apply(lambda x: x['distance'])
            bookings_df = bookings_df.drop('driving',1)
            
            print (3)
            bookings_df['type'] = bookings_df.origin_destination.apply(lambda x : x['type'])
            bookings_df['coordinates'] = bookings_df.origin_destination.apply(lambda x : x['coordinates'])
            bookings_df = bookings_df.drop('origin_destination',1)
            
            print (4)
            bookings_df['start'] = bookings_df.coordinates.apply(lambda x : x[0])
            bookings_df['end'] = bookings_df.coordinates.apply(lambda x : x[1])
            bookings_df = bookings_df.drop('coordinates',1)
            
            print (5)
            bookings_df['start_lon'] = bookings_df.start.apply(lambda x : float(x[0]) )
            bookings_df['start_lat'] = bookings_df.start.apply(lambda x : float(x[1]) )
            bookings_df = bookings_df.drop('start',1)
            
            print (6)
            bookings_df['end_lon'] = bookings_df.end.apply(lambda x : float(x[0]) )
            bookings_df['end_lat'] = bookings_df.end.apply(lambda x : float(x[1]) )
            bookings_df = bookings_df.drop('end', 1)
            
            print (7)
            bookings_df['distance'] = bookings_df.apply(lambda x : haversine(
                    float(x['start_lon']),float(x['start_lat']),
                    float(x['end_lon']), float(x['end_lat'])), axis=1
            )
            print (8)
            bookings_df['duration'] = bookings_df.final_date - bookings_df.init_date 
            bookings_df['duration'] = bookings_df['duration'].apply(lambda x: x.days*24*60 + x.seconds/60)
            
            print (9)
            bookings_df['duration_pt'] = bookings_df.public_transport.apply(lambda x : x['duration'] )
            bookings_df['distance_pt'] = bookings_df.public_transport.apply(lambda x : x['distance'] )
            bookings_df['arrival_date_pt'] = bookings_df.public_transport.apply(lambda x : x['arrival_date'] )
            bookings_df['arrival_time_pt'] = bookings_df.public_transport.apply(lambda x : x['arrival_time'] )
            bookings_df = bookings_df.drop('public_transport',1)
            
            if city == "Torino":
                bookings_df = bookings_df[ bookings_df["start_lon"] <= 7.8]  

            return bookings_df
        
        
def computeCDF(series, metric, city):
    
    y_set = series
    max_ticks = series.max()
    print (max_ticks, "[m]")
    
    values = y_set
    sorted_data = np.sort(values)
    yvals=np.arange(len(values))/float(len(values)-1)
    print("Sorted data len:", len(sorted_data))
    
    return [sorted_data, yvals]
    

def plotCDF(sorted_data, yvals, metric, save=False, city="", path="" ):
    title = "CF_" +city+ "_" + metric+".pdf"
    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    
    ax.set_title(city)
    ax.set_ylabel("CDF")
    ax.set_ylim(0,1)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    
#    yvals = dataset[1]
#    sorted_data = dataset[0]
    xmax = max(sorted_data)
    ax.tick_params()
    

    ax.set_xlabel("Goolge distance over Haversine distnace")
#    ax.set_xscale("log")
    
    ax.plot(sorted_data, yvals)

#    plt.legend(loc=4, fontsize=fontsize)
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    
    
    return [sorted_data, yvals]

        
#start = datetime.datetime(2017, 9, 5, 0, 0, 0)
#end = datetime.datetime(2017, 11, 2, 23, 59, 59)
### bookings ##
#for city in ["Milano"]:
#    start_proc_time = time.time()
#    print ("Queryng", city )
#    print ("init date", start.isoformat())
#    print ("final date", end.isoformat())
#    df = query_bookings_df(city, start, end)
#    if len(df) < 100: 
#        print (df)
#    else : df.to_pickle("../data/"+city+".pickle")
#    final_proc_time = time.time() - start_proc_time
#    print ("Process on", city, "requires ", int(final_proc_time/60), "minutes")
    
#c2g_bookings = query_bookings_df("Milano", start, end)
#cursor = query_bookings("Vancouver", start, end)

#for element in list(cursor):
#    print (element)
#    break

city="Milano"
df = pd.read_pickle("../data/"+city+".pickle")
trip_with_dr = df[
         (df['duration'] > 1) 
        &(df['duration'] > 60)
        &(df['distance'] > 700)
        &(df['distance_dr'] > -1)
        ]

corrective_factor =  trip_with_dr['distance_dr'] / trip_with_dr['distance']
sorted_data, yvals = computeCDF(corrective_factor, "", "")
plotCDF(sorted_data, yvals, "", save=True, 
        city="Milanio", path="../plot"+city+"/" )


















