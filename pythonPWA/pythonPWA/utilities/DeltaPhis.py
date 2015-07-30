import os, sys
import numpy as np
import math
import matplotlib.pyplot as plt

'''
SOME DEBUGGING CODE IS STILL IN HERE FOR THE CALCULATION OF DPHI, BUT COMMENTED OUT.
THIS CODE ALSO COMBINES PREVIOUS DELTAPHI CODE THAT WERE IN SEPARATE FILES IN VOLATILE AND WORK.


How to use:
Starting with a fitting directory or some directory that contains the mass bins with Vvalues.npy and optionally the covariance matrix
1) call the function generateDeltaPhis('./directory')
   -after this is succefully run you will have a deltaphi(n).npy file for every wave in every mass bin. n is the reference wave
    and will be an positive integer (1, 2, 3,...). Ex. if n is 2 then the second wave in the Vvalues.npy file is the reference wave.
    Later on I will have to add in the name of the wave.
   -you will be notified if the mass bin lacks a Vvalues.npy file.
   -if the mass bin contains a covariance matrix then it will generate the errors as well. If not it will only generate the deltaphis.
2) The current general plotter creates a funny looking plot. To produce said plot call the function plotDeltaPhis('./directory')
'''
#IMPROVEMENT IDEA: maybe use getDPhis in getDeltaPhis 
def getDeltaPhis(V, l, ref, sdir):
    """
    Saves the values of delta phi and the (statistical) errors to .npy files. The number in the filename indicates the reference wave.
    
    Args: Vvalues, Covariance Matrix, the reference wave (ex. 2 = the second wave in the list), sdir (the directory to save to)

    """
    #first make sure V is a dictionary and if it isn't, make it one
    if type(V) != dict:
        V = V[()]
    print V
    #make sure l is a numpy matrix
    if type(l) != np.matrix:
        l = np.asmatrix(l)

    n = len(V) 
    if n%2 != 0:
        print "Error in Vvalues size: need real and imaginary part for all waves."
        sys.exit()
     
    #set v_1 from the reference wave
    v_1 = np.complex(V[V.keys()[(ref*2)-2]], V[V.keys()[(ref*2)-1]])

    j = ref
    sw = 0

    num = 0
    i = 0
    phi = dict()
    err = dict()
    for key,val in V.iteritems():
        if num%2 == 0:
            i+=1

            v_2 = np.complex(V[key], V[V.keys()[num + 1]])
            im = (v_1 * np.conjugate(v_2)).imag
            re = (v_1 * np.conjugate(v_2)).real 

            #print "orig", np.arctan(im/re)
            #dphi = math.atan2(im/re, 1) #same as one below (and above for that matter)
            dphi = math.atan2(im, re) 
            
            #if re < 0:
            #    dphi += math.pi
            #    if im > 0:
            #        dphi += math.pi
            #    else:
            #        dphi -= math.pi
            #elif re > 0 and im < 0:
            #    dphi += 2 * math.pi
            #print "dphi1 adjust", dphi
            #if dphi > 2 * math.pi:
            #    print "Cry..."
            #http://stackoverflow.com/questions/16613546/using-arctan-arctan2-to-plot-a-from-0-to-2%CF%80
            #doesn't seem right either
            #dphi = np.arctan2(1, 1/(im/re))
            phi[i] = dphi
            
            if i == j: 
                error = 0.0
            elif i != j:
                #create a submatrix of l for error calculation
                # |l1, l2|
                # |l3, l4|

                if j < i:
                    temp = i
                    i = j
                    j = temp
                    sw = 1

                j2 = ((j*2)-2)
                i2 = ((i*2)-2)
                l1 = l[i2:i2+2, i2:i2+2]
                l2 = l[i2:i2+2, j2:j2+2]
                l3 = l[j2:j2+2, i2:i2+2]
                l4 = l[j2:j2+2, j2:j2+2]
                fl = np.bmat([[l1 ,l2], [l3, l4]])
               
                if sw == 1: #reset i and j after calculation of fl if they were switched
                    j = ref
                    i = temp
                    sw = 0

                #calculate error
                a = re
                b = im 
                da = (a/(a**2 + b**2))
                db = (((-1) * b)/(a**2 + b**2))
                ja = np.matrix([v_2.real, v_2.imag, v_1.real, v_1.imag])
                jb = np.matrix([(-1)*v_2.imag, v_2.real, v_1.imag, (-1)*v_1.real])

                siga2 = ja * fl * ja.transpose()
                sigb2 = jb * fl * jb.transpose() 
                sigab2 = ja * fl * jb.transpose()
                error = ((da)**2 * siga2 + (db)**2 * sigb2 + 2 * da * db * sigab2).item()

            err[i] = error

        num += 1
    #save the data
    np.save(os.path.join(sdir,'deltaphi' + str(ref) + '.npy'), phi)
    np.save(os.path.join(sdir,'deltaphi' + str(ref) + 'errors.npy'), err)
    
    
def getDPhis(V, ref, sdir):
    #Computes delta phi and saves it to an .npy file at a user specified directory.
    #this is the same as getDeltaPhis() without the error calculation which is useful
    #when the covariance matrix is absent from a mass bin
    
    if type(V) != dict:
        V = V[()]
    print V
    n = len(V)
    phi = dict()
    if n%2 != 0:
        print "Error in Vvalues size: need real and imaginary part for all waves."
        sys.exit()
        
    num = 0
    i = 0
    v_1 = np.complex(V[V.keys()[(ref*2)-2]], V[V.keys()[(ref*2)-1]])
    for key,val in V.iteritems():

        if num%2 == 0:
            i+=1

            v_2 = np.complex(V[key], V[V.keys()[num + 1]])
            im = (v_1 * np.conjugate(v_2)).imag
            re = (v_1 * np.conjugate(v_2)).real
            #print "orig", np.arctan(im/re)
            dphi = math.atan2(im,re)
            #print "dphi 1", dphi
            #if re < 0:
            #    dphi += math.pi
            #    if im > 0:
        #               dphi += math.pi
            #    else:
            #        dphi -= math.pi
            #elif re > 0 and im < 0:
        #           dphi += 2 * math.pi
            #print "dphi1 adjust", dphi
            #if dphi > 2 * math.pi:
            #    print "Cry..."
            #dphi = np.arctan2(1, 1/(im/re))
            #print "dphi2", dphi
            #dphi = np.arctan2(re, im)
            #print "dphi 1", dphi
            phi[i] = dphi
        num += 1
    np.save(os.path.join(sdir,'deltaphi' + str(ref) + '.npy'), phi)

def generateDeltaPhis(datadir):
    '''
    generates deltaphis for all mass bins. if the directory has a covariance matrix then it also generates the errors.
    Args: datadir- needs to be the fitting folder. (the folder with all the mass bins in it)
    will terminate if necessary files do not exist (Vvalues.npy).
    Assumes correct file structure
    '''
    subdirs = [name for name in os.listdir(datadir) if os.path.isdir(datadir + "/" + name)]
    #need to change the way it does this to one loop instead of 2 list comprehensions.
    subdirs = [x.strip('_MeV') for x in subdirs]
    subdirs = [int(x) for x in subdirs if x.isdigit()]
    subdirs.sort()

    for i in subdirs:
        Vvalues = 1
        if os.path.isfile(datadir + "/" + str(i)+"_MeV/Vvalues.npy"):
            Vvalues = np.load(datadir + "/" + str(i)+"_MeV/Vvalues.npy")[()]
            #print i, Vvalues
            l = 1
            if os.path.isfile(datadir +"/"+str(i)+"_MeV/minuitCovar3.npy"):
                l = np.load(datadir +"/"+str(i)+"_MeV/minuitCovar3.npy")
                l = np.asmatrix(l)
                for j in range(1,len(Vvalues)/2+1):
                    getDeltaPhis(Vvalues, l, j, datadir +"/"+str(i)+"_MeV/")
            else:
                for j in range(1,len(Vvalues)/2+1):
                    getDPhis(Vvalues, j, datadir +"/"+str(i)+"_MeV/")
                
        else:
            print "Could not find Vvalues.npy in " + "/" + str(datadir)+"/" +str(i)+"_MeV/, skipping..."
            
        


def plotDeltaPhis(datadir):
    '''
    GENERAL PHI PLOTTER. DPHIS *MIGHT* BE INCORRECT RIGHT NOW BUT IN PROGRESS
    ALSO NEED TO ADD ERROR BARS
    A NON GENERAL PLOTTER EXAMPLE IS IN testscript.py IN /work/clas/clasg12/skab/fromVolatile2015/skab/testscript.py


    Given a directory containing all of the mass bins, this will plot dphis. Currently this plotter will not apply error bars.
    This code assumes that all necessary deltaphi(n).npy files have been made.
    '''
    subdirs = [name for name in os.listdir(datadir) if os.path.isdir(datadir + "/" + name)]
    
    #need to change the way it does this to one loop instead of 2 list comprehensions.
    subdirs = [x.strip('_MeV') for x in subdirs]
    subdirs = [int(x) for x in subdirs if x.isdigit()]
    subdirs.sort()
    dphis = np.zeros(shape=[1,1,len(subdirs)],dtype=np.float64)
    #assumes that the appropriate .npy files have been made


    #need to load the errors as well and put them more than likely in an identical structure to the dphis
    #tests have shown that it looks best when sorted (though far from perfect), so we must sort the data and errors at the same time 
    #currently thinking something along the lines of: (that code snippet is from testscript.py)
    #keydict = sorted(zip(phi12,e12))
    #e12 = [x for y, x in keydict]
    #phi12 = [y for y, x in keydict]
    #plt.errorbar(subdirs,phi12, marker='*', yerr=e12)
    q=0
    for i in subdirs: #for every bin
        #load Vvalues every time to figure out how many waves are in 
        if os.path.isfile(datadir + "/" + str(i) + "_MeV/Vvalues.npy"):
            n = len(np.load(datadir + "/" + str(i) + "_MeV/Vvalues.npy")[()])/2
            dphis.resize([n,n,len(subdirs)])
        for j in range(0,n):
            phi = np.load(datadir + "/"+str(i)+"_MeV/deltaphi"+str(j+1)+".npy")[()]
            #print 'phi',phi
            for x in range(0, n):
                dphis[j,x,q]=phi[x+1]
        q+=1
    #print "dphis", dphis
    #np.save("./dhpis.npy",dphis)

    
    for m in range(n):
        for x in range(n):
            #for error bars plt.errorbars must be used.
            plt.plot(subdirs, dphis[m,x,:],marker='*',label=[str(x)])
        plt.legend()
        plt.show()




