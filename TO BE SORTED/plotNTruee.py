# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 12:56:35 2014

@author: salgado
"""

#import matplotlib libary
import matplotlib.pyplot as plt
import numpy
import os



#contents=numpy.load(os.path.join("/","home","salgado","pkk","results","wave1.npy"))
#contents=numpy.load(os.path.join("/","home","salgado","pkk","results","wave2.npy"))
#define some data


inFile1=open(os.path.join("/","home","salgado","pkk","mass_total.txt"),'r')
inFile2=open(os.path.join("/","home","salgado","pkk","massbins.txt"),'r')


#plotting control flags
plotTotal=1
plotWave1=1
plotWave2=1

#contents=sorted(contents,key=operator.itemgetter(0))
if plotTotal==1:
    contents=numpy.load(os.path.join("/","volatile","halld","pkk","results","total.npy"))
    x = [l[0] for l in contents]
    y = [float(l[1]) for l in contents]
    
    x1 = [l for l in inFile2]
    y1 = [l for l in inFile1]
    
    #error data
    y_error = [l[2] for l in contents]
    print y
    
    #plot data
    #plt.plot(x, y,'ro',x1,y1,'go')
    plt.plot(x, y,'ro')
    
    
    #plot only errorbars
    plt.errorbar(x, y, yerr=y_error,fmt='o')
    

#plotting waves
if plotWave1==1:
    contents=numpy.load(os.path.join("/","volatile","halld","pkk","results","wave1.npy"))
    
    x2 = [l[0] for l in contents]
    y2 = [float(l[1]) for l in contents]
    y2_error=[l[2] for l in contents]
    
    plt.plot(x2,y2,'go')
    
    plt.errorbar(x2,y2,yerr=y2_error,fmt='o')

if plotWave2==1:
    contents=numpy.load(os.path.join("/","volatile","halld","pkk","results","wave2.npy"))
    
    x3 = [l[0] for l in contents]
    y3 = [float(l[1]) for l in contents]
    y3_error=[l[2] for l in contents]
    
    plt.plot(x3,y3,'bo')
    
    plt.errorbar(x3,y3,yerr=y3_error,fmt='o')


print"="*10
print"total\t\twave1\t\twave2\t\tdelta"
for i in range(len(y)):
    print y[i],"\t",y2[i],"\t",y3[i],"\t",numpy.abs(y2[i]+y3[i]),"\n"

#configure  X axes
#plt.xlim(0.5,4.5)
#plt.xticks([1,2,3,4])

#configure  Y axes
#plt.ylim(19.8,21.2)
#plt.yticks([20, 21, 20.5, 20.8])

#labels
plt.xlabel("Mass Bin")
plt.ylabel("Predicted Event Count")

#title
if plotTotal==plotWave1==plotWave2==1:
    plt.title("Total Plot")

#plt.savefig("fitted.pdf")

#show plot
plt.show()
