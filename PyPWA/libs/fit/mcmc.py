from typing import Any as _Any, Callable as _Call, List as _List

import numpy as np

from PyPWA import info as _info
from PyPWA.libs.fit import likelihoods as _likelihoods

try:
    import emcee as _emcee
except ImportError:
    raise ImportError("Emcee must be installed!")

# modelled after minuit.py

__credits__ = ["Peter Pauli"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class _Translator:

    def __init__(
            self, parameters: _List[str],
            parameterlimits: _List[str],
            function_call: _Call[[_Any], float],
            prior: _Call[[_Any, _List[str]], float]
    ):
        self.__parameters = parameters
        self.__parameter_limits = parameterlimits
        self.__function = function_call
        self.__prior = prior

    def __call__(self, args: _List[float]) -> float:
        parameters_with_values = {}
        for parameter, arg in zip(self.__parameters, args):
            parameters_with_values[parameter] = arg
        prior = self.__prior(args, self.__parameter_limits)
        if not np.isfinite(prior):
            return -np.inf
        nll = self.__function(parameters_with_values) + prior
        if np.any(np.isnan(nll)):
            return -np.inf
        return nll


def mcmc(
        parlist: _List[str],
        likelihood: _likelihoods.ChiSquared,
        nwalker=20,
        prior=1,
        nsteps=100,
        startpars=None,
        parlimits=None,
        emceemoves=_emcee.moves.GaussianMove(0.05, mode='vector', factor=None)
):
    """Inference using the emcee package (<https://emcee.readthedocs.io/>)
    Parameters
    ----------
    parlist : List[str]
        List of parameter names
    likelihood : Likelihood object from likelihoods or single function
    startpars : nparray with dim nwalker x len(parlist)
        Set the start parameters for all chains
    parlimits : list of tuples (lower limit and upper limit) with
        length = number of parameters
    nwalker : int (optional)
        Choose the number of walkers for the Markov chains (default = 20)
    prior : int (optional)
        Set the prior that is used during the walk
        uniform prior : 1 (default, currently only option)
    nsteps : int (optional)
        Choose the number of steps to generate with each walker
        (default = 100)
    emceemoves : Move from emcee.moves (optional)
        Choose a suitable move to create chain.
        Default: GaussianMove(0.05, mode='vector', factor=None)
        (see emcee docs)
    Returns
    -------
    emcee.EnsembleSampler.run_mcmc
        Contains the whole chain. See emcee documentation for more info.
    See Also
    --------
    emcee's documentation : Should explain the various options that can
        be passed to emcee, and how to use the resulting object after
        the chain has been produced.
    """

    if prior == 1:
        translator = _Translator(
            parlist, parlimits, likelihood, log_uniform_prior
        )
    else:
        print("So far only uniform prior is implemented.")
        return 0

    ndimension = len(parlist)

    if startpars.any() is None:
        startpars = np.zeros((nwalker, ndimension))

    optimizer = _emcee.EnsembleSampler(
        nwalker, ndimension, translator, moves=emceemoves
    )
    output = optimizer.run_mcmc(
        startpars, nsteps, progress=True, skip_initial_state_check=True
    )
    return optimizer


def log_uniform_prior(pars, parlimits):
    for index, par in enumerate(pars):
        if par < parlimits[index][0] or par > parlimits[index][1]:
            return -np.inf
    return 0.
