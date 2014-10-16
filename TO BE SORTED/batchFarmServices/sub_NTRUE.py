import os, glob, shutil,numpy
from subprocess import Popen 


'''
for d in os.listdir(os.path.join("/","volatile","halld","pkk","data","Simulation")):
   
   cmd = 'python runSimNTrue.py '+str(d)
   proc = Popen(cmd,
       shell = True,
       executable = os.environ.get('SHELL', '/bin/tcsh'),
       env = os.environ)
   proc.wait()
   

 
   print(cmd)
'''
Results = []
for d in sorted(os.listdir(os.path.join("/","volatile","halld","pkk","data","Simulation"))):
    if os.path.isfile(os.path.join("/","volatile","halld","pkk","data","Simulation",d,"total.npy")):    
        t = numpy.load(os.path.join("/","volatile","halld","pkk","data","Simulation",d,"total.npy"))
        print(t)        
        Results.extend(t)
numpy.save(os.path.join("/","volatile","halld","pkk","data","Simulation","Results.npy"),Results)