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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import search_index_persistence_file_system_adapter_exceptions

PERSISTENCE_ADAPTER_TYPE = "file_system"
""" The persistence adapter type """

SERIALIZER_TYPE_VALUE = "serializer_type"
""" The serializer type value """

class SearchIndexPersistenceFileSystemAdapter:
    """
    The search index persistence file system adapter class.
    """

    search_index_persistence_file_system_adapter_plugin = None
    """ The search index persistence file system adapter plugin """

    def __init__(self, search_index_persistence_file_system_adapter_plugin):
        """
        Constructor of the class.

        @type search_index_persistence_file_system_adapter_plugin: SearchIndexPersistenceFileSystemAdapterPlugin
        @param search_index_persistence_file_system_adapter_plugin: The search index persistence file system adapter plugin.
        """

        self.search_index_persistence_file_system_adapter_plugin = search_index_persistence_file_system_adapter_plugin

    def get_type(self):
        return PERSISTENCE_ADAPTER_TYPE

    def persist_index(self, search_index, properties):

        # checks for the serializer type in the properties map
        if not SERIALIZER_TYPE_VALUE in properties:
            raise search_index_persistence_file_system_adapter_exceptions.MissingProperty(SERIALIZER_TYPE_VALUE)

        # retrieves the search index serializer plugins
        search_index_serializer_plugins = self.search_index_persistence_file_system_adapter_plugin.search_index_serializer_plugins

        serializer_type = properties[SERIALIZER_TYPE_VALUE]

        serializer_plugin = None

        for search_index_serializer_plugin in search_index_serializer_plugins:
            search_index_serializer_plugin_type = search_index_serializer_plugin.get_type()

            if search_index_serializer_plugin_type == serializer_type:
                serializer_plugin = search_index_serializer_plugin

        if not serializer_plugin:
            raise search_index_persistence_file_system_adapter_exceptions.MissingIndexSerializerPlugin(serializer_type)

        persistence_success = serializer_plugin.persist_index(search_index, properties)

        return persistence_success

    def load_index(self, properties):
        if not SERIALIZER_TYPE_VALUE in properties:
            raise search_index_persistence_file_system_adapter_exceptions.MissingProperty(SERIALIZER_TYPE_VALUE)

        # retrieves the search index serializer plugins
        search_index_serializer_plugins = self.search_index_persistence_file_system_adapter_plugin.search_index_serializer_plugins

        serializer_type = properties[SERIALIZER_TYPE_VALUE]

        serializer_plugin = None

        for search_index_serializer_plugin in search_index_serializer_plugins:
            search_index_serializer_plugin_type = search_index_serializer_plugin.get_type()

            if search_index_serializer_plugin_type == serializer_type:
                serializer_plugin = search_index_serializer_plugin

        if not serializer_plugin:
            raise search_index_persistence_file_system_adapter_exceptions.MissingIndexSerializerPlugin(serializer_type)

        search_index = serializer_plugin.load_index(properties)

        return search_index
