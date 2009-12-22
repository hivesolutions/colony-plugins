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

__author__ = "Jo�o Magalh�es <joamag@hive.pt> & Lu�s Martinho <lmartinho@hive.pt>"
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

class SearchIndexRepositoryPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Search Index Repository plugin.
    """

    id = "pt.hive.colony.plugins.search.index_repository"
    name = "Search Index Repository Plugin"
    short_name = "Search Index Repository"
    description = "Search Index Repository Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["search_index_repository"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    search_index_repository = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global search
        import search.index_repository.search_index_repository_system
        self.search_index_repository = search.index_repository.search_index_repository_system.SearchIndexRepository(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def add_index(self, search_index, search_index_identifier):
        return self.search_index_repository.add_index(search_index, search_index_identifier)

    def remove_index(self, search_index_identifier):
        return self.search_index_repository.remove_index(search_index_identifier)

    def get_index(self, search_index_identifier):
        return self.search_index_repository.get_index(search_index_identifier)

    def get_index_identifiers(self):
        return self.search_index_repository.get_index_identifiers()

    def get_indexes(self):
        return self.search_index_repository.get_indexes()

    def get_index_metadata(self, search_index_identifier):
        return self.search_index_repository.get_index_metadata(search_index_identifier)

    def get_indexes_metadata(self):
        return self.search_index_repository.get_indexes_metadata()
