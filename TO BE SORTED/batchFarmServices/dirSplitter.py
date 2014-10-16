#!/usr/bin/env python
import os

#getting the users input
minimum=int(raw_input("Enter Minimum Value: "))
maximum=int(raw_input("Enter Maximum Value: "))
binSize=int(raw_input("Enter Size of Each Bin: "))
targetDirectory=raw_input("Enter the Directory to Create the Bins In: ")

#testing the targetDirectory for existence
if os.path.exists(targetDirectory)==False:
    print "Error: Couldn't find path:",targetDirectory
    print "Breaking..."
    exit()

if os.path.exists(targetDirectory)==True:
    print "Path",targetDirectory,"found.  Beginning main directory creation loop."
    #main directory creation loop
    i=minimum
    while i<=maximum:
        print "creating directory",str(i)+"_MeV in",targetDirectory
        directoryBuffer=os.path.join(targetDirectory,str(i)+"_MeV")
        os.makedirs(directoryBuffer)
        i+=binSize