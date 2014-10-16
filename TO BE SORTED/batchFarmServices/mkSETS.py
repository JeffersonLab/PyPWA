import os, time
from subprocess import Popen
sets = int(raw_input("Number of sets?"))
for d in sorted(os.listdir(os.path.join(os.getcwd(),"data"))):
  for i in range(sets): 
    cmd = 'mkdir '+os.path.join(os.getcwd(),"data",str(d),"set_"+str(i))
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    proc.wait()
    print(cmd)
    
