import numpy
import os
import sys
sys.path.append("/u/home/jpond/bdemello/bdemello/pythonPWA/pythonPWA")

from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader
#from pythonPWA.utilities.dataSimulator import dataSimulator
from DataSimulatorFarm import dataSimulator

dataDir=os.path.join("/volatile","halld","pippimpi0","data",sys.argv[1]+"_MeV","set_"+sys.argv[2])


alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))


maxNumberOfEvents=float(len(alphaList))
    
testMass=1025.



#resonances=[resonance(cR=maxNumberOfEvents,wR=[1.],w0=1320.,r0=100000.)]
resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[0.,1.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[1.,0.],w0=1895.,r0=235.)]


    
waves=getwaves(dataDir)


rInt=normInt(waves=waves,alphaList=alphaList)
rInt.execute()
rInt.save(dataDir)
normint=numpy.load(os.path.join(dataDir,"normint.npy"))


dSimulator=dataSimulator(mass=testMass,waves=waves,resonances=resonances,normint=normint,alphaList=alphaList)

inputGampFile=open(os.path.join(dataDir,"events.gamp"),'r')
inputPfFile=open(os.path.join(dataDir,"events.pf"),'r')
outputRawGampFile=open(os.path.join(dataDir,"seq_raw_events.gamp"),'w')
outputAccGampFile=open(os.path.join(dataDir,"selected_events.acc.gamp"),'w')

dSimulator.execute(inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile)


