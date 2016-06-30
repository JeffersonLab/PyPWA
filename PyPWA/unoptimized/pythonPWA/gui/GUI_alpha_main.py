#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import glob
import sys
import time
import subprocess

import numpy

from PyPWA import LICENSE, STATUS, VERSION

__author__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__credits__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


def submit(jsub_file):
    """
    This function calls the JLab jsub command for a specific jsub .txt
    file created by this program.

    Args:
        jsub_file (string): The file name for the jsub file.
    """
    cmd = 'jsub '+jsub_file
    subprocess.Popen(
        cmd,
        shell=True,
        executable=os.environ.get('SHELL', '/bin/tcsh'),
        env=os.environ
    )

    time.sleep(.5)


if __name__ == '__main__':
    """
    This is the submition program for the alpha calculation.
    """
    indir = os.getcwd().strip("GUI")
    dataDir=os.path.join(indir,"fitting")
    scriptOutDir=os.path.join(indir,"scripts","submitions")
    cf = numpy.load(os.path.join(indir,"GUI","Control_List.npy"))
    i = 1
    M= cf[0]
    BoA = sys.argv[1]
    if BoA == 'n':
        DoM = sys.argv[2]
        if DoM == 'weight':
            dataDir=os.path.join(indir,"simulation")
            AoR = sys.argv[3]
            stri = '/'+DoM+'/'+AoR
            filen = '_events'
        elif DoM == 'flat':
            dataDir=os.path.join(indir,"simulation")
            stri = 'flat'
            filen = '_events'
    elif BoA == 'y':
        DoM = sys.argv[2]
        if DoM == 'mc':
            dataDir=os.path.join(indir,"fitting")
            AoR = sys.argv[3]
            stri = '/'+DoM+'/'+AoR
            filen = '_events'
        elif DoM == 'data':
            dataDir=os.path.join(indir,"fitting")
            stri = DoM
            filen = '_events'
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
                print(jsub_filename)
                submit(jsub_filename)

                i += 1
