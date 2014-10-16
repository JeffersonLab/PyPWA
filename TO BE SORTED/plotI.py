# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 12:56:35 2014

@author: salgado
"""

#import matplotlib libary
import matplotlib.pyplot as plt
import numpy
import os


contents=numpy.load(os.path.join("/","home","salgado","pkk","data","Simulation","1850_MeV","iList.npy"))
#contents=numpy.load(os.path.join("/","home","salgado","pkk","results","wave1.npy"))
#contents=numpy.load(os.path.join("/","home","salgado","pkk","results","wave2.npy"))
#define some data

#contents=sorted(contents,key=operator.itemgetter(0))
x = [x for x in range(len(contents))]
y = contents


#plot data
plt.plot(x, y,'ro')

#configure  X axes
#plt.xlim(0.5,4.5)
#plt.xticks([1,2,3,4])

#configure  Y axes
#plt.ylim(19.8,21.2)
#plt.yticks([20, 21, 20.5, 20.8])

#labels
plt.xlabel("this is X")
plt.ylabel("this is Y")

#title
plt.title("Simple plot")


#show plot
plt.show()
