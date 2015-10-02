import fileinput
import numpy
def kvParser(dataFile):  
    events =[]  
    for line in fileinput.input([dataFile]):
        kvAs = line.split(",")
        kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}   
        events.append(dict(kvAx))
    return numpy.array(events) 

