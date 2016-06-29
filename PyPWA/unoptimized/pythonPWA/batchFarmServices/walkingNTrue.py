#! /u/apps/anaconda/anaconda-2.0.1/bin/python2 
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import numpy
import os
import sys
from PyPWA.unoptimized.pythonPWA.dataTypes.resonance import resonance
from PyPWA.unoptimized.pythonPWA.fileHandlers.getWavesGen import getwaves
from PyPWA.unoptimized.pythonPWA.model.normInt import normInt
from PyPWA.unoptimized.pythonPWA.model.intensity import intensity
from PyPWA.unoptimized.pythonPWA.fileHandlers.gampReader import gampReader
from PyPWA.unoptimized.pythonPWA.utilities.dataSimulator import dataSimulator
from PyPWA.unoptimized.pythonPWA.model.nTrue import nTrueForFixedV1V2 as ntrue
from PyPWA.unoptimized.pythonPWA.model.nTrue import nTrueForFixedV1V2AndWave as ntrueforwave
from PyPWA.unoptimized.pythonPWA.model.nExpected import nExpForFixedV1V2 as nExp
from PyPWA.unoptimized.pythonPWA.model.nExpected import nExpForFixedV1V2AndWave as nExpforwave
from PyPWA.unoptimized.pythonPWA.model.nTrue import calcStatSquaredError
import operator

def calcNTrueForDir(dataDir): 
    """
        This function calculates the value of the total nTrue and the nTrue values for each wave for a single mass bin directory.

        Args:
        dataDir (string): The complete file path to the "mass_MeV" directory.
    """
       
    #list to hold nTrue errors
    errorList=[]
    errorListEx=[]
    wvNameList=[]
    #getting our waves
    waves=getwaves(os.path.join(dataDir,"data"))        
    #loading our accepted normalization integral (NOTE: its from the mc directory)
    accNormInt=numpy.load(os.path.join(dataDir,"mc","acc","normint.npy"))
    rawNormInt=numpy.load(os.path.join(dataDir,"mc","raw","normint.npy"))    
    apath = os.path.join(dataDir,"mc","acc","alphaevents.txt")
    rpath = os.path.join(dataDir,"mc","raw","alphaevents.txt")
    #apath = os.path.join(dataDir,"mc","acc","events.num")
    #rpath = os.path.join(dataDir,"mc","raw","events.num")
    #instantiating our list of complex production amplitudes, should be
    ##a list of 2 numpy complexes
    contents=numpy.load(os.path.join(dataDir,"Vvalues.npy"))    
    orderedContents=sorted(contents.tolist().iteritems(),key=operator.itemgetter(0))    
    vList=[]
    for i in range(0,len(orderedContents),2):
        realPart=orderedContents[i][1]
        imaginaryPart=orderedContents[i+1][1]
        vList.append(numpy.complex(realPart,imaginaryPart))         
    #calculating nTrue for both waves combined
    ntrueVal=ntrue(vList,waves,rawNormInt)       
    nExpVal=nExp(vList,waves,accNormInt,apath,rpath)    

    nTrueList=[]    
    nExpList=[]
    #then storing it
    nTrueList.append(ntrueVal)
    nExpList.append(nExpVal)
    #next calculating nTrue for each wave
    for wave in waves:
        nTrueList.append(ntrueforwave(vList[waves.index(wave)],waves,wave,rawNormInt).real)    
        nExpList.append(nExpforwave(vList[waves.index(wave)],waves,wave,accNormInt,apath,rpath).real)
        wvNameList.append(wave.filename)

    #next up lets load our raw normalization integral
      
    #loading our minuit covariance matrix obtained from fitting
    if os.path.isfile(os.path.join(dataDir,"minuitCovar3.npy")):
        covarianceMatrix=numpy.load(os.path.join(dataDir,"minuitCovar3.npy"))
        statSquared=calcStatSquaredError(covarianceMatrix,rawNormInt,vList,waves)
        statSquaredEx=calcStatSquaredError(covarianceMatrix,accNormInt,vList,waves)
        print(statSquared)
        print(statSquaredEx)
        errorList.append(numpy.sqrt(statSquared[0,0].real))
        errorListEx.append(numpy.sqrt(statSquaredEx[0,0].real))
    if not os.path.isfile(os.path.join(dataDir,"minuitCovar3.npy")):
        statSquared=0
        errorList.append(0)
        statSquaredEx=0
        errorListEx.append(0)
    for wave in waves:
        if statSquared != 0:
            buffer=numpy.zeros(shape=rawNormInt.shape)
            i=waves.index(wave)
            buffer[wave.epsilon,wave.epsilon,i,:]=rawNormInt[wave.epsilon,wave.epsilon,i,:]
            statSquared=calcStatSquaredError(covarianceMatrix,buffer,vList,waves)        
            errorList.append(numpy.sqrt(statSquared[0,0].real))
            buffer=numpy.zeros(shape=accNormInt.shape)
            i=waves.index(wave)
            buffer[wave.epsilon,wave.epsilon,i,:]=accNormInt[wave.epsilon,wave.epsilon,i,:]
            statSquared=calcStatSquaredError(covarianceMatrix,buffer,vList,waves)        
            errorListEx.append(numpy.sqrt(statSquared[0,0].real))
        else:
            errorList.append(0)        
            errorListEx.append(0)  
    #saving our results to be used in plotting later.  format is numpy array [[nTrueTotal,nTrueWave1,nTrueWave2],[errorNTrueTotal,errorNTrueWave1,errorNTrueWave2]]
    #numpy.save(os.path.join(dataDir,"nTrueError.npy"),numpy.array([nTrueList,errorList]))
    retList=[]
    for i in range(len(nTrueList)):
        if i == 0:
            retList.append([dataDir.strip("_MeV"),nTrueList[i],errorList[i],nExpList[i],errorListEx[i]])
        elif i > 0:
            retList.append([dataDir.strip("_MeV"),nTrueList[i],errorList[i],wvNameList[i-1],nExpList[i],errorListEx[i]])
    return retList

retList=[]
topDir = os.path.join(sys.argv[2],"fitting")
print("processing", sys.argv[1])
ret=calcNTrueForDir(os.path.join(topDir,sys.argv[1]+"_MeV"))
retList.append(ret)

plotLists=[[] for i in range(len(retList[0]))]
for bin in retList:
    for item in bin:
        plotLists[bin.index(item)].append(item)
for lists in plotLists:
    numpy.save(os.path.join(topDir,"results",sys.argv[1]+"_MeV","nTrueList-"+str(plotLists.index(lists))+"_"+sys.argv[1]+".npy"),lists)

