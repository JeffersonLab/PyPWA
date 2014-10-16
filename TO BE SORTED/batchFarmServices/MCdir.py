import os
from subprocess import Popen
MoD = raw_input("mc or data?: ")
for d in os.listdir(os.path.join(os.getcwd(),"data")):
    cmd = 'mkdir '+os.path.join(os.getcwd(),"data",str(d),MoD.lower())
    proc = Popen(cmd,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
    proc.wait()
    cmd1 = 'mkdir '+os.path.join(os.getcwd(),"data",str(d),MoD.lower(),"acc")+" "+os.path.join(os.getcwd(),"data",str(d),MoD.lower(),"raw")
    proc1 = Popen(cmd1,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
    proc1.wait()	
    print(cmd+"\n"+cmd1) 
