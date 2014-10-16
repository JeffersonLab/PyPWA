import numpy
import os
import sys
sys.path.append("/u/home/jpond/bdemello/bdemello/pythonPWA/pythonPWA")

from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader 
from batchFarmServices.DataSimulatorFarm import dataSimulator


dataDir=os.path.join(sys.argv[4],"data",sys.argv[1]+"_MeV","set_"+sys.argv[2])
topDir=os.path.join(sys.argv[4],"data")

alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
              
maxNumberOfEvents=float(len(alphaList))   

testMass= int(sys.argv[1])+(int(sys.argv[3])/2.)

resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[0.,1.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[1.,0.],w0=1670.,r0=259.)]


    
waves=getwaves(dataDir)


               
normint=numpy.load(os.path.join(dataDir,"normint.npy"))


dSimulator=dataSimulator(mass=testMass,waves=waves,resonances=resonances,normint=normint,alphaList=alphaList)

inputGampFile=open(os.path.join(dataDir,"events.gamp"),'r')
inputPfFile=open(os.path.join(dataDir,"events.pf"),'r')
outputRawGampFile=open(os.path.join(dataDir,"selected_events.raw.gamp"),'w')
outputAccGampFile=open(os.path.join(dataDir,"selected_events.acc.gamp"),'w')
                
iList = numpy.load(os.path.join(dataDir,"iList.npy"))

iMax = max(numpy.load(os.path.join(topDir,"IMaxList.npy")))


dSimulator.calcWList(iList,iMax,inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile)
                

