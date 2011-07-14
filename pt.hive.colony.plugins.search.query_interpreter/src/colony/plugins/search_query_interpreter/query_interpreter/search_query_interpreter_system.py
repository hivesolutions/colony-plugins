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

import search_query_interpreter_parser

class SearchQueryInterpreter:
    """
    The search query interpreter class.
    """

    search_query_interpreter_plugin = None
    """ The search query interpreter plugin """

    def __init__(self, search_query_interpreter_plugin):
        """
        Constructor of the class.

        @type search_query_interpreter_plugin: SearchQueryInterpreterPlugin
        @param search_query_interpreter_plugin: The search query interpreter plugin.
        """

        self.search_query_interpreter_plugin = search_query_interpreter_plugin

    def parse_query(self, query_string, properties):
        """
        The method to start the search query interpreter.

        @type query_string: String
        @param query_string: The query string with the search terms.
        @type properties: Dictionary
        @param properties: The map of properties for the query parsing.
        @rtype: SearchQuery
        @return: A search query object created according to the search interpreter adapters available.
        """

        root_query_node = search_query_interpreter_parser.query_parser.parse(query_string) #@UndefinedVariable

        search_query = SearchQuery()

        search_query.root_search_query_node = root_query_node

        return search_query

class SearchQuery:

    root_search_query_node = None

    def __init__(self):
        pass
