"""
GeneralFitting.py: The GeneralShell, provides users a flexible way of testing their calcutions
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Alpha"


class GeneralFitting(object):
    """
    Main point of entry into the General Shell, trying to stay as pythonic as possible.
    Tries to be both intelligent and provide a flexible way for users to do what they want how they want.
    """

    def __init__(self, config):
        """
        Actually runs all the data, not the best way of doing things but it works, functions as the main function of the program running all the other functions of the program.
        """

        with click.progressbar(length=6, label="Importing and Configuring GeneralFitting") as progress:
            self.config = config
            progress.update(1)
            self.data = PyPWA.lib.data.interface(self.config["data"])
            progress.update(2)
            self.calc = PyPWA.lib.calc.likelihood.calc(self.config["calc"])
            progress.update(3)
            self.calc.parameters = self.config["general"]["Minuit Parameters"]
            progress.update(4)
            self.data.config["Use QFactor"] = self.config["general"]["Use QFactor"]
            progress.update(5)
            self.calc.config["Number of Threads"] = self.config["general"]["Number of Threads"]
            progress.update(6)

        print("Begining Parseing")
        self.parser()
        print("Begining Calculation")
        self.minimalization()

    def parser(self):
        """
        This parses all the events into an variable, all actual parsing is done in the defined class
        """
        print("Loading events for processing.")
        self.data.parse("data")
        self.calc.kvar_data = self.data.values
        self.data.parse("accepted")
        self.calc.kvar_accepted = self.data.values
        self.data.parse("qfactor")
        if len(self.calc.kvar_data) == len(self.data.values):
            self.calc.qfactor = self.data.values
        else:
            #raise RuntimeWarning("QFactor is not the same lengh as kvar data")
            self.calc.qfactor = 1
    