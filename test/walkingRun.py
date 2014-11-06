import os

from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader
from pythonPWA.utilities.minuitLikelihood import minuitLikelihood

from iminuit import Minuit
import numpy

def runGampForDirectory(keyfiles,directory):
    eventsFile=os.path.join(directory,"events.gamp")
    for keyfile in keyfiles:
        outputFile=os.path.join(directory,keyfile.strip(".key")+".bamp")
        cmd="gamp /volatile/halld/pkk/keyfiles/"+keyfile+" < "+eventsFile+" > "+outputFile
        os.system(cmd)
        print cmd

def runNormIntForDirectory(dataDir):
    alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
    print"loaded alphaFile",os.path.join(dataDir,"alpha.txt"),"with",len(alphaList),"events"
    
    waves=getwaves(dataDir)
    print"loaded",len(waves),"waves"

    rInt=normInt(waves=waves,alphaList=alphaList)
    rInt.execute()
    rInt.save(dataDir)

    rInt.writeToAscii(dataDir)



#keyfilePWave=os.path.join("/","lustre","expphy","volatile","halld","pkk","keyfiles","1--0-P.key")
#keyfileDWave=os.path.join("/","lustre","expphy","volatile","halld","pkk","keyfiles","2++0-D.key")
#pWave=keyfilePWave.strip(os.path.join("/","lustre","expphy","volatile","halld","pkk","keyfiles"))+"bamp"
#dWave=keyfileDWave.strip(os.path.join("/","lustre","expphy","volatile","halld","pkk","keyfiles"))+"bamp"
#keyfiles=[keyfilePWave,keyfileDWave]
#keyfileNames=[pWave,dWave]

def runFitterForDir(dataDir,mass):
    dataDir=dataDir
    print"working with dataDir=",dataDir
    
    alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
    print"loaded alphaFile",os.path.join(dataDir,"alphaevents.txt"),"with",len(alphaList),"events"
    
    #maxNumberOfEvents=float(len(alphaList))
        
    testMass=mass
    print"using testMass=",testMass
    
    #resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[1.,0.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[0.,1.],w0=1895.,r0=235.)]
    #resonances=[resonance(cR=2.*maxNumberOfEvents/3.,wR=[0.,1.],w0=1320.,r0=107.),resonance(cR=maxNumberOfEvents/3.,wR=[1.,0.],w0=1895.,r0=235.)]
    
    #print"loaded",len(resonances),"resonances"
        
    waves=getwaves(dataDir)
    print"loaded",len(waves),"waves"
    print"wv1.complexamplitudes:",len(waves[0].complexamplitudes)
    print"wv2.complexamplitudes:",len(waves[1].complexamplitudes)
    
    #rInt=normInt(waves=waves,alphaList=alphaList)
    normint=numpy.load(os.path.join(dataDir,"mc","normint.npy"))
    accNormInt=numpy.load(os.path.join(dataDir,"mc","normint.npy"))
    
    
    #THESE DIRECTORIES NEED TO BE SET
    acceptedPath=os.path.join(dataDir,"mc","alphaevents.txt")
    generatedPath=os.path.join(dataDir,"mc","alphaevents.txt")
    
    
    
    #minuitLn=minuitLikelihood(resonances=resonances,waves=waves,normint=normint,alphaList=alphaList,acceptedPath=acceptedPath,generatedPath=generatedPath)
    minuitLn=minuitLikelihood(waves=waves,normint=normint,alphaList=alphaList,acceptedPath=acceptedPath,generatedPath=generatedPath,accNormInt=accNormInt)
    
    #CHANGE THESE VALUES IN ORDER TO TEST THE RESULTS OF THE CALCNEGLNL FUNCTION
    #wave1Re=.1
    #wave1Im=.1
    #wave2Re=.1
    #wave2Im=.1
    
    #print minuitLn.calcneglnL(wave1Re,wave1Im,wave2Re,wave2Im)
    
    #UNCOMMENT THE LINES BELOW TO TEST THE MINUIT MINIMIZATION OF THE CALCNEGLNL FUNCTION
    m=Minuit(minuitLn.calcneglnL,wave1Re=0.01,wave2Re=0.01,wave1Im=-0.01,wave2Im=-0.01)#,fix_wave1Im=True,fix_wave2Im=True)
    m.set_strategy(1)
    m.set_up(0.5)
    m.migrad(ncall=1000)
    Vvalues = m.values
    print Vvalues
    numpy.save(os.path.join(dataDir,"Vvalues.npy"),Vvalues)
    #m.draw_profile('wave1Re')
    #m.draw_profile('wave2Re')
    covariance=numpy.array(m.matrix())
    #covariance=numpy.array(m.covariance())
    numpy.save(os.path.join(dataDir,"minuitCovar3.npy"),covariance)
    print covariance
    print"done"

topDir=os.path.join("/","volatile","halld","pkk","data","4waves")
print"working with topDir=",topDir
keyfileNames=["1--0-P.key","1--1+P.key","2++0-D.key","2++1+D.key"]

print"="*80
for dirpath, dirnames, filenames in os.walk(topDir):
    if dirpath.find("1000d2p2_MeV")==-1:
        if dirpath.find("MeV")!=-1:
            if dirpath.find("raw")==-1:
                if dirpath.find("mc")!=-1:
                    if dirpath.find("acc")==-1:
                        if dirpath.find("4waves")!=-1:
                            if dirpath.find(".ipynb_checkpoints")==-1:
                                print"processing",dirpath
                                runGampForDirectory(keyfileNames,dirpath)
                                #runNormIntForDirectory(dirpath)
                            #mev=dirpath.strip(topDir).strip("Simulation").strip("pd_MeV")
                            #os.system("cp "+os.path.join(dirpath,"selected_events.raw.gamp")+" /home/salgado/pkk/data"+mev+"pd_MeV/events.gamp")                        
                            #os.system("cp /home/salgado/pkk/data/"+mev+"pd_MeV/mc/normint.npy /volatile/halld/pkk/data/"+mev+"pd_MeV/mc/normint.npy")
                            #print runGampForDirectory(keyfiles,dirpath,keyfileNames)
                    
                            #runFitterForDir(dirpath,float(mev.strip("/")))
