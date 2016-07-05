"""
.. module:: pythonPWA.dataTypes
   :platform: Unix, Windows, OSX
   :synopsis: Various data types used within the PWA project.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
class resonance():
    """
    This class represents a resonance.
    """
    def __init__(self,
                 cR=1.0,
                 wR=[],
                 w0=1.,
                 r0=.5,
                 phase=0.):
        """
        Default constructor for resonance class.

        Kwargs:
        cR (float):
        wR (list):
        w0 (float):
        r0 (float):
        phase (float):
        """
        self.wR=wR
        self.cR=cR
        self.w0=w0
        self.r0=r0
        self.phase=phase

    def toString(self):
        """
        Returns a string of the resonance data memebers delimited by newlines.
        """
        return "\n".join(["wR="+str(self.wR),"cR="+str(self.cR),"w0="+str(self.w0),"r0="+str(self.r0)])