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

"""

import multiprocessing
from PyPWA.builtin_plugins.process.communication import _simplex, _duplex

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class CommunicationFactory(object):

    @staticmethod
    def simplex_build(count):
        sends = [0] * count
        receives = [0] * count

        for pipe in range(count):
            receive, send = multiprocessing.Pipe(False)
            sends[pipe] = _simplex._SimplexSend(send)
            receives[pipe] = _simplex._SimplexReceive(receive)

        return [sends, receives]

    @staticmethod
    def duplex_build(count):
        main = [0] * count
        process = [0] * count

        for pipe in range(count):
            receive_one, send_one = multiprocessing.Pipe(False)
            receive_two, send_two = multiprocessing.Pipe(False)

            main[pipe] = _duplex._DuplexCommunication(send_one, receive_two)
            process[pipe] = _duplex._DuplexCommunication(
                send_two, receive_one
            )

        return [main, process]
