#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os

import colony

ENGINE_NAME = "fs"
""" The engine name """

BUFFER_SIZE = 4096
""" The size of the buffer for writing, this values
is relevant for the performance of that operation as
a small value would imply many operations and a large
value may require a large amount of memory"""


class FileFS(colony.System):
    """
    The File FS class, that implements the access to
    the file system according to the "generic" file
    engine interface definition.
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

        # creates the (full) base path by appending the context name and
        # resolves it (for configuration directories) using the plugin manager
        base_path = os.path.join(base_path, context_name)
        base_path = plugin_manager.resolve_file_path(base_path, True, True)

        # creates the required (base_path) directories for the
        # file system persistence
        if not os.path.isdir(base_path):
            os.makedirs(base_path)

        # creates the (FS) connection with the given
        # context name and base path
        fs_connection = FsConnection(context_name, base_path)

        # returns the created (FS) connection
        return fs_connection

    def close_connection(self, connection):
        pass

    def get(self, connection, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the extra path separator values
        # (avoids problems working with the file system)
        file_name = file_name.lstrip("/")

        # creates the target file path from the base path
        # and then opens the target file for reading using it
        target_file_path = os.path.join(base_path, file_name)
        target_file_path = os.path.normpath(target_file_path)
        target_file = open(target_file_path, "rb")

        # returns the opened target file
        return target_file

    def delete(self, connection, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the extra path separator values
        # (avoids problems working with the file system)
        file_name = file_name.lstrip("/")

        # creates the target file path from the base path
        # and removes it from the file system
        target_file_path = os.path.join(base_path, file_name)
        target_file_path = os.path.normpath(target_file_path)
        os.remove(target_file_path)

    def put(self, connection, file_path, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the extra path separator values
        # (avoids problems working with the file system)
        file_name = file_name.lstrip("/")

        # retrieves the (base) file name and constructs
        # the complete target file path based on it
        target_file_path = os.path.join(base_path, file_name)
        target_file_path = os.path.normpath(target_file_path)

        # retrieves the target directory path and creates
        # if if it does not already exists
        target_directory_path = os.path.dirname(target_file_path)
        if not os.path.isdir(target_directory_path):
            os.makedirs(target_directory_path)

        # opens both the source and target files
        # for binary reading and writing
        source_file = open(file_path, "rb")
        target_file = open(target_file_path, "wb")

        try:
            # iterates continuously for file copying
            # (copies a chunk for each iteration)
            while True:
                # retrieves a chunk from the source file
                source_chunk = source_file.read(BUFFER_SIZE)

                # in case no source chunk could be read
                if not source_chunk:
                    # breaks the loop (no more
                    # data to be copied)
                    break

                # writes the source chunk to the target
                # file (copy)
                target_file.write(source_chunk)
        finally:
            # closes the source and target files
            # (safe closing)
            source_file.close()
            target_file.close()

    def put_file(self, connection, file, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the extra path separator values
        # (avoids problems working with the file system)
        file_name = file_name.lstrip("/")

        # retrieves the (base) file name and constructs
        # the complete target file path based on it
        target_file_path = os.path.join(base_path, file_name)
        target_file_path = os.path.normpath(target_file_path)

        # retrieves the target directory path and creates
        # if if it does not already exists
        target_directory_path = os.path.dirname(target_file_path)
        if not os.path.isdir(target_directory_path):
            os.makedirs(target_directory_path)

        # opens target file for writing
        target_file = open(target_file_path, "wb")

        try:
            # iterates continuously for file copying
            # (copies a chunk for each iteration)
            while True:
                # retrieves a chunk from the (source) file
                source_chunk = file.read(BUFFER_SIZE)

                # in case no source chunk could be read
                if not source_chunk:
                    # breaks the loop (no more
                    # data to be copied)
                    break

                # writes the source chunk to the target
                # file (copy)
                target_file.write(source_chunk)
        finally:
            # closes target file (safe closing)
            target_file.close()

    def put_data(self, connection, data, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the extra path separator values
        # (avoids problems working with the file system)
        file_name = file_name.lstrip("/")

        # retrieves the (base) file name and constructs
        # the complete target file path based on it
        target_file_path = os.path.join(base_path, file_name)
        target_file_path = os.path.normpath(target_file_path)

        # retrieves the target directory path and creates
        # if if it does not already exists
        target_directory_path = os.path.dirname(target_file_path)
        if not os.path.isdir(target_directory_path):
            os.makedirs(target_directory_path)

        # opens target file for writing
        target_file = open(target_file_path, "wb")

        try:
            # writes the data to the target
            # file (copy)
            target_file.write(data)
        finally:
            # closes target file (safe closing)
            target_file.close()

    def list(self, connection, directory_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the extra path separator values
        # (avoids problems working with the file system)
        directory_name = directory_name.lstrip("/")

        # creates the full directory name from the base
        # path and the directory name
        full_directory_name = os.path.join(base_path, directory_name)

        # list the directory entries from the directory
        file_name_list = os.listdir(full_directory_name)

        # returns the file name list
        return file_name_list

    def size(self, connection, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the extra path separator values
        # (avoids problems working with the file system)
        file_name = file_name.lstrip("/")

        # creates the target file path from the base path
        # and uses it to retrieve the size of the file (in bytes)
        target_file_path = os.path.join(base_path, file_name)
        target_file_path = os.path.normpath(target_file_path)
        return os.path.getsize(target_file_path)

    def mtime(self, connection, file_name):
        # retrieves the base file connection and
        # then uses it to retrieve the base path
        file_connection = connection.file_connection
        base_path = file_connection.base_path

        # strips the extra path separator values
        # (avoids problems working with the file system)
        file_name = file_name.lstrip("/")

        # creates the target file path from the base path
        # and uses it to retrieve the modification timestamp
        target_file_path = os.path.join(base_path, file_name)
        target_file_path = os.path.normpath(target_file_path)
        return os.path.getmtime(target_file_path)


class FsConnection(object):
    """
    The connection that holds the information, regarding
    the connection to the file system (FS) engine.
    """

    context_name = None
    """ The name of the persistence context """

    base_path = None
    """ The base path used for the persistence
    for the files in the file system """

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
