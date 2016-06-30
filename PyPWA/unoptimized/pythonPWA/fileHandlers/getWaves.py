import re
import itertools as it
import os

from PyPWA.unoptimized.pythonPWA.dataTypes.wave import wave
from PyPWA.unoptimized.pythonPWA.fileHandlers.bampReader import read_bamp

def getwaves(totalpath):
    """
    This function finds and reads in all bamp files in the provided directory and returns
    a list of all waves of type pwawave.wave after populating the needed data members of
    each member.
    """
    wavelist=[]
    #filtering for bamp file types and populating bamplist
    regexp=re.compile(".*(.bamp).*")
    for files in os.listdir(totalpath):
        if regexp.search(files):
            #setting the beta value for the wave
            idex=files.find(".bamp")
            
            #seting the waves epsilon value
            bufferepsilon=files[idex-4]
            if bufferepsilon=="-":
                epsilon=0
            if bufferepsilon=="+":
                epsilon=1
            wavelist.append(wave(epsilon=epsilon, complexamplitudes=read_bamp(os.path.join(totalpath, files))))
    return wavelist
