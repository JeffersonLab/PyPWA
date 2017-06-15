"""
.. module:: batchFarmServices
   :platform: Unix, Windows, OSX
   :synopsis: Utilities for doing PWA with the Jlab batch system.

.. moduleauthor:: Joshua Pond <jpond@jlab.org>


""" 
class Help(object):
    
    def __init__(self):
        
        self.GPhelp ="""
GraphicPlot Help.

When the dashboard opens for the first time, or
if the file name specified in pwa_controls does
not exist the display will read that there isn't 
a saved list and that all the data will have to be 
updated to plot.

Hit pwa Controls and make sure that all the 
information there is correct. The last two 
are the only ones that will affect plotting.

1st: Hit Update All and wait for the display
    to read "PlotList updated."

2nd: Hit save and wait for the dashboard to 
    update with the individual wave buttons.

3rd: Hit any and all buttons for what you 
    would like to plot and then hit plot.

    You do not need to close the graph before
    plotting again. Plot as many graphs as you
    like.

The data will be automatically loaded if the .npy
file specified in pwa_controls exists, which will be 
indicated by the display. Start with step 3.

 """

        self.CFhelp = """
pwa_controls Help.

Fill in all entry boxes.

THERE ARE NO DEFAULT VALUES

Reaction mode [int] (as ppgen) identify reaction for generateAlphas:
(current supported)
5:gamma p -> K+ Ks pi- p
6:gamma p -> n pi+
7:gamma p -> pi+ pi+ pi- n
8:gamma p -> pi+ pi- pi0 p 
9:gamma p -> pi0 p 
15:gamma p -> e+ e- p
21:beam p -> pi+ pi- eta p 
22:beam p -> pi+ pi- p 
23:beam p -> pi+ pi+ pi-  (p,n) 
24:beam p -> K+ K- p 
25:beam p -> (pbar p) p 
26:beam p -> eta' pi p
27:beam p -> pi+ pi- pi-  (p,n) 
29:beam p -> K+ K- pi+  (p,n) 
30:beam p -> phi eta  (p,n) 
31:beam p -> K+ (K- p) 
32:beam p -> pi+ (pi- p) 
33:beam p -> pi- (pi+ p) 
34:beam p -> K+ Kl n 
41:beam p -> p pi0 eta 
42:beam p -> Kshort (-> pi+ pi-) KL p
43:beam p -> phi omega p

Beam polarization [float]: Fraction of Linear Polearization
No polarization = 0.0, full = 1.0

Angle of polarization [float] (in degrees): Angle of vector Polarization from
the x axis (Parallel to lab floor) PARA=0,PERP=90 

The Upper [int], lower [int], and range [int] of a mass bin (in MeV).
The number of mass bins will be then: (Upper-lower)/range

Frame Definition [sting]: The frame where to generate the resonance:
 GJ (Godfried-Jackson), HEL (Helicity), AD (Adair)

Sets is almost never used [int] (in case the MC has been divided in sets).
Put 0

In Minuit: The max number of Migrad calls should be at least 1000 [int], 
but any more will depend on other factors, like 
number of events and waves.

Name of tested reaction should just be a quick title,
possibly the same as the top directory of the project. 
It will be used as the title of graphs made by 
graphicPlot. [string]

Name for saved data (mostly same as before) It is the filename 
where graphicPlot will save the CURRENT data loaded to it and where 
it will look to load already saved data, they are all saved inside 
/GUI/plotLists. Change this as often as you need to make 
as many different sets of data and to view different sets 
of data by using the pwa_controls button on the graphicPlot 
button panel. But if you update anything and save over an
old file, then the old data will be lost. [string]

Project: CLAS or GlueX [string]


Press save when done.

Saved values will be loaded
next time.
 
"""

        self.PWAGhelp = """











"""
