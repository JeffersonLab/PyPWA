# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 14:10:01 2014

@author: sbramlett
"""

import numpy as np
import math

class rotation(object):
    def __init__(self, alpha = 1, beta = 1, gamma = 1):
        if type(alpha) == np.matrix:
            self.m = alpha
        else:
            #print type(alpha)
            self.setabg(alpha, beta, gamma)
            
    def setabg(self, alpha, beta, gamma):
        ca = math.cos(float(alpha))
        sa = math.sin(float(alpha))
        cb = math.cos(beta)
        sb = math.sin(beta)
        cg = math.cos(gamma)
        sg = math.sin(gamma)
        
        row0 = [ca*cb*cg - sa*sg, cb*cg*sa + ca*sg, -cg*sb]
        row1 = [-sg*cb*ca - cg*sa, -sg*cb*sa + cg*ca, sb*sg]
        row2 = [ca*sb, sa*sb, cb]
        
        self.m = np.matrix([row0, row1, row2])
        return self.m
    def toString(self):
        row0 = self.m.tolist()[0]
        row1 = self.m.tolist()[1]
        row2 = self.m.tolist()[2]
        return str(row0) + "\n" + str(row1) + "\n" + str(row2) + "\n"
    def __repr__(self):
        return self.toString()
    
        
        
#i = rotation(1, 2, 3)
#print i.m
#z = rotation(i.m)
#print z

 