"""
.. module:: pythonPWA.utilities
   :platform: Unix, Windows, OSX
   :synopsis: Module containing various useful scripts.

.. moduleauthor:: Brandon Kaleiokalani DeMello <bdemello@jlab.org>


"""
import random

def randm(low,high):
    """
    Returns a random value, used in generatePureWave.

    Args:
    low (float)
    high (float)

    Returns:
    Random value as a float.
    """
    return ((high-low)*random.random()+low)