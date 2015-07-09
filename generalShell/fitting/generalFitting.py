#! /u/apps/anaconda/anaconda-2.0.1/bin/python2
import numpy
import os, sys
import fileinput
from iminuit import Minuit
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
        if os.path.isfile(self.QDir):
           self.QList = numpy.loadtxt(self.QDir)
        else:
            self.QList = 1.0
        
    def calcLnLikeExtUB(self,params): 
        n = 0 
    	iList = numpy.zeros(shape = (1))
        for line in fileinput.input([self.dataDir]): 
            iList.resize(n+1)       
            kvAs = line.split(",")
            kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}
            iList[n] = intFn(kvAx,params)
            n+=1
        n = 0 
    	aList = numpy.zeros(shape = (1))
        for line in fileinput.input([self.accDir]): 
            aList.resize(n+1)       
            kvAs = line.split(",")
            kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}
            aList[n] = intFn(kvAx,params)
            n+=1
        val = -((self.QList*numpy.log(iList)).sum(0)) + ((1.0/float(self.genLen)) * aList.sum(0))
        print val
        return val

    def calcLnLikeUExtUB(self,params): 
        n = 0 
    	iList = numpy.zeros(shape = (1))
        for line in fileinput.input([self.dataDir]): 
            iList.resize(n+1)       
            kvAs = line.split(",")
            kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}
            iList[n] = intFn(kvAx,params)
            n+=1
        val = -((self.QList*numpy.log(iList)).sum(0))
        print val
        return val

    def calcLnLikeExtB(self,params):
        n = 0
    	iList = numpy.zeros(shape = (1))
        ibinList = numpy.zeros(shape = (1))
        for line in fileinput.input([self.dataDir]): 
            iList.resize(n+1)
            ibinList.resize(n+1)       
            kvAs = line.split(",")
            kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}
            iList[n] = intFn(kvAx,params)
            ibinList[n] = kvAx['BinN']
            n+=1
        n = 0        
        aList = numpy.zeros(shape = (1))
        abinList = numpy.zeros(shape = (1))
        for line in fileinput.input([self.accDir]): 
            aList.resize(n+1)       
            abinList.resize(n+1)    
            kvAs = line.split(",")
            kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}
            aList[n] = intFn(kvAx,params)
            abinList[n] = kvAx['BinN']
            n+=1
        val = -((self.QList*ibinList*numpy.log(iList)).sum(0)) + ((1.0/float(self.genLen)) *((abinList*aList).sum(0)))
        print val
        return val

    def calcLnLikeUExtB(self,params): 
        n = 0
    	iList = numpy.zeros(shape = (1))
        ibinList = numpy.zeros(shape = (1))
        for line in fileinput.input([self.dataDir]): 
            iList.resize(n+1)
            ibinList.resize(n+1)       
            kvAs = line.split(",")
            kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}
            iList[n] = intFn(kvAx,params)
            ibinList[n] = kvAx['BinN']
            n+=1
        val = -((self.QList*ibinList*numpy.log(iList)).sum(0))
        print val
        return val

if __name__ == '__main__':
    migFn() 







