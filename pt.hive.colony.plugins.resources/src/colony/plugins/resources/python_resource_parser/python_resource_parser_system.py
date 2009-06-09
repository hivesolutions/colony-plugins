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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

RESOURCE_PARSER_NAME = "python"
""" The resource parser name """

class PythonResourceParser:
    """
    The python resource parser class.
    """

    python_resource_parser_plugin = None
    """ The python resource parser plugin """

    def __init__(self, python_resource_parser_plugin):
        """
        Constructor of the class

        @type python_resource_parser_plugin: Plugin
        @param python_resource_parser_plugin: The python resource parser plugin.
        """

        self.python_resource_parser_plugin = python_resource_parser_plugin

    def get_resource_parser_name(self):
        return RESOURCE_PARSER_NAME

    def parse_resource(self, resource):
        # retrieves the python file path
        python_file_path = resource.data

        # retrieves the full resources path
        full_resources_path = resource.full_resources_path

        # adds the full resources path to the system path
        sys.path.append(full_resources_path)

        # import the python module
        python_module = __import__(python_file_path.rstrip(".py"))

        # pops the full resources path from the system path
        sys.path.pop()

        # parses the configuration contents from the python module
        resource.data = python_module.configuration
