import enum

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Types(enum.Enum):

    KERNEL_PROCESSING = 1
    OPTIMIZER = 2
    DATA_READER = 3
    DATA_PARSER = 4
    SKIP = 5


class BasePlugin(object):
    # Simply here for inheritance.
    pass


class Main(BasePlugin):

    def start(self):
        # type: () -> None
        """
        This is the method that should start the execution on the main object.
        It is assumed that basic setup of the program has been done by this
        point, and this should simply start the function of the program.
        """
        raise NotImplementedError
