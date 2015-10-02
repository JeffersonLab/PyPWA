import os

def readAmpdbList(filename):
    """
    filename needs to be whole path
    """
    listTest=open(filename,'r')
    wholeFile=listTest.readlines()
    events=wholeFile[1:len(wholeFile)]
    bufList=[]
    for event in events:
        a=event.strip("[").strip("]").split(",")
        b=[]
        for item in a:
            b.append(float(item.strip(" ").strip("]\n")))
        bufList.append(b)
    return bufList