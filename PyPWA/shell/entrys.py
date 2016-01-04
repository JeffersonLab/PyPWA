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
from PyPWA.libs.wrappers import start_builder


@start_builder
def likelihood_fitting():
    pass


@start_builder
def simulator():
    pass


@start_builder
def intensities():
    pass


@start_builder
def chi_squared():
    pass
