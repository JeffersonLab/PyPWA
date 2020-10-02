======================
Simulation and Fitting
======================

PyPWA defines both the monte carlo simulation method as well as the
several likelihoods. To use these, the cost function or amplitude needs
to be defined in a support object.

* :ref:`Defining an Amplitude<amplitude>` describes how to define a
  function for use with the simulation and likelihoods.
* :ref:`Simulating<simulation>` describes the Monte Carlo Simulation
  methods.
* :ref:`Likelihoods<likelihoods>` describes the built in likelihoods.
  These likelihoods also automatically distribute the fitting function
  across several processors.
* :ref:`Fitting<fitting>` describes the built in minuit wrapper, as well
  as how to use the Likelihood objects with other optimizers.


.. _amplitude:

Defining an Amplitude
---------------------

Amplitudes or cost functions can be defined for using either an Object
Oriented approach, or a Functional programming approach. If using pure
functions for the function, wrap the calculation function and optional
setup function in `PyPWA.FunctionalAmplitude`, if using the OOP approach,
extend the `PyPWA.NestedFunction` abstract class when defining the
amplitude.

It is assumed by both the Likelihoods and Monte Carlo that the calculate
functions of either methods will return a standard numpy array of final
values.

.. autoclass:: PyPWA.NestedFunction
   :members:

.. autoclass:: PyPWA.FunctionAmplitude
   :members:


.. _simulation:

Simulating
----------

There are two choices when using the Monte Carlo Simulation method
defined in PyPWA: Simulation in one pass producing the rejection list,
or simulation in two passes to produce the intensities and finally the
rejection list. Both methods will take advantage of SMP where available.

* If doing a single pass, just use the `PyPWA.monte_carlo_simulation`
  function. This will take the fitting function defined from
  :ref:`Defining an Amplitude<amplitude>` along with the data, and return
  a single rejection list.
* If doing two passes for more control over when the intensities and
  rejection list, use both `PyPWA.simulate.process_user_function` to
  calculate the intensity and local max value, and
  `PyPWA.simulate.make_rejection_list` to take the global max value and
  local intensity to produce the local rejection list.

.. autofunction:: PyPWA.monte_carlo_simulation
.. autofunction:: PyPWA.simulate.process_user_function
.. autofunction:: PyPWA.simulate.make_rejection_list


.. _likelihoods:

Likelihoods
-----------

PyPWA supports 3 unique likelihood types for use with either the Minuit
wrapper or any optimizer that expects a function. All likelihoods have
built in support for SMP when they're called, and require to be closed
when no longer needed.

* `PyPWA.LogLikelihood` defines the likelihood, and works with either
  the standard log likelihood, the binned log likelihood, or the extended
  log likelihood.
* `PyPWA.ChiSquared` defines the ChiSquared method, supporting both the
  binned and standard ChiSquare.
* `PyPWA.EmptyLikelihood` does no post operation on the final values
  except sum the array and return the final sum. This allows for defining
  unique likelihoods that have not already been defined, fitting functions
  that do not require a likelihood, or using the builtin multi  processing
  without the weight of a standard likelihood.

.. autoclass:: PyPWA.LogLikelihood
   :members:

.. autoclass:: PyPWA.ChiSquared
   :members:

.. autoclass:: PyPWA.EmptyLikelihood
   :members:


.. _fitting:

Fitting
-------

PyPWA supplies a single wrapper around iMinuit's module. This is a
convenience function to make working with Minuit's parameters easier.
However, if wanting to use a different fitting function, like Scikit or
Scipy, the likelihoods should work natively with them.

Most optimizers built in Python assume the data is some sort of global
variable, and the function passed to them is just accepting parameters
to fit against. The Likelihoods take advantage of this by wrapping the
data and the defined functions a wrapper that attempts to scale the
function to several processors, while providing function-like capabilities
by taking advantage of Python's builtin `__call__` magic function.

This should allow the likelihoods to work with any optimizer, as long as
they're expecting a function or callable object, and as long as the
parameters they pass are pickle-able.

.. autofunction:: PyPWA.minuit
