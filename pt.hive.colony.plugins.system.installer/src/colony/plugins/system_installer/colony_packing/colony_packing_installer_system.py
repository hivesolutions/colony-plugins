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
import threading

import colony.libs.path_util

import colony_packing_installer_exceptions

INSTALLER_TYPE = "colony_packing"
""" The installer type """

ID_VALUE = "id"
""" The id value """

VERSION_VALUE = "version"
""" The version value """

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
        plugins_file_path = os.path.join(manager_path, "var/plugins.json")

        # creates a new file transaction context
        file_context = file_context or FileTransactionContext("c:\\transactions\\")

        # opens a new transaction in the file context
        file_context.open()

        try:
            # ------ HARDCODES ----------

            CPX_PATH = "c:\\test.cpx"

            # ----------------------------

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(CPX_PATH, {}, "colony")

            # retrieves the plugin id
            plugin_id = packing_information.get_property(ID_VALUE)

            # retrieves the plugin version
            plugin_version = packing_information.get_property(VERSION_VALUE)

            # ------------------------------------------------

            # TENHO DE CONTAR COM O CASE DE O FICHEIRO NAO EXISTIR

            # tenho de obter as informacoes sobre o cpx aki
            # e depois tenho de acrescentar essas informacoes ao plugins.json
            # tenho tb de verificar conflicto de plgugins
            # se tiver a mesma versao so com force posso eu fazer deploy

            # HARDCODES

            # -----------------------------------------

            # retrieves the flag properties values
            upgrade = properties.get("upgrade", True)
            force = properties.get("force", False)

            # -----------------------------------------------------

            # reads the plugin file contents
            plugins_file_contents = file_context.read_file(plugins_file_path)

            # loads the plugin file contents from json
            plugins = json_plugin.loads(plugins_file_contents)

            # retrieves the installed plugins
            installed_plugins = plugins.get("installed_plugins", {})

            # retrieves the installed plugin value
            installed_plugin = installed_plugins.get(plugin_id, {})

            # in case there is an installed plugin and the upgrade
            # flag is not set
            if installed_plugin and not upgrade:
                # raises the plugin installation error
                raise colony_packing_installer_exceptions.PluginInstallationError("plugin already installed")

            # retrieves the installed plugin version
            installed_plugin_version = installed_plugin.get("version", None)

            # in case the installed plugin version is the same as the
            # plugin version and the force flag is not set
            if installed_plugin_version == plugin_version and not force:
                # raises the plugin installation error
                raise colony_packing_installer_exceptions.PluginInstallationError("plugin version already installed")

            # --------------------------------------

            # retrieves the main plugin path
            main_plugin_path = plugin_manager.get_main_plugin_path()

            # retrieves the "virtual" main plugin path from the file context
            # this is necessary to ensure a transaction mode
            main_plugin_virtual_path = file_context.get_file_path(main_plugin_path)

            # deploys the package using the main plugin "virtual" path
            self._deploy_package(CPX_PATH, main_plugin_virtual_path)

            # --------------------------------------

            # retrieves the current time
            current_time = time.time()

            # retrieves the current date time
            current_date_time = datetime.datetime.utcnow()

            # formats the current date time
            current_date_time_formated = current_date_time.strftime("%d-%m-%Y %H:%M:%S")

            # sets the installed plugin map
            installed_plugins[plugin_id] = {"version" : plugin_version, "timestamp" : current_time}

            # updates the plugins map with the current time
            # and date time values
            plugins["last_modified_timestamp"] = current_time
            plugins["last_modified_date"] = current_date_time_formated

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
        properties = {"target_path" : target_path}

        # unpacks the files using the colony service
        packing_manager_plugin.unpack_files([package_path], properties, "colony")

class FileContext:
    """
    The file context class used to read and write
    contents from files.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def read_file(self, file_path):
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

    def write_file(self, file_path, file_contents):
        # creates the directory for the file path
        self._create_directory(file_path)

        # open the file
        file = open(file_path, "wb")

        try:
            # writes the file contents
            file.write(file_contents)
        finally:
            # closes the file
            file.close()

    def get_file_path(self, file_path):
        # returns the file path
        return file_path

    def _create_directory(self, file_path):
        # retrieves the directory path for the file path
        directory_path = os.path.dirname(file_path)

        # in case the directory path exists
        if os.path.exists(directory_path):
            # returns immediately
            return

        # creates the various required directories
        os.makedirs(directory_path)

class FileTransactionContext(FileContext):
    """
    The file transaction context class that controls
    a transaction involving the file system.
    """

    transaction_level = 0
    """ The current transaction level in use """

    temporary_path = None
    """ The temporary path to be used in the file transaction """

    target_path = None
    """ The target path """

    path_tuples_list = []
    """ The list of path tuples associated with the transaction """

    access_lock = None
    """ The lock controlling the access to the file transaction """

    def __init__(self, temporary_path):
        """
        Constructor of the class.

        @type temporary_path: String
        @param temporary_path: The temporary path to be used
        for the transaction temporary files.
        """

        FileContext.__init__(self)
        self.temporary_path = temporary_path

        self.path_tuples_list = []
        self.access_lock = threading.RLock()

    def write_file(self, file_path, file_contents):
        # retrieves the virtual file path for the file path
        virtual_file_path = self._get_virtual_file_path(file_path)

        # writes the file using the file context (virtual file path used)
        FileContext.write_file(self, virtual_file_path, file_contents)

        # creates a path tuple with the virtual file path
        # and the file path
        path_tuple = (virtual_file_path, file_path)

        # adds the path tuple
        self._add_path_tuple(path_tuple)

    def get_file_path(self, file_path):
        # retrieves the virtual file path for the file path
        virtual_file_path = self._get_virtual_file_path(file_path)

        # creates a path tuple with the virtual file path
        # and the file path
        path_tuple = (virtual_file_path, file_path)

        # adds the path tuple
        self._add_path_tuple(path_tuple)

        # returns the virtual file path
        return virtual_file_path

    def open(self):
        # acquires the access lock
        self.access_lock.acquire()

        try:
            # increments the transaction level
            self.transaction_level += 1
        finally:
            # releases the access lock
            self.access_lock.release()

    def commit(self):
        # acquires the access lock
        self.access_lock.acquire()

        try:
            # decrements the transaction level
            self.transaction_level -= 1

            # in case the transaction level is positive
            if self.transaction_level > 0:
                # returns immediately
                return
            # in case the transaction level is negative
            elif self.transaction_level < 0:
                # raises the runtime error
                raise RuntimeError("Invalid transaction level")

            # iterates over all the path tuples in
            # path tuples list
            for path_tuple in self.path_tuples_list:
                # unpacks the path tuple
                virtual_file_path, file_path = path_tuple

                # in case the virtual file path is a directory
                if os.path.isdir(virtual_file_path):
                    # copies the directory in the virtual path to the directory in the file path
                    colony.libs.path_util.copy_directory(virtual_file_path, file_path)
                # otherwise it must be a "normal" file
                else:
                    # copies the file in the virtual path to the file in the file path
                    colony.libs.path_util.copy_file(virtual_file_path, file_path)

            # runs the cleanup
            self._cleanup()
        finally:
            # empties the path tuples list
            self.path_tuples_list = []

            # resets the transaction level
            self.transaction_level = 0

            # releases the access lock
            self.access_lock.release()

    def rollback(self):
        # acquires the access lock
        self.access_lock.acquire()

        try:
            # runs the cleanup
            self._cleanup()
        finally:
            # empties the path tuples list
            self.path_tuples_list = []

            # resets the transaction level
            self.transaction_level = 0

            # releases the access lock
            self.access_lock.release()

    def _cleanup(self):
        # retrieves the temporary path items
        temporary_path_items = os.listdir(self.temporary_path)

        # iterates over all the temporary path items
        for temporary_path_item in temporary_path_items:
            # creates the temporary complete path item, by joining the
            # temporary path and the temporary path item
            temporary_complete_path_item = os.path.join(self.temporary_path, temporary_path_item)

            # in case the temporary item is a directory
            if os.path.isdir(temporary_complete_path_item):
                # removes the directory in the temporary
                # complete path item
                colony.libs.path_util.remove_directory(temporary_complete_path_item)
            # otherwise it must be a "normal" file
            else:
                # removes the temporary complete path item
                os.remove(temporary_complete_path_item)

    def _add_path_tuple(self, path_tuple):
        # adds the path tuple to the path tuples list
        self.path_tuples_list.append(path_tuple)

    def _get_virtual_file_path(self, file_path):
        # splits the file path into drive and
        # base file path
        _drive, base_file_path = os.path.splitdrive(file_path)

        # strips the base file path
        base_file_path = base_file_path.lstrip("\\/")

        # joins the temporary path and the
        # base file path
        virtual_file_path = os.path.join(self.temporary_path, base_file_path)

        # normalizes the virtual file path
        virtual_file_path = os.path.normpath(virtual_file_path)

        # returns the virtual file path
        return virtual_file_path
