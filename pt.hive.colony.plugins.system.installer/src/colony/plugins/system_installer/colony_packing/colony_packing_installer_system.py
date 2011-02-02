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

import colony_packing_installer_exceptions

INSTALLER_TYPE = "colony_packing"
""" The installer type """

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
        bundles_file_path = os.path.join(manager_path, "var/bundles.json")

    def install_plugin(self, file_path, properties):
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

        # retrieves the json plugin
        json_plugin = self.colony_packing_installer_plugin.json_plugin

        # retrieves the manager path
        manager_path = plugin_manager.get_manager_path()

        # creates the plugins file path
        plugins_file_path = os.path.join(manager_path, "var/plugins.json")

        # TENHO DE CONTAR COM O CASE DE O FICHEIRO NAO EXISTIR

        # tenho de obter as informacoes sobre o cpx aki
        # e depois tenho de acrescentar essas informacoes ao plugins.json
        # tenho tb de verificar conflicto de plgugins
        # se tiver a mesma versao so com force posso eu fazer deploy

        # HARDCODES

        PLUGIN_ID = "pt.hive.colony.matias"

        PLUGIN_VERSION = "1.0.0"

        # -----------------------------------------

        # retrieves the flag properties values
        upgrade = properties.get("upgrade", True)
        force = properties.get("force", False)

        # reads the plugin file contents
        plugins_file_contents = self._read_file(plugins_file_path)

        # loads the plugin file contents from json
        plugins = json_plugin.loads(plugins_file_contents)

        # retrieves the installed plugins
        installed_plugins = plugins.get("installed_plugins", {})

        # retrieves the installed plugin value
        installed_plugin = installed_plugins.get(PLUGIN_ID, {})

        # in case there is an installed plugin and the upgrade
        # flag is not set
        if installed_plugin and not upgrade:
            # raises the colony packing installer exception
            raise colony_packing_installer_exceptions.ColonyPackingInstallerException("plugin already installed")

        # retrieves the installed plugin version
        installed_plugin_version = installed_plugin.get("version", None)

        # in case the installed plugin version is the same as the
        # plugin version and the force flag is not set
        if installed_plugin_version == PLUGIN_VERSION and not force:
            # raises the colony packing installer exception
            raise colony_packing_installer_exceptions.ColonyPackingInstallerException("plugin version already installed")

        # retrieves the current time
        current_time = time.time()

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time
        current_date_time_formated = current_date_time.strftime("%d-%m-%Y %H:%M:%S")

        installed_plugins[PLUGIN_ID] = {"version" : PLUGIN_VERSION, "timestamp" : current_time}
        plugins["last_modified_timestamp"] = current_time
        plugins["last_modified_date"] = current_date_time_formated

        # serializes the plugins (in pretty mode)
        plugins_serialized = json_plugin.dumps_pretty(plugins)

        # writes the plugins serialized value in the plugins file
        self._write_file(plugins_file_path, plugins_serialized)

    def _read_file(self, file_path):
        # open the file
        file = open(file_path, "rb")

        try:
            # reads the file contents
            file_contents = file.read()
        finally:
            # closes the file
            file.close()

        # returns the file contents
        return file_contents

    def _write_file(self, file_path, file_contents):
        # open the file
        file = open(file_path, "wb")

        try:
            # writes the file contents
            file.write(file_contents)
        finally:
            # closes the file
            file.close()
