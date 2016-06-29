# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 13:50:19 2014

@author: sbramlett
"""

import numpy as np
"""The class FourVector
examples of use
P0 = FourVector()
print P0

P1 = FourVector(ct = 9, x = 1, y = 2, z = 4) #or P1 = FourVector(9, 1, 2, 4)
print P1
#with a threevec list
P2 = FourVector(99.9,[1, 2, 3])
print P2
#given a list
P3 = FourVector([9, 1, 2, 3])
print P3

P4 = P1 + P2
print P4

P5 = P2 * P1 
print P5
"""
from PyPWA.unoptimized.pythonPWA.utilities.ThreeVec import ThreeVector
#import LorentzTransform

class FourVector(object):
    vec=[] #the FourVec
    p= ThreeVector()
    def __init__(self, E=0, x=0, y=0, z=0):
        if type(E) is list:
            temp = E
            self.E = temp[0]
            self.x = temp[1]
            self.y = temp[2]
            self.z = temp[3]
            self.p = ThreeVector([self.x, self.y, self.z])
            self.vec = [self.E, self.x, self.y, self.z]
        if type(x) is list and type(E) is not list:
            self.E = E
            temp = x
            self.x = temp[0]
            self.y = temp[1]
            self.z = temp[2]
            self.p = ThreeVector([self.x, self.y, self.z])
            self.vec =  [self.E, self.x, self.y, self.z]
        if type(x) is ThreeVector and (type(E) is not list and type(E) is not ThreeVector):
            self.E = E
            temp = x
            self.x = temp.x
            self.y = temp.y
            self.z = temp.z
            p = temp
            self.vec = [self.E, self.x, self.y, self.z]
        elif type(E) is not list and type (x) is not list and type(y) is not list and type(z) is not list:
            self.E = E
            self.x = x
            self.y = y
            self.z = z
            self.p = ThreeVector([self.x, self.y, self.z])
            self.vec = [self.E, self.x, self.y, self.z]
    #end __init__
    def __repr__(self):
        return str(self.vec)
    def __add__(self, n):
        pE = self.E + n.E
        px = self.x + n.x
        py = self.y + n.y
        pz = self.z + n.z
        pvec = FourVector(pE, px, py, pz)
        return pvec
    def __sub__(self, n):
        pE = self.E - n.E
        px = self.x - n.x
        py = self.y - n.y
        pz = self.z - n.z
        pvec = FourVector(pE, px, py, pz)
        return pvec
    def toMatrix(self):
        this = np.matrix([[self.E],[self.x], [self.y], [self.z]])
        return  this
    def times(self, L): #L is Lorentz transformation
        this = self.toMatrix().transpose().dot(L.m).flatten().tolist()
        t = this[0]
        return FourVector(t)
    def r(self):
        return (float(self.x**2) + float(self.y**2) + float(self.z**2))**(1./2.)
    def lenSq(self):
        return float(self.E)**2 - float(self.r())**2
    def phi(self):
        return self.p.phi()
    def theta(self):
        return  self.p.theta()
    def cosTheta(self):
        return self.p.CosTheta()
    def dot(self, n):
        return self.E*n.E - self.x*n.x - self.y*n.y - self.z*n.z    

#v = ThreeVector(1, 2, 3)
##print v
#P1 = FourVector(9, v)
#print P1
#print P1.E


#print str(P1.lenSq())
#P0 = FourVector()
#print P0
#
#P1 = FourVector(E = 9, x = 1, y = 2, z = 4)
##print P1
##
#P2 = FourVector(99.9,[1, 2, 3])
###print P2
#P1 + P2
#print P1
#P3 = FourVector([9, 1, 2, 3])
##print P3
#print type(P2.E)
#
#P4 = P1 + P2
#print P4
#
#P5 = P2 * P1
#print P5


