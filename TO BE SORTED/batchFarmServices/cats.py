"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import os, glob, shutil, sys 
from subprocess import Popen 

sets = int(raw_input("number of sets?: "))
MoD = raw_input("mc or data?: ")
AoR = raw_input("acc or raw?: ")
nfile = str(AoR+(MoD.upper())+".gamp")
if MoD.lower() == "mc":
    if AoR.lower() == "acc":
        ofile = "accMC.gamp"
    elif AoR.lower() == "raw":
        ofile = "events.gamp"
elif MoD.lower() == "data":
    if AoR.lower() == "acc":
        ofile = "selected_events.acc.gamp"
    elif AoR.lower() == "raw":
        ofile = "selected_events.raw.gamp"
for d in os.listdir(os.path.join(os.getcwd(),"data")):
    cmd = 'touch '+os.path.join(os.getcwd(),"data",str(d),MoD.lower(),AoR,nfile)
    proc = Popen(cmd,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
    proc.wait()
    print cmd+'\n'          
for d in os.listdir(os.path.join(os.getcwd(),"data")):        
    for i in range(sets):
        if os.path.isfile(os.path.join(os.getcwd(),"data",str(d),'set_'+str(i),str(ofile))):        
            cmd1 = 'cat '+os.path.join(os.getcwd(),"data",str(d),'set_'+str(i),str(ofile))+' >> '+os.path.join(os.getcwd(),"data",str(d),MoD.lower(),AoR.lower(),nfile)
            proc1 = Popen(cmd1,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
            proc1.wait()
            print cmd1+'\n'


