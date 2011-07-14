#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import installation_manager_exceptions

INSTALLATION_ADAPTER_VALUE = "installation_adapter"
""" The installation adapter value """

class InstallationManager:
    """
    The installation manager class.
    """

    installation_manager_plugin = None
    """ The installation manager plugin """

    installation_adapter_plugins_map = {}
    """ The installation adapter plugins map """

    def __init__(self, installation_manager_plugin):
        """
        Constructor of the class.

        @type installation_manager_plugin: InstallationManagerPlugin
        @param installation_manager_plugin: The installation manager plugin.
        """

        self.installation_manager_plugin = installation_manager_plugin

        self.installation_adapter_plugins_map = {}

    def generate_installation_file(self, parameters):
        """
        Generates the installation file for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the installation file generation.
        """

        # in case the installation adapter is not in the parameters map
        if not INSTALLATION_ADAPTER_VALUE in parameters:
            # raises the missing parameter exception
            raise installation_manager_exceptions.MissingParameter(INSTALLATION_ADAPTER_VALUE)

        # retrieves the installation adapter name from the parameters
        installation_adapter_name = parameters[INSTALLATION_ADAPTER_VALUE]

        # in case the adapter is not found in the adapter plugins map
        if not installation_adapter_name in self.installation_adapter_plugins_map:
            # raises an installation adapter not found exception
            raise installation_manager_exceptions.InstallationHandlerNotFoundException("no adapter found for current request: " + installation_adapter_name)

        # retrieves the installation adapter from the installation adapter plugins map
        installation_adapter = self.installation_adapter_plugins_map[installation_adapter_name]

        # generates the installation file using the installation adapter
        installation_adapter.generate_installation_file(parameters)

    def installation_adapter_load(self, installation_adapter_plugin):
        # retrieves the plugin adapter name
        adapter_name = installation_adapter_plugin.get_adapter_name()

        self.installation_adapter_plugins_map[adapter_name] = installation_adapter_plugin

    def installation_adapter_unload(self, installation_adapter_plugin):
        # retrieves the plugin adapter name
        adapter_name = installation_adapter_plugin.get_adapter_name()

        del self.installation_adapter_plugins_map[adapter_name]
