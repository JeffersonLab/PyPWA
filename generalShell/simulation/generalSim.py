#! /u/apps/anaconda/bin/python2.7
import numpy
import os, sys
from pythonPWA.fileHandlers.gampTranslator import gampTranslator
from FnSim import ampFn
from random import random

class generalSim (object):

    def __init__(self):
        pass

    def getdKVars(self,i):
        if ".gamp" in self.dataDir:
            return kvFn(self.dataT.writeEvent(self.dataT.events[i,:,:]))        
       
    def calcIList(self,params): 
        iList = numpy.zeros(shape = (self.dataLen))        
        for i in range(self.dataLen):
            iList[i] = ampFn(self.getdKVars(i),params)
            sys.stdout.write("int "+str(i)+"\r")
            sys.stdout.flush()
        return iList

    def simulate(self,nTrueDir,inputGampDir,outputRawGampDir,outputAccGampDir,inputPfDir,outputPFGampDir,iList,iMax):
        
        outputPFGampFile=open(outputPFGampDir,'w')    
        outputRawGampFile=open(outputRawGampDir,'w')
        outputAccGampFile=open(outputAccGampDir,'w')
        #igreader=gampReader(gampFile=inputGampFile)
        #inputGampEvents=igreader.readGamp() 
        nTrueList = [((1.0/(iList.shape[0]))*(iList.sum(0)))]  
        numpy.save(nTrueDir,nTrueList)

        gampT = gampTranslator(inputGampDir)
        if not os.path.isfile(inputGampDir.rstrip(".gamp")+".npy"):
            gampT.translate(inputGampDir.rstrip(".gamp")+".npy")
        gampList=numpy.load(inputGampDir.rstrip(".gamp")+".npy") 
      
        
        pflist = numpy.loadtxt(inputPfDir)

        wList=iList[:]/iMax
        
        wnList=numpy.zeros(shape=(wList.shape[0]))

        for wn in range(len(wList)):            
            if wList[wn]>random():                
                wnList[wn] = 1 
       	
        numpy.save(os.path.join(os.path.split(inputGampDir)[0],"wMaskList"),wnList)

        for wn in range(len(wnList)):
            wnEvent = gampT.writeEvent(gampList[wn,:,:])
            if float(pflist[wn])==1.0:
                wnEvent.writeGamp(outputPFGampFile)
            if wnList[wn] == 1:                
                wnEvent.writeGamp(outputRawGampFile)
            if wnList[wn] == 1 and float(pflist[wn])==1.0:
                wnEvent.writeGamp(outputAccGampFile)
        outputPFGampFile.close()
        outputRawGampFile.close()
        outputAccGampFile.close()

    
