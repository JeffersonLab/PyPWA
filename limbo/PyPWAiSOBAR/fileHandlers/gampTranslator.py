#! /usr/bin/python 
"""
.. module:: pythonPWA/fileHandlers
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import sys
import os
import numpy
import fileinput
from PyPWAiSOBAR.dataTypes.gampParticle import gampParticle
from PyPWAiSOBAR.dataTypes.gampEvent import gampEvent
class gampTranslator():
    """
    This class is a convience class used to convert a gamp .txt file into a 3 demensional numpy ndarray saved in numpy's .npy file format
    """
    def __init__(self,gampFile=None):
        """
        Default gampReader constructor.

        Kwargs:
        gampFile (file): Must be an open file handle, gamp file to be read.

        """
        self.gampFile=gampFile
        self.events= numpy.ones(shape=(1,1,6),dtype=float)

    def readFile(self): 
        """
        This function parses a whole gamp file and returns the 3 demensional array. The first demension is the event number. 
        The second is the line number in that event (0 is the number of particles, >0 is a particle). The third is the index within
        an individual particle.   
       
        """           
        i = 0
        n = 0 
        x = -1
        for line in fileinput.input([self.gampFile]):
            if i == 0:
                x = int(line)              
                self.events.resize(1+n,x+1,6)         
                self.events[n,0,0] = float(line)           
                i+=1
            elif i < x and i!= 0:                     
                particle = line.split() 
                self.events[n,i,0]= particle[0]
                self.events[n,i,1]= particle[1]
                self.events[n,i,2]= particle[2]
                self.events[n,i,3]= particle[3]
                self.events[n,i,4]= particle[4]
                self.events[n,i,5]= particle[5].strip("\n")
                i+=1
            elif i == x:
                particle = line.split()
                self.events[n,i,0]= particle[0]
                self.events[n,i,1]= particle[1]
                self.events[n,i,2]= particle[2]
                self.events[n,i,3]= particle[3]
                self.events[n,i,4]= particle[4]
                self.events[n,i,5]= particle[5].strip("\n")
                i = 0 
                n+=1 
                x = -1           
                sys.stdout.write(str(n)+"\r")
                sys.stdout.flush()    

    def translate(self,saveFile):
        """
        This function will run the readFile function and then save the array to the specified file name. 

        Args:
        saveFile (string): The file name the user wants the file named(will end in .npy).

        Returns:
        The 3D numpy array of gamp events 
        """
        self.readFile()        
        numpy.save(saveFile,self.events)
        return self.events

    def writeEvent(self,dataSlice):
        """
        This function takes a slice of the events array ([n,:,:]) and returns the pythonPWA gampEvent object of that slice. 

        Args:
        dataSlice (numpy ndarray): The 2 densional array of a single event fron the events 3D array.
        
        Returns:
        gampEvent 
        """
        nPart = dataSlice[0,0]
        event = []
        for i in range(int(nPart)):            
            dataList = dataSlice[i+1,:]
            particle=gampParticle(particleID=dataList[0],
                               particleCharge=dataList[1],
                               particleXMomentum=dataList[2],
                               particleYMomentum=dataList[3],
                               particleZMomentum=dataList[4],
                               particleE=dataList[5])
            event.append(particle)
        return gampEvent(particles=event)
    
    def writeFile(self,outFile,data):
        """
        This function will convert the 3 demensional array of gamp data back into a text file of those events. 

        Args:
        outFile (string): The file name the user wants the file named(will end in .txt).
        data (numpy ndarray): The 3D that will be converted. 
        """
        with open(outFile,"w") as gF:
            for i in range(data.shape[0]):                
                event = self.writeEvent(data[i,:,:])
                event.writeGamp(gF)
                sys.stdout.write(str(i)+"\r")
                sys.stdout.flush()
