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

__revision__ = "$LastChangedRevision: 583 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-02 18:00:35 +0000 (Ter, 02 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """


SERVICE_ID = "search_remote_service"
""" The service id """

class SearchRemoteService:
    """
    The search remote service class.
    """

    search_remote_service_plugin = None
    """ The search remote service plugin """

    def __init__(self, search_remote_service_plugin):
        """
        Constructor of the class.
        
        @type search_remote_service_plugin: SearchRemoteServicePlugin
        @param search_remote_service_plugin: The search remote service plugin.
        """

        self.search_remote_service_plugin = search_remote_service_plugin

    def get_service_id(self):
        return SERVICE_ID

    def get_service_alias(self):
        return []

    def get_available_rpc_methods(self):
        return []

    def get_rpc_methods_alias(self):
        return {}

    def search_index(self, search_index_identifier, search_query, properties):
        properties = {"query_evaluator_type" : "query_parser", "search_scorer_formula_type": "term_frequency_formula_type", "search_scorer_formula_type" : "term_frequency_formula_type"}
        search_plugin = self.search_remote_service_plugin.search_plugin

        return search_plugin.search_index_by_identifier(search_index_identifier, search_query, properties)
