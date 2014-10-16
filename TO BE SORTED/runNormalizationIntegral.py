import numpy
import os
import sys

from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt


dataDir=os.path.join("/","volatile","halld","pkk","data","4waves","1050d2p2_MeV","mc")
print"working with dataDir=",dataDir

alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
print"loaded alphaFile",os.path.join(dataDir,"alphaevents.txt"),"with",len(alphaList),"events"
    
waves=getwaves(dataDir)
print"loaded",len(waves),"waves"

rInt=normInt(waves=waves,alphaList=alphaList)
rInt.execute()
rInt.save(dataDir)

rInt.writeToAscii(dataDir)