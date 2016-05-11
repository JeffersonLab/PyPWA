import iminuit


class Minimizer(object):
    """Object based off of iminuit, provides an easy way to run minimalization
    Args:
        calc_function (function): function that holds the calculations.
        parameters (list): List of the parameters
        settings (dict): Dictionary of the settings for iminuit
        strategy (int): iminuit's strategy
        set_up (int): Todo
        ncall (int): Max number of calls
    """

    def __init__(self, calc_function, parameters, settings, strategy, set_up, ncall):
        self.fval = 0
        self.covariance = 0
        self.values = 0
        self._calc_function = calc_function
        self._parameters = parameters
        self._settings = settings
        self._strategy = strategy
        self._set_up = set_up
        self._ncall = ncall

    def min(self):
        """Method to call to start minimization process"""
        minimal = iminuit.Minuit(self._calc_function, forced_parameters=self._parameters, **self._settings )
        minimal.set_strategy(self._strategy)
        minimal.set_up(self._set_up)
        minimal.migrad(ncall=self._ncall)
        self.fval = minimal.fval
        self.covariance = minimal.covariance
        self.values = minimal.values
