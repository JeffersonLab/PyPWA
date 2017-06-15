#! /u/apps/anaconda/2.4/bin/python2  
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
import fileinput
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
    generator=fnGenerator.generator()
    generator.fileName=os.path.join(os.getcwd(),"generatedFn.py")
    generator.createFile(len(waves)*2)
    execfile(os.path.join(os.getcwd(),"generatedFn.py"))

    m.set_up(0.5)
    m.set_strategy(2)
    m.migrad(ncall=int(Control[6]))
else:
    kwdargs = []
    params = []  
    for line in fileinput.input([os.path.join(sys.argv[2],"scripts","minInit.txt")]):
        if line[0] != '#':
            kvAs = line.split()
            params.append(kvAs[0].split("=")[0])
            for kvAx in kvAs:
                kwdargs.append(kvAx)
    f = open(os.path.join(os.getcwd(),"generatedFn.py"),"w+")
    f.write("def fn(")
    for p in params:
        if p != params[-1]:
            f.write(str(p)+",")
        else:
            f.write(str(p)+"):\n")
    f.write("    retList=[")
    for i in range(0,len(params),2):
        if params[i+1] != params[-1]:
            f.write("numpy.complex("+params[i]+","+params[i+1]+"),")
        else:
            f.write("numpy.complex("+params[i]+","+params[i+1]+")]\n")
    f.write("    return minuitLn.calcneglnL(retList)\n\n")
    f.write("m=Minuit(fn,")
    for k in kwdargs:
        if k != kwdargs[-1]:
            f.write(str(k)+",")
        else:
            f.write(str(k)+")")
    f.close()
    execfile(os.path.join(os.getcwd(),"generatedFn.py"))
    m.set_up(0.5)
    m.set_strategy(2)
    m.migrad(ncall=int(Control[6]))
    
Vvalues = m.values
numpy.save(os.path.join(dataDir,"Vvalues.npy"),Vvalues)
covariance=numpy.array(m.matrix())
numpy.save(os.path.join(dataDir,"minuitCovar3.npy"),covariance)
