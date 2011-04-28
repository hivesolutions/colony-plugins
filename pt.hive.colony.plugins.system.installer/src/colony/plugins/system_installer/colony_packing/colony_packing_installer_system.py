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

UPGRADE_VALUE = "upgrade"
""" The upgrade value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

INSTALLED_PLUGINS_VALUE = "installed_plugins"
""" The installed plugins value """

FORCE_VALUE = "force"
""" The force value """

LAST_MODIFIED_TIMESTAMP_VALUE = "last_modified_timestamp"
""" The last modified timestamp value """

LAST_MODIFIED_DATE_VALUE = "last_modified_date"
""" The last modified date value """

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

    def install_bundle(self, file_path, properties):
        """
        Method called upon installation of the bundle with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the bundle file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the manager path
        manager_path = plugin_manager.get_manager_path()

        # creates the bundles file path
        bundles_file_path = os.path.join(manager_path, "var/registry/bundles.json")

    def install_plugin(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the plugin with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the plugin file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
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
        plugins_file_path = os.path.join(manager_path, "var/registry/plugins.json")

        # creates the plugins directory path
        plugins_directory_path = os.path.join(manager_path, "var/registry/plugins")

        # creates a new file transaction context
        file_context = file_context or colony.libs.file_util.FileTransactionContext("c:\\transactions\\")

        # opens a new transaction in the file context
        file_context.open()

        try:
            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(file_path, {}, "colony")

            # retrieves the packing file contents
            packing_file_contents = packing_manager_plugin.get_packing_file_contents(file_path, {}, "colony")

            # retrieves the plugin id
            plugin_id = packing_information.get_property(ID_VALUE)

            # retrieves the plugin version
            plugin_version = packing_information.get_property(VERSION_VALUE)

            # ------------------------------------------------

            # TENHO DE CONTAR COM O CASE DE O FICHEIRO NAO EXISTIR
            # tenho de obter as informacoes sobre o cpx aki
            # e depois tenho de acrescentar essas informacoes ao plugins.json

            # --------------------------------------

            # creates the plugin descriptor file path
            plugin_descriptor_file_path = os.path.join(plugins_directory_path, plugin_id + "_" + plugin_version + "." + JSON_FILE_EXTENSION)

            # writes the packing file contents to the plugin descriptor file path
            file_context.write_file(plugin_descriptor_file_path, packing_file_contents)

            #------------------------------------------------------------------

            # reads the plugin file contents
            plugins_file_contents = file_context.read_file(plugins_file_path)

            # loads the plugin file contents from json
            plugins = json_plugin.loads(plugins_file_contents)

            # retrieves the installed plugins
            installed_plugins = plugins.get(INSTALLED_PLUGINS_VALUE, {})

            # validates the plugin transaction requirements
            self._validate_plugin_transaction(properties, plugins_file_path, plugins, packing_information)

            # retrieves the main plugin path
            main_plugin_path = plugin_manager.get_main_plugin_path()

            # retrieves the "virtual" main plugin path from the file context
            # this is necessary to ensure a transaction mode
            main_plugin_virtual_path = file_context.get_file_path(main_plugin_path)

            # deploys the package using the main plugin "virtual" path
            self._deploy_package(file_path, main_plugin_virtual_path)

            # retrieves the current time
            current_time = time.time()

            # retrieves the current date time
            current_date_time = datetime.datetime.utcnow()

            # formats the current date time
            current_date_time_formated = current_date_time.strftime("%d-%m-%Y %H:%M:%S")

            # sets the installed plugin map
            installed_plugins[plugin_id] = {
                VERSION_VALUE : plugin_version,
                TIMESTAMP_VALUE : current_time
            }

            # updates the plugins map with the current time
            # and date time values
            plugins[LAST_MODIFIED_TIMESTAMP_VALUE] = current_time
            plugins[LAST_MODIFIED_DATE_VALUE] = current_date_time_formated

            # serializes the plugins (in pretty mode)
            plugins_serialized = json_plugin.dumps_pretty(plugins)

            # writes the plugins serialized value in the plugins file
            file_context.write_file(plugins_file_path, plugins_serialized)

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
