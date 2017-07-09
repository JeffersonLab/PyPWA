import enum
from typing import Any, Dict, List
from typing import Optional as Opt

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import common

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ProcessCodes(enum.Enum):

    SHUTDOWN = 1
    ERROR = 2


class KernelProcessing(common.BasePlugin):

    def main_options(
            self,
            data,  # type: Dict[str, numpy.ndarray]
            process_template,  # type: Kernel
            interface_template  # type: KernelInterface
    ):
        # type: (...) -> None
        """
        The main options for the KernelProcessor, these are options that are
        typically needed for processing, but due to the design of the
        program, these options can't be passed directly to the processor
        via its __init__ method.

        :param dict data: A dictionary with values being numpy arrays, each
        key should be loaded into the processing template as a public
        variable.
        :param internals.Kernel process_template: A predefined kernel that
        holds all the logic and static data needed to calculate the
        provided function. This static data does not include events,
        but instead data that should be needed no matter the event being
        calculated. Ex. the value of π.
        :param internals.KernelInterface interface_template: The definition
        of how the return values should be calculated from the kernels.
        This could be a simple as a Sum, or as complicated as you could want.
        """
        raise NotImplementedError

    def fetch_interface(self):
        # type: () -> ProcessInterface
        """
        Returns the finished interface for the processing.

        :rtype: internals.ProcessInterface
        :return: Returns a finalized implementation to the processing
        kernel for the receiving object to use.
        """
        raise NotImplementedError


class ProcessInterface(object):

    def run(self, *args):
        # type: (*Any) -> Any
        """
        This function will start the processing of the processes, whatever was
        passed through the kernel will be started with this method.

        :param args: Anything that you want to pass to your kernel.
        :return: The value kernel interface.
        """
        raise NotImplementedError

    def stop(self, force=False):
        # type: (Opt[bool]) -> None
        """
        Should stop all process, threads, etc, that are being used to
        calculate.

        :param bool force: whether children should be stopped gently or
        violently murdered.
        """
        raise NotImplementedError

    @property
    def is_alive(self):
        # type: () -> bool
        """
        Should return whether the children are still alive or have been
        shutdown.

        :return: The state of the processes.
        :rtype: bool
        """
        raise NotImplementedError


class Kernel(object):

    # process_id should be set by the Kernel Processing plugin.
    PROCESS_ID = None  # type: int

    def setup(self):
        # type: () -> None
        """
        Anything that should be setup in the thread or process should be
        put here, this will be called only once before any calculation begins.
        """
        raise NotImplementedError()

    def process(self, data=False):
        # type: (Opt[Any]) -> Any
        """
        The actual calculation or function of the program, can optionally
        support values from the main thread / process.

        :param data: Any data that you want to pass to the kernel.
        :return: The final value or object that should be sent back to the
        main thread.
        """
        raise NotImplementedError()


class KernelInterface(object):

    # is_duplex controls whether the kernel will shutdown after its first
    # run or if the kernel will wait for more information. If this is false
    # the kernel will only be able to send data and will shutdown after
    # its first run; however, if this is true then the kernel will stay
    # running and waiting for a value from the interface indefinitely until
    # they are shutdown manually.
    IS_DUPLEX = False

    def run(self, communicator, args):
        # type: (List[Any], Any) -> Any
        """
        The method that will be called to begin the calculation. This is
        the interface between the kernels and the calling object.

        :param communicator: A list of objects that will be used to
        communicate with the kernels.
        :param args: Any values that are sent to the main interface.
        :return: Whatever value that is calculated locally from the kernels.
        """
        raise NotImplementedError("The run method must be extended!")
