import os
import numpy

import subprocess

"""
This program is the first step for the PyPWA fitting process. It sets up
all directories and files needed for fitting as well as all binning in
mass as prescribed by the pwa_controls GUI.
"""

indir = os.path.split(os.path.split(os.getcwd())[0])[0]

if not os.path.isfile(os.path.join("Control_List.npy")):
    subprocess.call(os.path.abspath("pwa_controls"))

Control = numpy.load(os.path.join("Control_List.npy"))
print("Creating directory structure for PyPWA fitting")
top_dirs = ("fitting", "GUI", "keyfiles", "scripts")

for dir in top_dirs:
    directoryBuffer = os.path.join(indir, str(dir))
    os.makedirs(directoryBuffer)
    if dir == "fitting":
        for d in ("overflow", "results"):
            directoryBuffer = os.path.join(indir, "fitting", str(d))
            os.makedirs(directoryBuffer)
    if dir == "GUI":
        directoryBuffer = os.path.join(indir, "GUI", "plotLists")
        os.makedirs(directoryBuffer)
    if dir == "scripts":
        directoryBuffer = os.path.join(indir, "scripts", "submitions")
        os.makedirs(directoryBuffer)

programs = (
    "fnGenerator.py",
    "generateAlphaNPY.py",
    "GUI_alpha_main.py",
    "GUI_gamp_main.py",
    "GUI_subPyNormInt.py",
    "likelihoodTest.py",
    "mvBAMP_GUI",
    "run_normintFARM.py",
    "subLikelihood",
    "subWalkNTrue",
    "walkingNTrue.py",
    "massBinner2.py"
)

for program in programs:
    command = 'cp ' + os.path.join(os.getcwd(), str(program)) + " " + os.path.join(indir, "scripts")
    process = subprocess.Popen(
        command, shell=True,
        executable=os.environ.get('SHELL', '/bin/tcsh'),
        env=os.environ
    )

    process.wait()

graphical_interface = (
    "graphicPlot",
    "pwa_controls",
    "PWA_GUI",
    "Control_List.npy"
)

for interface in graphical_interface:
    if interface != graphical_interface[-1]:
        command = 'cp ' + os.path.join(os.getcwd(), str(interface)) + " " + os.path.join(indir, "GUI")
        process = subprocess.Popen(command, shell=True, executable=os.environ.get('SHELL', '/bin/tcsh'), env=os.environ)
        process.wait()
    elif interface == graphical_interface[-1]:
        command = 'mv ' + os.path.join(os.getcwd(), str(interface)) + " " + os.path.join(indir, "GUI")
        process = subprocess.Popen(command, shell=True, executable=os.environ.get('SHELL', '/bin/tcsh'), env=os.environ)
        process.wait()

command = "mv " + indir + "/*.keyfile " + os.path.join(indir, "keyfiles")
procx = subprocess.Popen(command, shell=True, executable=os.environ.get('SHELL', '/bin/tcsh'), env = os.environ)
procx.wait()

Waves = ["wave" + str(i) for i in range(len(os.listdir(os.path.join(indir, "keyfiles"))))]

if len(Waves) > 0:
    minInit = open(os.path.join(indir, "scripts", "minInit.txt"), "w+")
    minInit.write("# Fill out each line. Leave defaults that you are happy with. Completely remove any value you will not be using.\n")
    for wave in Waves:
        minInit.write(wave + "_real=.01 fix_" + wave + "_real=False error_" + wave + "_real=.1 limit_" + wave + "_real=(-1000,1000)\n")
        minInit.write(wave + "_imag=.01 fix_" + wave + "_imag=False error_" + wave + "_imag=.1 limit_" + wave + "_imag=(-1000,1000)\n")
    minInit.close()

for fil in os.listdir(indir):
    if ".gamp" in fil:
        command = indir + "/scripts/massBinner2.py " + os.path.join(indir) + " " + os.path.join(indir, "fitting") + " " + str(fil).rstrip(".gamp") + " v"
        procx = subprocess.Popen(command, shell=True, executable=os.environ.get('SHELL', '/bin/tcsh'), env=os.environ)
        procx.wait()
