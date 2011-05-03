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

__revision__ = "$LastChangedRevision: 2349 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:52:01 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import time
import datetime

import colony.libs.file_util

import colony_packing_installer_exceptions

INSTALLER_TYPE = "colony_packing"
""" The installer type """

JSON_FILE_EXTENSION = "json"
""" The json file extension """

ID_VALUE = "id"
""" The id value """

VERSION_VALUE = "version"
""" The version value """

TIMESTAMP_VALUE = "timestamp"
""" The timestamp value """

TYPE_VALUE = "type"
""" The type value """

BUNDLE_VALUE = "bundle"
""" The bundle value """

PLUGIN_VALUE = "plugin"
""" The plugin value """

BUNDLES_VALUE = "bundles"
""" The bundles value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

UPGRADE_VALUE = "upgrade"
""" The upgrade value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

INSTALLED_PACKAGES_VALUE = "installed_packages"
""" The installed packages value """

INSTALLED_BUNDLES_VALUE = "installed_bundles"
""" The installed bundles value """

INSTALLED_PLUGINS_VALUE = "installed_plugins"
""" The installed plugins value """

FORCE_VALUE = "force"
""" The force value """

LAST_MODIFIED_TIMESTAMP_VALUE = "last_modified_timestamp"
""" The last modified timestamp value """

LAST_MODIFIED_DATE_VALUE = "last_modified_date"
""" The last modified date value """

RELATIVE_REGISTRY_PATH = "var/registry"
""" The path relative to the manager path for the registry """

PACKAGES_FILE_NAME = "packages.json"
""" The packages file name """

BUNDLES_FILE_NAME = "bundles.json"
""" The bundles file name """

PLUGINS_FILE_NAME = "plugins.json"
""" The plugins file name """

COLONY_BUNDLE_FILE_EXTENSION = ".cbx"
""" The colony bundle file extension """

COLONY_PLUGIN_FILE_EXTENSION = ".cpx"
""" The colony plugin file extension """

class ColonyPackingInstaller:
    """
    The colony packing installer class.
    """

    colony_packing_installer_plugin = None
    """ The colony packing installer plugin """

    def __init__(self, colony_packing_installer_plugin):
        """
        Constructor of the class.

        @type colony_packing_installer_plugin: ColonyPackingInstallerPlugin
        @param colony_packing_installer_plugin: The colony packing installer plugin.
        """

        self.colony_packing_installer_plugin = colony_packing_installer_plugin

    def load_installer(self):
        """
        Method called upon load of the installer.
        """

        self.colony_packing_installer_plugin.info("Loading colony packing installer")

    def get_installer_type(self):
        """
        Retrieves the type of installer.

        @rtype: String
        @return: The type of installer.
        """

        return INSTALLER_TYPE

    def install_package(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the package with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the package file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # creates a new file transaction context
        file_context = file_context or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # resolves the file path retrieving the real file path
            real_file_path = file_context.resolve_file_path(file_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_file_path, {}, "colony")

            # retrieves the type
            type = packing_information.get_property(TYPE_VALUE)

            # retrieves the package id
            package_id = packing_information.get_property(ID_VALUE)

            # retrieves the package version
            package_version = packing_information.get_property(VERSION_VALUE)

            # in case the type is bundle
            if type == BUNDLE_VALUE:
                # installs the bundle
                self.install_bundle(file_path, properties, file_context)
            # in case the type is plugin
            elif type == PLUGIN_VALUE:
                # installs the plugin
                self.install_plugin(file_path, properties, file_context)
            # otherwise it's not a valid type
            else:
                raise Exception("TA FEITO !!!!")

            # retrieves the package item key
            package_item_key = package_id

            # creates the package item value
            package_item_value = {
                TYPE_VALUE : type,
                VERSION_VALUE : package_version
            }

            # adds the package item
            self._add_package_item(package_item_key, package_item_value, file_context)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def install_bundle(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the bundle with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the bundle file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the manager path
        manager_path = plugin_manager.get_manager_path()

        # creates the bundles directory path
        bundles_directory_path = os.path.join(manager_path, RELATIVE_REGISTRY_PATH + "/" + BUNDLES_VALUE)

        # creates a new file transaction context
        file_context = file_context or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # resolves the file path retrieving the real file path
            real_file_path = file_context.resolve_file_path(file_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_file_path, {}, "colony")

            # retrieves the bundle id
            bundle_id = packing_information.get_property(ID_VALUE)

            # retrieves the bundle version
            bundle_version = packing_information.get_property(VERSION_VALUE)

            # retrieves the plugins
            plugins = packing_information.get_property(PLUGINS_VALUE)

            # reads the bundle file contents
            bundle_file_contents = file_context.read_file(file_path)

            # creates the bundle descriptor file path
            bundle_file_path = os.path.join(bundles_directory_path, bundle_id + "_" + bundle_version + COLONY_BUNDLE_FILE_EXTENSION)

            # writes the bundle file contents to the bundle file path
            file_context.write_file(bundle_file_path, bundle_file_contents)

            # retrieves the temporary path
            temporary_path = plugin_manager.get_temporary_path()

            # creates the temporary bundles path
            temporary_bundles_path = os.path.join(temporary_path, BUNDLES_VALUE)

            # retrieves the "virtual" main bundle path from the file context
            # this is necessary to ensure a transaction mode
            main_bundle_virtual_path = file_context.get_file_path(temporary_bundles_path)

            # deploys the package using the main bundle "virtual" path
            self._deploy_package(real_file_path, main_bundle_virtual_path)

            # iterates over all the plugins
            for plugin in plugins:
                # retrieves the plugin id
                plugin_id = plugin[ID_VALUE]

                # retrieves the plugin version
                plugin_version = plugin[VERSION_VALUE]

                # creates the plugin file path
                plugin_file_path = os.path.join(temporary_bundles_path, PLUGINS_VALUE + "/" + plugin_id + "_" + plugin_version + COLONY_PLUGIN_FILE_EXTENSION)

                # installs the plugin for the given plugin file path
                # properties and file context
                self.install_plugin(plugin_file_path, properties, file_context)

                # retrieves the package item key
                package_item_key = plugin_id

                # creates the package item value
                package_item_value = {
                    TYPE_VALUE : PLUGIN_VALUE,
                    VERSION_VALUE : plugin_version
                }

                # adds the package item
                self._add_package_item(package_item_key, package_item_value, file_context)

            # retrieves the bundle item key
            bundle_item_key = bundle_id

            # creates the bundle item value
            bundle_item_value = {
                VERSION_VALUE : bundle_version
            }

            # adds the bundle item
            self._add_bundle_item(bundle_item_key, bundle_item_value, file_context)

            # removes the temporary bundles path (directory)
            file_context.remove_directory(temporary_bundles_path)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def install_plugin(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the plugin with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the plugin file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the json plugin
        json_plugin = self.colony_packing_installer_plugin.json_plugin

        # retrieves the manager path
        manager_path = plugin_manager.get_manager_path()

        # creates the plugins file path
        plugins_file_path = os.path.join(manager_path, RELATIVE_REGISTRY_PATH + "/" + PLUGINS_FILE_NAME)

        # creates the plugins directory path
        plugins_directory_path = os.path.join(manager_path, RELATIVE_REGISTRY_PATH + "/" + PLUGINS_VALUE)

        # creates a new file transaction context
        file_context = file_context or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # resolves the file path retrieving the real file path
            real_file_path = file_context.resolve_file_path(file_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_file_path, {}, "colony")

            # retrieves the plugin id
            plugin_id = packing_information.get_property(ID_VALUE)

            # retrieves the plugin version
            plugin_version = packing_information.get_property(VERSION_VALUE)

            # reads the plugin file contents
            plugins_file_contents = file_context.read_file(plugins_file_path)

            # loads the plugin file contents from json
            plugins = json_plugin.loads(plugins_file_contents)

            # validates the plugin transaction requirements
            self._validate_plugin_transaction(properties, plugins_file_path, plugins, packing_information)

            # reads the plugin file contents
            plugin_file_contents = file_context.read_file(file_path)

            # creates the plugin descriptor file path
            plugin_file_path = os.path.join(plugins_directory_path, plugin_id + "_" + plugin_version + COLONY_PLUGIN_FILE_EXTENSION)

            # writes the plugin file contents to the plugin file path
            file_context.write_file(plugin_file_path, plugin_file_contents)

            # retrieves the main plugin path
            main_plugin_path = plugin_manager.get_main_plugin_path()

            # retrieves the "virtual" main plugin path from the file context
            # this is necessary to ensure a transaction mode
            main_plugin_virtual_path = file_context.get_file_path(main_plugin_path)

            # deploys the package using the main plugin "virtual" path
            self._deploy_package(real_file_path, main_plugin_virtual_path)

            # retrieves the plugin item key
            plugin_item_key = plugin_id

            # creates the plugin item value
            plugin_item_value = {
                VERSION_VALUE : plugin_version
            }

            # adds the plugin item
            self._add_plugin_item(plugin_item_key, plugin_item_value, file_context)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _validate_plugin_transaction(self, properties, plugins_file_path, plugins, packing_information):
        # retrieves the plugin id
        plugin_id = packing_information.get_property(ID_VALUE)

        # retrieves the plugin version
        plugin_version = packing_information.get_property(VERSION_VALUE)

        # retrieves the flag properties values
        upgrade = properties.get(UPGRADE_VALUE, True)
        force = properties.get(FORCE_VALUE, False)

        # retrieves the installed plugins
        installed_plugins = plugins.get(INSTALLED_PLUGINS_VALUE, {})

        # retrieves the installed plugin value
        installed_plugin = installed_plugins.get(plugin_id, {})

        # in case there is an installed plugin and the upgrade
        # flag is not set
        if installed_plugin and not upgrade:
            # raises the plugin installation error
            raise colony_packing_installer_exceptions.PluginInstallationError("plugin already installed")

        # retrieves the installed plugin version
        installed_plugin_version = installed_plugin.get(VERSION_VALUE, None)

        # in case the installed plugin version is the same as the
        # plugin version and the force flag is not set
        if installed_plugin_version == plugin_version and not force:
            # raises the plugin installation error
            raise colony_packing_installer_exceptions.PluginInstallationError("plugin version already installed")

    def _deploy_package(self, package_path, target_path = None):
        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the main plugin path
        main_plugin_path = plugin_manager.get_main_plugin_path()

        # sets the target path
        target_path = target_path or main_plugin_path

        # creates the properties map for the file unpacking packing
        properties = {
            TARGET_PATH_VALUE : target_path
        }

        # unpacks the files using the colony service
        packing_manager_plugin.unpack_files([package_path], properties, "colony")

    def _touch_structure(self, structure):
        """
        Touches the structure, updating the timestamp
        references present in it.

        @type structure: Dictionary
        @param structure: The structure to be update with with
        new timestamps.
        """

        # retrieves the current time
        current_time = time.time()

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time
        current_date_time_formated = current_date_time.strftime("%d-%m-%Y %H:%M:%S")

        # updates the structure map with the current time
        # and date time values
        structure[LAST_MODIFIED_TIMESTAMP_VALUE] = current_time
        structure[LAST_MODIFIED_DATE_VALUE] = current_date_time_formated

    def _add_package_item(self, item_key, item_value, file_context, update_time = True):
        """
        Adds a package item to the packages file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, file_context, update_time, PACKAGES_FILE_NAME, INSTALLED_PACKAGES_VALUE)

    def _add_bundle_item(self, item_key, item_value, file_context, update_time = True):
        """
        Adds a bundle item to the bundles file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, file_context, update_time, BUNDLES_FILE_NAME, INSTALLED_BUNDLES_VALUE)

    def _add_plugin_item(self, item_key, item_value, file_context, update_time = True):
        """
        Adds a plugin item to the plugins file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, file_context, update_time, PLUGINS_FILE_NAME, INSTALLED_PLUGINS_VALUE)

    def __add_structure_item(self, item_key, item_value, file_context, update_time, structure_file_name, structure_key_name):
        """
        Adds a new structure item to an existing structures file.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        @type structure_file_name: String
        @param structure_file_name: The name of the structure file to be used.
        @type structure_key_name: String
        @param structure_key_name: The key to the structure base item.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the json plugin
        json_plugin = self.colony_packing_installer_plugin.json_plugin

        # retrieves the manager path
        manager_path = plugin_manager.get_manager_path()

        # retrieves the registry path
        registry_path = os.path.normpath(manager_path + "/" + RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.normpath(registry_path + "/" + structure_file_name)

        # reads the structure file contents
        structure_file_contents = file_context.read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json_plugin.loads(structure_file_contents)

        # retrieves the installed structure
        installed_structure = structure.get(structure_key_name, {})

        # in case the update time flag is set
        if update_time:
            # retrieves the current time
            current_time = time.time()

            # sets the item value
            item_value[TIMESTAMP_VALUE] = current_time

        # sets the installed structure map
        installed_structure[item_key] = item_value

        # touches the structure (internal structure)
        # updating the dates in it
        self._touch_structure(structure)

        # serializes the structure
        structure_serialized = json_plugin.dumps_pretty(structure)

        # writes the structure file contents
        file_context.write_file(structure_file_path, structure_serialized)
