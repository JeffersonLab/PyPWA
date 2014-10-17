import numpy as np
import os, sys
from pythonPWA.model.spinDensity import spinDensity

class rhoAA(object):
    def __init__(self,
             waves=[],
             alphaList=[],
             beamPolarization=0.4):
        
        self.waves=waves
        self.alphaList=alphaList
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
                    self.rhoAA[i,j,n] = spinDensity(self.beamPolarization,self.alphaList[n])[iwave.epsilon,jwave.epsilon] * Ai * np.conjugate(Aj) 
                    sys.stdout.write(str(n)+"\r")
                    sys.stdout.flush()                   
        return self.rhoAA
