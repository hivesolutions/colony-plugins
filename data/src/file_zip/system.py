#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import zipfile

import colony

ENGINE_NAME = "zip"
""" The engine name """

ZIP_FILE_EXTENSION = ".zip"
""" The zip file extension value """


class FileZip(colony.System):
    """
    The file zip class.
    """

    def get_engine_name(self):
        """
        Retrieves the name of the engine.

        :rtype: String
        :return: The name of the engine.
        """

        return ENGINE_NAME

    def get_internal_version(self):
        """
        Retrieves the internal database manager oriented
        version of the engine.

        :rtype: String
        :return: internal database manager oriented
        version of the engine.
        """

        return None

    def create_connection(self, connection_parameters):
        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the connection parameters
        context_name = connection_parameters.get("context_name", "default")
        base_path = connection_parameters.get(
            "base_path", "%configuration:" + self.plugin.id + "%"
        )

        # creates the zip file name from the context name
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
        zip_file = zipfile.ZipFile(base_path, mode="r")

        try:
            # reads the target file data from
            # the zip file for the given file name
            target_file_data = zip_file.read(file_name)
        finally:
            # closes the zip file
            zip_file.close()

        # creates a new string buffer as the file buffer and
        # writes the target file data into it
        target_file = colony.StringBuffer()
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
        zip_file = zipfile.ZipFile(base_path, mode="a", allowZip64=True)

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
        zip_file = zipfile.ZipFile(base_path, mode="a", allowZip64=True)

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
        zip_file = zipfile.ZipFile(base_path, mode="a", allowZip64=True)

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

    def size(self, connection, file_name):
        pass

    def mtime(self, connection, file_name):
        pass

    def exists(self, connection, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the file name in the left separators
        file_name = file_name.lstrip("/")

        # in case the zip file does not exist there's no
        # file to be found in it (nothing has been put)
        if not os.path.exists(base_path):
            return False

        # opens the zip file for reading
        zip_file = zipfile.ZipFile(base_path, mode="r")

        try:
            # verifies if the file name is one of the
            # names of the files contained in the zip file
            exists = file_name in zip_file.namelist()
        finally:
            # closes the zip file
            zip_file.close()

        # returns if the file exists in the zip file
        return exists

    def exists_directory(self, connection, directory_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the directory name in the left separators
        directory_name = directory_name.lstrip("/")

        # in case the zip file does not exist there's no
        # directory to be found in it (nothing has been put)
        if not os.path.exists(base_path):
            return False

        # the root directory exists as soon as the zip
        # file exists, there's nothing else to verify
        if not directory_name:
            return True

        # sets the directory name according to the default separator
        # value, so that it's used as the prefix of the file names
        directory_name = (
            directory_name.endswith("/") and directory_name or directory_name + "/"
        )

        # opens the zip file for reading
        zip_file = zipfile.ZipFile(base_path, mode="r")

        try:
            # retrieves the names of the files contained in the zip
            # file and filters the values based on the directory name
            # prefix (the files contained in the directory)
            file_name_list = zip_file.namelist()
            file_name_list = [
                value for value in file_name_list if value.startswith(directory_name)
            ]
        finally:
            # closes the zip file
            zip_file.close()

        # returns if the directory exists in the zip file, meaning
        # that there's at least one file contained in it
        return True if file_name_list else False


class ZipConnection(object):
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

        :type context_name: String
        :param context_name: The name of the persistence context.
        :type base_path: String
        :param base_path: The base path for persistence.
        """

        self.context_name = context_name
        self.base_path = base_path
