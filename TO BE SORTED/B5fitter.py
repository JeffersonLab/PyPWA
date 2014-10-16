import os
import sys
#used on salgado-l1 ONLY
sys.path.append(os.path.join("/","w","work","clas","clasg12","wphelps","B5"))
import numpy
import amp
#from iminuit import Minuit
from pythonPWA.utilities.gampSlist import gampSlist

mcKinematicVariables = []
dataKinematicVariables = []

def getAmplitude(kinematicVariables, paramsList):
    #                 m1,      m3,     sab,     sa1,     s12,     s23,      sb3,      c01,           a01,         d01,          c02,           a02,          d02,          c03,          a03,           d03,         c04,           a04,          d04,           c05,           a05,          d05
    [a,b]=amp.ampdb(kinematicVariables[0],kinematicVariables[1],kinematicVariables[2],kinematicVariables[3],kinematicVariables[4],kinematicVariables[5],kinematicVariables[6],paramsList[0],paramsList[1],paramsList[2],paramsList[3],paramsList[4],paramsList[5],paramsList[6],paramsList[7],paramsList[8],paramsList[9],paramsList[10],paramsList[11],paramsList[12],paramsList[13],paramsList[14])
    return numpy.complex(a,b)

def f(t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15):
    print "Calculating ln(L) function"
    parameters = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15]
    term1=numpy.complex(0.,0.)
    conjugate = numpy.conjugate
    log = numpy.log
    length = len(dataKinematicVariables)
    for i in range(length):
        amplitude = getAmplitude(dataKinematicVariables[i],parameters)
        term1 -= log(amplitude*conjugate(amplitude))
        if(i%1000==0):
            print(float(i)/float(length)*100.0)
    term2=numpy.complex(0.,0.)
    length = len(mcKinematicVariables)
    for i in range(length):
        amplitude = getAmplitude(mcKinematicVariables[i],parameters)
        term2+=amplitude*conjugate(amplitude)
        if(i%1000==0):
            print(float(i)/float(length)*100.0)
    full =  term1+term2
    print full
    print "Done Calculating ln(L) function"
    return full


print "Reading mc gamp file"
mcKinematicVariables = gampSlist("/w/hallb/clasg12/wphelps/B5/", "events.gamp").generate()
print "Done reading mc gamp file"
print "Reading data gamp file"
dataKinematicVariables = gampSlist("/w/hallb/clasg12/wphelps/B5/", "weighted_events.gamp").generate()
print "Done reading data gamp file"

print "Test ln(L) function"
print f(-0.187,0.9,0.15,0.45,0.70,0.05,0.60,0.99,0.22,-0.15,0.99,0.43,0.30,0.75,0.08)
print "Finished ln(L) function"

#parameters = dict(t1=-0.3,limit_t1=(-1.0,1.0),t2=0.8,limit_t2=(0.0,1.0),t3=.3,limit_t3=(0.0,1.0),t4=.5,limit_t4=(-1.0,1.0),t5=.6,limit_t5=(0.0,1.0),t6=.05,limit_t6=(0.0,1.0),t7=.5,limit_t7=(-1.0,1.0),t8=.8,limit_t8=(0.0,1.0),t9=.3,limit_t9=(0.0,1.0),t10=-.2,limit_t10=(-1.0,1.0),t11=.8,limit_t11=(0.0,1.0),t12=.5,limit_t12=(0.0,1.0),t13=.5,limit_t13=(-1.0,1.0),t14=.6,limit_t14=(0.0,1.0),t15=.05,limit_t15=(0.0,1.0))
#m=Minuit(f,**parameters)
#m.set_strategy(1)
#m.set_up(0.5)
#m.migrad(ncall=1000)
