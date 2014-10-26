#! /usr/bin/python
import numpy as np
import math
import os, sys
sys.path.append(os.path.join("/volatile","clas","clasg12","salgado","omega","pythonPWA"))
from pythonPWA.utilities.FourVec import FourVector
from pythonPWA.fileHandlers.gampTranslator import gampTranslator

class massBinner(object):

    def __init__(self,indir=None,bindir=None,gfile=None):
        self.indir = indir
        self.bindir = bindir
        self.Control = np.load(os.path.join(os.getcwd(),"Control_List.npy"))
        self.gfile = gfile+".gamp"
        self.nfile = gfile+".npy"        
        self.gampT = gampTranslator(os.path.join(self.indir,self.gfile))
        if not os.path.isfile(os.path.join(self.indir,self.nfile)):
            self.gampT.translate(os.path.join(self.indir,self.nfile))
        self.gampList=np.load(os.path.join(self.indir,self.nfile))
        self.nBins = int(((int(self.Control[3])-int(self.Control[2]))/int(self.Control[4])))+1  
        self.bins = np.zeros(shape=(self.nBins,int(self.gampList.shape[0])))
    
    def calcMass(self,event):
        mass = FourVector(E=[0,0,0,0])
        for part in range(len(event.particles)):
            if part > 1:
                pp = FourVector(E = [float(event.particles[part].particleE),
                                float(event.particles[part].particleXMomentum),
                                float(event.particles[part].particleYMomentum),
                                float(event.particles[part].particleZMomentum)])
                mass = mass.__add__(pp)
        return math.sqrt(mass.dot(mass))

    def binner(self):
        for i in range(int(self.gampList.shape[0])):
            event = self.gampT.writeEvent(self.gampList[i,:,:])
            mass = self.calcMass(event)            
            for x in range(0, self.nBins):
                if mass >= (float(self.Control[2] + (x * float(self.Control[4]))) / 1000.0) and mass < ( float(self.Control[2] + ((x + 1) * float(self.Control[4]))) / 1000.0):
                    self.bins[x,i] = 1
        np.save("bins",self.bins)                    
            
    def fill(self):
        self.binner()
        for b in range(self.nBins):
            if not os.path.isdir(os.path.join(self.bindir,str(self.Control[2] + (b * int(self.Control[4])))+"_MeV")):
                os.mkdir(os.path.join(self.bindir,str(self.Control[2] + (b * int(self.Control[4])))+"_MeV"))
        for r in range(self.nBins):
            with open(os.path.join(self.bindir,str(self.Control[2] + (r * int(self.Control[4])))+"_MeV","events.gamp"),"w") as gF:
                for i in range(int(self.gampList.shape[0])):
                    if self.bins[r,i] == 1:
                        event = self.gampT.writeEvent(self.gampList[i,:,:])
                        event.writeGamp(gF)
                    


mB = massBinner(indir=sys.argv[1],bindir=sys.argv[2],gfile=sys.argv[3])
mB.fill()






