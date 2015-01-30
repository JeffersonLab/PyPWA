"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 

import numpy as np
import os
"""
    This is the mathmatical class of the likelihood calculation and the calculation of the intensity. 
"""

class FASTLikelihood(object):
    
    def __init__(self,
                waves=[],
                productionAmplitudes=[],                
                alphaList=[],               
                acceptedPath=os.getcwd(),
                generatedPath=os.getcwd(),                
                rhoAA = None,
                accNormInt=None,                               
                ):
        
        self.waves=waves
        self.productionAmplitudes=productionAmplitudes
        self.alphaList=alphaList
        self.nwaves = len(self.waves)
        self.acceptedPath=acceptedPath
        self.generatedPath=generatedPath
        self.iList=[]
        self.accAlphaList=accAlphaList
        self.accNormInt=accNormInt.sum(0).sum(0)
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

    def calcInt(self):        
        a0 = 0.        
        for i in range(self.nwaves):
            for j in range(self.nwaves):
                VV = self.productionAmplitudes[i] * np.conjugate(self.productionAmplitudes[j])                
                a0 = a0 + (VV * self.rhoAA[i,j,:]).real    
        return a0

