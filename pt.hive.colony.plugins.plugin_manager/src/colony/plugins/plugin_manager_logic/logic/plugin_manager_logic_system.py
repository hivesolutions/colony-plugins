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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

SERIALIZABLE_PLUGIN_ATTRIBUTES = [
    "id",
    "name",
    "short_name",
    "description",
    "version",
    "author",
    "loaded"
]
""" List of attributes from the plugin that can be serialized and sent to the client """

class PluginManagerLogic:
    """
    The plugin manager logic class.
    """

    plugin_manager_logic_plugin = None
    """ The plugin manager logic plugin """

    business_logic_bundle = []
    """ The bundle containing the business logic classes """

    business_logic_bundle_map = {}
    """ The map associating the business logic classes with their names """

    def __init__(self, plugin_manager_logic_plugin):
        """
        Constructor of the class

        @type plugin_manager_logic_plugin: PluginManagerLogicPlugin
        @param plugin_manager_logic_plugin: The plugin manager logic plugin.
        """

        self.plugin_manager_logic_plugin = plugin_manager_logic_plugin

        self.business_logic_bundle = []
        self.business_logic_bundle_map = {}

    def generate_classes(self):
        # sets the business logic bundle
        self.business_logic_bundle = [
            PluginManagerBaseLogic
        ]

        # creates the business logic bundle map
        business_logic_bundle_map = {}

        # iterates over all the classes in the business logic bundle
        for business_logic_class in self.business_logic_bundle:
            # retrieves the business logic name
            business_logic_class_name = business_logic_class.__name__

            # sets the class in the business logic bundle map
            business_logic_bundle_map[business_logic_class_name] = business_logic_class

        # sets the business logic bundle map
        self.business_logic_bundle_map = business_logic_bundle_map

    def get_business_logic_bundle(self):
        return self.business_logic_bundle

    def get_business_logic_bundle_map(self):
        return self.business_logic_bundle_map

    def get_path_directory_name(self):
        return os.path.dirname(__file__)

class PluginManagerBaseLogic:
    """
    The plugin manager base logic class.
    """

    def get_plugins(self):
        # retrieves all plugins
        plugins = self.plugin_manager.get_all_plugins()

        # collects a list with maps containing the serializable plugin attributes
        plugins_data = []
        for plugin in plugins:

            # retrieves a map with the serializable plugin attributes
            plugin_data = {}
            for plugin_attribute in SERIALIZABLE_PLUGIN_ATTRIBUTES:
                plugin_data[plugin_attribute] = getattr(plugin, plugin_attribute)

            # adds the plugin attributes to the list
            plugins_data.append(plugin_data)

        return plugins_data

    def load_plugin(self, plugin_id):
        # loads the specified plugin
        self.plugin_manager.load_plugin(plugin_id)

    def unload_plugin(self, plugin_id):
        # unloads the specified plugin
        self.plugin_manager.unload_plugin(plugin_id)
