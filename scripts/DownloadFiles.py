#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import subprocess
import sys
import os
import pandas as ps
p = os.path.abspath('..')
sys.path.append(p+"/")

class Downloader:
    def __init__(self, city):
        self.city = city
        self.ssh_bigdatadb = "cocca@bigdatadb.polito.it:"
        self.ssh_tlcdocker1 = "d046373@polito.it@tlcdocker1.polito.it:"
        self.src_home_oo = "/data/03/Carsharing_data/output/"
        self.src_home_oa = "/data/03/Carsharing_data/output_analysis/"
        self.dst_home = "/Users/mc/Desktop/csExp/data"+city+"/"
        self.plt_home = "Users/mc/Desktop/csExp/plot"+city+"/"
        self.plt_aggr = "/Users/mc/Desktop/csExp/plotAggregated/"
    
    def changeDstHome(self, city):
        self.city = city
        self.dst_home = "~/Desktop/csExp/data"+city+"/"
        self.plt_home = "/Users/mc/Desktop/csExp/plot"+city+"/"
        
    
    def acquireLastSimulationID(self):
        lastS = int(subprocess.check_output("ssh bigdatadb \
                                     ls -tr " + src_home_oa   +\
                                     "| tail -1 \
                                     | tr -d Simulation_ ", shell=True))
        return lastS
    
    def dowloadOutAnalysis(self, simID):
        if simID == "last":
            lastS = self.acquireLastSimulationID()
            print("The last Simulation is", lastS)
        else :
            lastS = simID
        
        src1 = self.ssh_bigdatadb + self.src_home_oa + "Simulation_"+str(lastS) + "/out_analysis.txt "
        
        fileName="out_analysis_"+str(lastS)+"_cr.txt"
        dst =  self.dst_home + fileName
        print ('scp ' + src1 + dst)
        os.system('scp ' + src1 + dst)
        print ("Simulation_",lastS,"correctly downloaded")
        return lastS, fileName
    
    def downloadLog(self, simID, policy, algorithm, zones,acs,tt,wt,utt,p):
        if simID == "last":
            lastS = self.acquireLastSimulationID()
            print("The last Simulation is", lastS)
        else :
            lastS = simID
        
    
        fileName= "car2go_%s_%s_%d_%d_%d_%d_%d_%d.txt" %(policy,algorithm, zones,acs,tt,wt,utt,p)
        src1 = self.ssh_bigdatadb + self.src_home_oo + "Simulation_"+str(lastS) + "/"+ fileName + " "
    
        dst =  self.dst_home + fileName 
        os.system('scp ' + src1 + dst)
        print (fileName, "correctly downloaded")
        return fileName
    
    def downloadPlacementOrder(self, algorithm, city):
        name = "car2go_" + algorithm + "500.csv"
        
        command = "ssh -t d046373@polito.it@tlcdocker1.polito.it "
    #    awk_script =""
    #    awk_script = "\"awk -F\",\" '{print \$1}' /home/d046373@polito.it/sim3.0/input/"+name+"\""
        
        cat_script = "cat /home/d046373@polito.it/"+self.city+"sim3.0/input/"+name
    
        result = subprocess.Popen([command + cat_script], 
                                stdout=subprocess.PIPE, shell=True)
    #    result = result.stdout.decode('utf-8')
        result, err = result.communicate()
        result = result.decode('utf-8')
        result_list = result.split("\n")[1:-1]
        out =[]
        for i in result_list:
            out.append(int(i.split(",")[0]))
        return out
    
    def downloadBookingsStats(self, city):
    #    command = "ssh -t d046373@polito.it@tlcdocker1.polito.it "
    #    awk_script =""
    #    awk_script = "\"awk -F\",\" '{print \$1}' /home/d046373@polito.it/sim3.0/input/"+name+"\"
        dwld_script = "scp d046373@polito.it@tlcdocker1.polito.it:/home/d046373@polito.it/"+city.capitalize()+"_sim3.0/input/stats_on_bookings "
        dwld_script += dst_home
        print (dwld_script)
        result = subprocess.Popen([dwld_script], 
                                stdout=subprocess.PIPE, shell=True)
        df = pd.read_pickle("/Users/mc/Desktop/csExp/dataVancouver/stats_on_bookings")
        return df
    
    def downloadBookingsPerHour(self):
        
        srvr_ssh = "d046373@polito.it@tlcdocker1.polito.it:"
        srvr_ssh += "/home/d046373@polito.it/%s_sim3.0/output_analysis/bookings_per_hour_%s "%(self.city, self.city)
        dst = self.dst_home + "bookings_per_hour_"+self.city+".csv"
        os.system('scp ' + srvr_ssh + dst)
        print ("bookings_per_hour_"+self.city+".csv", "downloaded" )
        return dst


    def downloadLogHDFS(self, simID, policy, algorithm, zones, acs, tt, wt, utt, p, city):
        if simID == "last":
            lastS = self.acquireLastSimulationID()
            print("The last Simulation is", lastS)
        else :
            lastS = simID
        
        '''
        car2go_Needed_max-time_7_4_50_1000000_100_0.txt
        '''
        strOutput = ""
        while len(strOutput) == 0:
            fileName= "car2go_%s_%s_%d_%d_%d_%d_%d_%d.txt" %(policy,algorithm, zones,acs,tt,wt,utt,p)
        
    
            bashCommand = "ssh cocca@bigdatadb "+\
              "hdfs dfs -cat "+\
              "Simulator/output/Simulation_"+ str(simID) +"/"+\
              fileName
              
            print (bashCommand)
        
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            strOutput =  output.decode("utf-8") 
            
            print ("====",city, "====", len(strOutput))
            zones += 1
        
        path = "../data"+city+"/"
        newFileName = fileName
        
        f = open(path+newFileName, "w")
        f.write(strOutput)
        f.close()
        
        return newFileName

    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
