#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
The factory for the communication object.
"""

import multiprocessing
from multiprocessing.connection import Connection
from typing import Callable, List, Tuple

from PyPWA import VERSION, AUTHOR

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


factory_return = Tuple[List[Connection], List[Connection]]
factory_type = Callable[[int], factory_return]


def simplex_build(count):
    # type: (int) -> factory_return
    sends, receives = __build_lists(count)
    for pipe_index in range(count):
        receives[pipe_index], sends[pipe_index] = multiprocessing.Pipe(False)
    return sends, receives


def duplex_build(count):
    # type: (int) -> factory_return
    main, process = __build_lists(count)
    for pipe_index in range(count):
        main[pipe_index], process[pipe_index] = multiprocessing.Pipe(True)
    return main, process


def __build_lists(count):
    # type: (int) -> Tuple[List, List]
    main_bundle = [0] * count
    child_bundle = [0] * count
    return main_bundle, child_bundle
