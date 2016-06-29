"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import numpy as np
import os
from PyPWA.unoptimized.pythonPWA.model.spinDensity import spinDensity

class rhoAA(object):
    """
    This class calculates the 3D numpy array, rhoAA. Each value is the spin density matrix times a wave times the complex conjugate of another wave and 
    possibly times Q. 
    """
    def __init__(self,
             waves=[],
             alphaList=[],
             beamPolarization=0.4):
        """
        Default rhoAA constructor.

        Kwargs:\n
        waves (array): Array of all waves in this pwa fit/simulation.\n
        alphaList (list): List of all alpha values for this mass bin. \n
        beamPolarization (float): Value of beam polarization; 0.0 for no polarization. 

        """
        self.waves=waves
        self.alphaList=alphaList
        self.beamPolarization=beamPolarization
        self.eventNumber=len(self.alphaList)
        self.nwaves=len(self.waves)
        self.rhoAA = np.empty(shape=(self.nwaves,self.nwaves,self.eventNumber),dtype=np.complex)

    def calc(self):
        """
            Function that does the work of calculating rhoAA

            Return:
            rhoAA (numpy ndarray): Note, this class does NOT save the array and must be saved after returning. 
        """    
        for n in range(self.eventNumber):
            for i,iwave in enumerate(self.waves):
                for j,jwave in enumerate(self.waves):
                    Ai = iwave.complexamplitudes[n]                    
                    Aj = jwave.complexamplitudes[n]                  
                    self.rhoAA[i,j,n] = spinDensity(self.beamPolarization,self.alphaList[n])[iwave.epsilon,jwave.epsilon] * Ai * np.conjugate(Aj)                 
        return self.rhoAA
