#!/usr/bin/python 
import os, glob, shutil
from subprocess import Popen

indir = os.getcwd()
keyfileDir=os.path.join(indir,"keyfiles")
dataDir=os.path.join(indir,"fitting")
scriptOutDir=os.path.join(indir,"subGamps")

keyfiles=glob.glob(os.path.join(keyfileDir,'*.keyfile'))
i=1

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
    DoM = str(raw_input("mc or data?: "))
    AoR = str(raw_input("acc or raw?: "))
    stri = '/'+DoM+'/'+AoR
    
for keyfile in keyfiles:
    for path, subdirs, files in os.walk(dataDir):
        if stri in path:         
            for filename in glob.glob(os.path.join(path,'*.gamp')):
                filename = os.path.basename(filename)
                cmd_opts = dict(
    				outfile = os.path.join(path,os.path.basename(keyfile)).replace('.keyfile','.bamp'),
                    keyfile = os.path.join(keyfileDir,keyfile),
                    infile = os.path.join(path, filename))
                    #outfile = os.path.join(path, ".bamp")
                    #outfile = os.path.join(path,filename))
                    #outfile = os.path.join('/work/clas/clasg12/salgado/auger',keyfile+'_'+filename))
                cmd = '''\
/group/clas/builds/bin/gamp {keyfile} < {infile} > {outfile}
    '''.format(**cmd_opts)
                #print cmd
                auger_opts = dict(
                    project = 'gluex',
                    track = 'analysis',
                    jobname = 'runGamp',
                    os = 'centos62',
                    time = 30,
                    cmd = cmd)
                jsub_filename = os.path.join(scriptOutDir,"subGamp"+str(i))
                #print jsub_filename
                jsub_file = open(jsub_filename,'w')
                jsub_file.write('''\
PROJECT: {project}
TRACK: {track}
JOBNAME: {jobname}
OS: {os}
TIME: {time}
COMMAND: {cmd}
    '''.format(**auger_opts))
    
                jsub_file.close()
                if not os.path.isfile( os.path.join(path,os.path.basename(keyfile)).replace('.keyfile','.bamp')):
                    submit(jsub_filename)
                    #os.remove(jsub_filename)
                    i += 1  
