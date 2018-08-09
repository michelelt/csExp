#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 19:59:31 2018

@author: mc
"""
from plotter.header import *

########################################################################################################


def numberOfZones(city):
    c2id={"Vancouver":510, "Torino":261, "Berlino":833, "Milano":549}
    if city in c2id.keys():
        return c2id[city]
    

    command = 'ssh -t d046373@polito.it@tlcdocker1.polito.it wc -l %s_sim3.0/input/car2go_ValidZones.csv' % city
#    command = 'ssh -t d046373@polito.it@tlcdocker1.polito.it cd %s_sim3.0/ | ls '

    zones = int(str(subprocess.check_output(command, shell=True)).split(" ")[0][2:5]) - 1
#    zones = str(subprocess.check_output(command, shell=True)).split("\n")

    return zones

########################################################################################################

def plotDeathProb(init_df, city, tt, acs, save=False, onlyFF=True, path=""):
    

    if onlyFF == True :
        l = ['FreeFloating']
    else:
        l= ['FreeFloating', 'Hybrid', 'Needed']
        
    
#    mylists ={"max-time": [i * 1 for i in range(2,28,2)], 
#              "max-parking":[i * 1 for i in range(1,28,2)]}
        
#    mylists ={"max-time": [i * 1 for i in range(1,31,1)], 
#          "max-parking":[i * 1 for i in range(1,31,1)]}
    
    for policy in l:
        df = init_df[init_df["Policy"] == policy]
        df = df[df["pThreshold"] ==  0]
        df = df[df["upperTankThreshold"] ==  100]
        df = df[df["Algorithm"] !=  "max-time"]
        
        x = df.Zones.unique()
#        x = x / float(numeberOfZones(init_df.iloc[0]["Provider"]))*100
        x = x / numberOfZones(city)*100

        
        fig, ax = plt.subplots(1,1,figsize=(6,4))
        ax.grid()
        title = city+"_zonesVsDeaths_algorithms_acs-"+str(acs)+"_tt-"+str(tt) +"_policy-"+policy+".pdf"
#        ax.set_title(title)
        ax.set_xlabel(my_labels["Zones"])
        ax.set_ylabel(my_labels["Deaths"])
        ax.set_xlim(0,31)
        ax.set_ylim(bottom = -5, top=100)
        
        
        if "Free" not in policy:
            df = df[df["TankThreshold"] == tt]
        
        for algorithm in df.Algorithm.unique():
            print (algorithm)
            a = df[df["Algorithm"] == algorithm]
            a = a[a["Acs"] == acs]
            
            
            y = a.Deaths.div(a.iloc[0]["TypeS"]).mul(100)
            
#            if algorithm in ["max-parking", "max-time"]:
            if algorithm in ["max-parking"]:

                ax.plot(x,
                        y, 
                        color=colors_dict[algorithm],
                        label=my_labels[algorithm], 
                        marker=markers_dict[algorithm],
#                        markevery=mylists[algorithm]
                        )
            else :
                ax.plot(x,
                        y, 
                        color=colors_dict[algorithm],
                        label=my_labels[algorithm], 
                        marker=markers_dict[algorithm])
                
#                + ", acs:" + str(acs)
            
            
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=4, mode="expand", borderaxespad=0., edgecolor="white",
       handletextpad=0.1)

    if save :   
        plt.savefig(path+title, bbox_inches = 'tight')

    plt.show()

    return

########################################################################################################

def plotMetricVsZones_policy(init_df, city, acs, tt, utt, p,
                             metric, save=False, freeFloating=True, k=250, path=""):
    
    
    title = city + "_" + metric + "VsZones_Policy_acs-"+str(acs) + "_tt-"+str(tt) + "_" +\
    str(utt) + "_" +str(p) + ".pdf"
    
    df = init_df[init_df["Acs"] == acs]
    df = df[df["upperTankThreshold"] == utt]
    
    
    if freeFloating == False:
        df = df[(df["Policy"] == "Needed") | (df["Policy"] == "Hybrid")]
    x = df.Zones.unique()
    x = x*100 / float(numberOfZones(city))
    
    
    print (city, float(numberOfZones(city)))

    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    ax.set_xlabel(my_labels["Zones"])
    ax.set_ylabel(my_labels[metric])
    
    ax.set_xlim([0,max(x)+1])

    i = 0
#    for policy in df.Policy.sort_values(ascending=False).unique():
    for policy in ['Needed', 'FreeFloating']:

        if "Free" not in policy:
            tmp = df[(df["TankThreshold"] == tt) & 
                     (df["Policy"] == policy)]
            if utt != -1 :
                tmp = tmp[tmp["upperTankThreshold"] == utt]
        else :
            tmp = df[df["Policy"] == policy]

        for algorithm in ["max-parking"]:
            tmp2 = tmp[tmp["Algorithm"] == algorithm]
            
            
            if metric == "Deaths" or metric == "AmountRechargeForced":
                y = tmp2[metric]
                y = y.div(init_df.iloc[0]["TypeE"]).mul(100)
                
            elif metric == "TravelWithPenlaty":
                y = tmp2["AvgWalkedDistance"]
                y = y.mul(tmp2["ReroutePerc"])
                y = y + (tmp2["AmountRechargePerc"] -  tmp2["ReroutePerc"])*k
#                y = y.div(tmp2.iloc[0]["TypeE"])
                y = y.div(100)
                
            else:
                y= tmp2[metric]

            ax.plot(x,y, label= my_labels[policy], 
            linestyle=line_dict[policy], 
            marker = markers_dict_policy[policy],
            color=colors_dict_policy[policy])
            i=i+1
    
    if metric == "AvgSOC":
        ax.set_ylim(0,100)
        ax.plot(x,[25 for i in range(len(x))], linestyle ="--", color ="black")

    if metric == "AvgWalkedDistance":
        l = [i for i in range(0,2600,200)]
        ax.set_yticks(l)
    
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(top=ymax)
    x = x.tolist()
    x.insert(0,0)
    x = np.array(x)
    if metric in ["AmountRechargePerc", "AvgSOC", "TravelWithPenlaty"]:
        ax.set_ylim(bottom=0)
        ymin = 0
        

#    ax.fill_between(x,ymin, ymax, where= x<=6, color='red', alpha=0.2, label="Infeasible trips")
#    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#           ncol=3, mode="expand", borderaxespad=0., edgecolor="white")
    ax.legend()
    plt.show()
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    
    return

########################################################################################################

def plotMetricVsTT_policy(init_df, z, acs, algorithm, metric, save=False, path=""):
    title = metric + "VsTT_Policy_acs-"+str(acs) + "_z-"+str(z)+"_algorithm-"+str(metric) +".pdf"
    df = init_df[init_df["Acs"] == acs]
    df = df[df["Zones"] == z]
    df = df[df["Algorithm"] == algorithm]
    df = df[(df["Policy"] == "Needed") | (df["Policy"] == "Hybrid")]
    
    x = df.TankThreshold.unique()
    
    xticks = df.TankThreshold
    xticks[len(xticks)] = 0
    xticks = xticks.sort_values().unique()

    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    ax.set_xlabel(r'$\alpha$' +' [%]')
    ax.set_ylabel(my_labels[metric])
    ax.set_xticks(xticks)
    ax.set_xlim(0,55)
    i=0
    for policy in df.Policy.sort_values(ascending=False).unique():
        y=df[df["Policy"] == policy][metric]
        ax.plot(x,y, label= my_labels[policy], 
                    linestyle=line_dict[policy], 
                    marker = markers_dict[list(markers_dict.keys())[i]],
                    color=colors_dict[list(colors_dict.keys())[i]])
        i=i+1
        
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(bottom =0, top=ymax)
    x = x.tolist()
    x.insert(0,0)
    x = np.array(x)
    ax.fill_between(x,ymin, ymax, where= x<=15, color='red', alpha=0.2, label="Infeasible trips")
        

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0., edgecolor="white")
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    return

########################################################################################################

def aggreatePerCityCDF(cdfList, dataType, save, path): 
    title = "CDF_aggregate_"+dataType+".pdf"
    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    ax.set_ylabel("CDF")
    ax.set_ylim(0,1)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    xmax = 0
    for city in cdfList.keys():
        x = cdfList[city][0]
        y = cdfList[city][1]
        
        if (max(x)) > xmax: xmax =max(x)
        

        ax.plot(x, y, label=city)
    
    if dataType == "RentalsDistance":
        ax.set_xlabel("Rentals Distance")
        ax.set_xscale("log")
        ax.set_xlim(left=700, right=xmax)
        ax.set_xticks([700, 1000, 5000, 10000, xmax])
        ax.set_xticklabels(["0.7 km", "1 km", "5 km", "10 km", str(round(xmax/1000))+" km" ])
        
    elif dataType == "ParkingsDuration":
        ax.set_xlabel("Parkings Duration")
        ax.set_xscale("log")
        ax.set_xlim(0.083, 48)
        ax.set_xticks([0.083, 0.33, 1, 5, 12, 24, 48])
        ax.set_xticklabels(["5 min","20 min","1 h","5 h","12 h","1 d","2 d"])
        
    elif  dataType == "RentalsDuration":
        ax.set_xlabel("Rentals Duration")
        ax.set_xticks([2,10,20,30,40,50,60])
        ax.set_xticklabels(["2 min","10 min",
                            "20 min","30 min","40 min",
                            "50 min","1h"])
        ax.set_xlim(0, 60)

        
    ax.legend()
        
    if save:
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
        
    plt.legend()
    return
    

def computeCDF(df, metric, city):
    
    if metric == "RentalsDistance":
        df = df[df.Type == "e"]
        metric = "TripDistance"
        y_set = df[metric]
        max_ticks = df[metric].max()
        print (max_ticks, "[m]")
        y_set = df[metric]
        
        
    elif metric == "ParkingsDuration":
        cars_id = df.ID.unique()
        dur = pd.Series()
        for ID in cars_id:
            tmp = df[df["ID"]== ID]
            tmp = tmp.reset_index()
            a_start = tmp.loc[2::2, "Stamp"].reset_index()["Stamp"]
            a_end = tmp.loc[1::2, "Stamp"].reset_index()["Stamp"]
            dur = dur.append(a_start-a_end)
            
            if len(dur[dur < 0 ]) > 0:
                print ("Algorithm wrong")
        y_set = dur.dropna()
        y_set = y_set.div(3600)
        y_set = y_set[y_set >= 0.083]

    
    elif  metric == "RentalsDuration":
        df.ID.astype(int)
        df = df.sort_values(by=["ID", "Stamp"])
        starts = df[df["Type"] == 's'].reset_index()
        ends = df[df["Type"] == 'e'].reset_index()
        y_set = ends["Stamp"].div(60) - starts["Stamp"].div(60)


    else:
        return
    
    values = y_set
    sorted_data = np.sort(values)
    yvals=np.arange(len(values))/float(len(values)-1)
    print("Sorted data len:", len(sorted_data))
    
    return [sorted_data, yvals]
    



def plotCDF(dataset, metric, save=False, city="", path="" ):
    title = "CDF_" +city+ "_" + metric+".pdf"
    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    
    ax.set_title(city)
    ax.set_ylabel("CDF")
    ax.set_ylim(0,1)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    
    yvals = dataset[1]
    sorted_data = dataset[0]
    xmax = max(sorted_data)
    ax.tick_params()
    
    if metric == "RentalsDistance":
        print(1)
        ax.set_xlabel("Rentals Distance")
        ax.set_xscale("log")
        ax.set_xlim(left=700, right=xmax)
        ax.set_xticks([700, 1000, 5000, 10000, xmax])
        ax.set_xticklabels(["0.7 km", "1 km", "5 km", "10 km", str(round(xmax/1000))+" km" ])
        
    elif metric == "ParkingsDuration":
        print(2)
        ax.set_xlabel("Parkings Duration")
        ax.set_xscale("log")
        ax.set_xticks([0.083,0.33,1,5,12,24,48])
        ax.set_xticklabels(["5 min","20 min","1 h","5 h","12 h","1 d","2 d"])
        ax.set_xlim(0.083, 48)
        
    elif  metric == "RentalsDuration":
        print(3)
        ax.set_xlabel("Rentals Duration")
#        ax.set_xscale("log")
        ax.set_xticks([2,10,20,30,40,50,60])
        ax.set_xticklabels(["2 min","10 min",
                            "20 min","30 min","40 min",
                            "50 min","1h"])
        ax.set_xlim(0, 60)
    else:
        return
    
    ax.plot(sorted_data, yvals)

#    plt.legend(loc=4, fontsize=fontsize)
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    
    return [sorted_data, yvals]

########################################################################################################


def plotDeathsProb_policy(init_df, acs, utt, algorithm, save=False, path=""):
    title = "DeathsVsZones_Policy_acs-"+str(acs) +"_algorithm-"+algorithm+".pdf"
    df = init_df[init_df["Acs"] == acs]
    df = df[df["Algorithm"] == algorithm]
    df = df[df["pThreshold"] == 0]
    
    x = df.Zones.unique()
    x = x *100 / float(numeberOfZones("Torino"))
    mylists ={"Needed": [2,4,6,8,12,14,16,18], 
              "Hybrid":[1,3,5,7,9,11,13,15,17,19]}
#    print (mylists)
#    mylists ={"Needed": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26], 
#              "Hybrid": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]}
    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    ax.set_xlabel(my_labels["Zones"])
    ax.set_ylabel(my_labels["Deaths"])
    ax.set_xlim(0,28)
#    ax.set_ylim(-5,100)
    
    left, bottom, width, height = [0.40, 0.45, 0.45, 0.35]
    ax2 = fig.add_axes([left, bottom, width, height])
    
    ax2.set_xlim(left=3, right=6)
    ax2.set_ylim(bottom=0.0001, top=5)
    ax2.set_yscale("log")
    ax2.set_xlabel(my_labels["Zones"])
#    dpVsP_colors = {"Hybrid" :"blue", "Needed":"red", "FreeFloating":"brown"}
#    dpVsP_markers = {"Hybrid" :"s", "Needed":"o", "FreeFloating":"^"}
    i = 0
    for policy in ["Needed", "Hybrid",  "FreeFloating"]:

        tmp = df[df["Policy"] ==  policy]
        tmp = tmp[tmp["upperTankThreshold"] == utt]

        if policy in ["Needed", "Hybrid"]:
            tmp = tmp[tmp["TankThreshold"] == 25]
        
        y = tmp["Deaths"]
            
        y = y.div(init_df.iloc[0]["TypeE"]).mul(100)
#        if i==2:
#            return [x,y,tmp]
        print (policy)
        print ("len y", len(y))

        print ()
        if "Free" not in policy:
            ax.plot(x,y, 
                    label= my_labels[policy], 
                    linestyle=line_dict[policy], 
                    marker = markers_dict_policy[policy],
                    color = colors_dict_policy[policy],
                    markevery=mylists[policy]
                    )
#                    
        else: 
            ax.plot(x,y, 
                    label= my_labels[policy], 
                    linestyle=line_dict[policy], 
                    marker = markers_dict_policy[policy],
                    color = colors_dict_policy[policy]
                    )
            
        ax2.plot(x,y, 
                linestyle=line_dict[policy], 
                marker = dpVsP_markers[policy],
#                color=colors_dict[list(colors_dict.keys())[i]])
                color = dpVsP_colors[policy])
        i = i + 1
    
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0., edgecolor="white")
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    
    return

########################################################################################################


def checkStartEndsAlternates():
#    df = pd.read_csv(p+"/sim3.0/input/car2go_FreeFloating_max-time_40_8_-1_1000000.txt",
#                     skiprows=[0,1,2,3,4,5,6,7],
#                     sep=";")
    cars_id = df.ID.unique()
    for ID in cars_id:
        tmp = df[df["ID"]== ID]
        for i in range(len(tmp)-1):
            currentType = tmp.iloc[i]["Type"]
            if currentType == tmp.iloc[i+1]["Type"]:
                print ("errore")
    return

########################################################################################################


def pdfChargingTimeVsAlgorithm(dataset, save=False, cdf=True):
    algorithms = ["avg-time","max-parking"]
    title = "CDF_parking_time_per_algorithm"+".pdf"
    
    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.set_xlabel("Plugged time [h]")
    ax.set_ylabel("CDF")
    ax.set_ylim([0,1])
    ax.set_xlim([0,30])
    mymarker = {"avg-time":"*", 
                "max-parking":"o"}
    mylists ={"avg-time": [i * 1480 for i in range(1,6)], 
              "max-parking":[i * 9520 for i in range(1,6)]}
    
    ax.grid()
    
    for a in algorithms :
        
        test = dataset[dataset["StartRecharge"] > 0]
        test["parkingTime"] = test["Stamp"] - test["StartRecharge"]
        
        values = test["parkingTime"].div (3600)
        values = test["Recharge"]
        values = values[values < values.quantile(0.99)]
        values.tolist()
        print (len(values),a)
        sorted_data = np.sort(values)    
        yvals=np.arange(len(values))/float(len(values)-1)
        ax.plot(sorted_data,yvals,
                label=my_labels[a], 
                color=colors_dict[a], 
                linewidth=2, 
                markevery=mylists[a],
                marker=mymarker[a])
#        ax.plot(sorted_data,yvals, , label=my_labels[metric], linewidth=2, marker="o", markersize=6)
        print("aaa")
        
        print ("sorted data", len(sorted_data))
        print ("sorted data", len(yvals))

    
    
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0., edgecolor="white")
    
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    return

########################################################################################################


def maxTripCoordinates(dataset):
    max_carID = dataset[dataset.TripDistance == dataset.TripDistance.max()]["ID"].iloc[0]
    zz = dataset[dataset.ID == max_carID]
    zz = zz.reset_index()
    id_max = zz.TripDistance.idxmax()
    zz = zz.loc[id_max-1 : id_max]
    start = zz.iloc[0]["EventCoords"].replace("[", "").replace("]", "").split(",")
    print(start[1] + ",", start[0])
    end = zz.iloc[1]["EventCoords"].replace("[", "").replace("]", "").split(",")
    print(end[1] + ",", end[0])
    return dataset[dataset.TripDistance == zz.TripDistance.max()]["ID"].index


########################################################################################################

def plotMetricVsZones_policy_p(init_df, acs, tt, utt, plist,
                             metric, save=False, freeFloating=True, 
                             k=250, city="", path="", ax=None):
    
    title = city+ "_" + metric + "VsZones_Policy_" + str(acs) + str(acs) + "_tt-"+str(25) + "_" +\
    str(utt) + "_" +str(len(plist)) + ".pdf"
    print (title)
    
    df = init_df[init_df["Acs"] == acs]
#    df = df[df["Zones"] >= 4]
    if freeFloating == False:
        df = df[(df["Policy"] == "Needed") | (df["Policy"] == "Hybrid")]
    x = df.Zones.unique()   
    nz = numberOfZones(city)
    x = x / float(nz)*100
    x2 =df.Zones.unique() * acs

    if ax == None:
#        fig = plt.subplots(1,1,figsize=(6,4))
        fig = plt.figure(figsize=(7,4))
        ax = fig.add_axes([0.1, 0.12, 0.7, 0.7])
    ax.grid()
    ax.set_xlabel(my_labels["Zones"])
    ax.set_ylabel(my_labels[metric])
            
#    ax.set_title(city)
#    ttl = ax.title
#    ttl.set_position([.5, 1.15])

    ax.set_xlim([0,31])

    i = 0
    df = df[(df["TankThreshold"] == tt)]
    
    for policy in df.Policy.sort_values(ascending=False).unique():
        for p in plist :
            if "Hybrid" in policy :
                tmp = df[(df["TankThreshold"] == tt) 
                         & (df["Policy"] == policy) 
                         & (df["pThreshold"] == p)
                         & (df["upperTankThreshold"] == utt)
                         ]

            elif "Needed" in policy and p == 0 :
                tmp = df[(df["Policy"] == policy) 
                         & (df["pThreshold"] == 0)
                            ]
            else :
                continue
    
            for algorithm in ["max-parking"]:
                tmp2 = tmp[tmp["Algorithm"] == algorithm]
                
                
                if metric == "Deaths" or metric == "AmountRechargeForced":
                    y = tmp2[metric]
                    y = y.div(init_df.iloc[0]["TypeE"]).mul(100)
                    
                elif metric == "TravelWithPenlaty":
                    y = tmp2["AvgWalkedDistance"]
                    y = y.mul(tmp2["ReroutePerc"])
                    y = y + (tmp2["AmountRechargePerc"] -  tmp2["ReroutePerc"])*k
    #                y = y.div(tmp2.iloc[0]["TypeE"])
                    y = y.div(100)
                    
                else:
                    y= tmp2[metric]
    
                print (policy, p)

                
                ax.plot(x,y, label= my_labels[policy] + " p:" +str(p), 
                linestyle=line_dict[policy], 
                marker = markers_dict[list(markers_dict.keys())[i]],
                color=colors_dict[list(colors_dict.keys())[i]])
                
                
                i=i+1
                
                if metric == "Deaths" :
                    left, bottom, width, height = [0.30, 0.40, 0.45, 0.35]
                    ax2 = fig.add_axes([left, bottom, width, height])
                    
                    ax2.set_xlim(zoom_deaths[city])
                    ax2.set_ylim(bottom=10e-6, top=10e-3)
                    ax2.set_ylabel("[%]")
                    ax2.set_yscale("log")
                    ax2.set_xlabel(my_labels["Zones"])
                    ax2.plot(x,y, label= my_labels[policy] + " p:" +str(p), 
                    linestyle=line_dict[policy], 
                    marker = markers_dict[list(markers_dict.keys())[i]],
                    color=colors_dict[list(colors_dict.keys())[i]])
    

    ax.set_ylim(y_lim[metric])
    ymin, ymax = ax.get_ylim()
    x = x.tolist()
    x.insert(0,0)
    x = np.array(x)

    ax.fill_between(x,ymin, ymax, where= x<=zoom_deaths[city][1] , 
                    color='red', alpha=0.2, label="Infeasible trips")
    ax.legend(bbox_to_anchor=(1, 1), loc=2,
           ncol=1, mode="expand", borderaxespad=0., edgecolor="white")
    
    ax3 = ax.twiny()
    ax3.set_xlabel("Number of charging station")
    myX3ticks = ax.get_xticks()
    myX3ticksB = []
    for i in range(len(myX3ticks)):
        myX3ticksB.append(int(myX3ticks[i].astype(int) / 100 * nz * acs))
    myX3ticksB[-1:] = ""
    ax3.set_xticks([0,5,10,15,20,25,30,31])
    ax3.set_xticklabels(myX3ticksB)
    plt.show()
    
    if save :   
        plt.savefig(path+title, format='pdf')
    plt.show()
    
    return ax


def aggregateUtilizastionPerHour(cities, save,path):
    colors  = {"Vancouver":"green", "Berlino":"orange",  "Milano":"red", "Torino":"blue", }
    tmp = pd.DataFrame()
    df = pd.DataFrame()
    i=0
    for city in cities:
        tmp = pd.read_csv("../data"+city+"/bookings_per_hour_"+city+".csv")
        df = df.append(tmp)
                
        
    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    ax.set_xlabel("Hour")
    ax.set_ylabel("Bookings per Hour")
    
    i=0
    for city in colors.keys():
        tmp = df[df["city"] ==  city]
        ax.plot(tmp.dayHour, tmp.WD_BPD, label=city + "WD", color=colors[city])
        ax.plot(tmp.dayHour, tmp.WE_BPD, label=city + "WE", color=colors[city], linestyle='--')
        i += 1
    ax.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5, 1.175), 
             borderaxespad=0., edgecolor="white")
    ax.set_xticks(df.dayHour.unique())
    ax.set_xticklabels([str(hour) for hour in list(df.dayHour)], rotation=45)
    if save:
        plt.savefig(path+"aggBookginfsPerHour"+".pdf", bbox_inches = 'tight', format='pdf')
    return df

#def aggregateUtilizastionPerDay(cities, save,path):
#    color  = ["blue", "orange", "green", "red"]
#    tmp = pd.DataFrame()
#    df = pd.DataFrame()
#    i=0
#    for city in cities:
#        tmp = pd.read_csv("../data"+city+"/bookings_per_hour_"+city+".csv")
#        l = [city]*24
#        tmp["city"] = l
#        df = df.append(tmp)
#        
#    return df
#    fig, ax = plt.subplots(1,1,figsize=(6,4))
#    ax.grid()
#    ax.set_xlabel("Hour")
#    ax.set_ylabel("# of bookings ")
#    
#    i=0
#    for city in cities:
#        tmp = df[df["city"] ==  city]
#        ax.plot(tmp.dayHour, tmp.WD_BPD, label=city + "WD", color=color[city])
#        ax.plot(tmp.dayHour, tmp.WE_BPD, label=city + "WE", color=color[city], linestyle='--')
#        i += 1
#    ax.legend()
#    plt.savefig(path+"aggBookginfsPerHour_" + city +".pdf", bbox_inches = 'tight', format='pdf')
#
#    return df

def divisorGenerator(n):
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield int(divisor)

def metricVaryingZonesAndAcs(df, zones,tt, p, metric, ax):
    df = df[df.Algorithm == 'max-parking' ]
    df = df[df.Policy=="Hybrid"]
    df = df[df.TankThreshold == tt]
    
    if metric == "Deaths":
        div = df["TypeS"].iloc[0] * 0.01
    else : div =1 
        
    
    zones = list(divisorGenerator(zones))
    
    my_markers = {0:".",25:"o",50:"8",75:"x"}
    x = zones
    y = {}
    ticks = []
    
    head = 0
    tail = len(zones) -1
    
    for value in p:
        tmp = df[df.pThreshold == value]
        y[value] = []
    
        for head in range (len(zones)):
            print (value, zones[head], zones[tail-head])
            y[value].append(tmp[  (tmp.Zones == zones[head])\
                        & (tmp.Acs == zones[tail-head])][metric].values[0]/div
                   )
#            zone_str = round(zones[head]/numeberOfZones("Torino"))
            zone_str = round(zones[head])
            
            ticks.append(str(zone_str)+","+str(zones[tail-head]))
#    return x,y
            
#    fig, ax = plt.subplots(1,1,figsize=(9,6))
    ax.grid()
    ax.set_xlabel("Zones,Acs")
    ax.set_ylabel(my_labels[metric])
    ax.set_xticks(zones)
    ax.set_xticklabels(ticks)
    for value in p:
        print (value)
        ax.plot(x, y[value], label=value, marker=my_markers[value])
    ax.legend()

    return ax


def computeTravelWithPenlaty(df):
    k=150
    y = df["AvgWalkedDistance"]
    y = y.mul(df["ReroutePerc"])
    y = y + (df["AmountRechargePerc"] -  df["ReroutePerc"])*k
    y = y.div(100)
    return y


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    








