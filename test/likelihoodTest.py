import numpy
import os
from pythonPWA.dataTypes.resonance import resonance
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt
from pythonPWA.model.intensity import intensity
from pythonPWA.fileHandlers.gampReader import gampReader
from pythonPWA.utilities.minuitLikelihood import minuitLikelihood
import fnGenerator

from iminuit import Minuit

dataDir=os.path.join("/","volatile","halld","pkk","data","4waves","1050d2p2_MeV")
alphaList=numpy.loadtxt(os.path.join(dataDir,"alphaevents.txt"))
maxNumberOfEvents=float(len(alphaList))
testMass=1325.    
waves=getwaves(dataDir)
normint=numpy.load(os.path.join(dataDir,"mc","normint.npy"))
accNormInt=numpy.load(os.path.join(dataDir,"mc","normint.npy"))
acceptedPath=os.path.join(dataDir,"mc","alphaevents.txt")
generatedPath=os.path.join(dataDir,"mc","alphaevents.txt")


minuitLn=minuitLikelihood(waves=waves,normint=normint,alphaList=alphaList,acceptedPath=acceptedPath,generatedPath=generatedPath,accNormInt=accNormInt)

generator=fnGenerator.generator()
generator.fileName=os.path.join(os.getcwd(),"generatedFn.py")
generator.createFile(8)

execfile(os.path.join(os.getcwd(),"generatedFn.py"))
#m = Minuit(fn,error_t0 = 10.,error_t1 = 10.,error_t2 = 10.,error_t3 = 10.,error_t4 = 10.,error_t5 = 10.,error_t6 = 10.,error_t7 = 10.,)

m.set_strategy(0)
m.set_up(0.5)
m.migrad(ncall=500)

#m.draw_profile('t0')

Vvalues = m.values
numpy.save(os.path.join(dataDir,"Vvalues.npy"),Vvalues)
covariance=numpy.array(m.matrix())
numpy.save(os.path.join(dataDir,"minuitCovar3.npy"),covariance)
