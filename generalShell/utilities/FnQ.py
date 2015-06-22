import numpy,sys, os, time

def qMasFn(kVars,params): # Do not change the name of this function
    if kVars['theta'] < 180:
        return 0.0
    if kVars['t']*params['A1'] > 67:
        return 0.0 
    return 1.0

def runFn(): # Do not change the name of this function
    qList = qM.calcMask()
    qF = open(qM.QDir,"w+")
    for q in qList:
        qF.write(str(q)+"\n")
        sys.stdout.write("writing out: "+str(q)+"\r")
        sys.stdout.flush()

from qMask import qMask
dataDir="/lustre/expphy/volatile/clas/clasg12/jpond/B5/qTest.txt" #filepath for data text file
QDir="./QFactor.txt" #filepath for Q probability factor file. If you do not have one, set to what you would like to save the new one as. 
initial={'A1':134} 
qM = qMask(dataDir=dataDir,QDir=QDir,initial=initial)
