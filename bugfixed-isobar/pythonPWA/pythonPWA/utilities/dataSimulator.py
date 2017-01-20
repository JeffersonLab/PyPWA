"""
.. module:: pythonPWA.utilities
   :platform: Unix, Windows, OSX
   :synopsis: Module containing various useful scripts.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
from random import random

from pythonPWA.fileHandlers.gampReader import gampReader
from pythonPWA.model.intensity import intensity


class dataSimulator(object):
    """
    This is the main simulator class. By instantiating the variables to the desired values
    you can easily simulate data with any characteristics that you would like.
    """
    def __init__(self,
                 mass=1010.,
                 waves=[],
                 resonances=[],
                 normint=None,
                 productionAmplitudes=[],
                 alphaList=[],
                 dataDir=None,
                 beamPolarization=.4):
        """
        Default constructor for the dataSimulator class.

        Kwargs:
        mass (float):
        waves (list):
        resonances (list):
        normint (pythonPWA.model.normInt):
        productionAmplitudes (list):
        alphaList (list):
        beamPolarization (float):

        """

        
        self.mass=mass
        self.waves=waves
        self.resonances=resonances
        self.normint=normint
        self.productionAmplitudes=productionAmplitudes
        self.alphaList=alphaList
        self.beamPolarization=beamPolarization
        self.intensity=intensity(resonances=self.resonances,
                                 waves=self.waves,
                                 productionAmplitudes=self.productionAmplitudes,
                                 normint=self.normint,
                                 alphaList=self.alphaList,
                                 beamPolarization=self.beamPolarization)

    def calcIList(self):
        """
        Calculates and returns a list of intensities for each event.

        Returns:
        List
        """
        iList=[]
        for event in range(len(self.alphaList)):
            i=self.intensity.calculate(self.mass,event)
            iList.append(i)
        return iList
    
    def calcWList(self,iList,iMax,inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile):
        """
        Calculates the list of weights for each event, and writes the raw gamp file.

        Args:
        iList (list):
        iMax (float):
        inputGampFile (file):
        outputRawGampFile (file):
        outputAccGampFile (file):
        inputPfFile (file):

        """
        wList=[x/iMax for x in iList]
        igreader=gampReader(gampFile=inputGampFile)
        inputGampEvents=igreader.readGamp()

        rawGampEvents=[]
        for wn in range(len(wList)):
            if wList[wn]>random():
                inputGampEvents[wn].raw=True
                rawGampEvents.append(inputGampEvents[wn])
        
        for rawGamps in rawGampEvents:
            rawGamps.writeGamp(outputRawGampFile)        
        
        outputRawGampFile.close()
        outputAccGampFile.close()
    
