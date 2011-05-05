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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

HANDLER_NAME = "database"
""" The handler name """

class MainServiceDnsDatabaseHandler:
    """
    The main service dns database handler class.
    """

    main_service_dns_database_handler_plugin = None
    """ The main service dns database handler plugin """

    def __init__(self, main_service_dns_database_handler_plugin):
        """
        Constructor of the class.

        @type main_service_dns_database_handler_plugin: MainServiceDnsDatabaseHandlerPlugin
        @param main_service_dns_database_handler_plugin: The main service dns database handler plugin.
        """

        self.main_service_dns_database_handler_plugin = main_service_dns_database_handler_plugin

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request, arguments):
        """
        Handles the given dns request.

        @type request: DnsRequest
        @param request: The dns request to be handled.
        @type arguments: Dictionary
        @param arguments: The arguments to the dns handling.
        """

        # retrieves the dns storage database plugin
        dns_storage_database_plugin = self.main_service_dns_database_handler_plugin.dns_storage_database_plugin

        # creates the dns storage database client
        dns_storage_database_client = dns_storage_database_plugin.create_client(arguments)

        # retrieves the request queries
        queries = request.get_queries()

        # creates the records list
        records = []

        # iterates over all the queries to retrieve
        # their results
        for query in queries:
            # retrieves the name the type and the class
            # from the query
            name, type, class_ = query

            # retrieves the records that fullfill the given query
            query_records = dns_storage_database_client.get_records_filtered(name, type, class_)

            # extends the record list with the retrieved
            # query records
            records.extend(query_records)

        # creates the record tuples list
        record_tuples = []

        # iterates over all the retrieved records
        for record in records:
            # retrieves the record information
            record_name = record.get_name()
            record_type = record.get_type()
            record_class = record.get_class()
            record_time_to_live = record.get_time_to_live()
            record_value = record.get_value()

            # creates the record tuple
            record_tuple = (
                record_name,
                record_type,
                record_class,
                record_time_to_live,
                record_value
            )

            # adds the record tuple to the list of record tuples
            record_tuples.append(record_tuple)

        # adds a new answer to the request
        request.answers.extend(record_tuples)
