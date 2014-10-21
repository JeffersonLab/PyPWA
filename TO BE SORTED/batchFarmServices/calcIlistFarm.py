"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import numpy 
import os
import sys
import time
#sys.path.append("/home/salgado/bdemello/pythonPWA/pythonPWA")
from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
#from pythonPWA.utilities.OHMintensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader
from DataSimulatorFarm import dataSimulator



#topDir=os.path.join(sys.argv[3],"data")

#dataDir=os.path.join(topDir,sys.argv[4]+"_MeV","set_"+sys.argv[5])
dataDir = os.path.join("/","volatile","halld","pkk","data","Simulation","1000_MeV")
 
#maxNumberOfEvents=int(sys.argv[1])
maxNumberOfEvents=50000



testMass = 1025





alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
print("1")





#resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[0.,1.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[1.,0.],w0=1670.,r0=259.)]


#resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[0.,1.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[1.,0.],w0=1670.,r0=259.)]
resonances=[resonance(cR=.27*maxNumberOfEvents,wR=[1.,0.,0.,0.],w0=1260.,r0=300.),
                                            resonance(cR=.45*maxNumberOfEvents,wR=[0.,1.,0.,0.],w0=1320.,r0=107.),
                                            resonance(cR=.06*maxNumberOfEvents,wR=[0.,0.,1.,0.],w0=1600.,r0=234.),
                                            resonance(cR=.22*maxNumberOfEvents,wR=[0.,0.,0.,1.],w0=1670.,r0=259.)]
print("2")            


waves=getwaves(dataDir)
print("3")


normint=numpy.load(os.path.join(dataDir,"normint.npy"))
print("4")

dSimulator=dataSimulator(mass=testMass,waves=waves,resonances=resonances,normint=normint,alphaList=alphaList,dataDir=dataDir)
print("5")
TS = time.time()
print("START")
retIList=dSimulator.calcIList()
TS1 = time.time()
print("DONE "+str((TS1-TS)/60)+"minutes")
numpy.save(os.path.join(dataDir,"iListnew.npy"),retIList)

