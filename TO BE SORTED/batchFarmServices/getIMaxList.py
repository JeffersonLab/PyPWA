import numpy 
import os

topDir = os.getcwd()+"/data"
iMaxList = []
x = 0
sets = int(raw_input("Number of sets?: "))
for d in os.listdir(topDir):
    for i in range(sets):
        dataDir = os.path.join(topDir,d,"set_"+str(i))        
        if os.path.isfile(os.path.join(topDir,d,"set_"+str(i),"iList.npy")):        
            il = numpy.load(os.path.join(dataDir,"iList.npy"))
            iMaxList.append(max(il))
            print(x)
            x+=1
numpy.save(topDir+"/IMaxList.npy",iMaxList)

