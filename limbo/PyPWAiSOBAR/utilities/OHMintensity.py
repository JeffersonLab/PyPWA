"""
.. module:: pythonPWA.utilities
   :platform: Unix, Windows, OSX
   :synopsis: Module containing various useful scripts.

.. moduleauthor:: Josh Pond <jpond@jlab.org>


"""
import numpy
from PyPWAiSOBAR.model.complexV import complexV
from PyPWAiSOBAR.model.spinDensity import spinDensity


class intensity(object):
    """
    Class for calculating the intensity function from the PWA model by the omega vectorizing method
    """
    def __init__(self,
                 resonances=[],
                 waves=[],
                 
                 normint=None,
                 alphaList=[],
                 beamPolarization=.6
                 ):
        """
        Default constructor for the intensity class.

        Kwargs:
        resonances (list):
        waves (list):
        
        normint (pythonPWA.model.normInt):
        alphaList (list):
        beamPolarization (float):

        """
        self.resonances=resonances
        self.waves=waves
        
        self.normint=normint
        self.alphaList=alphaList
        self.beamPolarization=beamPolarization
        
        self.rex=numpy.ndarray((int(len(self.waves)),int(len(self.waves))),dtype=numpy.complex)
        self.rex[:,:]=numpy.complex(0.,0.)


    def calcRez(self,mass,wave1,wave2):
        """
        Calculate the value of omega for each index in the matrix, returns the value of omega for specified mass and waves.

        Args:
        mass (float):
        wave1 (pythonPWA.dataTypes.wave):
        wave2 (pythonPWA.dataTypes.wave):

        Returns:
        The value of the omega[i,i] as a numpy.complex type.

        """
        rez = numpy.complex(0.,0.)
        for resonance1 in self.resonances:
            for resonance2 in self.resonances:
                rez += complexV(resonance1,wave1,self.waves,self.normint,mass)*numpy.conjugate(complexV(resonance2,wave2,self.waves,self.normint,mass))
        return rez





    def calcOHM(self,mass):
        """
        Calculate the value of the omega matrix, returns the omega matrix for specified mass.

        Args:
        mass (float):
        
        Returns:
        The omega matrix as a numpy.ndarray of numpy.complex type.

        """
        for wave1 in self.waves:
            for wave2 in self.waves:
                #print(str(self.waves.index(wave1))+"'"+str(self.waves.index(wave2)))
                      
                
                self.rex[self.waves.index(wave1),self.waves.index(wave2)] = self.calcRez(mass,wave1,wave2)
        







        return self.rex

   
    def calculate(self,mass,eventNumber,ohmlist):
        """
        Calculate function for the instensity class, returns the value for the instensity for specified mass and event number.

        Args:
        mass (float):
        eventNumber (int):
        ohmlist (numpy.ndarray)        
        
        Returns:
        The value of the intensity function as a numpy.complex type.

        """
        ret=numpy.complex(0.,0.)
        self.testValues=[]
        for wave1 in self.waves:
            for wave2 in self.waves:
               ret+=ohmlist[self.waves.index(wave1),self.waves.index(wave2)]*wave1.complexamplitudes[eventNumber]*numpy.conjugate(wave2.complexamplitudes[eventNumber])*spinDensity(self.beamPolarization,self.alphaList[eventNumber])[wave1.epsilon,wave2.epsilon]
                    
        return ret                        
