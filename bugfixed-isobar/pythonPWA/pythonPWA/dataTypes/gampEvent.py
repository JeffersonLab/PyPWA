"""
.. module:: pythonPWA.dataTypes
   :platform: Unix, Windows, OSX
   :synopsis: Various data types used within the PWA project.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
class gampEvent():
    """
    This class represents a single gamp event.  That is to say that
    this class contains a set of particles and a flag to specify if
    this event is accepted into the filtered data set.
    """
    def __init__(self,
                 particles=[],
                 accepted=None,
                 raw=None):
        """
        gampEvent class default constructor.
        
        Kwargs:
        particles (list): A list of gampParticle items.
        accepted (bool): Flag to denote if the gampEvent instance is accepted.
        raw (bool): Flag to denote if the gampEvent instance is raw.

        """
        self.particles=particles
        self.raw=raw
        self.accepted=accepted
        
    def writeGamp(self,outputFile):
        """
        This function writes a gamp event instance to an output file.

        Args:
        outputFile (file):  Output .gamp file to write the event instance to.
        """
        outputFile.write(str(len(self.particles))+"\n")
        for particle in self.particles:
            outputFile.write(particle.toString())

    def writeGampIfAccepted(self,outputFile):
        """
        This function writes a gamp event instance to an output file,
        but only if the accepted data member of said gamp event instance
        is True.

        Args:
        outputFile (file):  Output .gamp file to write the event instance to.
        """
        if self.accepted==True:
            self.writeGamp(outputFile)