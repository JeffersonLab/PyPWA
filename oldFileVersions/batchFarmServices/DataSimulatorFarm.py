"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
from random import random 
import os
import sys
import numpy
#import time
sys.path.append("/u/home/jpond/bdemello/bdemello/pythonPWA/pythonPWA")
from pythonPWA.fileHandlers.gampReader import gampReader
from pythonPWA.utilities.OHMintensity import intensity
#from pythonPWA.model.intensity import intensity
import time

class dataSimulator(object):
    """description of class"""
    def __init__(self,
                 mass=1010.,
                 waves=[],
                 resonances=[],
                 normint=None,
                 productionAmplitudes=[],
                 alphaList=[],
                 beamPolarization=.4,
                 dataDir=None):
        
        self.mass=mass
        self.waves=waves
        self.resonances=resonances
        self.normint=normint
        
        self.alphaList=alphaList
        self.beamPolarization=beamPolarization
        self.dataDir=dataDir
        self.intensity=intensity(resonances=self.resonances,waves=self.waves,normint=self.normint,alphaList=self.alphaList,beamPolarization=self.beamPolarization)

#    def calcIList(self):
#        iList=[]
#        for event in xrange(len(self.alphaList)):
#        
#            i=self.intensity.calculate(self.mass,event)
#            iList.append(i)
#        return iList
 

    def calcIList(self):
        xList = xrange(0,len(self.alphaList))
        if not os.path.isfile(os.path.join(self.dataDir,"FITOHMlist.npy")):            
            #print("Start OHMlist"+self.dataDir)
            #ts = time.time()            
            OHMlist = self.intensity.calcFITOHM(self.mass)
            #ts1 = time.time()
            #print("Done OHMlist "+str(ts1-ts)+" seconds")       
            numpy.save(os.path.join(self.dataDir,"FITOHMlist.npy"),OHMlist)
        else:
            OHMlist = numpy.load(os.path.join(self.dataDir,"FITOHMlist.npy"))
            #print("loaded OHMlist")        
        #print("start iList")
        #Ts = time.time()               
        iList = [self.intensity.calculate(self.mass,i,OHMlist) for i in xList]
        #Ts1 = time.time()
        #print("DONE iList "+str((Ts1-Ts))+" seconds")
        return iList

   
    def calcWList(self,iList,iMax,inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile):
        
        wList=[x/iMax for x in iList]
        igreader=gampReader(gampFile=inputGampFile)
        inputGampEvents=igreader.readGamp()
        
        pf = inputPfFile
        pflist = pf.readlines()
        randomPFList=[]

        rawGampEvents=[]
        
        for wn in range(len(wList)):
            
            
            if wList[wn]>random(): 
            
                inputGampEvents[wn].raw=True
                
                rawGampEvents.append(inputGampEvents[wn])
                randomPFList.append(pflist[wn])

        for rawGamps in rawGampEvents:
            rawGamps.writeGamp(outputRawGampFile)    
            
            if int(randomPFList[rawGampEvents.index(rawGamps)])==1:
                rawGamps.writeGamp(outputAccGampFile)
            
        
        outputRawGampFile.close()
        outputAccGampFile.close()
    
