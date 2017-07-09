import enum
from typing import Any, Callable
from typing import Optional as Opt

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import common

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class LikelihoodTypes(enum.Enum):
    OTHER = 1
    CHI_SQUARED = 2
    LOG_LIKELIHOOD = 3


class Optimizer(common.BasePlugin):

    def main_options(self, calc_function, fitting_type=None):
        # type: (Callable[[Any], Any], Opt[LikelihoodTypes]) -> None
        """
        The main options for the Optimizer, these are options that are
        typically needed for optimization, but due to the design of the
        program, these options can't be passed directly to the optimizer
        via its __init__ method.

        :param calc_function: The main runtime function for the program.
        This is often the likelihood, or amplitude, that needs to be
        optimized.
        :param internals.LikelihoodTypes fitting_type: One of the
        enumerations from likelihood types.
        """
        raise NotImplementedError

    def start(self):
        # type: () -> None
        """
        This should start all the actual processing and logic inside the
        optimizer, anything being started before this is called could cause
        an internal error.
        """
        raise NotImplementedError

    def return_parser(self):
        # type: () -> OptimizerOptionParser
        """
        Since each optimizer is different, and as such sends and receives
        its arguments in a different way, this provides the object that
        will attempt to 'normalize' these arguments to make interact with
        them more transparent.

        :rtype: internals.OptimizerOptionParser
        :return: An object that extended the option parsing interface that
        will convert the received parameters.
        """
        raise NotImplementedError

    def save_extra(self, save_name):
        # type: (str) -> None
        """
        Takes whatever information the optimizer found and saves it using
        the supplied save_name.

        :param str save_name: The name of the file to save to, or the
        template of the name depending on the optimizer. The optimizer
        doesn't have to save all information to the file name provided
        explicitly, and can instead do save along the lines of
        "save_name_covariance" for example.
        """
        raise NotImplementedError


class OptimizerOptionParser(object):

    # A simple multiplier that will be multiplied to the final result of
    # every run call.
    MULTIPLIER = 1

    def convert(self, passed_value):
        # type: (Any) -> Any
        """
        This should take any value sent by optimizer and clean up the value
        to something easier for the user to interact with if possible.

        :param passed_value: The object sent by the optimizer.
        :return: The cleaned up value.
        """
        raise NotImplementedError
