#!/usr/bin/sh python 
import os
import sys 
import time



def makeExtendedIndex(directory,indexList,maxIndex):
    i=0
    extendedFile=open(os.path.join(directory,"events.pf"),'w')
    for i in range(maxIndex):
        if i+1 not in indexList:
            extendedFile.write("0"+"\n")
        if i+1 in indexList:
            extendedFile.write("1"+"\n")
        i+=1
    extendedFile.close()

def filterFile(indexFile):
    acceptedList=[]
    for lines in indexFile.readlines():
        acceptedList.append(int(lines.split(" ")[0]))
    return acceptedList

if __name__ == '__main__':
    #SPECIFY MAX NUMBER OF EVENTS HERE
    eventCount=int(sys.argv[3])
    if os.path.isdir(os.path.join(sys.argv[4],"data",sys.argv[1])):
        if sys.argv[1].find("_MeV")!=-1:
            fileBuf=open(os.path.join(sys.argv[4],"data",sys.argv[1],sys.argv[2],"output.gamp.index"),'r')
            makeExtendedIndex(os.path.join(sys.argv[4],"data",sys.argv[1],sys.argv[2]),filterFile(fileBuf),eventCount)
            fileBuf.close()
	    
	    
