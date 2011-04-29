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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types

ATTRIBUTE_EXCLUSION_LIST = []
""" The attribute exclusion list """

class MainDistributionPluginSystem:
    """
    The main distribution plugin system class.
    """

    main_distribution_plugin_system_plugin = None
    """ The main distribution plugin system plugin """

    def __init__(self, main_distribution_plugin_system_plugin):
        """
        Constructor of the class.

        @type main_distribution_plugin_system_plugin: MainDistributionPluginSystemPlugin
        @param main_distribution_plugin_system_plugin: The main distribution plugin system plugin.
        """

        self.main_distribution_plugin_system_plugin = main_distribution_plugin_system_plugin

    def create_plugin_proxy(self, plugin):
        # creates the plugin proxy
        plugin_proxy = PluginProxy()

        # sets the plugin proxy client proxy
        plugin_proxy.client_proxy = "null"

        # sets the plugin proxy plugin id
        plugin_proxy.id = plugin.id

        # sets the plugin proxy plugin version
        plugin_proxy.version = plugin.version

        # retrieves the plugin attributes
        plugin_attributes = dir(plugin)

        # filters the plugin attributes retrieving only the method names
        plugin_method_names = [value for value in plugin_attributes if not value in ATTRIBUTE_EXCLUSION_LIST and not value in dir(object) and type(getattr(plugin, value)) == types.MethodType]

        # iterates over all the plugin method names
        for plugin_method_name in plugin_method_names:
            plugin_proxy.add_plugin_method(plugin_method_name)

        # returns the plugin proxy
        return plugin_proxy

    def create_plugin_proxy_by_id(self, plugin_id):
        # retrieves the plugin manager
        manager = self.main_distribution_plugin_system_plugin.manager

        # retrieves the plugin
        plugin = manager.get_plugin_by_id(plugin_id)

        # retrieves the plugin proxy
        plugin_proxy = self.create_plugin_proxy(plugin)

        # returns the plugin proxy
        return plugin_proxy

class PluginProxy:
    """
    The plugin proxy class.
    """

    client_proxy = None
    """ The client proxy """

    plugin_methods = []
    """ The list of plugin methods """

    id = "none"
    """ The id of the plugin """

    version = "none"
    """ The version of the plugin """

    def __init__(self, client_proxy = None, id = "none", version = "none"):
        self.client_proxy = client_proxy
        self.id = id
        self.version = version

        self.plugin_methods = []

    def set_client_proxy(self, client_proxy):
        self.client_proxy = client_proxy

    def add_plugin_method(self, method_name):
        self.plugin_methods.append(method_name)

    def process_plugin_proxy(self, client_proxy):
        self.client_proxy = client_proxy

        for plugin_method in self.plugin_methods:
            caller = self.create_caller(plugin_method)
            setattr(self, plugin_method, caller)

    def create_caller(self, calling_name):
        """
        Creates the caller method for the given calling name.

        @type calling_name: String
        @param calling_name: The calling name for the calling method.
        @type calling_name: Function
        @param calling_name: The caller method for the given calling name.
        """

        def caller(*args, **kwargs):
            # retrieves the plugin id
            plugin_id = self.id

            # retrieves the plugin version
            plugin_version = self.version

            # call the plugin proxy method
            return_value = self.client_proxy.main_distribution_service.call_plugin_proxy_method(plugin_id, plugin_version, calling_name, args)

            return return_value

        return caller
