"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import os
import sys 
sys.path.append(os.path.join(sys.argv[4],"pythonPWA"))
import numpy
from pythonPWA.fileHandlers.getWavesGen import getwaves
from pythonPWA.model.normInt import normInt

dataDir=sys.argv[1]
alphaList=numpy.loadtxt(os.path.join(dataDir,sys.argv[2]))    
waves=getwaves(dataDir)
rInt=normInt(waves=waves,alphaList=alphaList,beamPolarization=sys.argv[3])
rInt.execute()
rInt.save(dataDir)
