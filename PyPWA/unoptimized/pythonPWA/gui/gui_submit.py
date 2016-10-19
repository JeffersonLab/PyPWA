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

import Tkinter as tk

import os
import subprocess

from PyPWA import LICENSE, STATUS, VERSION

__author__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__credits__ = ["Brandon Kaleiokalani DeMello", "Mark Jones"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


scriptOutDir = os.path.join(os.getcwd(), "subMCs")
binSize = int(input("bin width?: "))
maxEvents = int(input("max number of _events?: "))
i = int(input("Enter i value: "))
submitted = []


def submit(jlab_submission_file):
    cmd = 'jsub '+str(jlab_submission_file)
    process = subprocess.Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    process.wait()
    
def gen(directory,cmd):

    auger_opts = dict(
                    project = 'gluex',
                    track = 'simulation',
                    jobname = 'runMC',
                    os = 'centos62',
                    time = 2880,
            memory = '3000 MB',
            disk_space = '5000 MB',
                    cmd = cmd)

    jsub_filename = os.path.join(scriptOutDir,"subMC_"+directory)
    jsub_file = open(jsub_filename,'w')

    jsub_file.write('''\
PROJECT:{project}
TRACK:{track}
JOBNAME:{jobname}
OS:{os}
TIME:{time}
MEMORY:{memory}
DISK_SPACE:{disk_space}
COMMAND:{cmd}
'''.format(**auger_opts))

    jsub_file.close()
    return jsub_filename


def parseDir(directory):
    Bin=directory.strip("_MeV")
    L=float(Bin)/1000.
    U=L+(binSize/1000.)
    gampName=directory+".gamp"
    gampPath=os.path.join(os.getcwd(),"MC",directory,".")

    cmd = "/home/salgado/TESTMC/gluex/MC.sh" + " " + str(L) + " " + str(
        U) + " " + gampName + " " + gampPath + " " + str(i) + " "+str(
        maxEvents)

    return cmd


def All(list):
    for d in sorted(os.listdir(os.path.join(os.getcwd(),"MC"))):
        if not d.isalpha():
            list.extend([str(d)])


def Clear(list):
    del list[0:len(list)]


def Delete(list):
    del list[len(list)-1]    	
    

class Application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent        
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        frame = tk.Frame(self)
        frame1 = tk.Frame(self)
        frame2 = tk.Frame(self)
        text = tk.Text(self, width = 72, font=12)
        frame.pack(side = "left")
        frame1.pack(side = "left")
        frame2.pack(side = "left")
        text.pack(side = "top")
        root.wm_title("GUI SUBMIT")
        for d in sorted(os.listdir(os.path.join(os.getcwd(),"MC"))):
            if not d.isalpha():  	
                if int(d.strip("_MeV")) < 1520: 
                    add = tk.Button(frame)
                add["text"] = "add "+str(d)
                add["command"] = lambda d=d: submitted.extend([str(d)])
                add.pack(side="top", fill="both")
        for d in sorted(os.listdir(os.path.join(os.getcwd(),"MC"))):
            if not d.isalpha():
                if int(d.strip("_MeV")) > 1500 and int(d.strip("_MeV")) < 2020: 
                    add = tk.Button(frame1)
                add["text"] = "add "+str(d)
                add["command"] = lambda d=d: submitted.extend([str(d)])
                add.pack(side = "top", fill = "both")
        for d in sorted(os.listdir(os.path.join(os.getcwd(),"MC"))):
            if not d.isalpha():
                if int(d.strip("_MeV")) > 2000 and int(d.strip("_MeV")) < 2520: 
                    add = tk.Button(frame2)
                add["text"] = "add "+str(d)
                add["command"] = lambda d=d: submitted.extend([str(d)])
                add.pack(side = "top", fill = "both")
      
        self.All = tk.Button(
            self, text="ALL", fg="purple", command=lambda: All(submitted)
        )

        self.Clear = tk.Button(
            self, text="CLEAR"+"\n"+"LIST", fg="red",
            command=lambda: Clear(submitted)
        )

        self.Delete = tk.Button(
            self, text="DELETE"+"\n"+"LAST", fg="brown",
            command=lambda: Delete(submitted)
        )

        self.Print = tk.Button(
            self, text="PRINT", fg="blue",
            command=lambda: text.insert(
                "end","\n"+"i= "+str(i)+"\n"+str(submitted)
            )
        )

        self.Reset_Text = tk.Button(
            self, text="CLEAR"+"\n"+"TEXT", fg="orange",
            command=lambda: text.delete("0.0wordstart", "end")
        )

        self.QUIT = tk.Button(
            self, text="DONE", fg="green",
            command=root.destroy
        )


        self.All.pack(side = "left", fill = "both")       
        self.Delete.pack(side="left", fill = "both")
        self.Clear.pack(side="left", fill = "both")
        self.Reset_Text.pack(side="left", fill = "both")
        self.Print.pack(side = "left", fill = "both")       
        self.QUIT.pack(side="left", fill = "both")
        


root = tk.Tk()
app = Application(parent=root)
app.mainloop()

if __name__ == '__main__':

    A = str(raw_input("Submit these? (y/n) "))    
    if A.lower() == "y":		
        for d in submitted:
            print("Processing bin",d)
            submit(gen(d,parseDir(d)))
    else:
        print("Terminated")


