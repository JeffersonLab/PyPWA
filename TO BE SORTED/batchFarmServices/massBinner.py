#! /usr/bin/python
import numpy as np
import math
import os, sys
sys.path.append(os.path.join("/volatile","clas","clasg12","salgado","omega","pythonPWA"))
from pythonPWA.utilities.FourVec import FourVector
from pythonPWA.fileHandlers.gampTranslator import gampTranslator

class massBinner(object):

    def __init__(self,indir=None,bindir=None,gfile=None,verb="q"):
        self.indir = indir
        self.bindir = bindir
        self.Control = np.load(os.path.join(os.path.split(os.path.split(os.getcwd())[0])[0],"GUI","Control_List.npy"))
        self.gfile = gfile+".gamp"
        self.nfile = gfile+".npy" 
        self.verb = verb       
        self.gampT = gampTranslator(os.path.join(self.indir,self.gfile))
        if not os.path.isfile(os.path.join(self.indir,self.nfile)):
            if self.verb == "v":
                print "Starting translator, for",self.gfile
            self.gampT.translate(os.path.join(self.indir,self.nfile))
        self.gampList=np.load(os.path.join(self.indir,self.nfile))
        self.nBins = int(((int(self.Control[3])-int(self.Control[2]))/int(self.Control[4])))+1  
        self.bins = np.zeros(shape=(self.nBins,int(self.gampList.shape[0])))
    
    def calcMass(self,event):
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
        if self.verb == "v":
            print "\nStarting binner"
        self.binner()
        for b in range(self.nBins):
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
if "raw" in sys.argv[3]:
    direct = "mc/raw"
mB.fill(direct)

