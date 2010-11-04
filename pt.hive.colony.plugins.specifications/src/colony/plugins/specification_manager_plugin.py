#!/usr/bin/python
# -*- coding: Cp1252 -*-

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

__revision__ = "$LastChangedRevision: 429 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-21 13:03:27 +0000 (Sex, 21 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class SpecificationManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Specification Manager plugin.
    """

    id = "pt.hive.colony.plugins.specifications.specification_manager"
    name = "Specification Manager Plugin"
    short_name = "Specification Manager"
    description = "Plugin used to retrieve specification from plugin description file"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/specifications/specification_manager/resources/baf.xml"}
    capabilities = ["specification_manager", "build_automation_item"]
    capabilities_allowed = ["specification_parser"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["specifications.specification_manager.specification_manager_exceptions",
                    "specifications.specification_manager.specification_manager_system"]

    specification_manager = None

    specification_parser_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global specifications
        import specifications.specification_manager.specification_manager_system
        self.specification_manager = specifications.specification_manager.specification_manager_system.SepecificationManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.specifications.specification_manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.specifications.specification_manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_plugin_specification(self, file_path, properties):
        """
        Retrieves a structure describing the structure and specification
        of a plugin. This structure is created from the given file and
        using the given properties.

        @type file_path: String
        @param file_path: The path to the specification file.
        @type properties: Dictionary
        @param properties: The properties for the file parsing.
        """

        return self.specification_manager.get_plugin_specification(file_path, properties)

    def get_plugin_specification_file_buffer(self, file_buffer, properties):
        """
        Retrieves a structure describing the structure and specification
        of a plugin. This structure is created from the given file buffer and
        using the given properties.

        @type file_buffer: String
        @param file_buffer: The buffer to the specification file.
        @type properties: Dictionary
        @param properties: The properties for the file parsing.
        """

        return self.specification_manager.get_plugin_specification_file_buffer(file_buffer, properties)

    @colony.base.decorators.load_allowed_capability("specification_parser")
    def specification_parser_capability_load_allowed(self, plugin, capability):
        self.specification_parser_plugins.append(plugin)
        self.specification_manager.specification_parser_load(plugin)

    @colony.base.decorators.unload_allowed_capability("specification_parser")
    def specification_parser_capability_unload_allowed(self, plugin, capability):
        self.specification_parser_plugins.remove(plugin)
        self.specification_manager.specification_parser_unload(plugin)
