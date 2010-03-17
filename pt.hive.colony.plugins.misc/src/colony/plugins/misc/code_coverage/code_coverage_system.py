#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class CodeCoverage:
    """
    The code coverage class.
    """

    code_coverage_plugin = None
    """ The code coverage plugin """

    def __init__(self, code_coverage_plugin):
        """
        Constructor of the class.

        @type code_coverage_plugin: CodeCoveragePlugin
        @param code_coverage_plugin: The code coverage plugin.
        """

        self.code_coverage_plugin = code_coverage_plugin

    def start_code_coverage(self):
        self.code_coverage_plugin.debug("Starting code coverage")

    def stop_code_coverage(self):
        self.code_coverage_plugin.debug("Stopping code coverage")

    def write_code_coverage(self, code_coverage_file_path):
        self.code_coverage_plugin.debug("Writing code coverage")

    def get_code_coverage(self):
        return None
