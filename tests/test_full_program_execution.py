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


from pathlib import Path

from PyPWA.progs import simulation


"""
Ensures that when given a simple dataset, the builtin programs are
capable of executing.
"""


def test_simulation_execute():
    output = Path("output.txt")

    simulation.simulation(
        [
            "--disable_cache", "--output", "output.txt",
            "config", "tests/test_data/docs/program_data/rho/RHOsim",
        ]
    )

    if output.exists():
        output.unlink()
