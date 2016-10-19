# TODO Figure out where numpyInitialGampList is defined.

print( "_events in initial gamp:", len(numpyInitialGampList))

initial=[]
for initalGamp in numpyInitialGampList:
    initial.append(1)

accepted=[]
acceptedEvents=[]
for accGamp in numpyAccGampList:
    if accGamp !=None:
        accepted.append(1)
        acceptedEvents.append(accGamp)
    if accGamp ==None:
        accepted.append(0)
        
raw=[]
rawEvents=[]
for rawGamp in numpyRawGampList:
    if rawGamp != None:
        raw.append(1)
        rawEvents.append(rawGamp)
    if rawGamp==None:
        raw.append(0)

print("_events in raw gamp:",len(rawEvents))
print("_events in accepted gamp:",len(acceptedEvents))