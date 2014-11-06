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
scriptOutDir=os.path.join(indir,"genAlpha")
i = 1
M= str(raw_input("Which AlphaGen mode?: "))
def submit(jsub_file):
    cmd = 'jsub '+jsub_file
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    proc.wait()
BoA = str(raw_input("Have you used devTest?(y/n): ")) 
if BoA == 'n':
    filen = 'events'    
    stri = 'set_'
elif BoA == 'y':
    DoM = str(raw_input("mc or data?: ").lower())
    AoR = str(raw_input("acc or raw?: ").lower())
    stri = '/'+DoM+'/'+AoR
    filen = AoR+(DoM.upper())
for path, subdirs, files in os.walk(dataDir):
    for filename in glob.glob(path):
        if stri in filename:        
            #filename = os.path.basename(filename)
            cmd_opts = dict(
                cwd = indir,                
                filen = filen,
                direct = filename+'/',
                mode = M)
                    
            cmd = '''/apps/scicomp/java/jdk1.7/bin/java -Xmx256m -jar {cwd}/AlphaGen.jar {mode} {direct} {filen}
    '''.format(**cmd_opts)
            #print cmd
            auger_opts = dict(
                project = 'gluex',
                track = 'test',
                jobname = 'AlphaGen',
                os = 'centos62',
                memory = '512 MB',
    	    time = 30,
                cmd = cmd)
            jsub_filename = os.path.join(scriptOutDir,"subAlpha"+str(i))
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
