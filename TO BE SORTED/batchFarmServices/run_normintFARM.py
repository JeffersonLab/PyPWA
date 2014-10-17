import os
import sys 
sys.path.append(os.path.join("/volatile","clas","clasg12","salgado","omega","pythonPWA"))
import numpy
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt

dataDir=sys.argv[1]
alphaList=numpy.loadtxt(os.path.join(dataDir,sys.argv[2]))    
waves=getwaves(dataDir)
rInt=normInt(waves=waves,alphaList=alphaList)
rInt.execute()
rInt.save(dataDir)
