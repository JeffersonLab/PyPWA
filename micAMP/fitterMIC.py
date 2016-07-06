#!/usr/bin/which python
import numpy
import PyPWA.proc.calculation_tools
import ctypes
import os

the_lib = ctypes.cdll.LoadLibrary(os.getcwd() + "libIM.so")

the_lib.argtypes = ctypes.c_double
the_lib.LogLike_.restype = ctypes.c_double

set_up = .5
initial_settings = {"p": -9.0}
parameters = ["p"]
strategy = 0
ncall = 1000

the_lib.Initialize()


def likelihood_wrapper(parameter):
    likelihood = -numpy.float64(
        the_lib.LogLike_(ctypes.c_double(parameter))
    )

    print("parameter = {0} loglike = {1}".format(
        str(parameter), str(likelihood)
    ))

    return likelihood

minimization = PyPWA.proc.calculation_tools.Minimizer(
    likelihood_wrapper, parameters, initial_settings,
    strategy, set_up, ncall
)

minimization.min()

print(minimization.covariance)