from pythonPWA.model.normInt import normInt
from pythonPWA.fileHandlers.getWavesGen import getwaves
import os
import numpy

#set the directory that you want to run the normint -> ascii printer in
dataDir=os.path.join("C:\\","Users","books","Documents","Visual Studio 2012","Projects","pwa","pythonPWA","pythonPWA","data","1000_MeV")

#create and run a new normalization integral, note that if your alpha file is named differently than alpha.txt you have to change it below
rInt=normInt(waves=getwaves(dataDir),alphaList=numpy.loadtxt(os.path.join(dataDir,"alpha.txt")))
rInt.execute()

#printing normInt.txt into the directory specified above.
rInt.writeToAscii(dataDir)

print"done"