import numpy


def processing_function(the_array, the_params):
    if isinstance(the_params, dict) and 'A1' in the_params:
        return actual_function(the_array, the_params)
    elif isinstance(the_params, numpy.ndarray):
        params = {
            "A1": the_params[0], 
            "A2": the_params[1]
        }
        return actual_function(the_array, params)
    else:
        raise ValueError("Recieved unknown %s" % the_params)


def actual_function(the_array, the_params):
    wConst= the_params['A1']
    polar = the_params['A2']
    B= 6.

    theta = numpy.arccos(the_array["ctheta"])
    values = wConst*numpy.exp(B*the_array["tM"])*numpy.sin(theta)**2.*(1+polar*numpy.cos(2*the_array["psi"]))
    return values


def setup_function():
    pass

    
def prior_function(x):
    y = numpy.array([5000.*x[0], x[1]])
    return y 
