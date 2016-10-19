"""
.. module:: pythonPWA.model
   :platform: Unix, Windows, OSX
   :synopsis: Module describing the various mathematical constructs commonly used in partial wave analysis.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import numpy
from PyPWA.unoptimized.pythonPWA.model import models


class Intensity(object):
    def __init__(
            self,
            resonances=[],
            waves=[],
            productionAmplitudes=[],
            normint=None,
            alphaList=[],
            beamPolarization=.6
    ):
        """
        This represents the intensity function used in the PWA model.

        Args:
            resonances (list):
            waves (list):
            productionAmplitudes (list):
            normint (pythonPWA.model.NormalizeIntegral):
            alphaList (list):
            beamPolarization (float):

        """
        self.resonances = resonances
        self.waves = waves
        self.productionAmplitudes = productionAmplitudes
        self.normint = normint
        self.alphaList = alphaList
        self.beamPolarization = beamPolarization
        #DONT FORGET TO FIX AFTER DEBUGGING
        self.testWriting = 0
        self.testValues = []

    def calculate(self, mass, eventNumber):
        """
        Calculate function for the intensity class, returns the value for
        the intensity for specified mass and event number.

        Args:
        mass (float):
        eventNumber (int):

        Returns:
        The value of the intensity function as a numpy.complex type.

        """
        ret=numpy.complex(0.,0.)
        self.testValues=[]
        for resonance1 in self.resonances:
            for resonance2 in self.resonances:
                for wave1 in self.waves:
                    for wave2 in self.waves:
                        if len(self.productionAmplitudes) == 0:
                            ret += models.complexV(resonance1,wave1,self.waves,self.normint,mass)*numpy.conjugate(models.complexV(resonance2,wave2,self.waves,self.normint,mass))*wave1.complexamplitudes[eventNumber]*numpy.conjugate(wave2.complexamplitudes[eventNumber])*models.SpinDensity.calculate(self.beamPolarization,self.alphaList[eventNumber])[wave1.epsilon,wave2.epsilon]
                        if len(self.productionAmplitudes)!=0:
                            ret+=self.productionAmplitudes[self.waves.index(wave1)]*numpy.conjugate(self.productionAmplitudes[self.waves.index(wave2)])*wave1.complexamplitudes[eventNumber]*numpy.conjugate(wave2.complexamplitudes[eventNumber])*models.SpinDensity.calculate(self.beamPolarization,self.alphaList[eventNumber])[wave1.epsilon,wave2.epsilon]
                            if self.testWriting==1:
                                if [self.waves.index(wave1),self.waves.index(wave2),self.resonances.index(resonance1),self.resonances.index(resonance2),models.complexV(resonance1,wave1,self.waves,self.normint,mass),models.complexV(resonance2,wave2,self.waves,self.normint,mass),models.complexV(resonance1,wave1,self.waves,self.normint,mass)*numpy.conjugate(models.complexV(resonance2,wave2,self.waves,self.normint,mass))*wave1.complexamplitudes[eventNumber]*numpy.conjugate(wave2.complexamplitudes[eventNumber])*models.SpinDensity.calculate(self.beamPolarization,self.alphaList[eventNumber])[wave1.epsilon,wave2.epsilon],wave1.complexamplitudes[eventNumber],wave2.complexamplitudes[eventNumber]] not in self.testValues:
                                   self.testValues.append([self.waves.index(wave1),self.waves.index(wave2),self.resonances.index(resonance1),self.resonances.index(resonance2),models.complexV(resonance1,wave1,self.waves,self.normint,mass),models.complexV(resonance2,wave2,self.waves,self.normint,mass),models.complexV(resonance1,wave1,self.waves,self.normint,mass)*numpy.conjugate(models.complexV(resonance2,wave2,self.waves,self.normint,mass))*wave1.complexamplitudes[eventNumber]*numpy.conjugate(wave2.complexamplitudes[eventNumber])*models.SpinDensity.calculate(self.beamPolarization,self.alphaList[eventNumber])[wave1.epsilon,wave2.epsilon],wave1.complexamplitudes[eventNumber],wave2.complexamplitudes[eventNumber]])
        if self.testWriting==1:
            for items in self.testValues:
                print("="*10)
                print("wave1",items[0])

                print("wave2",items[1])
                print("resonance1:",items[2])
                print("resonance2:",items[3])
                print("v1:",items[4])
                print("v2:",items[5])

                print("amplitude1:",items[7])
                print("amplitude2:",items[8])
                print("term:",items[6])
        return ret
