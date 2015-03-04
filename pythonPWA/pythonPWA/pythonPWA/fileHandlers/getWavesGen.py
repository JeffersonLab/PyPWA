"""
.. module:: pythonPWA.fileHandlers
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for working with common PWA file formats.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>, Josh Pond <jpond@jlab.org>


"""
import re
import itertools as it
import os

from pythonPWA.dataTypes.wave import wave
from pythonPWA.fileHandlers.bampReader import readBamp
import operator

def getwaves(totalpath):
    """
    This function finds and reads in all bamp files in the provided directory and returns
    a list of all waves of type pwawave.wave after populating the needed data members of
    each member.

    Args:
    totalPath (string): Directory to scan for *.bamp files.

    Returns:
    List of type pythonPWA.dataTypes.wave sorted by the 'filename' data member to ensure preserved ordering.

    """
    wavelist=[]
    #filtering for bamp file types and populating bamplist
    regexp=re.compile(".*(.bamp).*")
    for files in os.listdir(totalpath):
        if regexp.search(files):
            #setting the beta value for the wave
            idex=files.find(".bamp")
            #setting the waves epsilon value
            for b in range(len(files)):
                if files[-int(b)] == '-':
                    epsilon=0 
                    break
                if files[-int(b)] == '+':
                    epsilon=1 
                    break
            wavelist.append(wave(epsilon=epsilon,complexamplitudes=readBamp(os.path.join(totalpath,files)),filename=files))
    return sorted(wavelist,key=operator.attrgetter('filename'))

