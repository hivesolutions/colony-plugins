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

import gridfs
import pymongo

import colony.base.system

ENGINE_NAME = "gridfs"
""" The engine name """

class FileGridfs(colony.base.system.System):
    """
    The file gridfs class.
    """

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

        return pymongo.version

    def create_connection(self, connection_parameters):
        # retrieves the connection parameters
        hostname = connection_parameters.get("hostname", "localhost")
        port = connection_parameters.get("port", 27017)
        database = connection_parameters.get("database", "test")

        # creates a new mongo connection
        # for file insertion and then retrieves the correct
        # database from it (as the connection)
        connection = pymongo.Connection(hostname, port)
        connection_database = connection[database]

        # creates the gridfs system from the connection
        # database reference
        gridfs_sytem = gridfs.GridFS(connection_database)

        # returns the gridfs system as the connection
        return gridfs_sytem

    def close_connection(self, connection):
        pass

    def get(self, connection, file_name):
        # retrieves the base file connection as the
        # gridfs system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the file name
        # in case it's necessary
        file_name = file_name.startswith("/") and file_name or "/" + file_name

        # retrieves the (last version) target file from the
        # given file name, from the gridfs system
        target_file = gridfs_sytem.get_last_version(file_name)

        # returns the target file
        return target_file

    def put(self, connection, file_path, file_name):
        # retrieves the base file connection as the
        # gridfs system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the file name
        # in case it's necessary
        file_name = file_name.startswith("/") and file_name or "/" + file_name

        # opens the source file for binary
        # reading (fast reading)
        source_file = open(file_path, "rb")

        try:
            # reads the contents from the source file
            # and writes them to the target file in the
            # gridfs system
            source_contents = source_file.read()
            gridfs_sytem.put(source_contents, filename = file_name)
        finally:
            # closes the source file (safe closing)
            source_file.close()

    def put_file(self, connection, file, file_name):
        # retrieves the base file connection as the
        # gridfs system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the file name
        # in case it's necessary
        file_name = file_name.startswith("/") and file_name or "/" + file_name

        # reads the contents from the (source) file
        # and writes them to the target file in the
        # gridfs system
        source_contents = file.read()
        gridfs_sytem.put(source_contents, filename = file_name)

    def put_data(self, connection, data, file_name):
        # retrieves the base file connection as the
        # gridfs system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the file name
        # in case it's necessary
        file_name = file_name.startswith("/") and file_name or "/" + file_name

        # writes the data to the target file in the
        # gridfs system
        gridfs_sytem.put(data, filename = file_name)

    def delete(self, connection, file_name):
        # retrieves the base file connection as the
        # gridfs system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the file name
        # in case it's necessary
        file_name = file_name.startswith("/") and file_name or "/" + file_name

        # retrieves the file for the given file
        # to retrieve the file id
        file = self.get(connection, file_name)
        file_id = file._id

        # deletes the file with the given file id
        gridfs_sytem.delete(file_id)

    def list(self, connection, directory_name):
        # retrieves the base file connection as the
        # gridfs system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the directory name
        # in case it's necessary
        directory_name = directory_name.startswith("/") and directory_name or "/" + directory_name

        # sets the directory name according to the default separator value
        directory_name = directory_name.endswith("/") and directory_name or directory_name + "/"

        # retrieves the file name list from the
        # gridfs system and filters the values
        # based on the directory name prefix
        file_name_list = gridfs_sytem.list()
        file_name_list = [value[len(directory_name):] for value in file_name_list if value.startswith(directory_name)]
        file_name_list = [value for value in file_name_list if value.find("/") == -1]

        # returns the file name list
        return file_name_list
