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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
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

import colony.plugins.plugin_system

class SearchIndexPersistenceFileSystemPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Search Index Persistence File System plugin.
    """

    id = "pt.hive.colony.plugins.search.index_persistence.file_system"
    name = "Search Index Persistence File System plugin"
    short_name = "Search Index Persistence File System"
    description = "Search Index Persistence File System Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["search_index_persistence"]
    capabilities_allowed = ["search_index_serializer"]
    dependencies = []
    events_handled = []
    events_registrable = []

    search_index_persistence_file_system = None

    search_index_serializer_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global search_index_persistence
        import search_index_persistence.file_system.search_index_persistence_file_system_system
        self.search_index_persistence_file_system = search_index_persistence.file_system.search_index_persistence_file_system_system.SearchIndexPersistenceFileSystem(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.search.index_persistence.file_system", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.search.index_persistence.file_system", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_type(self):
        return self.search_index_persistence_file_system.get_type()

    def persist_index(self, search_index, properties):
        return self.search_index_persistence_file_system.persist_index(search_index, properties)

    def load_index(self, properties):
        return self.search_index_persistence_file_system.load_index(properties)

    @colony.plugins.decorators.load_allowed_capability("search_index_serializer")
    def search_provider_file_system_load_allowed(self, plugin, capability):
        self.search_index_serializer_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("search_index_serializer")
    def search_provider_file_system_unload_allowed(self, plugin, capability):
        self.search_index_serializer_plugins.remove(plugin)
