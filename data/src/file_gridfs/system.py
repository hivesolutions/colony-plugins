#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import gridfs
import pymongo

import colony

ENGINE_NAME = "gridfs"
""" The engine name """

class FileGridFS(colony.System):
    """
    The file GridFS class.
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

        return pymongo.version

    def create_connection(self, connection_parameters):
        # retrieves the connection parameters
        hostname = connection_parameters.get("hostname", "localhost")
        port = connection_parameters.get("port", 27017)
        database = connection_parameters.get("database", "test")

        # creates a new MongoDB connection
        # for file insertion and then retrieves the correct
        # database from it (as the connection)
        is_new = int(pymongo.version[0]) >= 3
        if is_new: connection = pymongo.MongoClient(hostname, port)
        else: connection = pymongo.Connection(hostname, port) #@UndefinedVariable
        connection_database = connection[database]

        # creates the GridFS system from the connection
        # database reference
        gridfs_sytem = gridfs.GridFS(connection_database)

        # returns the GridFS system as the connection
        return gridfs_sytem

    def close_connection(self, connection):
        pass

    def get(self, connection, file_name):
        # retrieves the base file connection as the
        # GridFS system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the file name
        # in case it's necessary
        file_name = file_name.startswith("/") and file_name or "/" + file_name

        # retrieves the (last version) target file from the
        # given file name, from the GridFS system
        target_file = gridfs_sytem.get_last_version(file_name)

        # returns the target file
        return target_file

    def put(self, connection, file_path, file_name):
        # retrieves the base file connection as the
        # GridFS system
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
            # GridFS system
            source_contents = source_file.read()
            gridfs_sytem.put(source_contents, filename = file_name)
        finally:
            # closes the source file (safe closing)
            source_file.close()

    def put_file(self, connection, file, file_name):
        # retrieves the base file connection as the
        # GridFS system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the file name
        # in case it's necessary
        file_name = file_name.startswith("/") and file_name or "/" + file_name

        # reads the contents from the (source) file
        # and writes them to the target file in the
        # GridFS system
        source_contents = file.read()
        gridfs_sytem.put(source_contents, filename = file_name)

    def put_data(self, connection, data, file_name):
        # retrieves the base file connection as the
        # GridFS system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the file name
        # in case it's necessary
        file_name = file_name.startswith("/") and file_name or "/" + file_name

        # writes the data to the target file in the
        # GridFS system
        gridfs_sytem.put(data, filename = file_name)

    def delete(self, connection, file_name):
        # retrieves the base file connection as the
        # GridFS system
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
        # GridFS system
        gridfs_sytem = connection.file_connection

        # adds the path separator value to the directory name
        # in case it's necessary
        directory_name = directory_name.startswith("/") and directory_name or "/" + directory_name

        # sets the directory name according to the default separator value
        directory_name = directory_name.endswith("/") and directory_name or directory_name + "/"

        # retrieves the file name list from the
        # GridFS system and filters the values
        # based on the directory name prefix
        file_name_list = gridfs_sytem.list()
        file_name_list = [value[len(directory_name):] for value in file_name_list if value.startswith(directory_name)]
        file_name_list = [value for value in file_name_list if value.find("/") == -1]

        # returns the file name list
        return file_name_list

    def size(self, connection, file_name):
        pass

    def mtime(self, connection, file_name):
        pass
