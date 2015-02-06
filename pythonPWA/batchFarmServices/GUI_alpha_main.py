#!/usr/bin/python 
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


"""
import os, glob, numpy, sys, time
from subprocess import Popen

indir = os.getcwd().strip("GUI")
dataDir=os.path.join(indir,"fitting")
scriptOutDir=os.path.join(indir,"scripts","submitions")
cf = numpy.load(os.path.join(indir,"GUI","Control_List.npy"))
i = 1
M= cf[0]

def submit(jsub_file):
    cmd = 'jsub '+jsub_file
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    time.sleep(.5)

BoA = sys.argv[1]
if BoA == 'n':
    DoM = sys.argv[2]
    if DoM == 'weight':
        dataDir=os.path.join(indir,"simulation")
        AoR = sys.argv[3]
        stri = '/'+DoM+'/'+AoR
        filen = 'events'
    elif DoM == 'flat':
        dataDir=os.path.join(indir,"simulation")
        stri = 'flat'
        filen = 'events'
elif BoA == 'y':
    DoM = sys.argv[2]
    if DoM == 'mc':
        dataDir=os.path.join(indir,"fitting")
        AoR = sys.argv[3]
        stri = '/'+DoM+'/'+AoR
        filen = 'events'
    elif DoM == 'data':
        dataDir=os.path.join(indir,"fitting")
        stri = DoM
        filen = 'events'
for path, subdirs, files in os.walk(dataDir):
    for filename in glob.glob(path):
        if stri in filename:            
            cmd_opts = dict(
                indir = indir,
                cwd = os.path.join(indir,"scripts"),                
                filen = filen,
                direct = filename+'/',
                mode = M)                    
            cmd = '''/u/apps/anaconda/anaconda-2.0.1/bin/python2 {cwd}/generateAlphaNPY.py {mode} {direct} {filen} {indir}
    '''.format(**cmd_opts)
            auger_opts = dict(
                project = cf[9],
                track = 'analysis',
                jobname = 'AlphaGen',
                os = 'centos65',
                memory = '3000 MB',
    	        time = 300,
                cmd = cmd)
            jsub_filename = os.path.join(scriptOutDir,"subAlpha"+str(i))
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
