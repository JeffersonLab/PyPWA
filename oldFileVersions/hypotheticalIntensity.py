import numpy
import iminuit
import os

class hypotheticalIntensity(object):
    """hypothesized intensity function template"""
    def __init__(self,
                 parameters=[],
                 variables=[]):
        """
        so the parameters are the values of things that we are trying to fit,
        whilst the variables are things that we personally set. things like the
        number of waves and the number of resonances in the pythonPWA project.

        #TODO: MAKE INTENSITY FUNCTION WHICH IS FN*FN^*
        """
        self.parameters=parameters
        self.variables=[]
    
    def function(self):
        """
        this is to be a function of both the variables and parameters (which are the things to be fit).
        this function needs to return a numpy.complex number.
        this should be the intensity function.
        """
        pass

    def lnLikelihood(self,parameters):
        """
        this is the actual function that is going to be fit after it is passed through
        a little wrapper to allow for the argument here to be a list.  see the comments
        in hypotheticalIntensityFitter for more information.
        """
        self.parameters=parameters
        
        term1=numpy.complex(0.,0.)
        for i in range(self.variables[0]):
            term1-=numpy.log(self.function()*numpy.conjugate(self.function()))
        
        term2=numpy.complex(0.,0.)
        for i in range(self.variables[1]):
            term2+=self.function()*numpy.conjugate(self.function())
        
        term2*=self.variables[2]

        return term1+term2