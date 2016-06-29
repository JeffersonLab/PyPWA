#! /u/apps/anaconda/anaconda-2.0.1/bin/python2 
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


"""
import numpy
import os
"""
    This program runs in the interactive farm to retrieve the maximum intensity value among the whole mass range. 
"""

topDir = os.getcwd().rstrip("GUI")

iMax = [0]

for d in os.listdir(os.path.join(topDir,"simulation")):
    if "_MeV" in d:
        Max = numpy.amax(numpy.load(os.path.join(topDir,"simulation",d,"flat","iList.npy")))
        if Max > iMax[0]:
            iMax[0] = Max

numpy.save(os.path.join(topDir,"simulation","iMax.npy"),iMax)
print( "DONE")
