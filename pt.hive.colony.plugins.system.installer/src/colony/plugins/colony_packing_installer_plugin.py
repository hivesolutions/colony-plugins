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

__revision__ = "$LastChangedRevision: 7715 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-26 07:31:00 +0000 (sex, 26 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class ColonyPackingInstallerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Colony Packing Installer plugin.
    """

    id = "pt.hive.colony.plugins.system.installer.colony_packing_installer"
    name = "Colony Packing Installer Plugin"
    short_name = "Colony Packing Installer"
    description = "Colony Packing Installer Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/system_installer/colony_packing/resources/baf.xml"
    }
    capabilities = [
        "installer",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.packing.manager", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.0.0")
    ]
    main_modules = [
        "system_installer.colony_packing.colony_packing_installer_exceptions",
        "system_installer.colony_packing.colony_packing_installer_system"
    ]

    colony_packing_installer = None
    """ The colony packing installer """

    packing_manager_plugin = None
    """ Plugin for packing of files """

    json_plugin = None
    """ Plugin for json file handling """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import system_installer.colony_packing.colony_packing_installer_system
        self.colony_packing_installer = system_installer.colony_packing.colony_packing_installer_system.ColonyPackingInstaller(self)

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

    def get_installer_type(self):
        return self.colony_packing_installer.get_installer_type()

    def install_package(self, file_path, properties):
        """
        Method called upon installation of the package with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the package file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        return self.colony_packing_installer.install_package(file_path, properties)

    def install_bundle(self, file_path, properties):
        """
        Method called upon installation of the bundle with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the bundle file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        return self.colony_packing_installer.install_bundle(file_path, properties)

    def install_plugin(self, file_path, properties):
        """
        Method called upon installation of the plugin with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the plugin file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        return self.colony_packing_installer.install_plugin(file_path, properties)

    def install_container(self, file_path, properties):
        """
        Method called upon installation of the container with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the container file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        return self.colony_packing_installer.install_container(file_path, properties)

    def uninstall_package(self, package_id, package_version, properties):
        """
        Method called upon removal of the package with
        the given id, version and properties.

        @type package_id: String
        @param package_id: The id of the package to be removed.
        @type package_version: String
        @param package_version: The version of the package to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        """

        return self.colony_packing_installer.uninstall_package(package_id, package_version, properties)

    def uninstall_bundle(self, bundle_id, bundle_version, properties):
        """
        Method called upon removal of the bundle with
        the given id, version and properties.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to be removed.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        """

        return self.colony_packing_installer.uninstall_bundle(bundle_id, bundle_version, properties)

    def uninstall_plugin(self, plugin_id, plugin_version, properties):
        """
        Method called upon removal of the plugin with
        the given id, version and properties.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be removed.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        """

        return self.colony_packing_installer.uninstall_plugin(plugin_id, plugin_version, properties)

    def uninstall_container(self, container_id, container_version, properties):
        """
        Method called upon removal of the container with
        the given id, version and properties.

        @type container_id: String
        @param container_id: The id of the container to be removed.
        @type container_version: String
        @param container_version: The version of the container to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        """

        return self.colony_packing_installer.uninstall_container(container_id, container_version, properties)

    def open_transaction(self, transaction_properties):
        """
        Opens a new transaction and retrieves the transaction
        properties map.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the current transaction.
        @rtype: Dictionary
        @return: The map describing the transaction.
        """

        return self.colony_packing_installer.open_transaction(transaction_properties)

    def commit_transaction(self, transaction_properties):
        """
        Commits the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be commited.
        """

        return self.colony_packing_installer.commit_transaction(transaction_properties)

    def rollback_transaction(self, transaction_properties):
        """
        "Rollsback" the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be "rollbacked".
        """

        return self.colony_packing_installer.rollback_transaction(transaction_properties)

    def add_commit_callback(self, callback, transaction_properties):
        """
        Adds a commit callback to the current transaction.
        This callback will be called upon the final
        commit is passed.

        @type callback: Function
        @param callback: The callback function to be called
        upon the final commit.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction.
        """

        return self.colony_packing_installer.add_commit_callback(callback, transaction_properties)

    def add_rollback_callback(self, callback, transaction_properties):
        """
        Adds a rollback callback to the current transaction.
        This callback will be called upon the final
        rollback is passed.

        @type callback: Function
        @param callback: The callback function to be called
        upon the final rollback.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction.
        """

        return self.colony_packing_installer.add_rollback_callback(callback, transaction_properties)

    def get_packing_manager_plugin(self):
        return self.packing_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.packing.manager")
    def set_packing_manager_plugin(self, packing_manager_plugin):
        self.packing_manager_plugin = packing_manager_plugin

    def get_json_plugin(self):
        return self.json_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
