#!/usr/bin/python 
import os, glob, shutil, numpy, sys
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

BoA = sys.argv[1]
if BoA == 'n':
    dataDir=os.path.join(indir,"simulation")
    filen = 'events'    
    stri = 'set_'
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
                cwd = os.path.join(indir,"scripts"),                
                filen = filen,
                direct = filename+'/',
                mode = M)                    
            cmd = '''/u/apps/anaconda/anaconda-2.0.1/bin/python2 {cwd}/generateAlphas.py {mode} {direct} {filen}
    '''.format(**cmd_opts)
            auger_opts = dict(
                project = 'gluex',
                track = 'analysis',
                jobname = 'AlphaGen',
                os = 'centos62',
                memory = '8000 MB',
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
