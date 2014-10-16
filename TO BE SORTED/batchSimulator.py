import numpy
import os

from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWaves import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from fileHandlers.gampReader import gampReader
from pythonPWA.utilities.dataSimulator import dataSimulator


#working with bins
topDataDir=os.path.join(os.getcwd(),"data")
print"working with dataDir=",topDataDir

dataDirContents=os.listdir(topDataDir)


massBins=[]

for content in dataDirContents:
    if os.path.isdir(os.path.join(topDataDir,content)):
        if content.find("_MeV"):
            massBins.append(content)

meVList=[]
for massBin in massBins:
    meVList.append(int(massBin.strip("_MeV")))


deltaMass=(meVList[1]-meVList[0])/2.
bisectedMasses=[]
for meV in meVList:
    bisectedMasses.append(meV+deltaMass)


#working with data from above
print "beginning run on all mass bins"
for massBin in massBins:
    print "="*10
    dataDir=os.path.join(topDataDir,massBin)
    print"working with dataDir=",dataDir

    ###SAME ALPHA FILE FOR ALL BINS?  WHY ARE THERE NO ALPHA FILES IN ANY OTHER BIN BUT 1000_MeV?
    alphaList=numpy.loadtxt(os.path.join(dataDir,"alpha.txt"))
    print"loaded alphaFile",os.path.join(dataDir,"alpha.txt"),"with",len(alphaList),"events"

    maxNumberOfEvents=float(len(alphaList))
    
    testMass=bisectedMasses[massBins.index(massBin)]
    print"using testMass=",testMass

    resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[1.,0.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[0.,1.],w0=1895.,r0=235.)]
    print"loaded",len(resonances),"resonances"
    
    waves=getwaves(dataDir)
    print"loaded",len(waves),"waves"

    #normint.npy check
    print"checking normalization integral existance..."
    if os.path.exists(os.path.join(dataDir,"normint.npy"))==False:
        print"normalization integral not found, instantiating new normalization integrator"
        rInt=normInt(waves=waves,alphaList=alphaList)
        print"executing normalization integration, this may take some time"
        rInt.execute()
        print"finished, saving normalization integral"
        rInt.save(dataDir)
    if os.path.exists(os.path.join(dataDir,"normint.npy"))==True:
        print"loading normalization integral"
        normint=numpy.load(os.path.join(dataDir,"normint.npy"))
    
    dSimulator=dataSimulator(mass=testMass,waves=waves,resonances=resonances,normint=normint,alphaList=alphaList)

    inputGampFile=open(os.path.join(dataDir,"events.gamp"),'r')
    inputPfFile=open(os.path.join(dataDir,"events.pf"),'r')
    outputRawGampFile=open(os.path.join(dataDir,"selected_events.raw.gamp"),'w')
    outputAccGampFile=open(os.path.join(dataDir,"selected_events.acc.gamp"),'w')

    dSimulator.execute(inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile)

    print"done"