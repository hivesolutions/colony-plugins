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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class SearchProcessorPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Search Processor plugin.
    """

    id = "pt.hive.colony.plugins.search.processor"
    name = "Search Processor Plugin"
    short_name = "Search Processor"
    description = "Plugin that provides the interface with processor adapters for the main search plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/search_processor/processor/resources/baf.xml"
    }
    capabilities = [
        "search_processor",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "search_processor_adapter"
    ]
    main_modules = [
        "search_processor.processor.search_processor_exceptions",
        "search_processor.processor.search_processor_system"
    ]

    search_processor = None
    """ The search processor """

    search_processor_adapter_plugins = []
    """ The search processor adapter plugins """

    search_provider_file_system_plugins = []
    """ The search provider file system plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global search_processor
        import search_processor.processor.search_processor_system
        self.search_processor = search_processor.processor.search_processor_system.SearchProcessor(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.search.processor", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.search.processor", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def process_results(self, search_results, properties):
        return self.search_processor.process_results(search_results, properties)

    def get_search_processor_adapter_types(self):
        return self.search_processor.get_search_processor_adapter_types()

    @colony.base.decorators.load_allowed_capability("search_processor_adapter")
    def search_processor_adapter_load_allowed(self, plugin, capability):
        self.search_processor_adapter_plugins.append(plugin)
        self.search_processor.add_search_processor_adapter_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("search_processor_adapter")
    def search_processor_adapter_unload_allowed(self, plugin, capability):
        self.search_processor_adapter_plugins.remove(plugin)
        self.search_processor.remove_search_processor_adapter_plugin(plugin)
