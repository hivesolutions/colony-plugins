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

__revision__ = "$LastChangedRevision: 13673 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-04-28 19:21:40 +0100 (qui, 28 Abr 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class SystemRegistryPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the System Registry plugin.
    """

    id = "pt.hive.colony.plugins.system.registry"
    name = "System Registry Plugin"
    short_name = "System Registry"
    description = "System Registry Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/system_registry/registry/resources/baf.xml"
    }
    capabilities = [
        "system_registry",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.0.0")
    ]
    main_modules = [
        "system_registry.registry.system_registry_system"
    ]

    system_registry = None
    """ The system registry """

    json_plugin = None
    """ the json plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import system_registry.registry.system_registry_system
        self.system_registry = system_registry.registry.system_registry_system.SystemRegistry(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_packages_structure(self):
        """
        Retrieves the packages structure.

        @rtype: Dictionary
        @return: The packages structure.
        """

        return self.system_registry.get_packages_structure()

    def get_bundles_structure(self):
        """
        Retrieves the bundles structure.

        @rtype: Dictionary
        @return: The bundles structure.
        """

        return self.system_registry.get_bundles_structure()

    def get_plugins_structure(self):
        """
        Retrieves the plugins structure.

        @rtype: Dictionary
        @return: The plugins structure.
        """

        return self.system_registry.get_plugins_structure()

    def get_package_information(self, package_id, package_version):
        """
        Retrieves the package information for the package
        with the given id and version.

        @type package_id: String
        @param package_id: The id of the package information
        to retrieve.
        @type package_version: String
        @param package_version: The version of the package information
        to retrieve.
        @rtype: Dictionary
        @return: The package information for the package
        with the given id and version.
        """

        return self.system_registry.get_package_information(package_id, package_version)

    def get_bundle_information(self, bundle_id, bundle_version):
        """
        Retrieves the bundle information for the bundle
        with the given id and version.

        @type bundle_id: String
        @param bundle_id: The id of the bundle information
        to retrieve.
        @type bundle_version: String
        @param bundle_version: The version of the bundle information
        to retrieve.
        @rtype: Dictionary
        @return: The bundle information for the bundle
        with the given id and version.
        """

        return self.system_registry.get_bundle_information(bundle_id, bundle_version)

    def get_plugin_information(self, plugin_id, plugin_version):
        """
        Retrieves the plugin information for the plugin
        with the given id and version.

        @type plugin_id: String
        @param plugin_id: The id of the plugin information
        to retrieve.
        @type plugin_version: String
        @param plugin_version: The version of the plugin information
        to retrieve.
        @rtype: Dictionary
        @return: The plugin information for the plugin
        with the given id and version.
        """

        return self.system_registry.get_plugin_information(plugin_id, plugin_version)

    def get_json_plugin(self):
        return self.json_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
