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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
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

import search_scorer_function_repository_exceptions

class SearchScorerFunctionRepository:
    """
    The search scorer function repository.
    """

    search_scorer_function_repository_plugin = None
    """ The search scorer function repository plugin """

    functions_map = {}
    """ The map of functions instances currently injected in the repository """

    def __init__(self, search_scorer_function_repository_plugin):
        """
        Constructor of the class.

        @type search_scorer_function_repository_plugin: SearchScorerFunctionRepositoryPlugin
        @param search_scorer_function_repository_plugin: The search scorer function repository plugin.
        """

        self.functions_map = {}

        self.search_scorer_function_repository_plugin = search_scorer_function_repository_plugin

    def add_search_scorer_functions_map(self, scorer_functions_map):
        """
        Adds a set of functions to the repository.

        @type scorer_functions_map: Dictionary
        @param scorer_functions_map: A dictionary with the functions to be inserted into the repository.
        """

        # adds each function to the repository function map
        for function_identifier, function in scorer_functions_map.items():

            # checks for duplicates insertion
            if function_identifier in self.functions_map:
                raise search_scorer_function_repository_exceptions.SearchScorerFunctionRepositoryException(function_identifier)

            self.functions_map[function_identifier] = function

    def remove_search_scorer_functions_map(self, scorer_functions_map):
        """
        Adds a set of functions from the repository.

        @type scorer_functions_map: Dictionary
        @param scorer_functions_map: A dictionary with the functions to be deleted from the repository.
        """

        # removes all the functions made available by the plugin
        # (since no duplicates are allowed, the plugin is assumed to be the single provider of the function)
        for function_identifier in scorer_functions_map:
            del self.functions_map[function_identifier]

    def get_function_identifiers(self):
        """
        Retrieves the list of function identifiers registered in the repository.

        @rtype: List
        @return: The list of function identifiers in the repository.
        """

        return self.functions_map.keys()

    def get_function(self, scorer_function_identifier):
        """
        Retrieves the function instance for the provided function identifier

        @type scorer_function_identifier: String
        @param scorer_function_identifier: The identifier for the intended function.
        @rtype: SearchScorerFunction
        @return: The function instance for the provided function identifier.
        """

        return self.functions_map[scorer_function_identifier]
