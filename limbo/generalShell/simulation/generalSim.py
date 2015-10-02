#! /u/apps/anaconda/bin/python2.7
import numpy
import os, sys
import fileinput
from FnSim import intFn
from random import random

class generalSim (object):

    def __init__(self,KVDir):
        self.KVDir = KVDir
       
    def calcIList(self,params): 
        n = 0 
    	iList = numpy.zeros(shape = (1))
        for line in fileinput.input([self.KVDir]): 
            iList.resize(n+1)       
            kvAs = line.split(",")
            kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}
            iList[n] = intFn(kvAx,params)
            n+=1
            
        return iList

    def simulate(self,nTrueDir,inputKVDir,outputWeightDir,iList,iMax):
        
        nTrueList = [((1.0/(iList.shape[0]))*(iList.sum(0)))]  
        numpy.save(nTrueDir,nTrueList)

        wList=iList[:]/iMax
        
        wnList=numpy.zeros(shape=(wList.shape[0]))

        for wn in range(len(wList)):            
            if wList[wn]>random():                
                wnList[wn] = 1 
       	
        numpy.save(outputWeightDir,wnList)

        

    
