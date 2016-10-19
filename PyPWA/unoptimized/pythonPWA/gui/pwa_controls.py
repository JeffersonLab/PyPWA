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

import Tkinter as tk
import numpy

from PyPWA.unoptimized.pythonPWA.batchFarmServices.graphicHelp import Help
from PyPWA import VERSION, STATUS, LICENSE

__author__ = ["Joshua Pond"]
__credits__ = ["Joshua Pond", "Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Control(object):
    """
        This program is the pwa_controls GUI, or the gui the user uses to
        specify environment variables for PyPWA.
    """

    def __init__(self,
                 reactMode = 24,
                 BeamPole = 0.4,
                 LoMass = 1000,
                 UpMass = 2500,
                 RaMass = 20,
                 NumSet = 20,
                 MigNcal = 1000,
                 reactNm = None,
                 pltLstNm = None,
                 project = None):

        self.reactModeL = reactMode
        self.BeamPoleL = BeamPole
        self.UpMassL = UpMass
        self.LoMassL = LoMass
        self.RaMassL = RaMass
        self.NumSetL = NumSet
        self.MigNcalL = MigNcal
        self.reactNmL = reactNm
        self.pltLstNmL = pltLstNm
        self.project = project

    def reactMode(self):
        rM = ent0.get()
        self.reactModeL = rM

    def BeamPole(self):
        Bp = ent1.get()
        self.BeamPoleL = Bp

    def LoMass(self):
        Lm = ent2.get()
        self.LoMassL = Lm

    def UpMass(self):
        Um = ent3.get()
        self.UpMassL = Um

    def RaMass(self):
        Rm = ent4.get()
        self.RaMassL = Rm

    def NumSet(self):
        Ns = ent5.get()
        self.NumSetL = Ns

    def MigNcal(self):
        MnC = ent6.get()
        self.MigNcalL = MnC

    def reactNm(self):
        rNm = ent7.get()
        self.reactNmL = rNm

    def pltLstNm(self):
        plN = ent8.get()
        self.pltLstNmL = plN

    def projNm(self):
        prN = ent9.get()
        self.project = prN

    def run(self):
        self.reactMode()
        self.BeamPole()
        self.LoMass()
        self.UpMass()
        self.RaMass()
        self.NumSet()
        self.MigNcal()
        self.reactNm()
        self.pltLstNm()
        self.projNm()

    def load(self,Con):
        self.reactModeL = Con[0]
        self.BeamPoleL = Con[1]
        self.LoMassL = Con[2]
        self.UpMassL = Con[3]
        self.RaMassL = Con[4]
        self.NumSetL = Con[5]
        self.MigNcalL = Con[6]
        self.reactNmL = Con[7]
        self.pltLstNmL = Con[8]
        self.project = Con[9]

        ent0.insert("end",Con[0])
        ent1.insert("end",Con[1])
        ent2.insert("end",Con[2])
        ent3.insert("end",Con[3])
        ent4.insert("end",Con[4])
        ent5.insert("end",Con[5])
        ent6.insert("end",Con[6])
        ent7.insert("end",Con[7])
        ent8.insert("end",Con[8])
        ent9.insert("end",Con[9])

    def save(self):
        self.run()
        Con = [int(self.reactModeL),
                float(self.BeamPoleL),
                int(self.LoMassL),
                int(self.UpMassL),
                int(self.RaMassL),
                int(self.NumSetL),
                int(self.MigNcalL),
                self.reactNmL,
                self.pltLstNmL,
                self.project]
        numpy.save(os.getcwd()+"/Control_List.npy",Con)
        root.destroy()

    def help_window(self):
        window = tk.Toplevel(root)
        window.wm_title("HELP")
        tx = Help()
        label = tk.Label(window, text=tx.CFhelp)
        label.pack(side="top", fill="both", padx=10, pady=10)


Lst = [
    'Reaction Mode ',
    'Beam Polarization ',
    'Lower Mass ',
    'Upper Mass ',
    'Mass Range ',
    'Number of Sets ',
    'Max Number of Migrad Calls ',
    'Name of tested Reaction',
    'Name of saved plotting data',
    'Batch Farm project name'
    ]

Contr = Control()

root = tk.Tk()
root.wm_title("PWA CONTROLS")

frame=tk.Frame(root)
frame.grid(row=0,column=0,sticky="N"+"S"+"E"+"W")

L0=tk.Label(frame,text=Lst[0])
L0.pack(side="top")

ent0=tk.Entry(frame, width=30, font=55)
ent0.pack(side="top")

L1=tk.Label(frame,text=Lst[1])
L1.pack(side="top")

ent1=tk.Entry(frame, width=30, font=55)
ent1.pack(side="top")

L2=tk.Label(frame,text=Lst[2])
L2.pack(side="top")

ent2=tk.Entry(frame, width=30, font=55)
ent2.pack(side="top")

L3=tk.Label(frame,text=Lst[3])
L3.pack(side="top")

ent3=tk.Entry(frame, width=30, font=55)
ent3.pack(side="top")

L4=tk.Label(frame,text=Lst[4])
L4.pack(side="top")

ent4=tk.Entry(frame, width=30, font=55)
ent4.pack(side="top")

L5=tk.Label(frame,text=Lst[5])
L5.pack(side="top")

ent5=tk.Entry(frame, width=30, font=55)
ent5.pack(side="top")

L6=tk.Label(frame,text=Lst[6])
L6.pack(side="top")

ent6=tk.Entry(frame, width=30, font=55)
ent6.pack(side="top")

L7=tk.Label(frame,text=Lst[7])
L7.pack(side="top")

ent7=tk.Entry(frame, width=30, font=55)
ent7.pack(side="top")

L8=tk.Label(frame,text=Lst[8])
L8.pack(side="top")

ent8=tk.Entry(frame, width=30, font=55)
ent8.pack(side="top")

L9=tk.Label(frame,text=Lst[9])
L9.pack(side="top")

ent9=tk.Entry(frame, width=30, font=55)
ent9.pack(side="top")

frame1=tk.Frame(frame)
frame1.pack(side="top")

btnS=tk.Button(frame1, text="SAVE", command= lambda: Contr.save())
btnS.grid(row=0,column=0,sticky="N"+"S"+"E"+"W")

btnH=tk.Button(frame1,text="HELP",command=lambda: Contr.help_window())
btnH.grid(row=0,column=1,sticky="N"+"S"+"E"+"W")

if os.path.isfile(os.getcwd()+"/Control_List.npy"):
    Con = numpy.load(os.getcwd()+"/Control_List.npy")
    Contr.load(Con)

root.mainloop()



