import os, sys, numpy
from pythonPWA.utilities.ThreeVec import ThreeVector
from pythonPWA.utilities.FourVec import FourVector
from pythonPWA.fileHandlers.gampTranslator import gampTranslator
import math

class kVCalculator (object):

    def __init__(self,indir,gFile):
        self.indir = indir
        self.gfile = gFile+".gamp"
        self.nfile = gFile+".npy"
        self.gampT = gampTranslator(os.path.join(self.indir,self.gfile))
        if not os.path.isfile(os.path.join(self.indir,self.nfile)):
            self.gampT.translate(os.path.join(self.indir,self.nfile))
        self.gampList=numpy.load(os.path.join(self.indir,self.nfile))


