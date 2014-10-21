#!/usr/bin/env python 
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import os, glob, shutil
from subprocess import Popen

indir = os.getcwd()
dataDir=os.path.join(indir,"data")
scriptOutDir=os.path.join(indir,"subPyNormInt")
i = 1

def submit(jsub_file):
    cmd = 'jsub '+jsub_file
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    proc.wait()
BoA = str(raw_input("Have you used devTest?(y/n): ")) 
if BoA == 'n':
    stri = 'set_'
    name = 'alphaevents.txt'
elif BoA == 'y':
    AoR = str(raw_input("acc or raw?: ").lower())
    stri = '/mc/'+AoR
    name = 'alpha'+AoR+'MC.txt'
for path, subdirs, files in os.walk(dataDir):
    for filename in glob.glob(path):
        if stri in filename:        
            #filename = os.path.basename(filename)
            cmd_opts = dict(
                cwd = indir,
                dirc = path,
                name = name                
               )
                    
            cmd = '''/u/apps/anaconda/anaconda-2.0.1/bin/python2 {cwd}/run_normintFARM.py {dirc} {name}
    '''.format(**cmd_opts)
            #print cmd
            auger_opts = dict(
                project = 'gluex',
                track = 'test',
                jobname = 'normINT',
                os = 'centos62',
                memory = '512 MB',
    	    time = 30,
                cmd = cmd)
            jsub_filename = os.path.join(scriptOutDir,"subNormINT"+str(i))
            #print jsub_filename
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
            submit(jsub_filename)
            i += 1
