"""Objects for reading data from disk

All modules in this package are designed and optimized to read
specific data from the disk including GAMP events. This data
reading method will be slower than traditional memory based
methods but should be more resource efficient.
Best used for data that is too large for your memory and
can not be used in place of memory based functions.
"""

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION
