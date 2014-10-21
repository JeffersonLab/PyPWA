"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import os 
import sys
sys.path.append("/u/home/jpond/bdemello/bdemello/pythonPWA/pythonPWA")
from pythonPWA.fileHandlers.gampReader import gampReader



datadir = os.path.join(sys.argv[3],"data",sys.argv[1]+"_MeV","set_"+sys.argv[2])
    

acclist = []
gampfile = open(os.path.join(datadir,"events.gamp"),'r')
gr = gampReader(gampfile)

       
    
rawlist = gr.readGamp()

pf = open(os.path.join(datadir,"events.pf"),"r")
pflist = pf.readlines()

for i in range(len(rawlist)):
    if int(pflist[i]) == 1:
        acclist.append(rawlist[i])

with open(os.path.join(datadir,"accMC.gamp"),"w") as accfile:
    for rawGamps in acclist:
            rawGamps.writeGamp(accfile)
        





