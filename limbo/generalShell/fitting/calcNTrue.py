#! /u/apps/anaconda/anaconda-2.0.1/bin/python2
import numpy
import os, sys
from iminuit import Minuit
from kvParser import kvParser
from Fn import intFn

class calcNTrue (object):

    def __init__(self,genDir=None):
        self.genDir = genDir
        if ".txt" in self.genDir:
            if not os.path.isfile(self.genDir.rstrip(".txt")+".npy"):
                self.genKV = kvParser(self.genDir)
                numpy.save(self.genDir.rstrip(".txt")+".npy",self.genKV)
            else:
                self.genKV = numpy.load(self.genDir.rstrip(".txt")+".npy")
            self.genLen = len(self.genKV)
       
    def getgKVars(self,i):
        return self.genKV[i]   

    def calcNTrue(self,params): 
        gList = numpy.zeros(shape = (self.genLen),dtype = numpy.complex)
        for i in range(self.genLen):
            sys.stdout.write("generated "+str(i)+"\r")
            sys.stdout.flush()
            gList[i] = intFn(self.getgKVars(i),params)
        return gList.sum(0)

if __name__ == '__main__':
    nTureFn()







