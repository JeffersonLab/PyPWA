"""
.. module:: pythonPWA.model
   :platform: Unix, Windows, OSX
   :synopsis: Module describing the various mathematical constructs commonly used in partial wave analysis.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import numpy
from pythonPWA.utilities.breitWigner import breitWigner

class ProdAmp():
    """
    This is a recreation of the ProdAmp class written by Dennis Weygand.
    The algorithmic structuring of this class is as similar to the ProdAmp
    java version as possible.
    """
    def __init__(self,
                 gList=[[0,0.],
                        [1,.4],
                        [2,1.],
                        [3,0.],
                        [4,0.],
                        [5,0.],
                        [6,0.],
                        [7,0.],
                        [8,0.]]):
        self.gList=gList
        
        self.GAMMA1 = .340
        self.MASS1 = 1.400
        
        self.GAMMA2 = .107
        self.MASS2 = 1.320
        
        self.MASS3 = 2.040
        self.GAMMA3 = .313
        
        self.MASS4 = 1.720
        self.GAMMA4 = .135
        
        self.MASS5 = 2.20
        self.GAMMA5 = .313
        
        self.MASS_A1 = 1.230
        self.WIDTH_A1 = .360
        
        self.MASS_PI2 = 1.672
        self.WIDTH_PI2 = .259
        
        self.MASS_PI1 = 1.600
        self.WIDTH_PI1 = .350
        
    
    def getStrength(self,beta):
        for gPairs in self.gList:
            if gPairs[0]==beta:
                return gPairs[1]
        
    def V(self,mass,beta,k,eps):
        BW=numpy.complex(0.,0.)
        g=self.getStrength(beta)
        
        if(k<1):
            if eps <=1:
                return {
                        1:breitWigner(mass,self.MASS1,self.GAMMA1)*g,
                        2:breitWigner(mass,self.MASS2,self.GAMMA2)*g,
                        3:breitWigner(mass,self.MASS3,self.GAMMA3)*g,
                        4:breitWigner(mass,self.MASS4,self.GAMMA4)*g,
                        5:breitWigner(mass,self.MASS5,self.GAMMA5)*g,
                        6:breitWigner(mass,self.MASS_A1,self.WIDTH_A1)*g,
                        7:breitWigner(mass,self.MASS_PI2,self.WIDTH_PI2)*g,
                        8:breitWigner(mass,self.MASS_PI1,self.WIDTH_PI1)*g
                        }[beta]