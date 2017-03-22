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

import pytest
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.configurator.storage import template_parser

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


@pytest.fixture()
def templates():
    loader = template_parser.TemplateLoader()
    return loader.templates


def test_template_is_dict(templates):
    assert isinstance(templates, dict)


def test_global_settings_in_templates(templates):
    assert "Global Options" in templates


def test_builtin_parser_in_templates(templates):
    assert "Builtin Parser" in templates
