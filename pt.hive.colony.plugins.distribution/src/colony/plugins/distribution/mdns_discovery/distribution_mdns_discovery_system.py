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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

COLONY_SERVICE_ID = "_colony._tcp.local"
""" The colony service id """

TCP_VALUE = "tcp"
""" The tcp value """

DEFAULT_TIMEOUT_VALUE = 1
""" The default timeout value """

class DistributionMdnsDiscovery:
    """
    The distribution mdns discovery class.
    """

    distribution_mdns_discovery_plugin = None
    """ The distribution mdns discovery plugin """

    def __init__(self, distribution_mdns_discovery_plugin):
        """
        Constructor of the class.

        @type distribution_mdns_discovery_plugin: DistributionMdnsDiscoveryPlugin
        @param distribution_mdns_discovery_plugin: The distribution mdns discovery plugin.
        """

        self.distribution_mdns_discovery_plugin = distribution_mdns_discovery_plugin

    def handle_discover(self, parameters):
        # retrieves the main client mdns plugin
        main_client_mdns_plugin = self.distribution_mdns_discovery_plugin.main_client_mdns_plugin

        # creates the parameters for the queries resolution
        parameters = {
            "callback_function" : self._discovery_callback,
            "callback_timeout" : DEFAULT_TIMEOUT_VALUE
        }

        # creates the main client mdns client
        mdns_client = main_client_mdns_plugin.create_client({})

        # opens the mdns client
        mdns_client.open({})

        try:
            # resolves the queries
            mdns_client.resolve_queries([(COLONY_SERVICE_ID, "PTR", "IN")], parameters)
        finally:
            # closes the mdns client
            mdns_client.close({})

    def _discovery_callback(self, query, response):
        # retrieves the distribution registry plugin
        distribution_registry_plugin = self.distribution_mdns_discovery_plugin.distribution_registry_plugin

        response_answers = response.answers
        response_additional_resource_records = response.additional_resource_records

        hosts = []
        hosts_resolved = []

        for response_answer in response_answers:
            # unpacks the answer tuple, retrieving the name,
            # type, class and data
            answer_name, _answer_type, _answer_class, _answer_time_to_live, answer_data = response_answer

            # in case the answer name not is of type
            # colony service
            if not answer_name == COLONY_SERVICE_ID:
                # continues the loop
                continue

            # adds the answer data (host) to he hosts list
            hosts.append(answer_data)

        for response_additional_resource_record in response_additional_resource_records:
            # unpacks the additional resource record tuple, retrieving the name,
            # type, class and data
            record_name, record_type, _record_class, _record_time_to_live, record_data = response_additional_resource_record

            if record_name in hosts and record_type == "A":
                hosts_resolved.append((record_name, record_data))

        for host_resolved in hosts_resolved:
            # unpack the host resolved value
            hostname, address = host_resolved

            # adds the default endpoint
            endpoints = [(address, DEFAULT_TIMEOUT_VALUE)]

            distribution_registry_plugin.register_entry(hostname, "colony@" + hostname, "colony", endpoints, {})
