import sys, os
import numpy as np
import math
sys.path.append("/home/sbramlett/workspace/PythonPWA/bdemello/pythonPWA/pythonPWA/pythonPWA")
from utilities.FourVec import FourVector
from fileHandlers.gampReader import gampReader
#from pythonPWA.dataTypes.gampEvent import gampEvent
#from pythonPWA.dataTypes.gampParticle import gampParticle

''' Constants and stuff'''
nproc = 0 # number processed.... not #processors...
massPfastPbar = 0.0

'''User defined parameters'''
massLow = 1200
massHigh = 1800
binning = 50
nbins = (int) ((massHigh - massLow) / binning)
directory = "/home/sbramlett/Documents/"
#files = ["data","gen","acc"]; //This order matters to the acceptance calculation below (Fix this?)
files = ["data"]
d = []

'''Create directories'''
for i in range(0, nbins):
    d.append(directory + "mass" + str(massLow + i * binning) + "-" + str(massLow + (i + 1) * binning) + "/")
    if os.path.isdir(d[i]) == False:
        os.mkdir(d[i])
directories = np.array(d)
#print directories   
    
nEvents = np.zeros(shape=(len(files),nbins))
print nEvents
for nFile in range(0, len(files)):
    #open the file to read
    igreader=gampReader(gampFile = open(directory + files[nFile] + ".gamp",'r'))
    events = igreader.readGamp() #list of events from gamp file
#    fin = open(directory + files[nFile] + ".gamp")
#    for i in range(0, nbins):
#        nEvents[nFile][i] = 0
print len(events)   
    

'''list of output files'''
outputFiles = []
for i in range(0,nbins):
    outputFiles.append(directories[i] + files[nFile] + ".gamp")
print outputFiles
outputFiles = np.array(outputFiles)

'''Main event loop'''
#contents = fin.readlines()
#length = len(contents)
#while i < length:
#    nproc += 1
#    massPfastPbar = 
for event in events:
    print event
    for particles in event.particles:
         #calculate mass of resonance
        if particles.particleID == "14": #proton
            p = FourVector(float(particles.particleE), 
                           float(particles.particleXMomentum),
                           float(particles.particleYMomentum),
                           float(particles.particleZMomentum))
        if particles.particleID == "12": #photon gamma
            km = FourVector(float(particles.particleE), 
                            float(particles.particleXMomentum),
                            float(particles.particleYMomentum),
                            float(particles.particleZMomentum))
    X = p + km
    print "x = ", X
    massPfastPbar = math.sqrt(X.dot(X))
    print massPfastPbar
    #print event
    #event.writeGamp(open("/home/sbramlett/Documents/mass1750-1800/data.gamp", 'w'))
    nproc = 0
    for i in range(0, nbins):
        nproc += 1
        if (massPfastPbar > ((massLow + (i * binning))) / 1000.0 and massPfastPbar <= ( massLow + ((i + 1) * binning)) / 1000.0):
            #print "hi", outputFiles[i]  
            event.writeGamp(open(outputFiles[i], 'w+'))
        if nproc % 1000 == 0:
            print nproc
            

'''close files'''


for i in range(len(files)): 
    for i in range(0, nbins):
        nEventFile = open(directories[i] + files[nFile] + ".num", "w+")
        print nEvents[nFile][i]
#        nEventFile.write(nEvents[nFile][i])
#        nEventFile.close()
        
    
#original statement       
#for i in range(0, nbins):      
# nEventFile = open(directories[i] + files[nFile] + ".num", "w+")
#    nEventFile.index(i).close();
    





