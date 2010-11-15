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

__revision__ = "$LastChangedRevision: 427 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:22:26 +0000 (Thu, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class DummyDistributionClient:
    """
    The dummy distribution client class.
    """

    dummy_distribution_client_plugin = None
    """ The dummy distribution client plugin """

    def __init__(self, dummy_distribution_client_plugin):
        """
        Constructor of the class.

        @type dummy_distribution_client_plugin: DummyEntityManagerPlugin
        @param dummy_distribution_client_plugin: The dummy distribution client plugin.
        """

        self.dummy_distribution_client_plugin = dummy_distribution_client_plugin

    def test_get_remote_client_references(self):
        """
        Tests the retrieval of the remote client references.
        """

        # retrieves the distribution client plugin
        distribution_client_plugin = self.dummy_distribution_client_plugin.distribution_client_plugin

        # retrieves the remote client references
        remote_client_references = distribution_client_plugin.get_remote_client_references()

        # iterates over all the remote client references
        for remote_client_reference in remote_client_references:
            # retrieves the service type
            service_type = remote_client_reference.remote_reference.service_type

            # prints a debug message
            self.dummy_distribution_client_plugin.debug("The service type is: " + service_type)

            # retrieves the remote dummy plugin proxy
            dummy_plugin_proxy = remote_client_reference.main_distribution_service.get_plugin_proxy_by_id("pt.hive.colony.plugins.dummy")

            # processes the plugin proxy using the remote reference
            dummy_plugin_proxy.process_plugin_proxy(remote_client_reference)

            # calls the print dummy method in the remote plugin proxy
            dummy_plugin_proxy.print_dummy()
