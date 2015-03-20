import fileinput
import numpy
def kvParser():  
    events =[]  
    for line in fileinput.input(["kvArgsGen.txt"]):
        kvAs = line.split(",")
        kvAx = {kvA.split('=')[0]:float(kvA.split('=')[1]) for kvA in kvAs}   
        events.append(dict(kvAx))
    return events 
numpy.save("kvArgsGen.npy",kvParser())
