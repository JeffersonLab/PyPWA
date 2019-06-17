#! /u/apps/anaconda/2.4/bin/python2 
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import numpy as np
import math
import fileinput
import os, sys
sys.path.append(os.path.join(sys.argv[1],"pythonPWA"))
from pythonPWA.utilities.FourVec import FourVector
from pythonPWA.dataTypes.gampParticle import gampParticle
from pythonPWA.dataTypes.gampEvent import gampEvent
#from pythonPWA.fileHandlers.gampTranslator import gampTranslator
"""
    This is the PyPWA mass binning utility that simulation/fitting install uses to bin .gamp files in mass. 
"""


class massBinner(object):

    def __init__(self,indir=None,bindir=None,gfile=None,verb="q"):
        """
            This is the default massBinner constructor.

            Kwargs:
            indir (string): The full file path to the top directory.
            bindir (string): The full file path to the directory where the new mass bin directories will be written. 
            gfile (string): The name of the .gamp file to be binned. (/Without/ the .gamp extension.)
            verb (string): either "q" for quiet or "v" for verbose. 
        """
        
        self.indir = indir
        self.bindir = bindir
        self.Control = np.load(os.path.join(sys.argv[1],"GUI","Control_List.npy"))
        self.Qfile = os.path.join(sys.argv[1],"QFactor.txt")
        self.pFfile = os.path.join(sys.argv[1],"events.pf")
        self.gfile = gfile+".gamp"
        self.nfile = gfile+".npy" 
        self.verb = verb       
        self.nBins = int(((int(self.Control[3])-int(self.Control[2]))/int(self.Control[4])))+1  
        
    def calcMass(self,event):
        """
            This function calculates the mass of a single event.

            Args:
            event (PyPWA gampEvent object)
            
            Returns:
            mass of the event (float)
        """
        
        mass = FourVector(E=[0,0,0,0])
        for part in range(len(event.particles)):
            if part > 1 and event.particles[part].particleID != 0:
                pp = FourVector(E = [float(event.particles[part].particleE),
                                float(event.particles[part].particleXMomentum),
                                float(event.particles[part].particleYMomentum),
                                float(event.particles[part].particleZMomentum)])
                mass = mass.__add__(pp)
        if mass.dot(mass) >= 0.0:
            return math.sqrt(mass.dot(mass))
        elif mass.dot(mass) < 0.0:
            return -(math.sqrt(-(mass.dot(mass))))

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
           
    def fill(self,direct):
        """
            Uses the bins p/f array mask to create all bin directories and fill all binned .gamp files.
            
            Args:
            direct (string): keyword the program uses to know what kind of .gamp file is being binned and the directories to make. 
        """
        
        if self.verb == "v":
            print "Starting binner"
        if os.path.isfile(self.Qfile) and direct == "data":
            Qlist = np.loadtxt(self.Qfile)
        elif os.path.isfile(self.pFfile) and direct == "flat":
            pFlist = np.loadtxt(self.pFfile)
        for b in range(self.nBins):
            if "fitting" in self.bindir:
                if not os.path.isdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV")):
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV"))
                    os.mkdir(os.path.join(self.bindir,"results",str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV"))
                    os.mkdir(os.path.join(self.bindir,"overflow",str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV"))
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV","data"))                
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV","mc"))
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV","mc","acc"))
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV","mc","raw"))
                    if self.verb == "v" and b ==0:
                        print "\nWriting "+str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV"+" directories." 
                    if self.verb == "v" and b !=0:
                        print "Writing "+str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV"+" directories."
            elif "simulation" in self.bindir:
                if not os.path.isdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV")):
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV"))                    
                    os.mkdir(os.path.join(self.bindir,"overflow",str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV"))
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV","flat"))                
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV","weight"))
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV","weight","acc"))
                    os.mkdir(os.path.join(self.bindir,str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV","weight","raw"))
                    if self.verb == "v" and b ==0:
                        print "\nWriting "+str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV"+" directories." 
                    if self.verb == "v" and b !=0:
                        print "Writing "+str(int(self.Control[2]) + (b * int(self.Control[4])))+"_MeV"+" directories."          
        if os.path.isfile(self.Qfile) and direct == "data":
            nums = np.zeros(shape=[self.nBins])
            numFiles = [open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.num"),"w") for r in range(self.nBins)]
            binFiles = [open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.gamp"),"w") for r in range(self.nBins)]
            QFiles = [open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"QFactor.txt"),"w") for r in range(self.nBins)]
            i = 0
            n = 0  
            x = -1
            event=np.zeros(shape=[1,6])
            for line in fileinput.input([os.path.join(self.indir,self.gfile)]):
                if i == 0:
                    x = int(line)              
                    event.resize(x+1,6)         
                    event[0,0] = float(line)           
                    i+=1
                elif i < x and i!= 0:                     
                    particle = line.split() 
                    event[i,0]= particle[0]
                    event[i,1]= particle[1]
                    event[i,2]= particle[2]
                    event[i,3]= particle[3]
                    event[i,4]= particle[4]
                    event[i,5]= particle[5].strip("\n")
                    i+=1
                elif i == x:
                    particle = line.split()
                    event[i,0]= particle[0]
                    event[i,1]= particle[1]
                    event[i,2]= particle[2]
                    event[i,3]= particle[3]
                    event[i,4]= particle[4]
                    event[i,5]= particle[5].strip("\n")
                    mass = self.calcMass(self.writeEvent(event))            
                    for x in range(0, self.nBins):
                        if mass >= (float(float(self.Control[2]) + (x * float(self.Control[4]))) / 1000.0) and mass < ( float(float(self.Control[2]) + ((x + 1) * float(self.Control[4]))) / 1000.0):
                            Event = self.writeEvent(event)
                            Event.writeGamp(binFiles[x])
                            QFiles[x].write(str(Qlist[n])+"\n")
                            nums[x] = nums[x]+1
                    i = 0  
                    x = -1
                    n+=1
            for k in range(len(nums)):
                numFiles[k].write(str(nums[k]))
                numFiles[k].close()
                binFiles[k].close()
                QFiles[k].close()
                if nums[k] == 0 or self.verb == "v":
                    print direct , str(int(self.Control[2]) + (k * int(self.Control[4])))+"_MeV" , "has" , str(nums[k]) , "events."
            excluded = n-nums.sum(0)
            if self.verb == "v" or excluded != 0:
                print "Binning Complete, " + str(excluded) + " events not in range."
        elif os.path.isfile(self.pFfile) and direct == "flat":
            nums = np.zeros(shape=[self.nBins])
            numFiles = [open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.num"),"w") for r in range(self.nBins)]
            binFiles = [open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.gamp"),"w") for r in range(self.nBins)]
            pfFiles = [open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.pf"),"w") for r in range(self.nBins)]
            i = 0
            n = 0  
            x = -1
            event=np.zeros(shape=[1,6])
            for line in fileinput.input([os.path.join(self.indir,self.gfile)]):
                if i == 0:
                    x = int(line)              
                    event.resize(x+1,6)         
                    event[0,0] = float(line)           
                    i+=1
                elif i < x and i!= 0:                     
                    particle = line.split() 
                    event[i,0]= particle[0]
                    event[i,1]= particle[1]
                    event[i,2]= particle[2]
                    event[i,3]= particle[3]
                    event[i,4]= particle[4]
                    event[i,5]= particle[5].strip("\n")
                    i+=1
                elif i == x:
                    particle = line.split()
                    event[i,0]= particle[0]
                    event[i,1]= particle[1]
                    event[i,2]= particle[2]
                    event[i,3]= particle[3]
                    event[i,4]= particle[4]
                    event[i,5]= particle[5].strip("\n")
                    mass = self.calcMass(self.writeEvent(event))            
                    for x in range(0, self.nBins):
                        if mass >= (float(float(self.Control[2]) + (x * float(self.Control[4]))) / 1000.0) and mass < ( float(float(self.Control[2]) + ((x + 1) * float(self.Control[4]))) / 1000.0):
                            Event = self.writeEvent(event)
                            Event.writeGamp(binFiles[x])
                            pfFiles[x].write(str(pFlist[n])+"\n")
                            nums[x] = nums[x]+1
                    i = 0  
                    x = -1
                    n+=1
            for k in range(len(nums)):
                numFiles[k].write(str(nums[k]))
                numFiles[k].close()
                binFiles[k].close()
                pfFiles[k].close()
                if nums[k] == 0 or self.verb == "v":
                    print direct , str(int(self.Control[2]) + (k * int(self.Control[4])))+"_MeV" , "has" , str(nums[k]) , "events."
            excluded = n-nums.sum(0)
            if self.verb == "v" or excluded != 0:
                print "Binning Complete, " + str(excluded) + " events not in range."
        else:
            nums = np.zeros(shape=[self.nBins])
            numFiles = [open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.num"),"w") for r in range(self.nBins)]
            binFiles = [open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.gamp"),"w") for r in range(self.nBins)]
            i = 0
            n = 0  
            x = -1
            event=np.zeros(shape=[1,6])
            for line in fileinput.input([os.path.join(self.indir,self.gfile)]):
                if i == 0:
                    x = int(line)              
                    event.resize(x+1,6)         
                    event[0,0] = float(line)           
                    i+=1
                elif i < x and i!= 0:                     
                    particle = line.split() 
                    event[i,0]= particle[0]
                    event[i,1]= particle[1]
                    event[i,2]= particle[2]
                    event[i,3]= particle[3]
                    event[i,4]= particle[4]
                    event[i,5]= particle[5].strip("\n")
                    i+=1
                elif i == x:
                    particle = line.split()
                    event[i,0]= particle[0]
                    event[i,1]= particle[1]
                    event[i,2]= particle[2]
                    event[i,3]= particle[3]
                    event[i,4]= particle[4]
                    event[i,5]= particle[5].strip("\n")
                    mass = self.calcMass(self.writeEvent(event))            
                    for x in range(0, self.nBins):
                        if mass >= (float(float(self.Control[2]) + (x * float(self.Control[4]))) / 1000.0) and mass < ( float(float(self.Control[2]) + ((x + 1) * float(self.Control[4]))) / 1000.0):
                            Event = self.writeEvent(event)
                            Event.writeGamp(binFiles[x])
                            nums[x] = nums[x]+1
                    i = 0  
                    x = -1
                    n+=1
            for k in range(len(nums)):
                numFiles[k].write(str(nums[k]))
                numFiles[k].close()
                binFiles[k].close()
                if nums[k] == 0 or self.verb == "v":
                    print direct , str(int(self.Control[2]) + (k * int(self.Control[4])))+"_MeV" , "has" , str(nums[k]) , "events."
            excluded = n-nums.sum(0)
            if self.verb == "v" or excluded != 0:
                print "Binning Complete, " + str(excluded) + " events not in range."

if len(sys.argv)==4:
    mB = massBinner(indir=sys.argv[1],bindir=sys.argv[2],gfile=sys.argv[3])
if len(sys.argv)==5:
    mB = massBinner(indir=sys.argv[1],bindir=sys.argv[2],gfile=sys.argv[3],verb=sys.argv[4])

if "data" in sys.argv[3]:
    direct = "data"
if "acc" in sys.argv[3]:
    direct = "mc/acc"
if "raw" in sys.argv[3] and "fitting" in sys.argv[2]:
    direct = "mc/raw"
elif "raw" in sys.argv[3] and "simulation" in sys.argv[2]:
    direct = "flat"
mB.fill(direct)

