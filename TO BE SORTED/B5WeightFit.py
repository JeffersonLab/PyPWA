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
        amplist.append(getAmplitude(event, paramsList))
        if(i%1000==0):
            print ("Complete: [",float(i)/float(length)*100.0,"%]")
    return amplist

def getAmplitude(kinematicVariables, paramsList):
    #                 m1,      m3,     sab,     sa1,     s12,     s23,      sb3,      c01,           a01,         d01,          c02,           a02,          d02,          c03,          a03,           d03,         c04,           a04,          d04,           c05,           a05,          d05
    [a,b]=amp.ampdb(kinematicVariables[0],kinematicVariables[1],kinematicVariables[2],kinematicVariables[3],kinematicVariables[4],kinematicVariables[5],kinematicVariables[6],paramsList[0],paramsList[1],paramsList[2],paramsList[3],paramsList[4],paramsList[5],paramsList[6],paramsList[7],paramsList[8],paramsList[9],paramsList[10],paramsList[11],paramsList[12],paramsList[13],paramsList[14])
    return numpy.complex(a,b)

def calcIntensityList(amplist):
    intensities=[]
    length = len(amplist)
    for i in range(len(amplist)):
        intensities.append(calcIntensity(amplist[i]))
        if(i%1000==0):
            print ("Complete: [",float(i)/float(length)*100.0,"%]")
    return intensities

def calcIntensity(amplitude):
    return amplitude*numpy.conjugate(amplitude)

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

def getKinematicVariableB5(event):
    for particles in event.particles:
        if particles.particleID == "14": #proton
            prE = float(particles.particleE)
            prpx = float(particles.particleXMomentum)
            prpy = float(particles.particleYMomentum)
            prpz = float(particles.particleZMomentum)
            mp = float((float(particles.particleE)**2 - float(particles.particleXMomentum)**2 -
                        float(particles.particleYMomentum)**2 - float(particles.particleZMomentum)**2)**(1./2.))
        if particles.particleID == "1": #photon
            phE = float(particles.particleE)
            phpx = float(particles.particleXMomentum)
            phpy = float(particles.particleYMomentum)
            phpz = float(particles.particleZMomentum)
        if particles.particleID == "12": #K-
            kmE = float(particles.particleE)
            kmpx = float(particles.particleXMomentum)
            kmpy = float(particles.particleYMomentum)
            kmpz = float(particles.particleZMomentum)
        if particles.particleID == "11": #K+
            kpE = float(particles.particleE)
            kppx = float(particles.particleXMomentum)
            kppy = float(particles.particleYMomentum)
            kppz = float(particles.particleZMomentum)
            mk = float((float(particles.particleE)**2 - float(particles.particleXMomentum)**2 -
                        float(particles.particleYMomentum)**2 - float(particles.particleZMomentum)**2)**(1./2.))
    sab = (.93827 + phE)**2 - (0 + phpx)**2 - (0 + phpy)**2 - (0 + phpz)**2
    sa1 = (phE - kpE)**2 - (phpx - kppx)**2 - (phpy - kppy)**2 - (phpz - kppz)**2
    s12 = (kpE + kmE)**2 - (kppx + kmpx)**2 - (kppy + kmpy)**2 - (kppz + kmpz)**2
    s23 = (kmE + prE)**2 - (kmpx + prpx)**2 - (kmpy + prpy)**2 - (kmpz + prpz)**2
    sb3 = (.93827 - prE)**2 - (0 - prpx)**2 - (0 - prpy)**2 - (0 - prpz)**2
    slist = [mk, mp, sab, sa1, s12, s23, sb3]
    return slist



print ("Opening files/Reading gamp")
#Setup input and output
inputGampFile  = open("/w/hallb/clasg12/wphelps/B5/events.gamp",'r')
outputGampFile = open("/w/hallb/clasg12/wphelps/B5/weighted_events.gamp",'w')
inputGampReader=gampReader(gampFile=inputGampFile)
inputGampEvents=inputGampReader.readGamp()
intensities = []
addIntensity = intensities.append
print ("Done opening files/Reading gamp")


print ("Calculating intensities")
#Loop over events to calculate intensities
length = len(inputGampEvents)
for i in range(length):
    kinematicVariables  = getKinematicVariableB5(inputGampEvents[i])
    sa1 = kinematicVariables[3]
    sb3 = kinematicVariables[6]
    if(sa1>-1.0 and sa1<0.0 and sb3>-1.0 and sb3<0.0):
        addIntensity(calcIntensity(getAmplitude(kinematicVariables, [-0.187,0.9,0.15,0.45,0.70,0.05,0.60,0.99,0.22,-0.15,0.99,0.43,0.30,0.75,0.08])))
    else:
        addIntensity(-1000.0)
    if(i%1000==0):
        print(float(i)/float(length)*100.0)
print ("Done calculating intensities")

#Normalize intensities/probabilities
maxIntensity = max(intensities)
normalizedIntensities=[x/maxIntensity for x in intensities]

print ("Weighting and writing output file")
#Loop over events to weight and output to gamp file
for i in range(len(inputGampEvents)):
    if normalizedIntensities[i]>random():
        inputGampEvents[i].writeGamp(outputGampFile)
    if(i%1000==0):
        print(float(i)/float(length)*100.0)
print ("Done weighting and writing output file")

