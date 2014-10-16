import matplotlib.pyplot as plt

class plotter():
    """
    A very simple plotting shortcut.  Simply initialize the plotter by
    providing the desired data sets and labels.
    """
    def __init__(self,
                 xAxisData=[1,2,3,4,5],
                 yAxisData=[1,2,3,4,5],
                 title="",
                 xAxisTitle="",
                 yAxisTitle=""):
        
        self.xAxisData=xAxisData
        self.yAxisData=yAxisData
        plt.plot(self.xAxisData,self.yAxisData)
        plt.suptitle(title)
        plt.xlabel(xAxisTitle)
        plt.ylabel(yAxisTitle)
        self.numberOfPlots=0
        self.colors=['b','g','r','c','m','y']

    def showPlot(self):
        """
        Show the plotted figure with all yAxis data sets.
        """
        plt.show()

    def addSubPlot(self,newYAxisData):
        """
        Allows you to add a new plot of newYAxisData vs self.xAxisData.
        Very handy if you want to check multiple functions values on the same
        data set.
        """
        if len(newYAxisData)==len(self.xAxisData):
            self.numberOfPlots+=1
            plt.plot(self.xAxisData,newYAxisData,color=self.colors[self.numberOfPlots])