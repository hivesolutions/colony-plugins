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

import shelve

import search_index_serializer_shelve_exceptions

SEARCH_INDEX_SERIALIZER_TYPE = "shelve"
""" The search index serializer type """

FILE_PATH_VALUE = "file_path"
""" The file path value """

FORWARD_INDEX_MAP_SUFFIX = ".forward_index.map"
""" The suffix to apply to the forward index map """

INVERTED_INDEX_MAP_SUFFIX = ".inverted_index.map"

class SearchIndexSerializerShelve:
    """
    The search index serializer shelve class.
    """

    search_index_serializer_shelve_plugin = None
    """ The search index serializer shelve plugin """

    def __init__(self, search_index_serializer_shelve_plugin):
        """
        Constructor of the class.

        @type search_index_serializer_shelve_plugin: SearchIndexSerializerShelvePlugin
        @param search_index_serializer_shelve_plugin: The search index serializer shelve plugin.
        """

        self.search_index_serializer_shelve_plugin = search_index_serializer_shelve_plugin

    def get_type(self):
        return SEARCH_INDEX_SERIALIZER_TYPE

    def persist_index(self, search_index, properties):
        if not FILE_PATH_VALUE in properties:
            raise search_index_serializer_shelve_exceptions.MissingProperty(FILE_PATH_VALUE)

        # retrieves the file path
        file_path = properties[FILE_PATH_VALUE]

        # retrieves the forward index map file path
        forward_index_map_file_path = file_path + FORWARD_INDEX_MAP_SUFFIX

        # retrieves the inverted index map file path
        inverted_index_map_file_path = file_path + INVERTED_INDEX_MAP_SUFFIX

        # creates the forward index map
        forward_index_map = shelve.open(forward_index_map_file_path, writeback=False)

        # creates the inverted index map
        inverted_index_map = shelve.open(inverted_index_map_file_path, writeback=False)

        # creates the properties
        properties = shelve.open(file_path, writeback=False)

        # retrieves the original forward index map
        forward_index_map_original = search_index.forward_index_map

        # retrieves the original inverted index map
        inverted_index_map_original = search_index.inverted_index_map

        # retrieves the original properties
        properties_original = search_index.properties

        # iterates over all forward index map original keys to copy the content
        for forward_index_map_original_key in forward_index_map_original:
            forward_index_map_original_value = forward_index_map_original[forward_index_map_original_key]
            forward_index_map[forward_index_map_original_key] = forward_index_map_original_value

        # iterates over all inverted index map original keys to copy the content
        for inverted_index_map_original_key in inverted_index_map_original:
            inverted_index_map_original_value = inverted_index_map_original[inverted_index_map_original_key]
            inverted_index_map[inverted_index_map_original_key] = inverted_index_map_original_value

        # iterates over all properties original keys to copy the content
        for properties_original_key in properties_original:
            properties_original_value = properties_original[properties_original_key]
            properties_original[properties_original_key] = properties_original_value

        # closes the forward index map and writes back (flushes) the contains
        forward_index_map.close()

        # closes the inverted index map and writes back (flushes) the contains
        inverted_index_map.close()

        # closes the properties and writes back (flushes) the contains
        properties.close()

        return True

    def load_index(self, properties):
        if not FILE_PATH_VALUE in properties:
            raise search_index_serializer_shelve_exceptions.MissingProperty(FILE_PATH_VALUE)

        # retrieves the file path
        file_path = properties[FILE_PATH_VALUE]

        # retrieves the forward index map file path
        forward_index_map_file_path = file_path + FORWARD_INDEX_MAP_SUFFIX

        # retrieves the inverted index map file path
        inverted_index_map_file_path = file_path + INVERTED_INDEX_MAP_SUFFIX

        # creates the forward index map
        forward_index_map = shelve.open(forward_index_map_file_path, writeback=True)

        # creates the inverted index map
        inverted_index_map = shelve.open(inverted_index_map_file_path, writeback=True)

        # creates the properties
        properties = shelve.open(file_path, writeback=True)

        # creates the search index object
        search_index = SearchIndex()

        # sets the forward index map in the search index
        search_index.forward_index_map = forward_index_map

        # sets the inverted index map in the search index
        search_index.inverted_index_map = inverted_index_map

        # sets the properties in the search index
        search_index.properties = properties

        # returns the search index
        return search_index

class SearchIndex:
    """
    The search index class.
    """

    forward_index_map = {}
    """ The forward index map """

    inverted_index_map = {}
    """ The inverted index map """

    properties = {}
    """ The properties """

    def __init__(self):
        self.forward_index_map = {}
        self.inverted_index_map = {}
        self.properties = {}
