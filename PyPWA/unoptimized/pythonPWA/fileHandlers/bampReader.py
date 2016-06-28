"""
.. module:: pythonPWA.fileHandlers
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for working with common PWA file formats.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import numpy

def readBamp(filename):
    """
    This is a general bamp reading function.

    Args:
    filename (string): Path to bamp file to be read.

    Returns:
    List of numpy.complexes representing the complex amplitudes of the wave represented by the file.
    """
    temp1=numpy.fromfile(file=filename,dtype=numpy.dtype('f8'))
    temp2=temp1.reshape((2,-1),order='F')
    temp3=[]
    for lineNumber in range(temp2.shape[1]):
        temp3.append(numpy.complex(temp2[0,lineNumber],temp2[1,lineNumber]))
    return temp3