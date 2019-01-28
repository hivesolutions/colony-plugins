#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class FileFsPlugin(colony.Plugin):
    """
    The main class for the File File System Engine plugin.
    """

    id = "pt.hive.colony.plugins.data.file.fs"
    name = "File File System Engine"
    description = "File File System Engine Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "file_engine"
    ]
    main_modules = [
        "file_fs"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import file_fs
        self.system = file_fs.FileFs(self)

    def get_engine_name(self):
        return self.system.get_engine_name()

    def get_internal_version(self):
        return self.system.get_internal_version()

    def create_connection(self, connection_parameters):
        return self.system.create_connection(connection_parameters)

    def close_connection(self, connection):
        return self.system.close_connection(connection)

    def get(self, connection, file_name):
        return self.system.get(connection, file_name)

    def put(self, connection, file_path, file_name):
        return self.system.put(connection, file_path, file_name)

    def put_file(self, connection, file, file_name):
        return self.system.put_file(connection, file, file_name)

    def put_data(self, connection, data, file_name):
        return self.system.put_data(connection, data, file_name)

    def delete(self, connection, file_name):
        return self.system.delete(connection, file_name)

    def list(self, connection, directory_name):
        return self.system.list(connection, directory_name)

    def size(self, connection, file_name):
        return self.system.size(connection, file_name)

    def mtime(self, connection, file_name):
        return self.system.mtime(connection, file_name)
