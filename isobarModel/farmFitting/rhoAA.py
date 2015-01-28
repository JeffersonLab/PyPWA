"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import numpy as np
import os
from pythonPWA.model.spinDensity import spinDensity

class rhoAA(object):
    def __init__(self,
             waves=[],
             alphaList=[],
             Q = [1],
             beamPolarization=0.4):
        
        self.waves=waves
        self.alphaList=alphaList
        self.Q = Q
        self.beamPolarization=beamPolarization
        self.eventNumber=len(self.alphaList)
        self.nwaves=len(self.waves)
        self.rhoAA = np.empty(shape=(self.nwaves,self.nwaves,self.eventNumber),dtype=np.complex)

    def calc(self):    
        for n in range(self.eventNumber):
            for i,iwave in enumerate(self.waves):
                for j,jwave in enumerate(self.waves):
                    Ai = iwave.complexamplitudes[n]                    
                    Aj = jwave.complexamplitudes[n] 
                    if len(self.Q) == 1:                   
                        self.rhoAA[i,j,n] = spinDensity(self.beamPolarization,self.alphaList[n])[iwave.epsilon,jwave.epsilon] * Ai * np.conjugate(Aj)   
                    else:
                        self.rhoAA[i,j,n] = float(Q[n]) * spinDensity(self.beamPolarization,self.alphaList[n])[iwave.epsilon,jwave.epsilon] * Ai * np.conjugate(Aj)                 
        return self.rhoAA
