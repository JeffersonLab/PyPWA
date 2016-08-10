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
These are simple tests to make sure that when uninitialized methods are
called it will correctly raise a NotImplementedError.
"""


import pytest

from PyPWA.libs.data import definitions


def test_TemplateValidator_RaiseNotImplementedError():
    validator = definitions.TemplateValidator("Something")

    with pytest.raises(NotImplementedError):
        validator.test()


def test_TemplateMemory_RaiseNotImplementedError():
    memory = definitions.TemplateMemory()

    with pytest.raises(NotImplementedError):
        memory.parse("Something")

    with pytest.raises(NotImplementedError):
        memory.write("something", 12)

