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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

SPECIFICATION_GENERATOR_HANDLER_NAME = "json"
""" The specification genertor handler name """

class JsonSepecificationGeneratorHandler:
    """
    The json specification generator handler class.
    """

    json_specification_generator_handler_plugin = None
    """ The json specification generator handler """

    def __init__(self, json_specification_generator_handler_plugin):
        """
        Constructor of the class.

        @type json_specification_generator_handler_plugin: JsonSpecificationGeneratorHandlerPlugin
        @param json_specification_generator_handler_plugin: The json specification generator handler plugin.
        """

        self.json_specification_generator_handler_plugin = json_specification_generator_handler_plugin

    def get_specification_generator_handler_name(self):
        return SPECIFICATION_GENERATOR_HANDLER_NAME

    def generate_plugin_specification(self, plugin, properties):
        """
        Generates a specification string describing the structure
        and specification of the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin to be used to generate plugin specification.
        @type properties: Dictionary
        @param properties: The properties for plugin specification generation.
        @rtype: String
        @return: The generated plugin specification string.
        """

        pass
