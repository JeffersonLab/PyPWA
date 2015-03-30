#! /u/apps/anaconda/anaconda-2.0.1/bin/python2 
"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import os, glob
from subprocess import Popen
import time, sys, numpy

#add bin selection via 
indir = os.getcwd().strip("GUI")
Control = numpy.load(os.path.join(indir,"GUI","Control_List.npy"))
scriptOutDir=os.path.join(indir,"scripts","submitions")
"""
    This is submition program for the simulator.
"""

def submit(jsub_file):
    """
    This function calls the JLab jsub command for a specific jsub .txt file created by this program. 

    Args:
    jsub_file (string): The file name for the jsub file.
    """
    cmd = 'jsub '+jsub_file
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    time.sleep(1)




def gen(directory,cmd):
    """
    This function creates the jsub .txt file to be submitted to the JLab batch farm. 

    Args:
    directory (string): The file name for the jsub file.
    cmd (string): The full command to be used in the jsub file. 

    Returns:
    jsub_filename (string): name of the jsub file created by this function.
    """
    auger_opts = dict(
                    project = Control[9],
                    track = 'analysis',
                    jobname = 'simulator',
                    os = 'centos65',
                    memory = '1000 MB',
                    time = 30,
		    cmd = cmd)

    jsub_filename = os.path.join(scriptOutDir,directory)
    jsub_file = open(jsub_filename,'w')
    jsub_file.write('''\
PROJECT:{project}
TRACK:{track}
JOBNAME:{jobname}
OS:{os}
MEMORY:{memory}
TIME:{time}
COMMAND:{cmd}
'''.format(**auger_opts))

    jsub_file.close()

    return jsub_filename

def parseDir(Bin):
    """
    This function creates the cmd string to be submitted to the JLab batch farm. 

    Args:
    bin (int): The int value for the mass in MeV for the mass bin.
    
    Returns:
    cmd (string): The full command to be used in the jsub file.
    """
    cmd = "/u/apps/anaconda/anaconda-2.0.1/bin/python2 "+os.path.join(indir,"scripts","simulatorMain.py")+" "+str(Bin)+" "+indir+" "+sys.argv[1]

    return cmd



if __name__ == '__main__':
    top = int(Control[2])    
    bot = int(Control[3])
    ran = int(Control[4])
    for i in range(top,bot+ran,ran):
        print "Processing bin",i
        submit(gen(str(i)+"_MeV",parseDir(i)))
