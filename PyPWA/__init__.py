"""
__init__ for PyPWA Package
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

"""
PyPWA is an attempt to have a set multiprocessing tools to easy the
Partial Wave Analysis process.

Current there is a multiprocessing tool for both the Acceptance
Rejection Model, and the Maximum-Likelihood Estimation for fitting.

The tools work with Kinematic Variables defined in standard text files,
Comma Seperated Variables, and Tab Seperated Variables.

Example:
    For both the GeneralFitting and the GeneralSimulator you should
    first run [tool] -wc, ie:
        $ GeneralFitting -wc
    then afterwords modify and rename the Example.yml and Example.py
    files that are generated.
    Lastly to actually run the tool with your freshly created
    configuration file, run [tool] <configuration>.yml, ie:
        $ GeneralFitting Example.yml
"""
