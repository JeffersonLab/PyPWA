# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 13:43:14 2014

@author: salgado
"""
import numpy
import os
import sys
from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.nTrue import nTrue
from pythonPWA.model.nTrue import nTrueForWave

dataDir=os.path.join("/","volatile","halld","pkk","data","Simulation",str(sys.argv[1]))
print"working with dataDir=",dataDir

alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
maxNumberOfEvents=float(len(alphaList))
print"loaded alphaFile",os.path.join(dataDir,"alphaevents.txt"),"with",len(alphaList),"events"

    
testMass=int(sys.argv[1].strip("_MeV"))+25
print"using testMass=",testMass

#resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[0.,1.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[1.,0.],w0=1895.,r0=235.
resonances=[resonance(cR=.27*maxNumberOfEvents,wR=[1.,0.,0.,0.],w0=1260.,r0=300.),
            resonance(cR=.45*maxNumberOfEvents,wR=[0.,1.,0.,0.],w0=1320.,r0=107.),
            resonance(cR=.06*maxNumberOfEvents,wR=[0.,0.,1.,0.],w0=1600.,r0=234.),
            resonance(cR=.22*maxNumberOfEvents,wR=[0.,0.,0.,1.],w0=1670.,r0=259.)]
print"loaded",len(resonances),"resonances"
    
waves=getwaves(dataDir)
print"loaded",len(waves),"waves"

normint=numpy.load(os.path.join(dataDir,"normint.npy"))

print"done"
TrueList=[]
print nTrue(resonances,waves,testMass,normint)
TrueList.append(testMass)
TrueList.append(nTrue(resonances,waves,testMass,normint))
for wave in waves:
        print nTrueForWave(resonances,waves,wave,testMass,normint)
        TrueList.append(nTrueForWave(resonances,waves,wave,testMass,normint))

numpy.save(os.path.join(dataDir,"total.npy"),TrueList)