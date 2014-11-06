import numpy
import os

from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader
#from pythonPWA.utilities.dataSimulatorFarm import dataSimulator
from pythonPWA.utilities.dataSimulator import dataSimulator
import matplotlib.pyplot as plt
import numpy
import os
import operator
import numpy
import time

#dataDir=os.path.join("/","home","salgado","pkk","data","1050_MeV")#
#print"working with dataDir=",dataDir
#topDir=os.path.join("/","home","salgado","pkk","data","Simulation")
topDir=os.path.join("/","volatile","halld","pkk","data")
print"working with dataDir=",topDir

maxNumberOfEvents=50000.

iMax=0.
iMaxList=[]

for dirpath, dirnames, filenames in os.walk(topDir):
    if dirpath.find("_MeV")!=-1:
        if dirpath.find("mc")==-1:
            if dirpath.find(".ipynb_checkpoints")==-1:
                if "iList.npy" in filenames:
                    print dirpath                    
                    print"loading iList.npy"
                    iList=numpy.load(os.path.join(dirpath,"iList.npy"))
                    iMaxList.append(max(iList))
                if "iList.npy" not in filenames:
                    print"not loading iList.npy"
                    dataDir=dirpath
    
                    alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
                    print"loaded alphaFile",os.path.join(dataDir,"alphaevents.txt"),"with",len(alphaList),"events"
    
                    maxNumberOfEvents=float(len(alphaList))
                    
                    testMass=1075.
        
        
                                    #resonances=[resonance(cR=maxNumberOfEvents,wR=[1.],w0=1320.,r0=100000.)]
                                    #resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[1.,0.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[0.,1.],w0=1895.,r0=235.)]                                    
                    resonances=[resonance(cR=.27*maxNumberOfEvents,wR=[1.,0.,0.,0.],w0=1260.,r0=300.),resonance(cR=.45*maxNumberOfEvents,wR=[0.,1.,0.,0.],w0=1320.,r0=107.),resonance(cR=.06*maxNumberOfEvents,wR=[0.,0.,1.,0.],w0=1600.,r0=234.),resonance(cR=.22*maxNumberOfEvents,wR=[0.,0.,0.,1.],w0=1670.,r0=259.)]
        
                    print"loaded",len(resonances),"resonances"
            
                    waves=getwaves(dataDir)
                    print"loaded",len(waves),"waves"
        
                    #rInt=normInt(waves=waves,alphaList=alphaList)
                    #rInt.execute()
                    #rInt.save(dataDir)
                        #rInt=normInt(waves=waves,alphaList=alphaList)
                        #rInt.execute()
                        #rInt.save(dataDir)
                    normint=numpy.load(os.path.join(dataDir,"normint.npy"))
                    print"loaded normint"
        
                                    
                    dSimulator=dataSimulator(mass=testMass,waves=waves,resonances=resonances,normint=normint,alphaList=alphaList)
                    print"created dataSimulator"
                        
                    print"calculating IList"
                    retIList=dSimulator.calcIList()
                                    
                    numpy.save(os.path.join(dataDir,"iList.npy"),retIList)
                    print"done and saved"
                    iMaxList.append(max(retIList))

iMax=max(iMaxList)
print"="*80
for dirpath, dirnames, filenames in os.walk(topDir):
    if dirpath.find("pd_MeV")==-1:
        if dirpath.find("MeV")!=-1:
            if dirpath.find("raw")==-1:
                if dirpath.find("mc")==-1:
                    if dirpath.find("acc")==-1:
                        if dirpath.find("Simulation")!=-1:
                            if dirpath.find(".ipynb_checkpoints")==-1:
                                print"processing",dirpath
                                dataDir=dirpath

                                alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
                                print"loaded alphaFile",os.path.join(dataDir,"alphaevents.txt"),"with",len(alphaList),"events"

                
    
                                testMass=float(dataDir.strip(topDir).strip("_MeV").strip("Simulation/"))+25.
                                print"using testMass=",testMass


                #resonances=[resonance(cR=maxNumberOfEvents,wR=[1.],w0=1320.,r0=100000.)]
                                #resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[0.,1.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[1.,0.],w0=1895.,r0=235.)]
                                resonances=[resonance(cR=.27*maxNumberOfEvents,wR=[1.,0.,0.,0.],w0=1260.,r0=300.),
                                            resonance(cR=.45*maxNumberOfEvents,wR=[0.,1.,0.,0.],w0=1320.,r0=107.),
                                            resonance(cR=.06*maxNumberOfEvents,wR=[0.,0.,1.,0.],w0=1600.,r0=234.),
                                            resonance(cR=.22*maxNumberOfEvents,wR=[0.,0.,0.,1.],w0=1670.,r0=259.)]

                                print"loaded",len(resonances),"resonances"
    
                                waves=getwaves(dataDir)
                                print"loaded",len(waves),"waves"

                #rInt=normInt(waves=waves,alphaList=alphaList)
                #rInt.execute()
                #rInt.save(dataDir)
                                normint=numpy.load(os.path.join(dataDir,"normint.npy"))
                                print"loaded normint"
                                    
                                dSimulator=dataSimulator(mass=testMass,waves=waves,resonances=resonances,normint=normint,alphaList=alphaList)
                                print"created dataSimulator"                                
                                inputGampFile=open(os.path.join(dataDir,"events.gamp"),'r')
                                inputPfFile=open(os.path.join(dataDir,"events.pf"),'r')
                                
                                outputRawGampFile=open(os.path.join(dataDir,"selected_events.raw.gamp"),'w')
                                outputAccGampFile=open(os.path.join(dataDir,"selected_events.acc.gamp"),'w')
                                print"executing"
                                #dSimulator.execute(inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile)
                                iList=numpy.load(os.path.join(dataDir,"iList.npy"))
                                dSimulator.calcWList(iList,iMax,inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile)
                
print"done"
"""
gampSizes=[]
masses=[]


#this code block sorts the directories that satisfy the requirements set forth here
def satisfies(dirName):
    if dirName.find("pd_MeV")!=-1:
        if dirpath.find("mc")==-1:
            if dirpath.find(".ipynb_checkpoints")==-1:
                return 1

sortedBins=sorted([os.path.join(topDir,x) for x in os.listdir(topDir) if satisfies(x)==1])
#

for dirpath, dirnames, filenames in os.walk(topDir):
    if dirpath.find("pd_MeV")!=-1:
        if dirpath.find("mc")==-1:
            if dirpath.find(".ipynb_checkpoints")==-1:
                igreader=gampReader(gampFile=open(os.path.join(dirpath,"events.gamp"),'r'))
                inputGampEvents=igreader.readGamp()
                gampSizes.append(len(inputGampEvents))
                masses.append(float(dirpath.strip(topDir).strip("pd_MeV")))
                
x = masses
y = gampSizes

#plot data
plt.plot(x, y,'ro')

#configure  X axes
#plt.xlim(0.5,4.5)
#plt.xticks([1,2,3,4])

#configure  Y axes
#plt.ylim(19.8,21.2)
#plt.yticks([20, 21, 20.5, 20.8])

#labels
plt.xlabel("mass")
plt.ylabel("event count")

#title
plt.title("event count vs mass")

#show plot
plt.show()

print"mass\t\tevent count"
for i in range(len(x)):
    print x[i],"\t",y[i]


#sorting test