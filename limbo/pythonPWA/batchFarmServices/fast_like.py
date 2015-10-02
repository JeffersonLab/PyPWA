"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 

import numpy as np
import os
from pythonPWA.model.complexV import complexV

class FASTLikelihood(object):
    """
    This is the mathmatical class of the likelihood calculation and the calculation of the intensity. 
    """
    def __init__(self,
                waves=[],
                productionAmplitudes=[],                
                alphaList=[],               
                acceptedPath=os.getcwd(),
                generatedPath=os.getcwd(),                
                rhoAA = None,
                accNormInt=None,
                Q = [1.0]
                ):
        """
            Default FASTLikelihood constructor
            
            Kwargs:
            waves (array): Array of all waves in this pwa fit/simulation.
            productionAmplitudes (list): List of all production amplitudes/ V values.             
            alphaList (list): List of all alpha values for that bin.              
            acceptedPath (string): Full file path to the accepted MC alpha file
            generatedPath (string): Full file path to the generated MC alpha file
            rhoAA (numpy ndarray array): PyPWA rhoAA array. 
            accNormInt (numpy array): The normalization integral from the accepted MC.
            Q (list): List of all Q values for this mass bin. 
        """
        
        self.waves=waves
        self.productionAmplitudes=productionAmplitudes
        self.alphaList=alphaList
        self.nwaves = len(self.waves)
        self.acceptedPath=acceptedPath
        self.generatedPath=generatedPath
        self.iList=[]   
        self.normint=accNormInt      
        self.accNormInt=accNormInt.sum(0).sum(0)
        self.Q = Q
        self.rhoAA = rhoAA
        self.etaX = 0.
        
    
#    def countAlphas(self,fname):   This function will be able to read the .num file
#        with open(fname) as f:      instead of reading the entire file length. Uncomment
#            num = f.readlines()        it and comment '#' out the next function to
#        return float(num[0])           use it. 

    def countAlphas(self,path):
        """
            Returns the length of an alpha file.

            Args:
            path (string): Path to the alpha file to be measured. 

            Returns:
            Length of file. (float)
        """
        
        Alpha = open(path,'r')
        AlphaList = Alpha.readlines()
        return float(len(AlphaList)) 
       
    def calcetaX(self):
        """
            Sets the self.etaX variable. 
        """
        self.etaX=(self.countAlphas(self.acceptedPath)/self.countAlphas(self.generatedPath))
        

    def calclnL(self):
        """
            Calculates the value of the negative of the log likelihood function.

            Returns:
            Value of the negative of the log likelihood function. (float)
        """       
        a0 = 0.
        a1 = 0.
        for i in range(self.nwaves):
            for j in range(self.nwaves):
                VV = self.productionAmplitudes[i] * np.conjugate(self.productionAmplitudes[j])                
                a0 = a0 + (VV * self.rhoAA[i,j,:]).real                
                a1 = a1 + (VV * self.accNormInt[i,j]).real 
        return -((self.Q*(np.log(a0))).sum(0)) + (self.etaX * a1)

    def calcneglnL(self,paramsList):
        """
            Sets the production Amplitudes from Minuit and calculates the value of the negative of the log likelihood function.

            Returns:
            Value of the negative of the log likelihood function. (float)
        """ 
        self.productionAmplitudes=paramsList
        self.calcetaX()
        LLog = self.calclnL()    
        print"LLog:",LLog        
        return LLog
    

    def calcInt(self):
        """
            Calculates the list of intensities for a mass bin.
            Returns:
            iList (numpy array)
        """        
        a0 = 0.        
        for i in range(self.nwaves):
            for j in range(self.nwaves):
                VV = self.productionAmplitudes[i] * np.conjugate(self.productionAmplitudes[j])                
                a0 = a0 + (VV * self.rhoAA[i,j,:]).real    
        return self.Q*a0

    def calcIntRes(self,resonances,testMass):
        """
            Calculates the list of intensities for a mass bin.

            Returns:
            iList (numpy array)
        """        
        a0 = 0.   
        for resonance1 in resonances:    
            for resonance2 in resonances:  
                for wave1 in self.waves:
                    for wave2 in self.waves:
                        VV = complexV(resonance1,wave1,self.waves,self.normint,testMass) * np.conjugate(complexV(resonance2,wave2,self.waves,self.normint,testMass))                
                        a0 = a0 + (VV * self.rhoAA[self.waves.index(wave1),self.waves.index(wave2),:]).real    
        return self.Q*a0

