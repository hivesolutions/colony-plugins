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

class DistributionClient:
    """
    The distribution client class.
    """

    distribution_client_plugin = None
    """ The distribution client plugin """

    def __init__(self, distribution_client_plugin):
        """
        Constructor of the class.
        
        @type distribution_client_plugin: DistributionClientPlugin
        @param distribution_client_plugin: The distribution client plugin.
        """

        self.distribution_client_plugin = distribution_client_plugin

    def get_remote_instance_references(self):
        """
        Retrieves all the available remote instance references.
        
        @rtype: List
        @return: All the available remote instance references.
        """

        # creates the remote references list
        remote_references = []

        # retrieves the distribution client adapter plugins
        distribution_client_adapter_plugins = self.distribution_client_plugin.distribution_client_adapter_plugins

        # iterates over all the distribution client adapter plugins
        for distribution_client_adapter_plugin in distribution_client_adapter_plugins:
            # retrieves the adapter remote references
            adapter_remote_references = distribution_client_adapter_plugin.get_remote_instance_references()

            # in case the retrieval was successful
            if adapter_remote_references:
                # extends the remote references with the adapter remote references
                remote_references.extend(adapter_remote_references)

        # returns the remote references
        return remote_references

    def get_remote_client_references(self):
        # creates the remote references list
        remote_references = []

        # retrieves the remote instance references
        remote_instance_references = self.get_remote_instance_references()

        # iterates over all the remote instance references
        for remote_instance_reference in remote_instance_references:
            remote_client_reference = self.create_client(remote_instance_reference)
            remote_references.append(remote_client_reference)

        # returns the remote references
        return remote_references

    def get_remote_client_references_by_host(self):
        # creates the host remote client references map
        host_remote_client_references_map = {}
        
        # retrieves the remote client references
        remote_client_references = self.get_remote_client_references()

        # iterates over all the remote client references
        for remote_client_reference in remote_client_references:
            # retrieves the remote client reference hostname
            remote_client_reference_hostname = remote_client_reference.remote_reference.hostname

            # in case the remote client reference hostname is not referenced in the map keys
            if not remote_client_reference_hostname in host_remote_client_references_map:
                # creates the remote client reference hostname element
                host_remote_client_references_map[remote_client_reference_hostname] = []

            # adds the remote client reference to the map relating the host with the remote client references map
            host_remote_client_references_map[remote_client_reference_hostname].append(remote_client_reference)

        # returns the host remote client references map
        return host_remote_client_references_map

    def get_remote_plugin_reference(self):
        """
        Retrieves the first available plugin reference.
        
        @rtype: PluginReference
        @return: The first available plugin referecence.
        """

        pass

    def create_client(self, remote_reference):
        """
        Creates a remote client from a remote reference.
        
        @type remote_reference: RemoteReference
        @param remote_reference: The remote reference to retrieve the remote client.
        @rtype: RemoteClient
        @return: The remote client retrieved from a remote reference.
        """

        # retrieves the remote reference service type
        remote_reference_service_type = remote_reference.service_type

        # retrieves the distribution helper plugins
        distribution_helper_plugins = self.distribution_client_plugin.distribution_helper_plugins

        # iterates over all the distribution helper plugins
        for distribution_helper_plugin in distribution_helper_plugins:
            # retrieves the helper name
            helper_name = distribution_helper_plugin.get_helper_name()

            # in case the helper name is the same as the remote reference service type
            if helper_name == remote_reference_service_type:
                # calls the helper to retrieve the client
                return distribution_helper_plugin.create_client(remote_reference)
