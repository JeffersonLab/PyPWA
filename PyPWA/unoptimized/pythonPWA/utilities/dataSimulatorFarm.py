# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 10:15:05 2014

@author: salgado
"""

from random import random
import os
from PyPWA.unoptimized.pythonPWA.fileHandlers.gampReader import gampReader
from PyPWA.unoptimized.pythonPWA.model.intensity import intensity


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
                 dataDir = None):
        
        self.mass=mass
        self.waves=waves
        self.resonances=resonances
        self.normint=normint
        self.productionAmplitudes=productionAmplitudes
        self.alphaList=alphaList
        self.beamPolarization=beamPolarization
        self.dataDir=dataDir
        self.intensity=intensity(resonances=self.resonances,
                                 waves=self.waves,
                                 productionAmplitudes=self.productionAmplitudes,
                                 normint=self.normint,
                                 alphaList=self.alphaList,
                                 beamPolarization=self.beamPolarization)

    def execute(self,inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile):
        
        igreader=gampReader(gampFile=inputGampFile)
        inputGampEvents=igreader.readGamp()               
        
        iList=[]
        iMax=0.
        
        pf = inputPfFile
        pflist = pf.readlines()
        randomPFList=[]
        
        for event in range(len(self.alphaList)):
            i=self.intensity.calculate(self.mass,event)
            iList.append(i)
            
        iMax=max(iList)
        wList=[x/iMax for x in iList]
            
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