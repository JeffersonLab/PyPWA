#! /usr/bin/python
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import os, sys
from subprocess import Popen

dirs = os.listdir(os.path.join(os.path.split(os.path.split(os.getcwd())[0])[0],"fitting"))

for d in dirs:
    if "_MeV" in d:
        for i in ("data","mc"):
            cmd = 'mkdir '+os.path.join(os.path.join(os.path.split(os.path.split(os.getcwd())[0])[0],"fitting",str(d),str(i)))
            proc = Popen(cmd,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
            proc.wait()
        cmd1 = 'mkdir '+os.path.join(os.path.join(os.path.split(os.path.split(os.getcwd())[0])[0],"fitting",str(d),"mc","acc")+" "+os.path.join(os.path.join(os.path.split(os.path.split(os.getcwd())[0])[0],"fitting",str(d),"mc","raw")))
        proc1 = Popen(cmd1,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
        proc1.wait()	
        if d != dirs[-1]:
            sys.stdout.write("Filling Bins"+"."*(dirs.index(d)+1)+"\r")
            sys.stdout.flush()
        elif d == dirs[-1]:
            sys.stdout.write("Filling Bins"+"."*(dirs.index(d)+1)+"\r\n")
            sys.stdout.flush()
