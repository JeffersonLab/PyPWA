#!/usr/bin python 
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import os, glob, shutil
from subprocess import Popen
import time, sys

#add bin selection via 
indir = os.getcwd().strip("GUI")
Control = numpy.load(os.path.join(indir,"GUI","Control_List.npy"))
scriptOutDir=os.path.join(indir,"scripts","submitions")

def submit(jsub_file):
    cmd = 'jsub '+jsub_file
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    time.sleep(1)




def gen(directory,cmd):

    auger_opts = dict(
                    project = 'gluex',
                    track = 'analysis',
                    jobname = 'devTest',
                    os = 'centos62',
                    time = 30,
		    cmd = cmd)

    jsub_filename = os.path.join(scriptOutDir,directory)
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

def parseDir(Bin):
    
    cmd = "/u/apps/anaconda/anaconda-2.0.1/bin/python2 "+os.path.join(indir,"devTestFarm.py")+" "+str(Bin)+" "+indir+" "+sys.argv[1]

    return cmd



if __name__ == '__main__':
    top = int(Control[2])    
    bot = int(Control[3])
    ran = int(Control[4])
    for i in range(top,bot+ran,ran):
        print "Processing bin",i
        submit(gen(str(i)+"_MeV",parseDir(i)))
