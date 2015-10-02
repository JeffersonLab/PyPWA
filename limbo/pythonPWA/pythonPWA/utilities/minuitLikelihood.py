"""
.. module:: pythonPWA.utilities
   :platform: Unix, Windows, OSX
   :synopsis: Module containing various useful scripts.

.. moduleauthor:: Josh Pond <jpond@jlab.org>, Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
from pythonPWA.utilities.chunks import chunks
import numpy
from math import log 
from pythonPWA.model.complexV import complexV
from pythonPWA.model.spinDensity import spinDensity
from pythonPWA.model.intensity import intensity
from random import random

import os

class minuitLikelihood(object):
    """
    This class represents the likelihood function, with arguments modified to work well with iminuit.
    """
    def __init__(self,
                 waves=[],
                 productionAmplitudes=[],
                 normint=None,
                 alphaList=[],
                 beamPolarization=.4,
                 mass=1010.,
                 eventNumber=10000,
                 acceptedPath=os.getcwd(),
                 generatedPath=os.getcwd(),
                 accAlphaList=[],
                 accNormInt=None,
                 rawAlphaList=[],
                 rawNormInt=None
                 ):
        """
        Default constructor for the minuitLikelihood class.

        Kwargs:
        waves (list):
        productionAmplitudes (list):
        normint (pythonPWA.model.normInt):
        alphaList (list):
        beamPolarization (float):
        mass (float):
        eventNumber (int):
        acceptedPath (string):
        generatedPath (string):
        accAlphaList (list):
        accNormInt (pythonPWA.model.normInt):
        rawAlphaList (list):
        rawNormInt (pythonPWA.model.normInt):
        """

        self.waves=waves
        self.productionAmplitudes=productionAmplitudes
        self.normint=normint
        self.alphaList=alphaList
        self.beamPolarization=beamPolarization
        self.mass=mass
        self.eventNumber=len(self.alphaList)
        self.acceptedPath=acceptedPath
        self.generatedPath=generatedPath
        self.debugPrinting=0
        self.iList=[]
        self.accAlphaList=accAlphaList
        self.accNormInt=accNormInt
        self.rawAlphaList=rawAlphaList
        self.rawNormInt=rawNormInt
        

    def calclogI(self):
        """
        The logarithm intensity function.

        Returns:
        Numpy.complex data type representing the value of the logarithm of the intensity function.
        """
        ret=numpy.complex(0.,0.)
        for n in range(0,len(self.alphaList)-1,1):    
            argret=numpy.complex(0.,0.)            
            for wave1 in self.waves:
                for wave2 in self.waves:
                    if len(self.productionAmplitudes)!=0:
                                #logarithmic domain error
                        arg = self.productionAmplitudes[self.waves.index(wave1)]*numpy.conjugate(self.productionAmplitudes[self.waves.index(wave2)])*wave1.complexamplitudes[n]*numpy.conjugate(wave2.complexamplitudes[n])*spinDensity(self.beamPolarization,self.alphaList[n])[wave1.epsilon,wave2.epsilon]
                        argret+=arg
            argret=argret.real
            if self.debugPrinting==1:                        
                print"loop#",n,"="*10
                print"argval:",arg
                print"argtype:",type(arg)
                print"productionAmps1:",self.productionAmplitudes[self.waves.index(wave1)]
                print"productionAmps2*:",numpy.conjugate(self.productionAmplitudes[self.waves.index(wave2)])
                print"spinDensityValue:",spinDensity(self.beamPolarization,self.alphaList[n])[wave1.epsilon,wave2.epsilon]
                print"A1:",wave1.complexamplitudes[n]                        
                print"A2*:",numpy.conjugate(wave2.complexamplitudes[n])
            if argret > 0.:                        
                ret+=log(argret)
            
            self.iList.append(argret)                           
        return ret

    def countAlphas(self,path):
        """
        Returns the length of an alpha angle file.

        Args:
        path (string):

        Returns:
        Int equivalent to the length of the alpha file.
        """
        Alpha = open(path,'r')
        AlphaList = Alpha.readlines()
        
        return float(len(AlphaList))                        
    
    #This calculates Eta x                         
    def etaX(self):
        """
        Calculates the acceptance.

        Returns:
        Float value of the acceptance.
        """
        etax=(self.countAlphas(self.acceptedPath)/self.countAlphas(self.generatedPath))
 #       print "etax:",etax        
        return etax 


    #This calculates only the sums in the right term
    def calcSigmaN(self):
        """
        Returns:
        Numpy.complex
        """
        reN=numpy.complex(0,0)
        for wave1 in self.waves:
            for wave2 in self.waves:
                if len(self.productionAmplitudes)!=0:
                    #print"for wave index:",self.waves.index(wave1),"\nV=",self.productionAmplitudes[self.waves.index(wave1)]
                    reN+=self.productionAmplitudes[self.waves.index(wave1)]*numpy.conjugate(self.productionAmplitudes[self.waves.index(wave2)])*self.accNormInt[wave1.epsilon,wave2.epsilon,self.waves.index(wave1),self.waves.index(wave2)]
                         
        return reN                   
    
    #This multiplies Eta and the sums to make the entire N/right term                        
    def calcN(self):
        """
        This multiplies Eta and the sums to make the entire N/right term.

        Returns:
        Float
        """
        return self.etaX() * self.calcSigmaN()
            
    #This adds the left and right terms to make the log likelihood.         
    #def calcneglnL(self,wave1Re,wave1Im,wave2Re,wave2Im):
    def calcneglnL(self,paramsList):
        



        """
        This adds the left and right terms to make the log likelihood.         

        Args:
        paramsList (list):

        Returns:
        Numpy.complex
        """
        self.productionAmplitudes=paramsList
        #this needs to be generalizable to n number of waves, not just 2
        #imags=[x for x in paramsList if x%2==0]
        #reals=[x for x in paramsList if x not in imags]


        #for i in range(len(imags)):
        #    self.productionAmplitudes.append(numpy.complex(reals[i],imags[i]))

        #self.productionAmplitudes=[numpy.complex(wave1Re,wave1Im),numpy.complex(wave2Re,wave2Im)]
        LLog =  -(self.calclogI()) + self.calcN()      
        print"LLog:",LLog        
        return LLog
