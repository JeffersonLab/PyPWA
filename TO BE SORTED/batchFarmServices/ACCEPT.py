#!/usr/bin python
import os, glob, shutil, sys
from subprocess import Popen


#add bin selection via  

scriptOutDir=os.path.join(os.getcwd(),"genACC")
binSize=int(raw_input("bin width?: "))
maxEvents=int(raw_input("max number of events?: "))
sets=int(raw_input("number of sets?: "))

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
                    jobname = 'makePF',
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
    
    cmd = "/u/apps/anaconda/anaconda-2.0.1/bin/python2 "+os.getcwd()+"/acceptanceFilter_farm.py "+str(Bin)+" set_"+str(i)+" "+str(maxEvents)+" "+os.getcwd()

    return cmd



if __name__ == '__main__':
	for d in os.listdir(os.path.join(os.getcwd(),"data")):
		for i in range(sets):
			if os.path.isdir(os.path.join(os.getcwd(),"data",d)):
				if d.find("_MeV")!=-1:
					print "Processing bin",d,i
					submit(gen(d,parseDir(d,i),str(i)))
