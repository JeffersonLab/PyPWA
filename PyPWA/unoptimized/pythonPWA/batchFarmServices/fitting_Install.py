
import os
import numpy,sys
import subprocess as sp
from subprocess import Popen
"""
    This program is the first step for the PyPWA fitting process. It sets up all directories and files needed for fitting
    as well as all binning in mass as prescribed by the pwa_controls GUI. 
"""
indir = os.path.split(os.path.split(os.getcwd())[0])[0]
print( "Top Directory: ",indir )
sys.path.append(os.path.join(indir,"pythonPWA"))
if not os.path.isfile(os.path.join("Control_List.npy")):
    sp.call(os.path.abspath("pwa_controls"))
Control = numpy.load(os.path.join("Control_List.npy"))  
print("Creating directory structure for PyPWA fitting")
tdirs = ("fitting","GUI","keyfiles","scripts")
for i in tdirs:
    directoryBuffer=os.path.join(indir,str(i))
    os.makedirs(directoryBuffer)
    if i != tdirs[-1]:
        sys.stdout.write("Writing Directories"+"."*(tdirs.index(i)+1)+"\r")
        sys.stdout.flush()
    elif i == tdirs[-1]:
        sys.stdout.write("Writing Directories"+"."*(tdirs.index(i)+1)+"\r\n")
        sys.stdout.flush()
    if i == "fitting":
        for d in ("overflow","results"):
            directoryBuffer=os.path.join(indir,"fitting",str(d))
            os.makedirs(directoryBuffer)  
    if i == "GUI":
        directoryBuffer=os.path.join(indir,"GUI","plotLists")
        os.makedirs(directoryBuffer)          
    if i == "scripts":
        directoryBuffer=os.path.join(indir,"scripts","submitions")
        os.makedirs(directoryBuffer)        
progs = ("fnGenerator.py","generateAlphaNPY.py","GUI_alpha_main.py",
"GUI_gamp_main.py","GUI_subPyNormInt.py","likelihoodTest.py","mvBAMP_GUI",
"run_normintFARM.py","subLikelihood","subWalkNTrue","walkingNTrue.py","massBinner2.py")
for s in progs:
    cmd = 'cp '+os.path.join(os.getcwd(),str(s))+" "+os.path.join(indir,"scripts")
    proc = Popen(cmd,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
    proc.wait()
    if s != progs[-1]:
        sys.stdout.write("Filling scripts"+"."*(progs.index(s)+1)+"\r")
        sys.stdout.flush()
    elif s == progs[-1]:
        sys.stdout.write("Filling scripts"+"."*(progs.index(s)+1)+"\r\n")
        sys.stdout.flush()
guis = ("graphicPlot","pwa_controls","PWA_GUI","Control_List.npy")
for g in guis:    
    if g != guis[-1]:
        cmd = 'cp '+os.path.join(os.getcwd(),str(g))+" "+os.path.join(indir,"GUI")
        proc = Popen(cmd,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
        proc.wait()   
        sys.stdout.write("Filling GUI"+"."*(guis.index(g)+1)+"\r")
        sys.stdout.flush()
    elif g == guis[-1]:
        cmd = 'mv '+os.path.join(os.getcwd(),str(g))+" "+os.path.join(indir,"GUI")
        proc = Popen(cmd,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
        proc.wait()
        sys.stdout.write("Filling GUI"+"."*(guis.index(g)+1)+"\r\n")
        sys.stdout.flush() 
cmd = "mv "+indir+"/*.keyfile "+os.path.join(indir,"keyfiles")
procx = Popen(cmd,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
procx.wait()
print( "Filling keyfiles")
Waves = ["wave"+str(i) for i in range(len(os.listdir(os.path.join(indir,"keyfiles"))))]
if len(Waves) > 0:
    minInit = open(os.path.join(indir,"scripts","minInit.txt"),"w+")
    minInit.write("# Fill out each line. Leave defaults that you are happy with. Completely remove any value you will not be using.\n")
    for wave in Waves:
        minInit.write(wave+"_real=.01 fix_"+wave+"_real=False error_"+wave+"_real=.1 limit_"+wave+"_real=(-1000,1000)\n")
        minInit.write(wave+"_imag=.01 fix_"+wave+"_imag=False error_"+wave+"_imag=.1 limit_"+wave+"_imag=(-1000,1000)\n")
    minInit.close()
for fil in os.listdir(indir):
    if ".gamp" in fil:
        cmd = indir+"/scripts/massBinner2.py "+os.path.join(indir)+" "+os.path.join(indir,"fitting")+" "+str(fil).rstrip(".gamp")+" v"
        procx = Popen(cmd,shell = True,executable = os.environ.get('SHELL', '/bin/tcsh'),env = os.environ)
        procx.wait()
    
print("Welcome to PyPWA!\nYou are now ready to start Partial Wave Analysis!")
