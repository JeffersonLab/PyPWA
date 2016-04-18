#! /apps/anaconda/bin/python2
import numpy,sys
from matplotlib import pyplot as plt
from Fn import intFn

x = numpy.arange(-3.0,3.0,.1)#example domain
y=numpy.zeros(shape=[len(x)])

from generalFitting import generalFit # Do not change this line
dataDir="" #filepath for data text file
accDir="" #filepath for accepted Monte Carlo text file
QDir="" #filepath for Q probability factor file. Leave empty if you do not have one. 
genLen=139249 #Integer value for number of generated Monte Carlo events
gF = generalFit(dataDir=dataDir,accDir=accDir,QDir=QDir,genLen=genLen)

for p in range(len(x)):
    y[p]=gF.calcLnLikeExtUB({'A2r': 186.5, 'R0': 1000.0, 'A1r': 186.5, 'p': 1.2,'b':x[p] ,'A2i': 0.0, 'A1i': 0.46})#example
    sys.stdout.write(str(p)+"/"+str(len(x))+"\r")
    sys.stdout.flush()
plt.plot(x,y,linestyle='',marker='*')
plt.show()
