import amp
from random import random
from pythonPWA.fileHandlers.gampReader import gampReader
from pythonPWA.model.intensity import intensity
import numpy
import os
from ampdbListReader import readAmpdbList

def getAmplitudes(inputKinematicVariableList,paramsList):
    amplist=[]
    length = len(inputKinematicVariableList)
    for i in range(len(inputKinematicVariableList)):
        event = inputKinematicVariableList[i]
       #                 m1,      m3,     sab,     sa1,     s12,     s23,      sb3,      c01,           a01,         d01,          c02,           a02,          d02,          c03,          a03,           d03,         c04,           a04,          d04,           c05,           a05,          d05
        [a,b]=amp.ampdb(event[0],event[1],event[2],event[3],event[4],event[5],event[6],paramsList[0],paramsList[1],paramsList[2],paramsList[3],paramsList[4],paramsList[5],paramsList[6],paramsList[7],paramsList[8],paramsList[9],paramsList[10],paramsList[11],paramsList[12],paramsList[13],paramsList[14])
        amplist.append(numpy.complex(a,b))
        if(i%1000==0):
            print ("Complete: [",float(i)/float(length)*100.0,"%]")
    return amplist


def calcIntensityList(amplist):
    intensities=[]
    length = len(amplist)
    for i in range(len(amplist)):
        intensities.append(amplist[i]*numpy.conjugate(amplist[i]))
        if(i%1000==0):
            print ("Complete: [",float(i)/float(length)*100.0,"%]")
    return intensities

def weightGamp(inputKinematicVariableList, intensities,inputGampFile,outputGampFile):
    maxIntensity = max(intensities)
    normalizedIntensities=[x/maxIntensity for x in intensities]
    inputGampReader=gampReader(gampFile=inputGampFile)
    inputGampEvents=inputGampReader.readGamp()
    length = len(normalizedIntensities)
    for i in range(len(normalizedIntensities)):
        if normalizedIntensities[i]>random():
            sa1 = inputKinematicVariableList[i][3]
            sb3 = inputKinematicVariableList[i][6]
            if(sa1>-1.0 and sa1<0.0 and sb3>-1.0 and sb3<0.0):
                inputGampEvents[i].writeGamp(outputGampFile)
        if(i%1000==0):
            print ("Complete: [",float(i)/float(length)*100.0,"%]")
    outputGampFile.close()

print "Reading input kinematic variables"
inputKinematicVariableList = readAmpdbList("/w/hallb/clasg12/wphelps/B5/eventslisttest.txt")
print "Done reading input kinematic variables"

print "Calculating amplitudes"
amplitudes  = getAmplitudes(inputKinematicVariableList,[-0.187,0.9,0.15,0.45,0.70,0.05,0.60,0.99,0.22,-0.15,0.99,0.43,0.30,0.75,0.08])
print "Done calculating amplitudes"

print "Calculating intensities"
intensities = calcIntensityList(amplitudes)
print "Done calculating intensities"

print "Weighting  events"
weightGamp(inputKinematicVariableList, intensities,open("/w/hallb/clasg12/wphelps/B5/events.gamp",'r'),open("/w/hallb/clasg12/wphelps/B5/weighted_events.gamp",'w'))
print "Done weighting  events"

#print intensities
#print len(intensities)
#print max(intensities)
