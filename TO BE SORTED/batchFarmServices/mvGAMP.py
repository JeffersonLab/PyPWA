"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import os, glob, shutil
from subprocess import Popen 
sets = int(raw_input("number of sets?: "))
for d in os.listdir(os.path.join(os.getcwd(),"MC")):
    cmd = 'cp '+os.path.join(os.getcwd(),"MC",str(d))+'/'+str(d)+'.gamp* '+os.path.join(os.getcwd(),"data",str(d))
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    proc.wait()
   
    print(cmd)

    cmd1 = 'cp '+os.path.join(os.getcwd(),"MC",str(d))+'/output.gamp.index* '+os.path.join(os.getcwd(),"data",str(d))
    proc = Popen(cmd1,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    proc.wait()
   
    print(cmd1)

for d in os.listdir(os.path.join(os.getcwd(),"data")):
    for i in range(sets):
        cmd2 = 'mv '+os.path.join(os.getcwd(),"data",str(d))+'/'+str(d)+'.gamp_'+str(i)+" "+os.path.join(os.getcwd(),"data",str(d),"set_"+str(i),"events.gamp")
        proc = Popen(cmd2,
            shell = True,
            executable = os.environ.get('SHELL', '/bin/tcsh'),
            env = os.environ)
        proc.wait()
   
        print(cmd2)
        
        cmd3 = 'mv '+os.path.join(os.getcwd(),"data",str(d))+'/output.gamp.index_'+str(i)+" "+os.path.join(os.getcwd(),"data",str(d),"set_"+str(i),"output.gamp.index")
        proc = Popen(cmd3,
            shell = True,
            executable = os.environ.get('SHELL', '/bin/tcsh'),
            env = os.environ)
        proc.wait()
   
        print(cmd3)
