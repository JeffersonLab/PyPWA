inputGampFile=open(os.path.join(dataDir,"_events.gamp"),'r')
initialGampList,rawGampList,accGampList=dSimulator.execute(inputGampFile,outputRawGampFile,outputAccGampFile,inputPfFile)
numpyInitialGampList=numpy.array(initialGampList)
numpyRawGampList=numpy.array(rawGampList)
numpyAccGampList=numpy.array(accGampList)

numpy.save(os.path.join(dataDir,"numpyInitialGampList"),numpyInitialGampList)
numpy.save(os.path.join(dataDir,"numpyRawGampList"),numpyRawGampList)
numpy.save(os.path.join(dataDir,"numpyAccGampList"),numpyAccGampList)
numpyInitialGampList=numpy.load(os.path.join(dataDir,"numpyInitialGampList.npy"))
numpyRawGampList=numpy.load(os.path.join(dataDir,"numpyRawGampList.npy"))
numpyAccGampList=numpy.load(os.path.join(dataDir,"numpyAccGampList.npy"))

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def plotGampEvents(initial,raw,accepted,nInitial,nFinal):
    initial=initial[nInitial:nFinal]
    raw=raw[nInitial:nFinal]
    accepted=accepted[nInitial:nFinal]

    fig = plt.figure(figsize=(14, 10), dpi=100)
    fig.suptitle("Gamp Events "+str(nInitial)+" to "+str(nFinal))
    ax = fig.add_subplot(111, projection='3d')

    xCoords=[x for x in range(nFinal) if x>=nInitial]
    ax.bar(xCoords,initial,zs=[2 for z in range(nFinal) if z>=nInitial],zdir='y',color='g',alpha=0.6)
    ax.bar(xCoords,raw,zs=[1 for z in range(nFinal) if z>=nInitial],zdir='y',color='b',alpha=0.75)
    ax.bar(xCoords,accepted,zs=[0 for z in range(nFinal) if z>=nInitial],zdir='y',color='r',alpha=.8)

    ax.set_xlabel('Event Number')
    ax.set_ylabel('Gamp File')
    ax.set_zlabel('Event Present')
    
    ax.axes.yaxis.set_ticklabels(['accepted','','raw','','initial'])
    ax.axes.zaxis.set_ticklabels(['not present','','','','','present'])
    plt.show()

plotGampEvents(initial,raw,accepted,0,200)