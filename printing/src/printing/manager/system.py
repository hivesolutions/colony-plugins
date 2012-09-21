#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system

import parser
import exceptions

TEST_IMAGE_PATH = "printing/manager/resources/test_logo.png"
""" The test image relative path """

class PrintingManager(colony.base.system.System):
    """
    The printing manager class.
    """

    printing_plugins_map = {}
    """ The printing plugins map """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        self.printing_plugins_map = {}

    def print_test(self, printing_options = {}):
        # retrieves the printing plugin for the given
        # printing options
        printing_plugin = self._get_printing_plugin(printing_options)

        # prints the test in the printing plugin
        printing_plugin.print_test(printing_options)

    def print_test_image(self, printing_options = {}):
        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)

        # creates the complete image path
        image_path = plugin_path + "/" + TEST_IMAGE_PATH

        # retrieves the printing plugin for the given
        # printing options
        printing_plugin = self._get_printing_plugin(printing_options)

        # prints the test image in the printing plugin
        printing_plugin.print_test_image(image_path, printing_options)

    def print_printing_language(self, printing_language_string, printing_options = {}):
        # creates a new printing language parser
        _parser = parser.PrintingLanguageParser()

        # sets the printing language string in the parser
        _parser.string = printing_language_string

        # parses the string
        _parser.parse_string()

        # retrieves the printing document
        printing_document = _parser.get_value()

        # retrieves the printing plugin for the given
        # printing options
        printing_plugin = self._get_printing_plugin(printing_options)

        # prints the printing language document in the printing plugin
        printing_plugin.print_printing_language(printing_document, printing_options)

    def load_printing_plugin(self, printing_plugin):
        # retrieves the printing name from the printing plugin
        printing_name = printing_plugin.get_printing_name()

        # sets the printing plugin in the printing plugins map
        self.printing_plugins_map[printing_name] = printing_plugin

    def unload_printing_plugin(self, printing_plugin):
        # retrieves the printing name from the printing plugin
        printing_name = printing_plugin.get_printing_name()

        # unsets the printing plugin from the printing plugins map
        del self.printing_plugins_map[printing_name]

    def _get_printing_plugin(self, printing_options):
        # retrieves the printing name (engine) from the printing options
        printing_name = printing_options.get("printing_name", None)

        # in case the printing name is defined
        if printing_name:
            # tries to retrieve the printing plugin from the printing plugins
            # map
            printing_plugin = self.printing_plugins_map.get(printing_name, None)
        else:
            if self.plugin.printing_plugins:
                # retrieves the first printing plugin
                printing_plugin = self.plugin.printing_plugins[0]
            else:
                # sets the printing plugin as invalid, because there
                # is not printing plugin available
                printing_plugin = None

        # in case no printing plugin is selected
        if not printing_plugin:
            # raises the printing not available exception
            raise exceptions.PrintingPluginNotAvailable("the required printer is not available or no printers are available")

        # returns the printing plugin
        return printing_plugin
