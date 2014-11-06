"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
from math import log 
from pythonPWA.model.complexV import complexV
from pythonPWA.model.spinDensity import spinDensity
from pythonPWA.model.intensity import intensity
from random import random
import numpy as np
import os, math

class FASTLikelihood(object):
    
    def __init__(self,
                waves=[],
                productionAmplitudes=[],
                normint=None,
                alphaList=[],
                beamPolarization=.4,
                mass=1010.,
                eventNumber=7540,
                acceptedPath=os.getcwd(),
                generatedPath=os.getcwd(),
                accAlphaList=[],
                rhoAA = None,
                accNormInt=None,
                rawAlphaList=[],
                rawNormInt=None,                
                ):
        
        self.waves=waves
        self.productionAmplitudes=productionAmplitudes
        self.normint=normint
        self.alphaList=alphaList
        self.beamPolarization=beamPolarization
        self.mass=mass
        self.eventNumber=len(self.alphaList)
        self.nwaves = len(self.waves)
        self.acceptedPath=acceptedPath
        self.generatedPath=generatedPath
        self.debugPrinting=0
        self.iList=[]
        self.accAlphaList=accAlphaList
        self.accNormInt=accNormInt.sum(0).sum(0)
        self.rawAlphaList=rawAlphaList
        self.rawNormInt=rawNormInt
        self.rhoAA = rhoAA
        self.etaX = 0.
        
    
#    def countAlphas(self,fname):   This function will be able to read the .num file
#        with open(fname) as f:      instead of reading the entire file length. Uncomment
#            num = f.readlines()        it and comment '#' out the next function to
#        return float(num[0])           use it. 

    def countAlphas(self,path):
        Alpha = open(path,'r')
        AlphaList = Alpha.readlines()
        return float(len(AlphaList)) 
       
    def calcetaX(self):
        self.etaX=(self.countAlphas(self.acceptedPath)/self.countAlphas(self.generatedPath))
        

    def calclnL(self):       
        a0 = 0.
        a1 = 0.
        for i in range(self.nwaves):
            for j in range(self.nwaves):
                VV = self.productionAmplitudes[i] * np.conjugate(self.productionAmplitudes[j])                
                a0 = a0 + (VV * self.rhoAA[i,j,:]).real                
                a1 = a1 + (VV * self.accNormInt[i,j]).real 
        return -((np.log(a0)).sum(0)) + (self.etaX * a1)

    def calcneglnL(self,paramsList):
            self.productionAmplitudes=paramsList
            self.calcetaX()
            LLog = self.calclnL()    
            print"LLog:",LLog        
            return LLog

