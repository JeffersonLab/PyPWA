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
from PyPWA.unoptimized.pythonPWA.fileHandlers.getWavesGen import getwaves
from PyPWA.unoptimized.pythonPWA.model.normInt import normalize_integral
"""
This is the program that does the work of calculating the normilization integral and returning it as a .npy file.
"""
dataDir=sys.argv[1]
alphaList=numpy.loadtxt(os.path.join(dataDir,sys.argv[2]))
waves=getwaves(dataDir)
rInt=normalize_integral(waves=waves, alpha_list=alphaList, beam_polarization=sys.argv[3])
rInt.execute()
rInt.save(dataDir)
