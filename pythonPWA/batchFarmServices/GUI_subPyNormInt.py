#!/usr/bin/env python
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


"""
import os, glob, sys, numpy, time
from subprocess import Popen

indir = os.getcwd().strip("GUI")
cf = numpy.load(os.path.join(indir,"GUI","Control_List.npy"))
scriptOutDir=os.path.join(indir,"scripts","submitions")
i = 1

def submit(jsub_file):
    cmd = 'jsub '+jsub_file
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    time.sleep(.5)
    
BoA = sys.argv[1] 
if BoA == 'n':
    dataDir=os.path.join(indir,"simulation")
    AoR = sys.argv[2]
    stri = '/mc/'+AoR
    name = 'alphaevents.txt'
elif BoA == 'y':
    dataDir=os.path.join(indir,"fitting")
    AoR = sys.argv[2]
    stri = '/mc/'+AoR
    name = "alphaevents.txt"
for path, subdirs, files in os.walk(dataDir):
    for filename in glob.glob(path):
        if stri in filename:             
            cmd_opts = dict(
                cwd = os.path.join(indir,"scripts"),
                dirc = path,
                name = name,
                beamP = cf[1],
                indir = indir            
               )                    
            cmd = '''/u/apps/anaconda/anaconda-2.0.1/bin/python2 {cwd}/run_normintFARM.py {dirc} {name} {beamP} {indir}
    '''.format(**cmd_opts)            
            auger_opts = dict(
                project = cf[9],
                track = 'analysis',
                jobname = 'normINT',
                os = 'centos65',
                memory = '3000 MB',
    	        time = 360,
                cmd = cmd)
            jsub_filename = os.path.join(scriptOutDir,"subNormINT"+str(i))            
            jsub_file = open(jsub_filename,'w')
            jsub_file.write('''\
PROJECT: {project}
TRACK: {track}
JOBNAME: {jobname}
OS: {os}
MEMORY: {memory}
TIME: {time}
COMMAND: {cmd}
    '''.format(**auger_opts))
    
            jsub_file.close()
            print jsub_filename
            submit(jsub_filename)
            #os.remove(jsub_filename)            
            i += 1
