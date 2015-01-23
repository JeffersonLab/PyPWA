from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def plotnTrue(nTrueList,nTrueDWaveList,nTruePWaveList,massList):

    fig = plt.figure(figsize=(14, 10), dpi=100)
    fig.suptitle("Predicted Events")
    ax = fig.add_subplot(111, projection='3d')

    xCoords=massList
    ax.bar(xCoords,nTrueList,zs=[0 for z in range(len(massList))],zdir='y',color='g',alpha=0.6,width=1.,linewidth=0)
    ax.bar(xCoords,nTruePWaveList,zs=[1 for z in range(len(massList))],zdir='y',color='b',alpha=0.75,width=1.,linewidth=0)
    ax.bar(xCoords,nTrueDWaveList,zs=[2 for z in range(len(massList))],zdir='y',color='r',alpha=.8,width=1.,linewidth=0)

    ax.set_xlabel('Mass (MeV)')
    ax.set_ylabel('Wave')
    ax.set_zlabel('Number of Events')
    
    ax.axes.yaxis.set_ticklabels(['Total','','Wave 1','','Wave 2'])
    #ax.axes.zaxis.set_ticklabels(['not present','','','','','present'])
    plt.show()    
    
nTrueList=[]
nTrueDWaveList=[]
nTruePWaveList=[]
for mass in massList:
    nTrueList.append(nTrue(resonances,waveList,mass,normint))
    nTrueDWaveList.append(nTrueForWave(resonances,waveList,waveList[1],mass,normint))
    nTruePWaveList.append(nTrueForWave(resonances,waveList,waveList[0],mass,normint))
    
plotnTrue(nTrueList,nTrueDWaveList,nTruePWaveList,massList)