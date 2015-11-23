"""
.. module:: pythonPWA.dataTypes
   :platform: Unix, Windows, OSX
   :synopsis: Various data types used within the PWA project.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
class wave():
    """
    This class represents a PWA wave.
    """
    def __init__(self,
                 epsilon=0,
                 complexamplitudes=[],
                 w0=1000.,
                 r0=100.,
                 beta=0,
                 k=0,
                 filename=None):
        
        """
        Default constructor for the wave class

        Kwargs:
        epsilon (int): Integer representing reflectivity of this wave.
        beta (int):
        k (int):
        filename (string): Name of the file used to instantiate a wave instance, if getwaves was used to instantiate the wave instance.
        """
        self.epsilon=epsilon
        self.complexamplitudes=complexamplitudes
        self.beta=beta
        self.k=k
        self.filename=filename

    def toString(self):
        """
        returns a string of all the wave properties delimited by newlines.
        """
        return "\n".join(["epsilon="+str(self.epsilon),"len(complexamplitudes)="+str(len(self.complexamplitudes)),"beta="+str(self.beta),"k="+str(self.k)])