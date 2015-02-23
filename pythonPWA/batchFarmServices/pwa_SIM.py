import os, sys, time
import subprocess as sp
sys.path.append(os.path.join(os.getcwd().rstrip("scripts"),"pythonPWA"))
from batchFarmServices.farmCheck import farmCheck

fC = farmCheck("jobstat -u jpond")
print "GAMP"
sp.call([os.path.join(os.getcwd(),"GUI_gamp_main.py"),"n","flat"])
time.sleep(5)
print "ALPHA"
sp.call([os.path.join(os.getcwd(),"GUI_alpha_main.py"),"n","flat"])
if fC.check():
    print "NORM INT"
    sp.call([os.path.join(os.getcwd(),"GUI_subPyNormInt.py"),"n","flat"])
if fC.check():
    print "I LIST"
    sp.call([os.getcwd()+"/subSimulator","i"])
if fC.check():
    print "I MAX"
    sp.call(os.getcwd()+"/getImax.py")
if fC.check():
    print "SIMULATOR"
    sp.call([os.getcwd()+"/subSimulator","s"])
    

