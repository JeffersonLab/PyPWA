# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 10:45:11 2014

@author: sbramlett
"""
import os, sys
#sys.path.append("/home/sbramlett/workspace/PythonPWA/bdemello/pythonPWA/pythonPWA/pythonPWA")
from utilities.ThreeVec import ThreeVector
from utilities.FourVec import FourVector
from utilities.LorentzTransform import lorentzTransform

from fileHandlers.gampReader import gampReader
import math

class generateAlphas(object):
    alphaName = "alpha"
    labelOut = ""
    '''
    ONLY MODE 24 HAS BEEN TESTED
    mode -  8 = p pi+ pi- pi0
            22 = p p+ p-
            24 = p k+ k-
            42 = gamma p --> p Ks Ks (pi+ pi- pi+ pi-)
            eta pi n
    indir - directory of file
    gfile - file name
    '''
    def __init__(self, mode, indir, gfile):
        self.mode = mode
        self.indir = indir
        self.gfile = gfile
        f = gfile.partition(".")[0]
        #read the file
        igreader=gampReader(gampFile = open(os.path.join(indir,gfile),'r'))
        self.events = igreader.readGamp() #list of events from gamp file
        #fileIn = self.indir + gfile + ".gamp" <-from weygands code
        
        self.alphaName = "alpha" + f + ".txt"
    
        self.alphalist = []
        if self.mode == "8":
            self.analyze8()
        if self.mode == "22":
            self.analyze22()
        if self.mode == "24" or self.mode == 24 :
            self.analyze24()
        if self.mode == "42":
            self.analyze42()
        if self.mode == "EtaPiN":
            self.analyzeEtaPiN
    '''
    p pi+ pi- pi0
    '''
    def analyze8(self):
        for event in self.events:
            for particles in event.particles:
                if particles.particleID == "14": #proton
                    p = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "1": #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "9": #p-
                    pim = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "8": #p+
                    pip = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
            
            ptarget = FourVector(.938, 0.,0.,0.)  
            initp = bm + ptarget
            finalp = pip + pim + p
            pi0 = initp + finalp
            pmeson = pip + pim + pi0
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = ThreeVector(0.,1.,0.)
            Normal = beam3 * pMeson
            
            cosAlpha = Normal.dot(polarization) / Normal.r()
            alpha = math.acos(cosAlpha)
            self.alphalist.append(alpha)
    '''
    p p+ p-
    '''
    def analyze22(self):
        for event in self.events:
            for particles in event.particles:
                if particles.particleID == "14": #proton
                    pp = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "1": #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "9": #p-
                    pim = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "8": #p+
                    pip = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
            #
            pmeson = pip + pim
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = ThreeVector(0.,1.,0.)
            Normal = beam3 * pMeson
            
            cosAlpha = Normal.dot(polarization) / Normal.r()
            alpha = math.acos(cosAlpha)
            self.alphalist.append(alpha)
            
    '''
    P k+ k-
    will generate a list of alphas for each event saved in 
    variable name alphalist 
    '''
    def analyze24(self):
        for event in self.events:
            for particles in event.particles:
                if particles.particleID == "14": #proton
                    pp = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "1": #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "12": #K-
                    km = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "11": #K+
                    kp = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
#            target = FourVector(.938, 0., 0., 0.)
            pmeson = kp + km # K+ K-

#            if bm.z > 4.4:
#                miss = bm + target - kp - km
#                totalmiss = bm + target - kp - kp - pp
                #determine alpha
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = ThreeVector(0.,1.,0.)
            Normal = beam3 * pMeson

            cosAlpha = Normal.dot(polarization) / Normal.r()
            alpha = math.acos(cosAlpha)
            #print alpha
            self.alphalist.append(alpha)
    '''
    gamma p --> p Ks Ks (pi+ pi- pi+ pi-)
    '''
    def analyze42(self):
        for event in self.events:
            nks = 0
            for particles in event.particles:
                if particles.particleID == "14": #proton
                    p = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "1": #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "16": #Ks
                    if nks == 0:
                        ks1 = FourVector(float(particles.particleE), 
                                        float(particles.particleXMomentum),
                                        float(particles.particleYMomentum),
                                        float(particles.particleZMomentum))
                    else: 
                        ks2 = FourVector(float(particles.particleE), 
                                        float(particles.particleXMomentum),
                                        float(particles.particleYMomentum),
                                        float(particles.particleZMomentum))
                    nks += 1
                    
            pmeson = ks1 + ks2
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = ThreeVector(0.,1.,0.)
            Normal = beam3 * pMeson

            cosAlpha = Normal.dot(polarization) / Normal.r()
            alpha = math.acos(cosAlpha)

            self.alphalist.append(alpha)
            
                            
    '''
    eta pi n
    '''      
    def analyzeEtaPiN(self):
        for event in self.events:
            for particles in event.particles:
                if particles.particleID == "13": #neutron
                    n = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "1": #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "12": #eta
                    eta = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == "11": #p+
                    pip = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
            pmeson = eta + pip
            pMeson = pmeson.p
            beam3 = bm.p
            polarization = ThreeVector(0.,1.,0.)
            Normal = beam3 * pMeson

            cosAlpha = Normal.dot(polarization) / Normal.r()
            alpha = math.acos(cosAlpha)

            self.alphalist.append(alpha)
            
        
    def toFile(self):
        f = open(os.path.join(self.indir, self.alphaName), 'w')
        for alpha in self.alphalist:
            f.write(str(alpha) + "\n")
        f.close()

    
    
#indir = "/home/sbramlett/Documents/"
#gfile = "test.gamp"
##
#a = generateAlphas("24", indir, gfile)
#a.toFile()
