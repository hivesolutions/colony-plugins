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

SEARCH_INDEX_IDENTIFIER_VALUE = "search_index_identifier"
""" The search index identifier parameter name """

PROPERTIES_VALUE = "properties"
""" The properties parameter name """

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

    def create_index_with_identifier(self, search_index_identifier, properties):

        # the task options map
        options = {SEARCH_INDEX_IDENTIFIER_VALUE : search_index_identifier,
                   PROPERTIES_VALUE : properties}

        # creates an index creation task using the task manager
        self.task = self.search_remote_service_plugin.task_manager_plugin.create_new_task("Search Remote Service", "Creating index", self.start_create_index_handler)
        self.task.set_task_pause_handler(self.pause_handler)
        self.task.set_task_resume_handler(self.resume_handler)
        self.task.set_task_stop_handler(self.stop_handler)
        self.task.start(options)

        return True

    def remove_index_with_identifier(self, search_index_identifier, properties):
        search_plugin = self.search_remote_service_plugin.search_plugin

        return search_plugin.remove_index_with_identifier(search_index_identifier, properties)

    def search_index(self, search_index_identifier, search_query, properties):
        search_plugin = self.search_remote_service_plugin.search_plugin

        return search_plugin.search_index_by_identifier(search_index_identifier, search_query, properties)

    def get_indexes_metadata(self):
        search_plugin = self.search_remote_service_plugin.search_plugin

        return search_plugin.get_indexes_metadata()

    def get_search_crawler_adapter_types(self):
        search_plugin = self.search_remote_service_plugin.search_plugin

        return search_plugin.get_search_crawler_adapter_types()

    def start_create_index_handler(self, task, options):
        """
        Handler invoked when the create index task starts

        @param task: Create index task object
        @param options: Create index task options.
        """

        # retrieves the search index identifier for the creation operation
        search_index_identifier = options[SEARCH_INDEX_IDENTIFIER_VALUE]
        # retrieves the creation properties for the creation operation
        properties = options[PROPERTIES_VALUE]

        search_plugin = self.search_remote_service_plugin.search_plugin

        search_plugin.create_index_with_identifier(search_index_identifier, properties)

        task.confirm_stop(True)

    def pause_handler(self, options):
        """
        Handler invoked when a task pauses.

        @param options: Task options.
        """
        pass

    def resume_handler(self, options):
        """
        Handler invoked when a task resumes.

        @param options: Task options.
        """
        pass

    def stop_handler(self, options):
        """
        Handler invoked when a task stops.

        @param options: Task options.
        """
        pass
