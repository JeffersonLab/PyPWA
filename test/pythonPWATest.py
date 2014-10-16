import os
import numpy

from dataTypes.resonance import resonance
from fileHandlers.getWaves import getwaves
from model.normInt import normInt
from model.getPhi import getPhi
from model.complexV import complexV
from model.nTrue import nTrue
from model.nTrue import nTrueForWave
from utilities.plotter import plotter
from model.intensity import intensity
from model.spinDensity import spinDensity

if __name__==('__main__'):

    dataDir=os.path.join(os.getcwd(),"data","1000_MeV")
    print"working with dataDir=",dataDir

    alphaList=numpy.loadtxt(os.path.join(dataDir,"alpha.txt"))
    print"loaded alphaFile",os.path.join(dataDir,"alpha.txt"),"with",len(alphaList),"events"

    maxNumberOfEvents=float(len(alphaList))
    
    testMass=1400.
    print"using testMass=",testMass

    resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[1.,0.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[0.,1.],w0=1895.,r0=235.)]
    print"loaded",len(resonances),"resonances"
    
    waves=getwaves(dataDir)
    print"loaded",len(waves),"waves"

    rInt=normInt(waves=waves,alphaList=alphaList)
    normint=rInt.execute()
    #rInt.save(dataDir)
    #print"loaded raw norm int:\n",normint
    
    #for resonance in resonances:
    #    print"Phi( testMass , resonance",resonances.index(resonance),")=",getPhi(testMass,resonance)

    mass=1000.
    massList=[]
    nTrueList=[]
    nTrueWave1=[]
    nTrueWave2=[]
    while mass<=2000.:
        massList.append(mass)
        nTrueList.append(nTrue(resonances,waves,mass,normint))
        nTrueWave1.append(nTrueForWave(resonances,waves,waves[0],mass,normint))
        nTrueWave2.append(nTrueForWave(resonances,waves,waves[1],mass,normint))
        mass+=1.

    pl=plotter(xAxisData=massList,yAxisData=nTrueList,title="nTrue vs mass",xAxisTitle="mass",yAxisTitle="nTrue")
    pl.addSubPlot(nTrueWave1)
    pl.addSubPlot(nTrueWave2)
    pl.showPlot()

    itt=intensity(resonances=resonances,waves=waves,productionAmplitudes=[],normint=normint,alphaList=alphaList)