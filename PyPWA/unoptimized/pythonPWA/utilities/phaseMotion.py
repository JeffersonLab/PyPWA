"""
.. module:: pythonPWA
   :platform: Unix, Windows, OSX
   :synopsis: Module containing various functions associated with calculating the phase motion between 2 waves.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>
"""

import numpy

def createComplexList(vList):
    """
    This function takes in a list of v's (for example the returned list from an iminuit fit)
    and returns a list of numpy complexes representing the proper v's for each wave.  Note
    that this function should maintain the ordering established on wave list instantiation,
    i.e. alphabetical ordering of waves based on filename.
    """
    reals=[vList[x] for x in range(0,len(vList),2)]
    imags=[vList[x] for x in range(1,len(vList),2)]
    complexes=[]   
    for i in range(len(reals)):
        complexes.append(numpy.complex(reals[i],imags[i]))
    return complexes
    
def deltaPhi(v1,v2):
    """
    Returns the value of equation 372 in the paper by Salgado and Weygand.
    """
    return numpy.atan(numpy.imag(v1*numpy.conj(v2))/numpy.real(v1*numpy.conj(v2)))
    
def phaseDifference(waves,vList,waveName1,waveName2):
    """
    A higher level wrapper around deltaPhi that allows you to simply supply the list
    of waves, vs, and 2 strings of the filenames of the waves that you want to calculate
    deltaPhi for and returns you the desired phase difference between the 2 specified waves.
    """
    complexes=createComplexList(vList)
    index1=None
    index2=None
    
    #this loop can be cleaned up using the fact that
    ##index1 and index2 are initially set to None.
    ###will do this later.
    for wave in waves:
        if wave.filename==waveName1:
            index1=waves.index(wave)
    for wave in waves:
        if wave.filename==waveName2:
            index2=waves.index(wave)        
    
    #checking to make sure that filenames are valid
    if index1==None:
        print("File name 1 not found")
    if index2==None:
        print("File name 2 not found")
        
    return deltaPhi(complexes[index1],complexes[index2])