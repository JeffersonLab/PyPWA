#! /u/apps/anaconda/anaconda-2.0.1/bin/python2 
import numpy
import os
import sys
sys.path.append("/u/home/jpond/bdemello/bdemello/pythonPWA/pythonPWA")
from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader
from pythonPWA.utilities.dataSimulator import dataSimulator

from pythonPWA.model.nTrue import nTrueForFixedV1V2 as ntrue
from pythonPWA.model.nTrue import nTrueForFixedV1V2AndWave as ntrueforwave

from pythonPWA.model.nTrue import calcStatSquaredError
import operator

def calcNTrueForDir(dataDir):
    
    """
    only works for 2 waves right now.
    """
    #list to hold nTrue errors
    errorList=[]
    
    #getting our waves
    waves=getwaves(os.path.join(dataDir,"data","acc"))
    print"loaded",len(waves),"waves"
    
    #loading our accepted normalization integral (NOTE: its from the mc directory)
    accNormInt=numpy.load(os.path.join(dataDir,"mc","acc","normint.npy"))
    
    #instantiating our list of complex production amplitudes, should be
    ##a list of 2 numpy complexes
    contents=numpy.load(os.path.join(dataDir,"Vvalues.npy"))
    
    orderedContents=sorted(contents.tolist().iteritems(),key=operator.itemgetter(0))
    
    vList=[]

    for i in range(0,len(orderedContents),2):
        realPart=orderedContents[i][1]
        imaginaryPart=orderedContents[i+1][1]
        vList.append(numpy.complex(realPart,imaginaryPart))
    
    #vList=[numpy.complex(contents['wave1Re'],contents['wave1Im']),numpy.complex(contents['wave2Re'],contents['wave2Im'])]
    print"using production amplitudes:",vList
    
    #calculating nTrue for both waves combined
    ntrueVal=ntrue(vList,waves,accNormInt)    
    
    nTrueList=[]    
    
    #then storing it
    nTrueList.append(ntrueVal)
    
    #next calculating nTrue for each wave
    for wave in waves:
        nTrueList.append(ntrueforwave(vList[waves.index(wave)],waves,wave,accNormInt).real)    


    #next up lets load our raw normalization integral
    rawNormalizationIntegral=numpy.load(os.path.join(dataDir,"mc","raw","normint.npy"))
    
    #loading our minuit covariance matrix obtained from fitting
    covarianceMatrix=numpy.load(os.path.join(dataDir,"minuitCovar3.npy"))
    statSquared=calcStatSquaredError(covarianceMatrix,rawNormalizationIntegral,vList,waves)


    #appending our error
    errorList.append(numpy.sqrt(statSquared[0,0].real))
    
    print"nTrue:", ntrueVal,"+/-",numpy.sqrt(statSquared[0,0].real)
    
    for wave in waves:
        buffer=numpy.zeros(shape=rawNormalizationIntegral.shape)
        i=waves.index(wave)
        buffer[wave.epsilon,wave.epsilon,i,:]=rawNormalizationIntegral[wave.epsilon,wave.epsilon,i,:]
        statSquared=calcStatSquaredError(covarianceMatrix,buffer,vList,waves)
        print"nTrue:", nTrueList[i],"+/-",numpy.sqrt(statSquared[0,0].real)
        errorList.append(numpy.sqrt(statSquared[0,0].real))

    
        #hack work-around to get wave 1 error
    v1rawNormalizationIntegral=numpy.copy(rawNormalizationIntegral)
    v1rawNormalizationIntegral[waves[0].epsilon,waves[0].epsilon,1,0]=numpy.complex(0.,0.)
    v1rawNormalizationIntegral[waves[0].epsilon,waves[0].epsilon,1,1]=numpy.complex(0.,0.)
    statSquared=calcStatSquaredError(covarianceMatrix,v1rawNormalizationIntegral,vList,waves)
    print"nTrue:", nTrueList[1],"+/-",numpy.sqrt(statSquared.real)    
    
    errorList.append(numpy.sqrt(statSquared.real))
    
    #hack workaround to get wave 2 error
    v2rawNormalizationIntegral=numpy.copy(rawNormalizationIntegral)
    v2rawNormalizationIntegral[waves[0].epsilon,waves[0].epsilon,0,0]=numpy.complex(0.,0.)
    v2rawNormalizationIntegral[waves[0].epsilon,waves[0].epsilon,0,1]=numpy.complex(0.,0.)
    statSquared=calcStatSquaredError(covarianceMatrix,v2rawNormalizationIntegral,vList,waves)
    print"nTrue:", nTrueList[2],"+/-",numpy.sqrt(statSquared.real)
    
    errorList.append(numpy.sqrt(statSquared.real))
    

    #saving our results to be used in plotting later.  format is numpy array [[nTrueTotal,nTrueWave1,nTrueWave2],[errorNTrueTotal,errorNTrueWave1,errorNTrueWave2]]
    #numpy.save(os.path.join(dataDir,"nTrueError.npy"),numpy.array([nTrueList,errorList]))
    retList=[]
    for i in range(len(nTrueList)):
        retList.append([dataDir.strip("pd_MeV"),nTrueList[i],errorList[i]])
    return retList#[[dataDir.strip("pd_MeV"),nTrueList[0],errorList[0]],[dataDir.strip("pd_MeV"),nTrueList[1],errorList[1]],[dataDir.strip("pd_MeV"),nTrueList[1],errorList[2]]]

def runGampForDirectory(keyfiles,directory):
    eventsFile=os.path.join(directory,"events.gamp")
    for keyfile in keyfiles:
        outputFile=os.path.join(directory,keyfile.strip(".key")+".bamp")
        cmd="gamp "+keyfile+" < "+eventsFile+" > "+outputFile
    
topDir=os.path.join(sys.argv[2],"data")
print"working with topDir=",topDir
"""
keyfilePWave=os.path.join("/","lustre","expphy","volatile","pkk","keyfiles","1--0-P.key")
keyfileDWave=os.path.join("/","lustre","expphy","volatile","pkk","keyfiles","2++0-D.key")
keyfiles=[keyfilePWave,keyfileDWave]
"""
print"="*80

retList=[]

for dirpath, dirnames, filenames in os.walk(topDir):
    #if dirpath.find("pd_MeV")!=-1:
    if dirpath.find(sys.argv[1]+"_MeV")!=-1:
        if dirpath.find("set_")==-1:
            if dirpath.find(sys.argv[1]+"_MeV/data")==-1:
                if dirpath.find("mc")==-1:
                    if dirpath.find(".ipynb_checkpoints")==-1:
                        print"processing",dirpath
                        ret=calcNTrueForDir(dirpath)
                        retList.append(ret)

plotLists=[[] for i in range(len(retList[0]))]
for bin in retList:
    for item in bin:
        plotLists[bin.index(item)].append(item)


for lists in plotLists:
    numpy.save(os.path.join(topDir,"results","nTrueList-"+str(plotLists.index(lists))+"_"+sys.argv[1]+".npy"),lists)
                
print"done"
