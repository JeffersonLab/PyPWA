"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


"""
from random import random
import os, numpy
from pythonPWA.fileHandlers.gampReader import gampReader
from pythonPWA.model.intensity import intensity
from batchFarmServices.fast_like import FASTLikelihood
from batchFarmServices.rhoAA import rhoAA
from pythonPWA.fileHandlers.gampTranslator import gampTranslator
from batchFarmServices.fast_like import FASTLikelihood

class dataSimulator(object):
    """description of class"""
    def __init__(self,
                 mass=1010.,
                 waves=[],                 
                 normint=None,
                 productionAmplitudes=[],
                 alphaList=[],
                 beamPolarization=.4,
                 dataDir = None,
                 rhoAA=None,
                 iList=None,
                 iMax=0):
        
        self.mass=mass
        self.waves=waves        
        self.normint=normint
        self.productionAmplitudes=productionAmplitudes
        self.alphaList=alphaList
        self.beamPolarization=beamPolarization
        self.dataDir=dataDir
        self.rhoAA=rhoAA
        self.iList=iList
        self.iMax=iMax

    def calcIList():
        minuitLn=FASTLikelihood(waves=self.waves,normint=self.normint,alphaList=self.alphaList,productionAmplitudes=self.productionAmplitudes,rhoAA=self.rhoAA,accNormInt=self.normint)        
        iList = minuitLn.calcInt()     
        
        return iList        
        
    def execute(self,inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile):
        
        #igreader=gampReader(gampFile=inputGampFile)
        #inputGampEvents=igreader.readGamp() 

        gampT = gampTranslator(os.path.join(os.path.split(inputGampFile.name)[0],os.path.split(inputGampFile.name)[1]))
        if not os.path.isfile(os.path.join(os.path.split(inputGampFile.name)[0],"events.npy")):
            gampT.translate(os.path.join(os.path.split(inputGampFile.name)[0],"events.npy"))
        gampList=numpy.load(os.path.join(os.path.split(inputGampFile.name)[0],"events.npy")) 
      
        pf = inputPfFile
        pflist = pf.readlines()

        wList=self.iList[:]/self.iMax
        
        wnList=numpy.zeros(shape=(wList.shape[0]))

        for wn in range(len(wList)):            
            if wList[wn]>random():                
                wnList[wn] = 1 
       	
        numpy.save(os.path.join(os.path.split(inputGampFile.name)[0],"wnList"),wnList)

        for wn in range(len(wnList)): 
            if wnList[wn] == 1:
                wnEvent = gampT.writeEvent(gampList[wn,:,:])
                wnEvent.writeGamp(outputRawGampFile)
                if int(pflist[wn])==1:
                    wnEvent.writeGamp(outputAccGampFile)

        outputRawGampFile.close()
        outputAccGampFile.close()
