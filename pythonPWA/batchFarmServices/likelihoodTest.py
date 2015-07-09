#! /u/apps/anaconda/anaconda-2.0.1/bin/python2 
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
"""
    This is the main program for running the calculation of the log likelihood fitter/minuit
"""

import numpy
import os
import sys
sys.path.append(os.path.join(sys.argv[2],"pythonPWA"))
from pythonPWA.fileHandlers.getWavesGen import getwaves
from batchFarmServices.fast_like import FASTLikelihood
from batchFarmServices.rhoAA import rhoAA
from iminuit import Minuit

def minFn(*args):
    retList=[numpy.complex(args[i],args[i+1]) for i in range(0,len(args),2)]
	return minuitLn.calcneglnL(retList)

def initParsre(fileName):
    kwdargs = {}  
    for line in fileinput.input([dataFile]):
        if line[0] != '#':
            kvAs = line.split()
            for kvAx in kvAs:
                kwdargs[str(kvAx.split("=")[0])] = float(kvAx.split("=")[1])
    return kwdargs 

indir = sys.argv[2]
Control = numpy.load(os.path.join(indir,"GUI","Control_List.npy"))
dataDir=os.path.join(indir,"fitting",sys.argv[1]+"_MeV")
alphaList=numpy.loadtxt(os.path.join(dataDir,"data","alphaevents.txt"))
if os.path.isfile(os.path.join(dataDir,"data","QFactor.txt")):
    QFactor = numpy.loadtxt(os.path.join(dataDir,"data","QFactor.txt"))
else:
    QFactor = [1]
maxNumberOfEvents=float(len(alphaList))
waves=getwaves(os.path.join(dataDir,"data"))
normint=numpy.load(os.path.join(dataDir,"mc","raw","normint.npy"))
accNormInt=numpy.load(os.path.join(dataDir,"mc","acc","normint.npy"))
acceptedPath=os.path.join(dataDir,"mc","acc","alphaevents.txt")
generatedPath=os.path.join(dataDir,"mc","raw","alphaevents.txt")
rAA = rhoAA(waves=waves,alphaList=alphaList,beamPolarization=float(Control[1]))
rhoAA = rAA.calc()  
numpy.save(os.path.join(dataDir,"data","rhoAA.npy"),rhoAA)
minuitLn=FASTLikelihood(waves=waves,alphaList=alphaList,acceptedPath=acceptedPath,generatedPath=generatedPath,accNormInt=accNormInt,Q=QFactor,rhoAA=rhoAA)
if not os.path.isfile(os.path.join(sys.argv[2],"scripts","minInit.txt")):
    kwdarg = {"t"+str(i):.01 for i in range(len(waves)*2)}
    kwdarg['errordef']=0.5
    m=Minuit(minfn,**kwdarg)
    m.set_strategy(2)
    m.migrad(ncall=int(Control[6]))
else:
    kwdarg = initParser(os.path.join(sys.argv[2],"scripts","minInit.txt"))
    kwdarg['errordef']=0.5
    m=Minuit(minfn,**kwdarg)
    m.set_strategy(2)
    m.migrad(ncall=int(Control[6]))
    
Vvalues = m.values
numpy.save(os.path.join(dataDir,"Vvalues.npy"),Vvalues)
covariance=numpy.array(m.matrix())
numpy.save(os.path.join(dataDir,"minuitCovar3.npy"),covariance)
