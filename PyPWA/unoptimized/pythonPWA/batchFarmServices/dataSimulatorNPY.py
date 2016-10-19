"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


"""
from random import random
import os, numpy

from PyPWA.unoptimized.pythonPWA.fileHandlers.gampTranslator import \
    GampTranslator
from PyPWA.unoptimized.pythonPWA.batchFarmServices.fast_like import \
    FASTLikelihood

class dataSimulator(object):
    """
        This is the program that does the work of simulation for PyPWA simulaton. 
    """
    def __init__(self,
                 mass=1010.,
                 waves=[],                 
                 normint=None,
                 productionAmplitudes=[],
                 alphaList=[],                 
                 dataDir = None,
                 rhoAA=None,
                 iList=None,
                 iMax=0):
        """
            Default FASTLikelihood constructor
            
            Kwargs:
            mass (float): Test mass at the center of the bin. 
            waves (array): Array of all waves in this pwa fit/simulation.
            normint (array): PyPWA normalization integral object
            productionAmplitudes (list): List of all production amplitudes/ V values.             
            alphaList (list): List of all alpha values for that bin.   
            dataDir (string): File path to the mass bin directory that is being simulated. 
            rhoAA (numpy ndarray): The PyPWA rhoAA object.
            iList (numpy array): List of all intensities.
            iMax (float): The maximum intensity for the whole mass range. 
        """
        self.mass=mass
        self.waves=waves        
        self.normint=normint
        self.productionAmplitudes=productionAmplitudes
        self.alphaList=alphaList        
        self.dataDir=dataDir
        self.rhoAA=rhoAA
        self.iList=iList
        self.iMax=iMax

    def calcIList(self):
        """
            Calculates the list of intensities. 

            Returns:
            iList; Note, does NOT save it. Must be saved after returning. 
        """
        
        minuitLn=FASTLikelihood(waves=self.waves,productionAmplitudes=self.productionAmplitudes,rhoAA=self.rhoAA,accNormInt=self.normint)        
        iList = minuitLn.calcInt()     
        return iList 
    
    def calcIListRes(self,resonances):
        """
            Calculates the list of intensities. 

            Returns:
            iList; Note, does NOT save it. Must be saved after returning. 
        """
        
        minuitLn=FASTLikelihood(waves=self.waves,productionAmplitudes=self.productionAmplitudes,rhoAA=self.rhoAA,accNormInt=self.normint)        
        iList = minuitLn.calcIntRes(resonances)
        return iList               
        
    def execute(self,inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile,outputPFGampFile):
        """
            This function does the bulk of the simulation work for PyPWA simulation.

            Args:
            inputGampFile (file): Open file with the flat .gamp _events.
            outputRawGampFile (file): Open file for the _events that only pass the weight filter.
            outputAccGampFile (file): Open file for the _events that pass both the weight and p/f filter.
            inputPfFile (file): Open file with the acceptance of the _events (p/f).
            outputPFGampFile (file): Open file for the _events that only pass the p/f filter.
        """
        
        #igreader=gampReader(_gamp_file=inputGampFile)
        #inputGampEvents=igreader.readGamp() 

        gampT = GampTranslator(os.path.join(os.path.split(inputGampFile.name)[0], os.path.split(inputGampFile.name)[1]))
        if not os.path.isfile(os.path.join(os.path.split(inputGampFile.name)[0],"_events.npy")):
            gampT.translate(os.path.join(os.path.split(inputGampFile.name)[0],"_events.npy"))
        gampList=numpy.load(os.path.join(os.path.split(inputGampFile.name)[0],"_events.npy"))
      
        pf = inputPfFile
        pflist = pf.readlines()

        wList=self.iList[:]/self.iMax
        
        wnList=numpy.zeros(shape=(wList.shape[0]))

        for wn in range(len(wList)):            
            if wList[wn]>random():                
                wnList[wn] = 1 
       	
        numpy.save(os.path.join(os.path.split(inputGampFile.name)[0],"wnList"),wnList)

        for wn in range(len(wnList)):
            wnEvent = gampT.write_event(gampList[wn, :, :])
            if float(pflist[wn])==1.0:
                wnEvent.writeGamp(outputPFGampFile)
            if wnList[wn] == 1:                
                wnEvent.writeGamp(outputRawGampFile)
            if wnList[wn] == 1 and float(pflist[wn])==1.0:
                wnEvent.writeGamp(outputAccGampFile)
        inputGampFile.close()
        inputPfFile.close()
        outputPFGampFile.close()
        outputRawGampFile.close()
        outputAccGampFile.close()
