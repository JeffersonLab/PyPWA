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

Reaction mode is the mode for generateAlphas:
8 = p pi+ pi- pi0
22 = p p+ p-
24 = p k+ k-
42 = gamma p --> p Ks Ks 
(pi+ pi- pi+ pi-)eta pi n

Beam polarization is an important value for some 
experiments. It must be a float value!
No polarization = 0.0

The Upper, lower, and range of the mass are inclusive 
and will affect binning.

Sets is almost never used.
Put 0

The number of Migrad calls should be at least 1000, 
but any more will depend on other factors, like 
number of events and waves.

Name of tested reaction should just be a quick title,
possibly the same as the top directory of the project. 
It will be used as the title of graphs made by 
graphicPlot.

Name of the saved data is the filename where graphicPlot
will save the CURRENT data loaded to it and where it will
look to load already saved data, they are all saved inside 
/GUI/plotLists. Change this as often as you need to make 
as many different sets of data and to view different sets 
of data by using the pwa_controls button on the graphicPlot 
button panel. But if you update anything and save over an
old file, then the old data will be lost.

Press save when done.

Saved values will be loaded
next time.
 
"""

        self.PWAGhelp = """











"""
