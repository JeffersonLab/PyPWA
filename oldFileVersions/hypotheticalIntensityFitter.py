import numpy
import os
import hypotheticalIntensity
import fnGenerator2

from iminuit import Minuit


"""
here is where we should setup the variables for hypothetical intensity, then when we instantiate it
we simply pass those values into the constructor for the class.  see the contructor for more
information on what the differences between the parameters and the variables are.
"""

hI=hypotheticalIntensity.hypotheticalIntensity()

"""
this next bit is used to allow for the lnLikelihood function of the hypothetical intensity
to be called with a list of paramters instead of an explicitly defined set of parameters
for example: instead of 'hI.lnLikelihood(t1,t2)' we would have 'hI.lnLikelihood(paramList)'
where 'paramList=[t1,t2]'.
"""
generator=fnGenerator2.generator()

generator.fileName=os.path.join(os.getcwd(),"hypotheticalGeneratedFn.py")#'REFERENCE 1'

generator.createFile(15) #change the argument here to the number of terms in your hypothetical intensity

"""
note that the line below is open to exploitation, so only run this program if you trust its source.
a malicious user can modify fnGenerator2 to write exploitative code to the file specified above and then
when the next line below is ran, that code is ran as well.  just a precautionary note.
"""
execfile(os.path.join(os.getcwd(),"hypotheticalGeneratedFn.py"))#this filename needs to match the filename specified in 'REFERENCE 1'

"""
m is an iminuit.Minuit class object.  it is instantiated in the file created and executed above.
"""
m.migrad(ncall=1000)
m.set_strategy(1)
m.set_up(0.5)

"""
you can then simply save these values or print them or w/e
"""
print m.values
print numpy.array(m.matrix())
