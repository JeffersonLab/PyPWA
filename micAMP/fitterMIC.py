#!/usr/bin/which python
import numpy
import PyPWA.proc.calculation_tools
import ctypes
from ctypes import *
the_lib = ctypes.cdll.LoadLibrary("/home/mvick/PyPWA/Xeon Phi/libIM.so")

the_lib.argtypes = ctypes.c_double
the_lib.LogLike_.restype = ctypes.c_double

set_up = .5
initial_settings = { "p": -9.0 }
parameters = ["p"]
strategy = 0
ncall = 1000

the_lib.Initialize()


def likelihood_Wrapper(parameter):
	something = -numpy.float64(the_lib.LogLike_(ctypes.c_double(parameter)))
	print ("parameter = " + str(parameter) + " loglike = " + str(something))
	return something

minimization = PyPWA.proc.calculation_tools.Minimizer(likelihood_Wrapper,
												 parameters, initial_settings, 
												 strategy, set_up, ncall)
												 

minimization.min()

print(minimization.covariance)
#for i in range(60):
#likelihood_Wrapper(i/3.0-10)
