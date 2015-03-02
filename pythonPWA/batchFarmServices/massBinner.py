#! /usr/bin/python
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import numpy as np
import math
import os, sys
sys.path.append(os.path.join(sys.argv[1],"pythonPWA"))
from pythonPWA.utilities.FourVec import FourVector
from pythonPWA.fileHandlers.gampTranslator import gampTranslator
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
        self.gampT = gampTranslator(os.path.join(self.indir,self.gfile))
        if not os.path.isfile(os.path.join(self.indir,self.nfile)):
            if self.verb == "v":
                print "Starting translator, for",self.gfile
            self.gampList=self.gampT.translate(os.path.join(self.indir,self.nfile))        
        self.nBins = int(((int(self.Control[3])-int(self.Control[2]))/int(self.Control[4])))+1  
        self.bins = np.zeros(shape=(self.nBins,int(self.gampList.shape[0])))
    
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
        return math.sqrt(mass.dot(mass))

    def binner(self):
        """
            Creates a pass/fail 2D array mask for all bins and events.
        """
        
        for i in range(int(self.gampList.shape[0])):
            event = self.gampT.writeEvent(self.gampList[i,:,:])
            mass = self.calcMass(event)            
            for x in range(0, self.nBins):
                if mass >= (float(float(self.Control[2]) + (x * float(self.Control[4]))) / 1000.0) and mass < ( float(float(self.Control[2]) + ((x + 1) * float(self.Control[4]))) / 1000.0):
                    self.bins[x,i] = 1
            if self.verb == "v":
                sys.stdout.write("Binning event "+str(i+1)+"\r")
                sys.stdout.flush()
        np.save("bins",self.bins)                    
            
    def fill(self,direct):
        """
            Uses the bins p/f array mask to create all bin directories and fill all binned .gamp files.
            
            Args:
            direct (string): keyword the program uses to know what kind of .gamp file is being binned and the directories to make. 
        """
        
        if self.verb == "v":
            print "\nStarting binner"
        self.binner()
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
            totNum = 0
            for r in range(self.nBins):
                num = 0
                with open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.gamp"),"w") as gF:
                    with open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"QFactor.txt"),"w") as qfF:
                        for i in range(int(self.gampList.shape[0])):
                            if self.bins[r,i] == 1:
                                event = self.gampT.writeEvent(self.gampList[i,:,:])
                                event.writeGamp(gF)
                                qfF.write(str(Qlist[i])+"\n")
                                num+=1 
                totNum+=num
                with open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.num"),"w") as nF: 
                    nF.write(str(num))
                if num == 0 or self.verb == "v":
                    print direct , str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV" , "has" , str(num) , "events."
            excluded = self.gampList.shape[0]-totNum
            if self.verb == "v" or excluded != 0:
                print "Binning Complete, " + str(excluded) + " events not in range."
        elif os.path.isfile(self.pFfile) and direct == "flat":
            totNum = 0
            for r in range(self.nBins):
                num = 0
                with open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.gamp"),"w") as gF:
                    with open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.pf"),"w") as pfF:
                        for i in range(int(self.gampList.shape[0])):
                            if self.bins[r,i] == 1:
                                event = self.gampT.writeEvent(self.gampList[i,:,:])
                                event.writeGamp(gF)
                                pfF.write(str(pFlist[i])+"\n")
                                num+=1 
                totNum+=num
                with open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.num"),"w") as nF: 
                    nF.write(str(num))
                if num == 0 or self.verb == "v":
                    print direct , str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV" , "has" , str(num) , "events."
            excluded = self.gampList.shape[0]-totNum
            if self.verb == "v" or excluded != 0:
                print "Binning Complete, " + str(excluded) + " events not in range."
        else:
            totNum = 0
            for r in range(self.nBins):
                num = 0
                with open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.gamp"),"w") as gF:
                    for i in range(int(self.gampList.shape[0])):
                        if self.bins[r,i] == 1:
                            event = self.gampT.writeEvent(self.gampList[i,:,:])
                            event.writeGamp(gF)                                
                            num+=1 
                totNum+=num
                with open(os.path.join(self.bindir,str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV",direct,"events.num"),"w") as nF: 
                    nF.write(str(num))
                if num == 0 or self.verb == "v":
                    print direct , str(int(self.Control[2]) + (r * int(self.Control[4])))+"_MeV" , "has" , str(num) , "events."
            excluded = self.gampList.shape[0]-totNum
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

