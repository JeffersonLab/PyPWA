"""
.. module:: pythonPWA.dataTypes
   :platform: Unix, Windows, OSX
   :synopsis: Various data types used within the PWA project.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
class gampParticle():
    """
    This class represents a particle described in a single line of a 
    .gamp file.
    """
    def __init__(self,
                 particleID=None,
                 particleCharge=None,
                 particleXMomentum=None,
                 particleYMomentum=None,
                 particleZMomentum=None,
                 particleE=None):
        """
        gampParticle class default constructor.
        
        Kwargs:
        particleID (int): Key used to lookup the type of this particle.
        particleCharge (float): The electric charge value of this particle.
        particleXMomentum (float): X-direction momentum of this particle.
        particleYMomentum (float): Y-direction momentum of this particle.
        particleZMomentum (float): Z-direction momentum of this particle.
        particleE (float): Total energy of this particle.
        """
        self.particleID=particleID
        self.particleCharge=particleCharge
        self.particleXMomentum=particleXMomentum
        self.particleYMomentum=particleYMomentum
        self.particleZMomentum=particleZMomentum
        self.particleE=particleE
    
    def toString(self):
        """
        Returns a string of the particle data members delimited by newlines.
        """
        return " ".join([str(self.particleID),str(self.particleCharge),str(self.particleXMomentum),str(self.particleYMomentum),str(self.particleZMomentum),str(self.particleE)])