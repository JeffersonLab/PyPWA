from pythonPWA.fileHandlers.gampReader import gampReader
import os

class gampComparison(object):
    """
    Simple class to produce various comparisons between 2 gamp files.
    Args are simply the path to gamp1 and gamp2.
    """
    def __init__(self,
                 gamp1Path,
                 gamp2Path):
        
        self.gampReader1=gampReader(gampFile=open(gamp1Path,'r'))
        self.gampReader2=gampReader(gampFile=open(gamp2Path,'r'))
        
        self.gamp1Events=self.gampReader1.readGamp()
        self.gamp2Events=self.gampReader2.readGamp()
    
    def countGampEvents(self):
        print"="*10
        print"Gamp 1:",len(self.gamp1Events),"events"
        print"Gamp 2:",len(self.gamp2Events),"events"

if __name__==('__main__'):
    topDataDir=os.path.join(os.getcwd(),"data","1000_MeV")

    gamp1Path=os.path.join(topDataDir,"seq_raw_events.gamp")
    gamp2Path=os.path.join(topDataDir,"threaded_raw_events.gamp")

    print"=-"*5
    print"gamp1:",gamp1Path
    print"gamp2:",gamp2Path

    gampComp=gampComparison(gamp1Path,gamp2Path)

    gampComp.countGampEvents()

