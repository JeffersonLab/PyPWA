'''
Created on Jun 13, 2014

@author: jpond
'''
import os, time
from pythonPWA.fileHandlers.gampReader import gampReader


ts = time.time()
datadir = os.path.join("/volatile/halld/pippimpi0/data",raw_input("Which bin(number only)?")+"_MeV","set_"+raw_input("Which set(number only)?"))
print "data directory = "+datadir    

acclist = []
gampfile = open(os.path.join(datadir,"events.gamp"),'r')
gr = gampReader(gampfile)

       
    
rawlist = gr.readGamp()

pf = open(os.path.join(datadir,"events.pf"),"r")
pflist = pf.readlines()

for i in range(len(rawlist)):
    if int(pflist[i]) == 1:
        acclist.append(rawlist[i])

with open(os.path.join(datadir,"selected_events.acc.gamp"),"w") as accfile:
    for rawGamps in acclist:
            rawGamps.writeGamp(accfile)
        
print str(len(acclist))+" events accepted"

ts1 = time.time()
print(str(ts1 - ts)+" seconds taken")
