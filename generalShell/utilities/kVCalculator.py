import os, sys, numpy
sys.path.append(os.path.join(sys.argv[4],"pythonPWA"))
from pythonPWA.utilities.ThreeVec import ThreeVector
from pythonPWA.utilities.FourVec import FourVector
from pythonPWA.fileHandlers.gampTranslator import gampTranslator
import math

class kVCalculator (object):

    def __init__(self,indir,gFile):
        self.indir = indir
        self.gfile = gfile+".gamp"
        self.nfile = gfile+".npy"
        self.gampT = gampTranslator(os.path.join(self.indir,self.gfile)
        if not os.path.isfile(os.path.join(self.indir,self.nfile)):
            self.gampT.translate(os.path.join(self.indir,self.nfile))
        self.gampList=numpy.load(os.path.join(self.indir,self.nfile))


