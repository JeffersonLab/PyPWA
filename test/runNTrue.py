import numpy
import os

from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader
from pythonPWA.utilities.dataSimulator import dataSimulator
from pythonPWA.model.nTrue import nTrueForFixedV1V2 as ntrue
from pythonPWA.model.nTrue import nTrueForFixedV1V2AndWave as ntrueforwave
from pythonPWA.model.nTrue import calcStatSquaredError

dataDir=os.path.join("/","home","salgado","pkk","data","1000pd_MeV")
print"working with dataDir=",dataDir
    
waves=getwaves(dataDir)
print"loaded",len(waves),"waves"

accNormInt=numpy.load(os.path.join(dataDir,"mc","normint.npy"))#removed mc

v1=numpy.complex(0.1346340081457815,-0.030796926688671816)

v2=numpy.complex(0.10799449275227248,-0.024710925389957686)

ntrueVal=ntrue([v1,v2],waves,accNormInt)


vList=[v1,v2]

nTrueList=[]

for wave in waves:
    nTrueList.append(ntrueforwave(vList[waves.index(wave)],waves,wave,accNormInt))
    


rawNormalizationIntegral=numpy.load(os.path.join(dataDir,"normint.npy"))
covarianceMatrix=numpy.load(os.path.join(dataDir,"minuitCovar.npy"))
statSquared=calcStatSquaredError(covarianceMatrix,rawNormalizationIntegral,vList,waves)
print rawNormalizationIntegral[waves[0].epsilon,waves[0].epsilon,1,0]
"""
for wave in waves:
    print"statSquaredError:", calcStatSquaredError(covarianceMatrix,rawNormalizationIntegral,vList,[wave])
"""
print"covariance:",covarianceMatrix
print"="*10
print"nTrue:", ntrueVal,"+/-",numpy.sqrt(statSquared.real)
print"="*10
v1rawNormalizationIntegral=numpy.copy(rawNormalizationIntegral)
v1rawNormalizationIntegral[waves[0].epsilon,waves[0].epsilon,1,0]=numpy.complex(0.,0.)
v1rawNormalizationIntegral[waves[0].epsilon,waves[0].epsilon,1,1]=numpy.complex(0.,0.)
statSquared=calcStatSquaredError(covarianceMatrix,v1rawNormalizationIntegral,vList,waves)
print"nTrue:", nTrueList[0],"+/-",numpy.sqrt(statSquared.real)
print"="*10
v2rawNormalizationIntegral=numpy.copy(rawNormalizationIntegral)
v2rawNormalizationIntegral[waves[0].epsilon,waves[0].epsilon,0,0]=numpy.complex(0.,0.)
v2rawNormalizationIntegral[waves[0].epsilon,waves[0].epsilon,0,1]=numpy.complex(0.,0.)
statSquared=calcStatSquaredError(covarianceMatrix,v2rawNormalizationIntegral,vList,waves)
print"nTrue:", nTrueList[1],"+/-",numpy.sqrt(statSquared.real)
