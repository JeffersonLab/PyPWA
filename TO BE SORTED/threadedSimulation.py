from multiprocessing import Pool
import os
import numpy
import time
from random import random

from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWaves import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from fileHandlers.gampReader import gampReader

def threadedIntensity(varlist):
    #alphaList,resonances,waves,normint,beamPolarization,mass
    alphaList=varlist[0]
    resonances=varlist[1]
    waves=varlist[2]
    normint=varlist[3]
    beamPolarization=varlist[4]
    mass=varlist[5]
    offset=varlist[6]
    #calculate intensity
    iList=[]

    #NEED OFFSET HERERERERERERERERERERERERERERERERERe
    #so basiclly I am here only working with  Y=(len(waveX.complexAmplitudes))/nProcs, waveX.complexamplitudes[:,Y]
    for event in range(len(alphaList)):
        iList.append(intensity(resonances=resonances,waves=waves,productionAmplitudes=[],normint=normint,alphaList=alphaList,beamPolarization=beamPolarization).calculate(mass,offset+event))
    return iList


def chunks(l, n):
    if n<1:
        n=1
    return [l[i:i+n] for i in range(0, len(l), n)]

if __name__=='__main__':
    #working with bins
    topDataDir=os.path.join(os.getcwd(),"data")
    print"working with dataDir=",topDataDir

    dataDirContents=os.listdir(topDataDir)


    massBins=[]

    for content in dataDirContents:
        if os.path.isdir(os.path.join(topDataDir,content)):
            if content.find("_MeV"):
                if os.path.exists(os.path.join(topDataDir,content,"alpha.txt")):
                    massBins.append(content)

    meVList=[]
    for massBin in massBins:
        meVList.append(int(massBin.strip("_MeV")))


    deltaMass=10.#(meVList[1]-meVList[0])/2.
    bisectedMasses=[]
    for meV in meVList:
        bisectedMasses.append(meV+deltaMass)



    beamPolarization=.4

    numberOfProcs=2
    
    print "using",numberOfProcs,"cores" 

    #PARALLELL
    time1=time.clock()

    for bin in massBins:
        #reading gamp
        igreader=gampReader(gampFile=open(os.path.join(topDataDir,bin,"events.gamp"),'r'))
        inputGampEvents=igreader.readGamp()

        #reading alphalist
        alphaList=numpy.loadtxt(os.path.join(topDataDir,bin,"alpha.txt"))
        print"loaded alphaFile",os.path.join(topDataDir,bin,"alpha.txt"),"with",len(alphaList),"events"

        maxNumberOfEvents=float(len(alphaList))
    
        resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[1.,0.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[0.,1.],w0=1895.,r0=235.)]
        print"loaded",len(resonances),"resonances"

        mass=bisectedMasses[massBins.index(bin)]
        print"using testMass=",mass    
    
        waves=getwaves(os.path.join(topDataDir,bin))
        print"loaded",len(waves),"waves"

        #rInt=normInt(waves=waves,alphaList=alphaList)
        normint=numpy.load(os.path.join(topDataDir,bin,"normint.npy"))
        print "normInt loaded"

        pool = Pool(processes=numberOfProcs)
    
        alphaChunks=chunks(alphaList,numberOfProcs)
        
        varlist=[]
        
        for alphaChunk in alphaChunks:
            #offset=??
            offset=0 #NEED TO DECIDE OFFSET HERE, POSSIBLY NUMPROC RELATED?
            varlist.append([alphaChunk,resonances,waves,normint,beamPolarization,mass,offset])

        print"calculating intensity"
        result = pool.map(threadedIntensity, varlist)

        iList=[]
        for results in result:
            iList.extend(results)

        iMax=max(iList)

        print"calculating weight"
        weightList=[x/iMax for x in iList]


        lastPercent=0.
        b=float(len(weightList))
        rawGampEvents=[]
        

        for wn in range(len(weightList)):
            r=random()
            if (float(wn)/b)*100. -lastPercent > 1.:
                print"random filter:",(float(wn)/b)*100.,"%"
                lastPercent=(float(wn)/b)*100.
            if weightList[wn]>r:
                inputGampEvents[wn].raw=True
                rawGampEvents.append(inputGampEvents[wn])

        outputRawGampFile=open(os.path.join(topDataDir,bin,"threaded_raw_events.gamp"),'w')

        for rawGamp in rawGampEvents:
            rawGamp.writeGamp(outputRawGampFile)

        outputRawGampFile.close()

        print"done"



    
