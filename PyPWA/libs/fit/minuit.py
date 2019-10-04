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
A python a cython minimizer
---------------------------
Attempts to find a minima, for information about how it works read Iminuit's
documentation online.

- _ParserObject - Translates the received value inside run to something the
  user can easily interact with.
- Minuit - The main optimizer object.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Union

import iminuit
import numpy
import tabulate
from PyPWA.libs.components.fit import fit_plugin

from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


@dataclass
class Settings:
    parameters: List[str]
    settings: Dict[str, Any]
    strategy: Union[0, 1, 2]
    number_of_calls: int


class ParserObject:

    def __init__(self, parameters: List[str]):
        self.__parameters = parameters

    def convert(self, *args: List[float]) -> Dict[str, List[float]]:
        parameters_with_values = {}
        for parameter, arg in zip(self.__parameters, args):
            parameters_with_values[parameter] = arg

        return parameters_with_values


class MinuitWrap:

    def __init__(self):
        self.__minimal = None

    def get_argument_parser(self, settings: Settings) -> ParserObject:
        return ParserObject(settings.parameters)

    def optimize(self, optimize_function, settings, fitting_type):
        self.__minimal = iminuit.Minuit(
            optimize_function, forced_parameters=settings.parameters,
            **settings.settings
        )
        self.__minimal.set_strategy(settings.strategy)
        self.__setup_set_up(fitting_type)
        self.__minimal.migrad(settings.num_of_calls)
        return self.__minimal

    def __setup_set_up(self, fitting_type):
        if fitting_type is fit_plugin.LikelihoodType.CHI_SQUARED:
            self.__minimal.set_up(1)
        else:
            self.__minimal.set_up(.5)

    def print_results(self):
        print(self.__make_table(self.__minimal.covariance))

    def __make_table(self, use_fancy):
        if use_fancy:
            table_type = 'fancy_grid'
        else:
            table_type = 'grid'

        xs, ys = set(), set()
        covariance = list()

        for field in self.__minimal.covariance:
            xs.add(field[0])
            ys.add(field[1])

        for x in xs:
            row = [x]
            for y in ys:
                row.append(self.__minimal.covariance[(x, y)])
            covariance.append(row)

        return tabulate.tabulate(
            covariance, ys, table_type, numalign='center'
        )

    def __make_data(self, save_location, table_data):
        text_path = Path(str(save_location.stem) + ".txt")
        with text_path.open("w") as stream:
            stream.write(
                "Covariance.\n{0}\nvalues: {1}".format(
                    table_data, self.__minimal.values
                )
            )

        numpy.save(str(save_location), {
            "covariance": self.__minimal.covariance,
            "fval": self.__minimal.fval,
            "values": self.__minimal.values
        })
