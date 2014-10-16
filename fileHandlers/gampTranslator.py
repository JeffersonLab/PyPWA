#! /usr/bin/python 
import sys
import os
import numpy
import fileinput
sys.path.append(os.path.join("/volatile","clas","clasg12","salgado","omega","pythonPWA"))
from pythonPWA.dataTypes.gampParticle import gampParticle
from pythonPWA.dataTypes.gampEvent import gampEvent
class gampTranslator():
    
    def __init__(self,gampFile=None):
        self.gampFile=gampFile
        self.events= numpy.ones(shape=(1,1,6),dtype=float)

    def readFile(self):            
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
                particle = line.split(" ") 
                self.events[n,i,0]= particle[0]
                self.events[n,i,1]= particle[1]
                self.events[n,i,2]= particle[2]
                self.events[n,i,3]= particle[3]
                self.events[n,i,4]= particle[4]
                self.events[n,i,5]= particle[5].strip("\n")
                i+=1
            elif i == x:
                particle = line.split(" ")
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
        self.readFile()        
        numpy.save(saveFile,self.events)

    def writeEvent(self,dataSlice):
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
        with open(outFile,"w") as gF:
            for i in range(data.shape[0]):                
                event = self.writeEvent(data[i,:,:])
                event.writeGamp(gF)
                sys.stdout.write(str(i)+"\r")
                sys.stdout.flush()
