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

import colony.base.plugin_system

class FileManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the File Manager plugin.
    """

    id = "pt.hive.colony.plugins.data.file_manager"
    name = "File Manager Plugin"
    short_name = "Data File Manager"
    description = "The plugin that manages the file system abstraction sub system"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/data/file_manager/resources/baf.xml"
    }
    capabilities = [
        "file_manager",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "file_manager_engine"
    ]
    main_modules = [
        "data.file_manager.file_manager_system"
    ]

    file_manager = None
    """ The file manager """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import data.file_manager.file_manager_system
        self.file_manager = data.file_manager.file_manager_system.DataFileManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_file_manager(self, engine_name):
        """
        Loads an file manager for the given engine name.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @rtype: FileManager
        @return: The loaded file manager.
        """

        return self.file_manager.load_file_manager(engine_name)

    def load_file_manager_properties(self, engine_name, properties):
        """
        Loads an file manager for the given engine name.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @type properties: Dictionary
        @param properties: The properties to be used in the
        loading of the file manager
        @rtype: FileManager
        @return: The loaded file manager.
        """

        return self.file_manager.load_file_manager(engine_name, properties)

    @colony.base.decorators.load_allowed_capability("file_manager_engine")
    def file_manager_engine_load_allowed(self, plugin, capability):
        self.file_manager.register_file_manager_engine_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("file_manager_engine")
    def file_manager_engine_unload_allowed(self, plugin, capability):
        self.file_manager.unregister_file_manager_engine_plugin(plugin)
