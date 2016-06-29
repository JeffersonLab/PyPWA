"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
import Tkinter as tk
import os, glob, shutil
from subprocess import Popen


scriptOutDir=os.path.join(os.getcwd(),"subMCs")
binSize=int(raw_input("bin width?: "))
maxEvents=int(raw_input("max number of events?: "))
i=int(raw_input("Enter i value: "))
submitted = []

def submit(jsub_file):
    cmd = 'jsub '+str(jsub_file)
    proc = Popen(cmd,
        shell = True,
        executable = os.environ.get('SHELL', '/bin/tcsh'),
        env = os.environ)
    proc.wait()
    
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

    cmd = "/home/salgado/TESTMC/gluex/MC.sh"+" "+str(L)+" "+str(U)+" "+gampName+" "+gampPath+" "+str(i)+" "+str(maxEvents)

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
                add.pack(side = "top", fill = "both")
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
      
        self.All = tk.Button(self, text="ALL", fg="purple", command=lambda: All(submitted))        
        self.Clear = tk.Button(self, text="CLEAR"+"\n"+"LIST", fg="red", command=lambda: Clear(submitted))
        self.Delete = tk.Button(self, text="DELETE"+"\n"+"LAST", fg="brown", command=lambda: Delete(submitted))	
        self.Print = tk.Button(self, text="PRINT", fg="blue", command=lambda: text.insert("end","\n"+"i= "+str(i)+"\n"+str(submitted)))
        self.Reset_Text = tk.Button(self, text="CLEAR"+"\n"+"TEXT", fg="orange", command=lambda: text.delete("0.0wordstart", "end"))
        self.QUIT = tk.Button(self, text="DONE", fg="green", command=root.destroy)

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


