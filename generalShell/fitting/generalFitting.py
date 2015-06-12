#! /u/apps/anaconda/anaconda-2.0.1/bin/python2
import numpy
import os, sys
from iminuit import Minuit
from kvParser import kvParser
from Fn import intFn
from Fn import parFn
from Fn import migFn

class generalFit (object):

    def __init__(self,dataDir=None,accDir=None,QDir=None,genLen=None,initial={}):
        self.dataDir = dataDir
        self.accDir = accDir
        self.QDir = QDir
        self.genLen = genLen
        self.initial = initial
        if ".txt" in self.dataDir:
            if not os.path.isfile(self.dataDir.rstrip(".txt")+".npy"):
                self.dataKV = kvParser(self.dataDir)
                numpy.save(self.dataDir.rstrip(".txt")+".npy",self.dataKV)
            else:
                self.dataKV = numpy.load(self.dataDir.rstrip(".txt")+".npy")
            if not os.path.isfile(self.accDir.rstrip(".txt")+".npy"):
                self.accKV = kvParser(self.accDir)
                numpy.save(self.accDir.rstrip(".txt")+".npy",self.accKV)
            else:
                self.accKV = numpy.load(self.accDir.rstrip(".txt")+".npy")
            self.dataLen = len(self.dataKV)
            self.accLen = len(self.accKV)
        if os.path.isfile(self.QDir):
           self.QList = numpy.loadtxt(self.QDir)
        else:
            self.QList = numpy.ones(shape=(self.dataLen))
        
    def getdKVars(self,i):
        return self.dataKV[i]

    def getaKVars(self,i):
        return self.accKV[i]   

    def calcLnLike(self,params): 
        iList = numpy.zeros(shape = (self.dataLen))        
        for i in range(self.dataLen):
            iList[i] = intFn(self.getdKVars(i),params)
            sys.stdout.write("int "+str(i)+"\r")
            sys.stdout.flush()
        aList = numpy.zeros(shape = (self.accLen))
        for i in range(self.accLen):
            sys.stdout.write("accepted "+str(i)+"\r")
            sys.stdout.flush()
            aList[i] = intFn(self.getaKVars(i),params)
        val = -((self.QList*numpy.log(iList)).sum(0)) + ((1.0/float(self.genLen)) * aList.sum(0))
        print val
        return val

if __name__ == '__main__':
    migFn() 







