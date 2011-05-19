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

class SpecificationGeneratorPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Specification Generator plugin.
    """

    id = "pt.hive.colony.plugins.specifications.specification_generator"
    name = "Specification Generator Plugin"
    short_name = "Specification Generator"
    description = "Plugin used to generate specification files from the source plugin files"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/specifications/specification_generator/resources/baf.xml"
    }
    capabilities = [
        "specification_generator",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "specification_generator_handler"
    ]
    main_modules = [
        "specifications.specification_generator.specification_generator_exceptions",
        "specifications.specification_generator.specification_generator_system"
    ]

    specification_generator = None
    """ The specification generator """

    specification_generator_handler_plugins = []
    """ The specification generator handler plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import specifications.specification_generator.specification_generator_system
        self.specification_generator = specifications.specification_generator.specification_generator_system.SepecificationGenerator(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.specifications.specification_generator", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.specifications.specification_generator", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def generate_plugin_specification(self, plugin_id, plugin_version, properties, file_path):
        """
        Generates a specification file describing the structure
        and specification of the plugin with the given id and version.
        The file is generated using the plugin internal information and
        is stored in the given file path.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be used for
        specification generation.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be used for
        specification generation.
        @type properties: Dictionary
        @param properties: The properties for plugin specification generation.
        @type file_path: String
        @param file_path: The path to store the file being generated.
        """

        return self.specification_generator.generate_plugin_specification(plugin_id, plugin_version, properties, file_path)

    def generate_plugin_specification_file_buffer(self, plugin_id, plugin_version, properties):
        """
        Generates a specification file describing the structure
        and specification of the plugin with the given id and version.
        The file is generated using the plugin internal information and
        is returned in a file buffer.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be used for
        specification generation.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be used for
        specification generation.
        @type properties: Dictionary
        @param properties: The properties for plugin specification generation.
        @rtype: File
        @return: The generated specification file.
        """

        return self.specification_generator.generate_plugin_specification_file_buffer(plugin_id, plugin_version, properties)

    @colony.base.decorators.load_allowed_capability("specification_generator_handler")
    def specification_generator_handler_capability_load_allowed(self, plugin, capability):
        self.specification_generator_handler_plugins.append(plugin)
        self.specification_generator.specification_generator_handler_load(plugin)

    @colony.base.decorators.unload_allowed_capability("specification_generator_handler")
    def specification_generator_handler_capability_unload_allowed(self, plugin, capability):
        self.specification_generator_handler_plugins.remove(plugin)
        self.specification_generator.specification_generator_handler_unload(plugin)
