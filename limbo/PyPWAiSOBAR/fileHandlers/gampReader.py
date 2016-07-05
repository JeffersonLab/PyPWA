"""
.. module:: pythonPWA.fileHandlers
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for working with common PWA file formats.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import sys
import os


from PyPWAiSOBAR.dataTypes.gampParticle import gampParticle
from PyPWAiSOBAR.dataTypes.gampEvent import gampEvent

class gampReader():
    """
    This class is a convience class used to ease the reading (and eventually writing) of gamp files.
    """
    def __init__(self,
                 gampFile=None):

        """
        Default gampReader constructor.

        Kwargs:
        gampFile (file): Must be an open file handle, gamp file to be read.

        """

        self.gampFile=gampFile
        self.events=[]
        self.nParticles=0
    
    def parseParticle(self,line):
        """
        This function takes in a space delimited line representing a particle, and 
        instantiates a new instance of the gampParticle class from it then returns it.

        Args:
        line (string): A single line representing a gamp particle.

        Returns:
        A gampParticle, of type pythonPWA.dataTypes.gampParticle, instantiated from the argument.
        """
        dataList=line.split(" ")
        particle=gampParticle(particleID=dataList[0],
                           particleCharge=dataList[1],
                           particleXMomentum=dataList[2],
                           particleYMomentum=dataList[3],
                           particleZMomentum=dataList[4],
                           particleE=dataList[5])
        return particle
    
    def readGamp(self):
        """
        This function parses a whole gamp file and returns a list of all gamp events.

        Returns:
        List of all gampEvents contained within self.gampFile.
        """
        contents=self.gampFile.readlines()
        self.nParticles=int(contents[0])
        nLinesPerEvent=self.nParticles+1
        i=0
        while i <len(contents):
            event=[]
            for line in contents[i+1:i+nLinesPerEvent]:
                event.append(self.parseParticle(line))
            i+=nLinesPerEvent
            self.events.append(gampEvent(particles=event))
        return self.events