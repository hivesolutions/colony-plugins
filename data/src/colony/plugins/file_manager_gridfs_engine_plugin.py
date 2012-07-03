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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class FileManagerGridfsEnginePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the File Manager Gridfs Engine plugin.
    """

    id = "pt.hive.colony.plugins.data.file_manager.gridfs_engine"
    name = "File Manager Gridfs Engine Plugin"
    short_name = "File Manager Gridfs Engine"
    description = "File Manager Gridfs Engine Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/data/file_manager_gridfs_engine/resources/baf.xml"
    }
    capabilities = [
        "file_manager_engine",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PackageDependency("MongoDB python bindings", "pymongo", "1.6.x", "http://mongodb.org"),
        colony.base.plugin_system.PackageDependency("MongoDB GridFS python bindings", "gridfs", "1.6.x", "http://mongodb.org")
    ]
    main_modules = [
        "data.file_manager_gridfs_engine.file_manager_gridfs_engine_system"
    ]

    file_manager_gridfs_engine = None
    """ The file manager gridfs engine """

    business_helper_plugin = None
    """ The business helper plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import data.file_manager_gridfs_engine.file_manager_gridfs_engine_system
        self.file_manager_gridfs_engine = data.file_manager_gridfs_engine.file_manager_gridfs_engine_system.FileManagerGridfsEngine(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_engine_name(self):
        return self.file_manager_gridfs_engine.get_engine_name()

    def get_internal_version(self):
        return self.file_manager_gridfs_engine.get_internal_version()

    def create_connection(self, connection_parameters):
        return self.file_manager_gridfs_engine.create_connection(connection_parameters)

    def close_connection(self, connection):
        return self.file_manager_gridfs_engine.close_connection(connection)

    def get(self, connection, file_name):
        return self.file_manager_gridfs_engine.get(connection, file_name)

    def put(self, connection, file_path, file_name):
        return self.file_manager_gridfs_engine.put(connection, file_path, file_name)

    def put_file(self, connection, file, file_name):
        return self.file_manager_gridfs_engine.put_file(connection, file, file_name)

    def put_data(self, connection, data, file_name):
        return self.file_manager_gridfs_engine.put_data(connection, data, file_name)

    def delete(self, connection, file_name):
        return self.file_manager_gridfs_engine.delete(connection, file_name)

    def list(self, connection, directory_name):
        return self.file_manager_gridfs_engine.list(connection, directory_name)
