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

__author__ = "João Magalhães <joamag@hive.pt>"
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

ADAPTER_NAME = "ping"
""" The adapter name """

COLONY_VALUE = "colony"
""" The colony value """

STATUS_VALUE = "status"
""" The status value """

UP_STATUS = "up"
""" The up status """

DOWN_STATUS = "down"
""" The down status """

VALID_STATUS_CODE = 200
""" The valid status code """

class DistributionPingStatus:
    """
    The distribution ping status class.
    """

    distribution_ping_status_plugin = None
    """ The distribution ping status plugin """

    def __init__(self, distribution_ping_status_plugin):
        """
        Constructor of the class.

        @type distribution_ping_status_plugin: DistributionPingStatusPlugin
        @param distribution_ping_status_plugin: The distribution ping status plugin.
        """

        self.distribution_ping_status_plugin = distribution_ping_status_plugin

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return ADAPTER_NAME

    def handle_status(self, arguments):
        """
        Handles a (distribution) status.

        @type arguments: Dictionary
        @param arguments: The arguments to the
        (distribution) status.
        """

        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_ping_status_plugin.distribution_registry_plugin

        # retrieves the main client http plugin
        main_client_http_plugin = self.distribution_ping_status_plugin.main_client_http_plugin

        # retrieves the "current" list of registry entries for the colony type
        registry_entries_list = distribution_registry_plugin.get_registry_entries_type(COLONY_VALUE)

        # creates the main client http client
        http_client = main_client_http_plugin.create_client({})

        # opens the http client
        http_client.open({})

        try:
            # iterates over all the list of registry entries to "check status"
            # for the distribution information
            for registry_entry in registry_entries_list:
                address = registry_entry.endpoints[0][0]

                try:
                    # resolves the "ping" url
                    result = http_client.fetch_url("http://" + address + ":8080/colony_dynamic/rest/services/main_distribution_service.ping.json")

                    # in case the result is valid
                    if result.status_code == VALID_STATUS_CODE:
                        registry_entry.metadata[STATUS_VALUE] = UP_STATUS
                    # in case the result is not valid
                    else:
                        registry_entry.metadata[STATUS_VALUE] = DOWN_STATUS
                except:
                    registry_entry.metadata[STATUS_VALUE] = DOWN_STATUS
        finally:
            # closes the http client
            http_client.close({})
