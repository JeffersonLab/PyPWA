'''
Created on Jun 10, 2014

@author: jpond
'''
import numpy
import os

from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader
from pythonPWA.utilities.minuitLikelihood import minuitLikelihood

dataDir=os.path.join("/","home","salgado","pkk","data",raw_input("BIN? (number only)")+"_MeV")
print"working with dataDir=",dataDir

alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
print"loaded alphaFile",os.path.join(dataDir,"alphaevents.txt"),"with",len(alphaList),"events"

maxNumberOfEvents=float(len(alphaList))

testMass=1025.
print"using testMass=",testMass

#resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[1.,0.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[0.,1.],w0=1895.,r0=235.)]
#print"loaded",len(resonances),"resonances"
    
waves=getwaves(dataDir)
print"loaded",len(waves),"waves"

#rInt=normInt(waves=waves,alphaList=alphaList)
normint=numpy.load(os.path.join(dataDir,"normint.npy"))


#setting the directories
acceptedPath=os.path.join(dataDir,"alphaevents.txt")
generatedPath=os.path.join(dataDir,"alphaevents.txt")

#minuitLn=minuitLikelihood(resonances=resonances,waves=waves,normint=normint,alphaList=alphaList,acceptedPath=acceptedPath,generatedPath=generatedPath)
minuitLn=minuitLikelihood(waves=waves,normint=normint,alphaList=alphaList,acceptedPath=acceptedPath,generatedPath=generatedPath)
minuitLn.calcneglnL(wave1Re=.0625,wave1Im=-.0109,wave2Re=.0438,wave2Im=-.0089)
numpy.save(os.path.join(dataDir,"minuitIList"),minuitLn.iList)
print"done"