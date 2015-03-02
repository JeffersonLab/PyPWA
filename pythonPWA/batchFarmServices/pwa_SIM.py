import os, sys, time
import subprocess as sp
sys.path.append(os.path.join(os.getcwd().rstrip("GUI"),"pythonPWA"))
from batchFarmServices.farmCheck import farmCheck

fC = farmCheck("jobstat -u jpond")
print "GAMP"
sp.call([os.path.join(os.getcwd().strip("GUI"),"scripts","GUI_gamp_main.py"),"n","flat"])
time.sleep(5)
print "ALPHA"
sp.call([os.path.join(os.getcwd().strip("GUI"),"scripts","GUI_alpha_main.py"),"n","flat"])
if fC.check():
    print "NORM INT"
    sp.call([os.path.join(os.getcwd().strip("GUI"),"scripts","GUI_subPyNormInt.py"),"n","flat"])
if fC.check():
    print "I LIST"
    sp.call([os.getcwd().strip("GUI")+"/scripts/subSimulator","i"])
if fC.check():
    print "I MAX"
    sp.call(os.getcwd().strip("GUI")+"/scripts/getImax.py")
if fC.check():
    print "SIMULATOR"
    sp.call([os.getcwd().strip("GUI")+"/scripts/subSimulator","s"])
    

