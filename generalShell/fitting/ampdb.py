import os
import sys

#used on salgado-l1 ONLY
sys.path.append(os.path.join("/","w","work","clas","clasg12","salgado","B5"))
import amp

import numpy
from ampdbListReader import readAmpdbList

def getAmplitudes(filename,paramsList):
    listtest=readAmpdbList(filename)
    amplist=[]

    for event in listtest:
        #                 m1,      m3,     sab,     sa1,     s12,     s23,      sb3,      c01,           a01,         d01,          c02,           a02,          d02,          c03,          a03,           d03,         c04,           a04,          d04,           c05,           a05,          d05
        [a,b]=amp.ampdb(event[0],event[1],event[2],event[3],event[4],event[5],event[6],paramsList[0],paramsList[1],paramsList[2],paramsList[3],paramsList[4],paramsList[5],paramsList[6],paramsList[7],paramsList[8],paramsList[9],paramsList[10],paramsList[11],paramsList[12],paramsList[13],paramsList[14])
        amplist.append(numpy.complex(a,b))
    
    return amplist
    
print getAmplitudes(os.path.join("/","w","work","clas","clasg12","salgado","B5","listtest.txt"),[-0.187,0.9,0.15,0.45,0.70,0.05,0.60,0.99,0.22,-0.15,0.99,0.43,0.30,0.75,0.08])
