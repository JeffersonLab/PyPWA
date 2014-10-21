#!/usr/bin python 
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import os, glob, shutil
from subprocess import Popen


#add bin selection via 

scriptOutDir=os.path.join(os.getcwd(),"subpfFilter")

def submit(jsub_file):
    cmd = 'jsub '+jsub_file
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    proc.wait()




def gen(directory,cmd,i):

    auger_opts = dict(
                    project = 'gluex',
                    track = 'analysis',
                    jobname = 'pfFilter',
                    os = 'centos62',
                    time = 30,
		    cmd = cmd)

    jsub_filename = os.path.join(scriptOutDir,directory)+"_"+str(i)
    jsub_file = open(jsub_filename,'w')
    jsub_file.write('''\
PROJECT:{project}
TRACK:{track}
JOBNAME:{jobname}
OS:{os}
TIME:{time}
COMMAND:{cmd}
'''.format(**auger_opts))

    jsub_file.close()

    return jsub_filename

def parseDir(Bin,i):
    
    cmd = "/u/apps/anaconda/anaconda-2.0.1/bin/python2 "+os.getcwd()+"/pfFilterFarm.py "+str(Bin)+" "+str(i)+" "+os.getcwd()

    return cmd



if __name__ == '__main__':
    sets = int(raw_input("number of sets?: "))	
    for d in os.listdir(os.path.join(os.getcwd(),"data")):
        for i in range(sets):
            if os.path.isdir(os.path.join(os.getcwd(),"data",d)):
                if d.find("_MeV")!=-1:
                    print "Processing bin",d,i
                    submit(gen(d,parseDir(d.strip("_MeV"),i),str(i)))
