#! /u/apps/anaconda/anaconda-2.0.1/bin/python2
import numpy
import os, sys
from iminuit import Minuit
from gampTranslator import gampTranslator
from kvParser import kvParser
from Fn import ampFn
from Fn import kvFn
from Fn import parFn
from Fn import migFn

class generalFit (object):

    def __init__(self,dataDir=None,genDir=None,QDir=None,initial={}):
        self.dataDir = dataDir
        self.genDir = genDir
        self.QDir = QDir
        self.initial = initial
        self.dataT = gampTranslator(self.dataDir)
        if ".gamp" in self.dataDir:
            self.dataT = gampTranslator(self.dataDir)
            if not os.path.isfile(self.dataDir.rstrip(".gamp")+".npy"):                        
                self.dataT.translate(self.dataDir.rstrip(".gamp")+".npy")
            else:
                self.dataT.events=numpy.load(self.dataDir.rstrip(".gamp")+".npy")
            self.genT = gampTranslator(self.genDir)
            if not os.path.isfile(self.genDir.rstrip(".gamp")+".npy"):
                self.genT.translate(self.genDir.rstrip(".gamp")+".npy")
            else:
                self.genT.events=numpy.load(self.genDir.rstrip(".gamp")+".npy")
            self.dataLen = self.dataT.events.shape[0]
            self.genLen = self.genT.events.shape[0]
        elif ".txt" in self.dataDir:
            if not os.path.isfile(self.dataDir.rstrip(".txt")+".npy"):
                self.dataKV = kvParser(self.dataDir)
                numpy.save(self.dataDir.rstrip(".txt")+".npy",self.dataKV)
            else:
                self.dataKV = numpy.load(self.dataDir.rstrip(".txt")+".npy")
            if not os.path.isfile(self.genDir.rstrip(".txt")+".npy"):
                self.genKV = kvParser(self.genDir)
                numpy.save(self.genDir.rstrip(".txt")+".npy",self.genKV)
            else:
                self.genKV = numpy.load(self.genDir.rstrip(".txt")+".npy")
            self.dataLen = len(self.dataKV)
            self.genLen = len(self.genKV)
        if os.path.isfile(self.QDir):
           self.QList = numpy.loadtxt(self.QDir)
        else:
            self.QList = numpy.ones(shape=(self.dataLen))
        
    def getdKVars(self,i):
        if ".gamp" in self.dataDir:
            return kvFn(self.dataT.writeEvent(self.dataT.events[i,:,:]))        
        elif ".txt" in self.dataDir:
            return self.dataKV[i]

    def getgKVars(self,i):
        if ".gamp" in self.genDir:
            return kvFn(self.genT.writeEvent(self.genT.events[i,:,:]))        
        elif ".txt" in self.genDir:
            return self.genKV[i]

    def calcIList(self,**kwargs):      
        iList = numpy.zeros(shape = (self.dataLen))        
        for i in range(self.dataLen):
            iList[i] = self.ampFn(self.getKVars(i))
        return iList

    def calcLnLike(self,params): 
        iList = numpy.zeros(shape = (self.dataLen),dtype = numpy.complex)        
        for i in range(self.dataLen):
            iList[i] = ampFn(self.getdKVars(i),params)
            sys.stdout.write("int "+str(i)+"\r")
            sys.stdout.flush()
        gList = numpy.zeros(shape = (self.genLen),dtype = numpy.complex)
        for i in range(self.genLen):
            sys.stdout.write("generated "+str(i)+"\r")
            sys.stdout.flush()
            gList[i] = ampFn(self.getgKVars(i),params)
        val = -((self.QList*numpy.log(iList)).sum(0)) + ((1.0/float(self.genLen)) * gList.sum(0))
        print val.real.item()
        return val.real.item()

if __name__ == '__main__':
    migFn()







