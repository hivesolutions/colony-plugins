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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import search_exceptions

TYPE_VALUE = "type"
""" The type value """

class Search:
    """
    The search class.
    """

    search_plugin = None
    """ The search plugin """

    def __init__(self, search_plugin):
        """
        Constructor of the class.
        
        @type search_plugin: SearchPlugin
        @param search_plugin: The search plugin.
        """

        self.search_plugin = search_plugin

    def create_index(self, properties):
        """
        Creates the search index for the given properties.
        
        @type properties: Dictionary
        @param properties: The properties to create the search index.
        @rtype: SearchIndex
        @return: The search index for the given properties.
        """

        # in case type value is not defined in properties
        if not TYPE_VALUE in properties:
            raise search_exceptions.MissingProperty(TYPE_VALUE)

        # retrieves the search crawler plugins
        search_crawler_plugins = self.search_plugin.search_crawler_plugins

        # retrieves the search interpreter plugin
        search_interpreter_plugin = self.search_plugin.search_interpreter_plugin

        # retrieves the search indexer plugin
        search_indexer_plugin = self.search_plugin.search_indexer_plugin

        # retrieves the type of index
        index_type = properties[TYPE_VALUE]

        # creates the crawling plugin temporary variable
        crawling_plugin = None

        # iterates over all the available search crawler plugins
        for search_crawler_plugin in search_crawler_plugins:
            # retrieves 
            search_crawler_plugin_type = search_crawler_plugin.get_type()

            # in case the index type is the same as the search crawler plugin type
            if index_type == search_crawler_plugin_type:
                # sets the crawling plugin
                crawling_plugin = search_crawler_plugin

                # breaks the for cycle
                break

        # in case there was no crawling plugin selected
        if not crawling_plugin:
            raise search_exceptions.MissingCrawlingPluginProperty(index_type)

        # retrieves the tokens list 
        tokens_list = crawling_plugin.get_tokens(properties)

        # processes the tokens list (modifying it) and retrieves the used interpreter adapters list
        used_interpreter_adapter_list = search_interpreter_plugin.process_tokens_list(tokens_list, properties)

        # creates the search index with the given tokens list and properties
        search_index = search_indexer_plugin.create_index(tokens_list, properties)

        # returns the search index
        return search_index
