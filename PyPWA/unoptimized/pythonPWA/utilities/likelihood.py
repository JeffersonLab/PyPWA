"""
.. module:: pythonPWA.utilities
   :platform: Unix, Windows, OSX
   :synopsis: Module containing various useful scripts.

.. moduleauthor:: Josh Pond


"""
import numpy
from math import log 
from PyPWA.unoptimized.pythonPWA.model.complexV import complexV
from PyPWA.unoptimized.pythonPWA.model.spinDensity import spinDensity
from PyPWA.unoptimized.pythonPWA.model.intensity import intensity
from random import random

class likelihood(object):
    """
    Description of class
    """
    def __init__(self,
                 resonances=[],
                 waves=[],
                 productionAmplitudes=[],
                 normint=None,
                 alphaList=[],
                 beamPolarization=.6
                 ):
        
        self.resonances=resonances
        self.waves=waves
        self.productionAmplitudes=productionAmplitudes
        self.normint=normint
        self.alphaList=alphaList
        self.beamPolarization=beamPolarization
    #This is the intensity including the extra sigma and the natural log
    def calclogI(self,mass,eventNumber):
        ret=numpy.complex(0.,0.)
        for n in range(1,eventNumber,1):    
            for resonance1 in self.resonances:
                for resonance2 in self.resonances:
                    for wave1 in self.waves:
                        for wave2 in self.waves:
                            if len(self.productionAmplitudes)!=0:
                                ret+=log(self.productionAmplitudes[self.waves.index(wave1)]*numpy.conjugate(self.productionAmplitudes[self.waves.index(wave2)])*wave1.complexamplitudes[eventNumber]*numpy.conjugate(wave2.complexamplitudes[eventNumber])*spinDensity(self.beamPolarization,self.alphaList[eventNumber])[wave1.epsilon,wave2.epsilon])
        return ret


    def countAlphas(self,path):
        Alpha = open(path,'r')
        AlphaList = Alpha.readlines()
        
        return len(AlphaList)                        
    #This calculates Eta x                         
    def etaX(self,pathA,pathG):
        etax=(self.countAlphas(pathA)/self.countAlphas(pathG))
        
        return etax 




    #This calculates only the sums in the right term
    def calcSigmaN(self,mass,eventNumber):
        reN=numpy.complex(0,0)
#        for resonance1 in self.resonances:
#            for resonance2 in self.resonances:
        for wave1 in self.waves:
            for wave2 in self.waves:
                if len(self.productionAmplitudes)!=0:
                    reN+=self.productionAmplitudes[self.waves.index(wave1)]*numpy.conjugate(self.productionAmplitudes[self.waves.index(wave2)])*self.normint
        return reN                   
    
    #This multiplies Eta and the sums to make the entire N/right term                        
    def calcN(self,pathA,pathG,mass,eventNumber):
        return self.etaX(pathA,pathG) * self.calcSigmaN(mass,eventNumber)
            
    #This adds the left and right terms to make the log likelihood.         
    def calcneglnL(self, mass, eventNumber, pathA, pathG):
        return -(self.calclogI(mass,eventNumber)) + self.calcN(pathA,pathG,mass,eventNumber)

