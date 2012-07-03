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

__revision__ = "$LastChangedRevision: 7750 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-29 14:32:40 +0100 (seg, 29 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import zipfile

import colony.libs.string_buffer_util

ENGINE_NAME = "zip"
""" The engine name """

ZIP_FILE_EXTENSION = ".zip"
""" The zip file extension value """

class FileManagerZipEngine:
    """
    The file manager zip engine class.
    """

    file_manager_zip_engine_plugin = None
    """ The file manager zip engine plugin """

    def __init__(self, file_manager_zip_engine_plugin):
        """
        Constructor of the class

        @type file_manager_zip_engine_plugin: FileManagerZipEnginePlugin
        @param file_manager_zip_engine_plugin: The file manager  zip engine plugin.
        """

        self.file_manager_zip_engine_plugin = file_manager_zip_engine_plugin

    def get_engine_name(self):
        """
        Retrieves the name of the engine.

        @rtype: String
        @return: The name of the engine.
        """

        return ENGINE_NAME

    def get_internal_version(self):
        """
        Retrieves the internal database manager oriented
        version of the engine.

        @rtype: String
        @return: internal database manager oriented
        version of the engine.
        """

        return None

    def create_connection(self, connection_parameters):
        # retrieves the plugin manager
        plugin_manager = self.file_manager_zip_engine_plugin.manager

        # retrieves the connection parameters
        context_name = connection_parameters.get("context_name", "default")
        base_path = connection_parameters.get("base_path", "%configuration:" + self.file_manager_zip_engine_plugin.id + "%")

        # creates the zip file anme from the context name
        zip_file_name = context_name + ZIP_FILE_EXTENSION

        # creates the (full) base path by appending the zip file name and
        # resolves it (for configuration directories) using the plugin manager
        base_path = os.path.join(base_path, zip_file_name)
        base_path = plugin_manager.resolve_file_path(base_path, True, True)

        # creates the zip connection with the given
        # context name and base path
        zip_connection = ZipConnection(context_name, base_path)

        # returns the created (zip) connection
        return zip_connection

    def close_connection(self, connection):
        pass

    def get(self, connection, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the file name in the left separators
        file_name = file_name.lstrip("/")

        # opens the zip file for reading
        zip_file = zipfile.ZipFile(base_path, "r")

        try:
            # reads the target file data from
            # the zip file for the given file name
            target_file_data = zip_file.read(file_name)
        finally:
            # closes the zip file
            zip_file.close()

        # creates a new string buffer as the file buffer and
        # writes the target file data into it
        target_file = colony.libs.string_buffer_util.StringBuffer()
        target_file.write(target_file_data)

        # returns the target file
        return target_file

    def put(self, connection, file_path, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the file name in the left separators
        file_name = file_name.lstrip("/")

        # opens the zip file for appending
        zip_file = zipfile.ZipFile(base_path, "a")

        try:
            # writes the file in the given file path
            # to the zip file (put operation)
            zip_file.write(file_path, file_name)
        finally:
            # closes the zip file
            zip_file.close()

    def put_file(self, connection, file, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the file name in the left separators
        file_name = file_name.lstrip("/")

        # reads the contents from the (source)
        # file to the write them
        source_contents = file.read()

        # opens the zip file for appending
        zip_file = zipfile.ZipFile(base_path, "a")

        try:
            # writes the source contents read from the
            # file to the zip file (put operation)
            zip_file.writestr(file_name, source_contents)
        finally:
            # closes the zip file
            zip_file.close()

    def put_data(self, connection, data, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the file name in the left separators
        file_name = file_name.lstrip("/")

        # opens the zip file for appending
        zip_file = zipfile.ZipFile(base_path, "a")

        try:
            # writes the (received) data
            # to the zip file (put operation)
            zip_file.writestr(file_name, data)
        finally:
            # closes the zip file
            zip_file.close()

    def delete(self, connection, file_name):
        pass

    def list(self, connection, directory_name):
        pass

class ZipConnection:
    """
    The connection that holds the information, regarding
    the connection to the file system (zip) engine.
    """

    context_name = None
    """ The name of the persistence context """

    base_path = None
    """ The base path used for the zip file in the file system """

    def __init__(self, context_name, base_path):
        """
        Constructor of the class.

        @type context_name: String
        @param context_name: The name of the persistence context.
        @type base_path: String
        @param base_path: The base path for persistence.
        """

        self.context_name = context_name
        self.base_path = base_path
