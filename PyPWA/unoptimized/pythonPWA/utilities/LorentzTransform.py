# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 15:13:23 2014

@author: sbramlett
"""
from PyPWA.unoptimized.pythonPWA.utilities.FourVec import FourVector
from PyPWA.unoptimized.pythonPWA.utilities.ThreeVec import ThreeVector
import numpy as np
import sys, os
#sys.path.append("/home/sbramlett/workspace/PythonPWA/bdemello/pythonPWA/pythonPWA/pythonPWA/utilities")
from PyPWA.unoptimized.pythonPWA.utilities.rotation import rotation
'''
can be called 3 ways
1. with a FourVector
2. with alpha, beta, gamma
3. with a matrix
'''

class lorentzTransform(object):
    #vec should be a FourVector
    def __init__(self, a = 1., b = 1., g = 1.):
        #sets beta, the velocity = p/E
        self.m = np.matrix(np.identity(4))
        if isinstance(a, FourVector):
            x = -a.x / a.E
            y = -a.y / a.E
            z = -a.z / a.E
            _beta = ThreeVector(x, y, z)
            self.setBeta(_beta)
        if type(a) == np.matrix:
            self.m = a
        elif type(a) == float: #alpha beta and gamma should all be floats
            self.alpha = a
            self.beta = b
            self.gamma = g
            rot = rotation(self.alpha, self.beta, self.gamma)
            self.setrot(rot)

    def setBeta(self, _beta):
        #beta = _beta.r()
        gamma = 1./((1. - _beta.lenSq()))**(1./2.)
        gFactor = gamma**2 / (gamma + 1.)
        row0 = [gamma, gamma * _beta.x, gamma * _beta.y, gamma * _beta.z]
        row1 = [gamma * _beta.x, (_beta.x**2 * gFactor)+1., _beta.x * _beta.y * gFactor, _beta.x * _beta.z * gFactor]
        row2 = [gamma * _beta.y, _beta.x * _beta.y * gFactor, (_beta.y**2 * gFactor)+1., _beta.y * _beta.z * gFactor]
        row3 = [gamma * _beta.z, _beta.x * _beta.z * gFactor, _beta.y * _beta.z * gFactor ,(_beta.z**2 * gFactor)+1.]
        self.m = np.matrix([row0, row1, row2, row3])
        return self.m
    def setrot(self, rot):
        for i in range(1,4):
            for j in range(1,4):
                self.m[i,j] = rot.m[i-1, j-1]
        self.m[0,0] = 1
    def toString(self):
        this = self.m.tolist()
        row0 = this[0]
        row1 = this[1]
        row2 = this[2]
        row3 = this[3]
        return str(row0) + "\n" + str(row1) + "\n" + str(row2) + "\n" + str(row3) + "\n"
       
    def __repr__(self):
        return self.toString()
    
    
#v = FourVector(-0.165421, -0.188449, 0.546792, 1.11454)
##print v
##print "in main",type(v)
#l = lorentzTransform(v)
##print l.m
#print v.times(l)
#l = lorentzTransform(1., 2., 3.)
#print l
#f = FourVector(2.,4.,6.,8.)
#print f.times(l)
#test = FourVector(5., 1., 1., 1.)
#l = lorentzTransform(test)
#print l
#test.times(l)
#print test      

  