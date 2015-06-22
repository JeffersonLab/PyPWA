#! /u/apps/anaconda/anaconda-2.0.1/bin/python2
import numpy
import os, sys
from kvParser import kvParser
from FnQ import qMasFn
from FnQ import runFn

class qMask (object):

    def __init__(self,dataDir=None,QDir=None,initial={}):
        self.dataDir = dataDir
        self.QDir = QDir
        self.initial = initial
        if ".txt" in self.dataDir:
            if not os.path.isfile(self.dataDir.rstrip(".txt")+".npy"):
                self.dataKV = kvParser(self.dataDir)
                numpy.save(self.dataDir.rstrip(".txt")+".npy",self.dataKV)
            else:
                self.dataKV = numpy.load(self.dataDir.rstrip(".txt")+".npy")
            self.dataLen = len(self.dataKV)
        if os.path.isfile(self.QDir):
            self.QList = numpy.loadtxt(self.QDir)
        else:
            self.QList = numpy.ones(shape=(self.dataLen))

    def calcMask(self): 
        for i in range(self.dataLen):
            m = qMasFn(self.dataKV[i],self.initial)
            if m == 0.0:
                self.QList[i] = 0.0
            sys.stdout.write("Calculating: "+str(i)+"\r")
            sys.stdout.flush()
        return self.QList

if __name__ == '__main__':
    runFn()
