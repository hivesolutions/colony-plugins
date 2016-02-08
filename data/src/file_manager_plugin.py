#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class FileManagerPlugin(colony.Plugin):
    """
    The main class for the File Manager plugin.
    """

    id = "pt.hive.colony.plugins.data.file.manager"
    name = "File Manager"
    description = "The plugin that manages the file system abstraction sub system"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "file_manager"
    ]
    capabilities_allowed = [
        "file_engine"
    ]
    main_modules = [
        "file_manager"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import file_manager
        self.system = file_manager.DataFileManager(self)

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    def load_file_manager(self, engine_name):
        """
        Loads an file manager for the given engine name.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @rtype: FileManager
        @return: The loaded file manager.
        """

        return self.system.load_file_manager(engine_name)

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

        return self.system.load_file_manager(engine_name, properties)

    @colony.load_allowed_capability("file_engine")
    def file_engine_load_allowed(self, plugin, capability):
        self.system.register_file_engine_plugin(plugin)

    @colony.unload_allowed_capability("file_engine")
    def file_engine_unload_allowed(self, plugin, capability):
        self.system.unregister_file_engine_plugin(plugin)
