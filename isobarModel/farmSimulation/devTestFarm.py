"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import numpy
import os
import sys
sys.path.append(os.path.join(sys.argv[2],"pythonPWA"))
from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader 
from batchFarmServices.dataSimulatorNPY import dataSimulator
import operator

from batchFarmServices.rhoAA import rhoAA

Control = numpy.load(os.path.join(sys.argv[2],"GUI","Control_List.npy"))

dataDir=os.path.join(sys.argv[2],"simulation",sys.argv[1]+"_MeV")
topDir=os.path.join(sys.argv[2])

alphaList=numpy.loadtxt(os.path.join(dataDir,"mc","raw","alphaevents.txt"))
              
maxNumberOfEvents=float(len(alphaList))   

testMass= int(sys.argv[1])+(int(Control[4])/2.)

resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[0.,1.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[1.,0.],w0=1670.,r0=259.)]

contents=numpy.load(os.path.join(dataDir,"Vvalues.npy"))    
orderedContents=sorted(contents.tolist().iteritems(),key=operator.itemgetter(0))    
productionAmplitudes=[]
for i in range(0,len(orderedContents),2):
    realPart=orderedContents[i][1]
    imaginaryPart=orderedContents[i+1][1]
    productionAmplitudes.append(numpy.complex(realPart,imaginaryPart))
    
waves=getwaves(os.path.join(dataDir,"mc","raw"))
               
normint=numpy.load(os.path.join(dataDir,"mc","raw","normint.npy"))

if sys.argv[3] == "i":
    if os.path.isfile(os.path.join(dataDir,"mc","raw","rhoAA.npy")):
        rhoAA = numpy.load(os.path.join(dataDir,"mc","raw","rhoAA.npy"))
    if not os.path.isfile(os.path.join(dataDir,"mc","raw","rhoAA.npy")):
        rAA = rhoAA(waves=waves,alphaList=alphaList,beamPolarization=float(Control[1]))
        rhoAA = rAA.calc()  
        numpy.save(os.path.join(dataDir,"mc","raw","rhoAA.npy"),rhoAA)

    dSimulator=dataSimulator(mass=testMass,waves=waves,resonances=resonances,productionAmplitudes=productionAmplitudes,normint=normint,alphaList=alphaList,rhoAA=rhoAA)
    iList = dSimulator.calcIList()
    numpy.save(os.path.join(dataDir,"mc","raw","iList"),iList)

elif if sys.argv[3] == "s":
    inputGampFile=open(os.path.join(dataDir,"mc","raw","events.gamp"),'r')
    inputPfFile=open(os.path.join(dataDir,"mc","raw","events.pf"),'r')
    outputRawGampFile=open(os.path.join(dataDir,"data","selected_events.raw.gamp"),'w')
    outputAccGampFile=open(os.path.join(dataDir,"data","selected_events.acc.gamp"),'w')
    
    rhoAA = numpy.load(os.path.join(dataDir,"mc","raw","rhoAA.npy"))
                
    iList = numpy.load(os.path.join(dataDir,"mc","raw","iList.npy"))

    iMax = numpy.load(os.path.join(dataDir,"mc","raw","iMax.npy"))

    dSimulator=dataSimulator(mass=testMass,waves=waves,resonances=resonances,productionAmplitudes=productionAmplitudes,normint=normint,alphaList=alphaList,rhoAA=rhoAA,iList=iList,iMax=iMax)

    dSimulator.execute(inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile)
                

