"""
Entry point for console GeneralShell
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"
from PyPWA.libs.wrappers import StartBuilder


@StartBuilder()
def likelihood_fitting(*args):
    description = u"""Amplitude Fitting using the Likelihood Estimation Method."""
    configuration = {
        "Description": description,
        "Calculation": example.example,
        "Configuration": example.example,
        "Python File": example.example,
        "AdvancedHelp": False,
        "Extras": args
    }
    return configuration


@StartBuilder()
def simulator(*args):
    description = u"""Simulation using the the Acceptance Reject Method"""
    configuration = {
        "Description": description,
        "Calculation": example.example,
        "Configuration": example.example,
        "Python File": example.example,
        "AdvancedHelp": False,
        "Extras": args
    }
    return configuration


@StartBuilder()
def intensities(*args):
    description = u"""Generates the Intensities for Rejection Method"""
    configuration = {
        "Description": description,
        "Calculation": example.example,
        "Configuration": example.example,
        "Python File": example.example,
        "AdvancedHelp": False,
        "Extras": args
    }
    return configuration


@StartBuilder()
def rejection_method(*args):
    description = u"""Takes generated intensities to run through the Rejection Method"""
    configuration = {
        "Description": description,
        "Calculation": example.example,
        "Configuration": example.example,
        "Python File": example.example,
        "AdvancedHelp": False,
        "Extras": args
    }
    return configuration


@StartBuilder()
def chi_squared(*args):
    description = u"""Amplitude Fitting using the ChiSquared Method"""
    configuration = {
        "Description": description,
        "Calculation": example.example,
        "Configuration": example.example,
        "Python File": example.example,
        "AdvancedHelp": False,
        "Extras": args
    }
    return configuration
