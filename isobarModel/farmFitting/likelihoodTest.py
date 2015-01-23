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
import fnGenerator
from iminuit import Minuit

indir = sys.argv[2]
Control = numpy.load(os.path.join(indir,"GUI","Control_List.npy"))
dataDir=os.path.join(indir,"fitting",sys.argv[1]+"_MeV")
alphaList=numpy.loadtxt(os.path.join(dataDir,"data","alphaevents.txt"))
maxNumberOfEvents=float(len(alphaList))
waves=getwaves(os.path.join(dataDir,"data"))
normint=numpy.load(os.path.join(dataDir,"mc","raw","normint.npy"))
accNormInt=numpy.load(os.path.join(dataDir,"mc","acc","normint.npy"))
acceptedPath=os.path.join(dataDir,"mc","acc","alphaevents.txt")
generatedPath=os.path.join(dataDir,"mc","raw","alphaevents.txt")
print float(Control[1])
print float(Control[6])
if os.path.isfile(os.path.join(dataDir,"data","rhoAA.npy")):
    rhoAA = numpy.load(os.path.join(dataDir,"data","rhoAA.npy"))
if not os.path.isfile(os.path.join(dataDir,"data","rhoAA.npy")):
    rAA = rhoAA(waves=waves,alphaList=alphaList,beamPolarization=float(Control[1]))
    rhoAA = rAA.calc()  
    numpy.save(os.path.join(dataDir,"data","rhoAA.npy"),rhoAA)
minuitLn=FASTLikelihood(waves=waves,normint=normint,alphaList=alphaList,acceptedPath=acceptedPath,generatedPath=generatedPath,accNormInt=accNormInt,rhoAA=rhoAA)
generator=fnGenerator.generator()
generator.fileName=os.path.join(os.getcwd(),"generatedFn.py")
generator.createFile(len(waves)*2)
execfile(os.path.join(os.getcwd(),"generatedFn.py"))

m.set_strategy(2)
m.set_up(0.5)
m.migrad(ncall=int(Control[6]))

Vvalues = m.values
numpy.save(os.path.join(dataDir,"Vvalues.npy"),Vvalues)
covariance=numpy.array(m.matrix())
numpy.save(os.path.join(dataDir,"minuitCovar3.npy"),covariance)
