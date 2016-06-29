import os
import numpy
from PyPWA.unoptimized.pythonPWA.utilities.randM import randm
from PyPWA.unoptimized.pythonPWA.fileHandlers.bampReader import readBamp
from PyPWA.unoptimized.pythonPWA.fileHandlers.gampReader import gampReader

class generatePureWave():
    """
    This class generates weight files, gamp files, and acceptance
    masks for a chosen wave.  Simply call generatePureWave().execute(directory,mcGamp,ampFile)
    to produce said files.
    """
    def __init__(self):
        pass
    
    def execute(self,directory,mcGamp,ampFile):
        """
        Creates the weight file, gamp file, and acceptance mask for 
        specified wave.
        """
        amps=readBamp(os.path.join(directory,ampFile+".bamp"))
        nEvent=0
        wtMax=0.
        wtFile=os.path.join(directory,mcGamp+"."+ampFile+".wt")
        output=open(wtFile,'w')
        print( "weight file:\t",wtFile )
        
        for amplitude in amps:
            wt=numpy.real(amplitude*numpy.conjugate(amplitude))
            if nEvent < 10:
                print("wt ",wt)
            if wt>wtMax:
                wtMax=wt
            output.write(str(wt)+"\n")
            nEvent+=1
        
        print("Number of Events = ",nEvent,"\tMaximum weight=",wtMax)
        output.close()
        
        print("select events")
        fileBase=mcGamp
        inputGampFile=os.path.join(directory,fileBase+".gamp")
        inputPfFile=os.path.join(directory,fileBase+".pf")
        
        fin=open(inputGampFile,'r')
        pfin=open(inputPfFile,'r')
        print("input gamp file=",inputGampFile," ",inputPfFile)
        
        outputGampFileRaw=os.path.join(directory,ampFile+".gamp")
        outputPfFile=os.path.join(directory,ampFile+".pf")
        
        outWt=open(outputGampFileRaw,'w')
        outPf=open(outputPfFile,'w')
        
        src=gampReader(fin)
        pfSrc=pfin
        
        fwt=open(wtFile,'r')
        wtSrc=fwt
        
        nout=0
        
        n=0
        for event in src.readGamp():
            accFlag=int(pfSrc.readline())
            
            n+=1
            
            wt=float(wtSrc.readline())
            r=randm(0.0,wtMax)
            
            if wt>r:
                event.writeGamp(outWt)
                outPf.write(str(accFlag)+"\n")
                nout+=1
        
        outWt.close()
        outPf.close()
        
        print("# written ",nout," to file",outputGampFileRaw)