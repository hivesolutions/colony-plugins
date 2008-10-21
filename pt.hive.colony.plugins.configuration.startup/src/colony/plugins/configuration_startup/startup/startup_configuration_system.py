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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

import startup_configuration_parser

STARTUP_CONFIGURATION_FILE_PATH = "resources/startup_configuration.xml"

class StartupConfiguration:

    startup_configuration_plugin = None

    startup_configuration = None

    def __init__(self, startup_configuration_plugin):
        self.startup_configuration_plugin = startup_configuration_plugin

    def load_startup_configuration_file(self):
        startup_configuration_file_path = os.path.join(os.path.dirname(__file__), STARTUP_CONFIGURATION_FILE_PATH)
        startup_configuration_parser_parser = startup_configuration_parser.StartupConfigurationParser(startup_configuration_file_path)
        startup_configuration_parser_parser.parse()
        self.startup_configuration = startup_configuration_parser_parser.get_value()

    def is_plugin_loadable(self, plugin, type, loading_type):

        # retrieves the plugin manager
        plugin_manager = self.startup_configuration_plugin.manager

        # in case the plugin manager initialization is complete
        if plugin_manager.get_init_complete():
            return True

        for startup_configuration_plugin in self.startup_configuration.plugins:
            if startup_configuration_plugin.id == plugin.id:
                if not startup_configuration_plugin.load:
                    return False
                else:
                    return True
        return True
