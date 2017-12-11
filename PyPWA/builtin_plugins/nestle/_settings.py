#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

"""

from PyPWA import AUTHOR, VERSION
from PyPWA.libs import configuration_db

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class NestleSettings(object):

    def __init__(self):
        self.__db = configuration_db.Connector()

    @property
    def prior_location(self):
        return self.__db.read("nestle", "prior location")

    @property
    def prior_name(self):
        return self.__db.read("nestle", "prior name")

    @property
    def ndim(self):
        return self.__db.read("nestle", "ndim")

    @property
    def npoints(self):
        return self.__db.read("nestle", "npoints")

    @property
    def method(self):
        return self.__db.read("nestle", "method")

    @property
    def update_interval(self):
        return self.__db.read("nestle", "update interval")

    @property
    def npdim(self):
        return self.__db.read("nestle", "npdim")

    @property
    def maxiter(self):
        return self.__db.read("nestle", "maxiter")

    @property
    def maxcall(self):
        return self.__db.read("nestle", "maxcall")

    @property
    def dlogz(self):
        return self.__db.read("nestle", "dlogz")

    @property
    def decline_factor(self):
        return self.__db.read("nestle", "decline factor")

    @property
    def parameters(self):
        return self.__db.read("nestle", "parameters")
