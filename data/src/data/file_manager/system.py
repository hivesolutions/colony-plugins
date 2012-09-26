#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

import colony.base.system

class DataFileManager(colony.base.system.System):
    """
    The data file manager class.
    """

    file_manager_plugin = None
    """ The file manager plugin """

    file_engine_plugins_map = {}
    """ The map of file engine plugins """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        self.file_engine_plugins_map = {}

    def load_file_manager(self, engine_name, properties = {}):
        """
        Loads an file manager for the given engine name.
        The loading of an file manager may return an existing
        instance in case an file manager with the same id is
        already loaded.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @type properties: Dictionary
        @param properties: The properties to be used in the
        loading of the file manager.
        @rtype: FileManager
        @return: The loaded file manager.
        """

        # prints a debug message
        self.plugin.debug("Loading new file manager with engine: %s" % engine_name)

        # retrieves the file mager engine plugin
        file_engine_plugin = self.file_engine_plugins_map[engine_name]

        # creates a new file manager with the file engine plugin, file classes list
        # and the file classes map
        file_manager = FileManager(file_engine_plugin)

        # returns the file manager
        return file_manager

    def register_file_engine_plugin(self, file_engine_plugin):
        # retrieves the plugin engine name and sets the file
        # engine plugin in the file engine plugins map
        engine_name = file_engine_plugin.get_engine_name()
        self.file_engine_plugins_map[engine_name] = file_engine_plugin

    def unregister_file_engine_plugin(self, file_engine_plugin):
        # retrieves the plugin engine name and removes the
        # file engine plugin from the file engine plugins map
        engine_name = file_engine_plugin.get_engine_name()
        del self.file_engine_plugins_map[engine_name]

class FileManager:
    """
    The file manager class.
    This class is responsible for the coordination of
    the underlying driver for file access.
    """

    file_engine_plugin = None
    """ The file engine plugin """

    connection = None
    """ The current available (global) connection """

    file_connection = None
    """ The current available file connection """

    connection_parameters = {}
    """ The map containing the connection parameters """

    def __init__(self, file_engine_plugin):
        """
        Constructor of the class.

        @type file_engine_plugin: FileManagerEnginePlugin
        @param file_engine_plugin: The engine file manager plugin to be used.
        """

        self.file_engine_plugin = file_engine_plugin

        self.connection_parameters = {}

    def get_engine_name(self):
        """
        Retrieves the engine name for the current
        connection.

        @rtype: String
        @return: The engine name for the current
        connection.
        """

        return self.file_engine_plugin.get_engine_name()

    def get_internal_version(self):
        """
        Retrieves the internal version for the current
        connection.

        @rtype: String
        @return: The internal version for the current
        connection.
        """

        return self.file_engine_plugin.get_internal_version()

    def get_connection(self):
        """
        Retrieves the current available connection.

        @rtype: Connection
        @return: The current available file connection.
        """

        # in case the connection is not defined
        if not self.connection:
            # retrieves the file connection
            file_connection = self.get_file_connection()

            # creates the connection object with the specified file connection
            # and connection parameters (the file manager reference is also sent)
            self.connection = Connection(self, file_connection, self.connection_parameters)

        # returns the current connection
        return self.connection

    def close_connection(self):
        """
        Closes the current available connection.
        """

        # closes the file connection
        self.close_file_connection()

    def get_file_connection(self):
        """
        Retrieves the current available file connection.

        @rtype: Connection
        @return: The current available file connection.
        """

        if not self.file_connection:
            # creates the file connection to the specified engine with the
            # specified connection parameters
            self.file_connection = self.file_engine_plugin.create_connection(self.connection_parameters)

        return self.file_connection

    def close_file_connection(self):
        """
        Closes the current available file connection.
        """

        # retrieves the file connection
        file_connection = self.get_file_connection()

        # closes the file connection to the specified engine
        self.file_engine_plugin.close_connection(file_connection)

    def set_connection_parameters(self, connection_parameters):
        """
        Sets the connection parameters of the entity manager.
        The connection parameters are used to established the connection
        with the file endpoint.

        @type connection_parameters: Dictionary
        @param connection_parameters: The map containing the connection parameters.
        """

        self.connection_parameters = connection_parameters

    def get(self, file_name):
        # retrieves the connection object
        connection = self.get_connection()

        return self.file_engine_plugin.get(connection, file_name)

    def put(self, file_path, file_name = None):
        # retrieves the connection object
        connection = self.get_connection()

        # sets the file name (target path) as the base
        # file path name in case no file name is defined
        file_name = file_name or os.path.basename(file_path)

        return self.file_engine_plugin.put(connection, file_path, file_name)

    def put_file(self, file, file_name):
        # retrieves the connection object
        connection = self.get_connection()

        return self.file_engine_plugin.put_file(connection, file, file_name)

    def put_data(self, data, file_name):
        # retrieves the connection object
        connection = self.get_connection()

        return self.file_engine_plugin.put_data(connection, data, file_name)

    def delete(self, file_name):
        # retrieves the connection object
        connection = self.get_connection()

        return self.file_engine_plugin.delete(connection, file_name)

    def list(self, directory_name):
        # retrieves the connection object
        connection = self.get_connection()

        return self.file_engine_plugin.list(connection, directory_name)

class Connection:
    """
    The class representing a data source (file)
    connection with the associated attributes.
    """

    file_manager = None
    """ The reference to the "owner" file manager """

    file_connection = None
    """ The file connection object """

    connection_parameters = {}
    """ The connection parameters for the connection """

    def __init__(self, file_manager, file_connection, connection_parameters):
        """
        Constructor of the class.

        @type file_manager: FileManager
        @param file_manager: The reference to the "owner" file manager.
        @type file_connection: FileConnection
        @param file_connection: The file connection object.
        @type connection_parameters: Dictionary
        @param connection_parameters: The connection parameters for the connection.
        """

        self.file_connection = file_connection
        self.connection_parameters = connection_parameters

    def add_conection_parameter(self, key, value):
        """
        Adds a parameter to the connection.

        @type key: String
        @param key: The name of the parameter to be added.
        @type value: Object
        @param value: The parameter value to be added.
        """

        self.connection_parameters[key] = value

    def remove_connection_parameter(self, key):
        """
        Removes the parameter with the given name
        from the connection parameters.

        @type key: String
        @param key: The name of the parameter to be removed.
        """

        del self.connection_parameters[key]

    def get_connection_parameter(self, key):
        """
        Retrieves the parameter with the given name
        from the connection.

        @type key: String
        @param key: The name of the parameter to be
        retrieved.
        @rtype: Object
        @return: The retrieved parameter.
        """

        return self.connection_parameters.get(key, None)
