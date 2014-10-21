"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Stephanie K. A. Bramlett <skab@jlab.org>, Joshua Pond <jpond@jlab.org>


""" 
import os, sys, numpy
sys.path.append(os.path.join("/volatile","clas","clasg12","salgado","omega","pythonPWA"))
from pythonPWA.utilities.ThreeVec import ThreeVector
from pythonPWA.utilities.FourVec import FourVector
from pythonPWA.utilities.LorentzTransform import lorentzTransform
from pythonPWA.fileHandlers.gampTranslator import gampTranslator
from pythonPWA.fileHandlers.gampReader import gampReader
import math

class generateAlphas(object):
    alphaName = "alpha"
    labelOut = ""
    
    def __init__(self, mode, indir, gfile):
        self.mode = mode
        self.indir = indir
        self.gfile = gfile+".gamp"
        self.nfile = gfile+".npy"
        f = gfile.partition(".")[0]
        self.gampT = gampTranslator(os.path.join(self.indir,self.gfile))
        if not os.path.isfile(os.path.join(self.indir,self.nfile)):
            self.gampT.translate(os.path.join(self.indir,self.nfile))
        self.gampList=numpy.load(os.path.join(self.indir,self.nfile))
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
        for i in range(int(self.gampList.shape[0])):
            event = self.gampT.writeEvent(self.gampList[i,:,:])
            for particles in event.particles:
                if particles.particleID == 14.0: #proton
                    p = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 1.0: #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 9.0: #p-
                    pim = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 8.0: #p+
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
            sys.stdout.write(str(i)+"\r")
            sys.stdout.flush()
            self.alphalist.append(alpha)
    '''
    p p+ p-
    '''
    def analyze22(self):
        for i in range(int(self.gampList.shape[0])):
            event = self.gampT.writeEvent(self.gampList[i,:,:])
            for particles in event.particles:
                if particles.particleID == 14.0: #proton
                    pp = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 1.0: #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 9.0: #p-
                    pim = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 8.0: #p+
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
            
    
    def analyze24(self):
        for i in range(int(self.gampList.shape[0])):
            event = self.gampT.writeEvent(self.gampList[i,:,:])
            for particles in event.particles:
                if particles.particleID == 14.0: #proton
                    pp = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 1.0: #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 12.0: #K-
                    km = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 11.0: #K+
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
    
    def analyze42(self):
        for i in range(int(self.gampList.shape[0])):
            event = self.gampT.writeEvent(self.gampList[i,:,:])
            nks = 0
            for particles in event.particles:
                if particles.particleID == 14.0: #proton
                    p = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 1.0: #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 16.0: #Ks
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
            
        
    def analyzeEtaPiN(self):
        for i in range(int(self.gampList.shape[0])):
            event = self.gampT.writeEvent(self.gampList[i,:,:])
            for particles in event.particles:
                if particles.particleID == 13.0: #neutron
                    n = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 1.0: #photon gamma
                    bm = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 12.0: #eta
                    eta = FourVector(float(particles.particleE), 
                                    float(particles.particleXMomentum),
                                    float(particles.particleYMomentum),
                                    float(particles.particleZMomentum))
                if particles.particleID == 11.0: #p+
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

    
    
indir = sys.argv[2]
gfile = sys.argv[3]
mode = sys.argv[1]
a = generateAlphas(mode, indir, gfile)
a.toFile()

