#! /u/apps/anaconda/anaconda-2.0.1/bin/python2 
import os, sys
import numpy 

indir = os.path.split(os.path.split(os.getcwd())[0])[0]
Control = numpy.load(os.path.join(indir,"GUI","Control_List.npy"))

#getting the users input
minimum = int(Control[2])    
maximum = int(Control[3])
binSize = int(Control[4])
targets=sys.argv
#testing the targetDirectory for existence
for i in range(1,len(sys.argv)):
    if os.path.exists(targets[i])==False:
        print "Error: Couldn't find path:",targets[i]
        print "Breaking..."
        exit()
    if os.path.exists(targets[i])==True:
        #main directory creation loop
        x=minimum
        h=1
        while x<=maximum:
            if x != maximum:
                sys.stdout.write("Writing Bins"+"."*h+"\r")
                sys.stdout.flush()
            elif x == maximum:
                sys.stdout.write("Writing Bins"+"."*h+"\r\n")
                sys.stdout.flush()
            directoryBuffer=os.path.join(targets[i],str(x)+"_MeV")
            os.makedirs(directoryBuffer)
            x+=binSize
            h+=1
