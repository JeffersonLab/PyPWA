# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 13:48:01 2014

@author: sbramlett
"""
#import numbers
import numpy as np
import math


class ThreeVector(object):
    vec = []

    def __init__(self, x = 0, y = 0, z = 0):
        if type(x) is not list:
            self.x = x
            self.y = y
            self.z = z
            self.vec = [x,y,z]
        if type(x) is list and len(x) == 3:
            temp = x
            self.x = temp[0]
            self.y = temp[1]
            self.z = temp[2]
            self.vec = [self.x, self.y, self.z]
    '''
    For printing the Three Vector
    '''
    def __repr__(self):
        return str(self.vec)
    '''
    Add two Three Vectors together
    '''  
    def __add__(self, n):
        px = self.x + n.x
        py = self.y + n.y
        pz = self.z + n.z
        pvec = ThreeVector(px, py, pz)
        return pvec
    '''
    Subtract two Three Vectors together
    '''  
    def __sub__(self, n):
        px = self.x - n.x
        py = self.y - n.y
        pz = self.z - n.z
        pvec = ThreeVector(px, py, pz)
        return pvec
    '''    
    def __mul__(self, n):
        px = self.x * n.x
        py = self.y * n.y
        pz = self.z * n.z
        pvec = ThreeVector(px, py, pz)
        return pvec
    '''
    '''
    Cross or scalar product
    '''
    def __mul__(self, n):
       if type(n) is ThreeVector:
            px = self.y * n.z - self.z * n.y
            py = self.z * n.x - self.x * n.z
            pz = self.x * n.y - self.y * n.x
            pvec = ThreeVector(px, py, pz)
            return pvec
       else:
            print n
            px = self.x * n
            py = self.y * n
            pz = self.z * n
            pvec = ThreeVector(px, py, pz)
            return pvec               
    '''
    #Dot Product of two Three Vectors together
    '''  
    def dot(self, A):
        new = self.x * A.x + self.y * A.y + self.z * A.z
        return new
    '''
    #The Length of the vector
    '''
    def r(self):
        r = (self.x**2 + self.y**2 + self.z**2)**(1./2.)
        return r
    '''
    #The length of the vectore squared
    '''
    def lenSq(self):
        return self.r()**2
    '''
    '''
    def cosTheta(self, args):
        if type(args) is ThreeVector:
            n = self.dot(args)
            ret = n / self.r() / args.r()
            return ret

    def CosTheta(self):
        return self.z /self.r()

    def sinTheta(self):
        return (self.x**2 + self.y**2)/r()

    def phi(self):
        return math.atan2(self.y, self.x)

    def theta(self):
        return math.acos(self.CosTheta())
   
# x = [1, 2, 3]
# y = [4, 5, 6]
# print np.cross(x, y)
#
# P1 = ThreeVector(x)
# print str(P1.lenSq())
# print P1
# P2 = ThreeVector(y)
# print P1 * P2
# print np.cross(P1.vec, P2.vec)
