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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import Pyro.core

import main_pyro_manager_exceptions

HANDLER_NAME = "pyro"
""" The handler name """

class MainPyroManager:
    """
    The main pyro manager class.
    """

    main_pyro_manager_plugin = None
    """ The main pyro manager plugin """

    pyro_daemon = []
    """ The pyro daemon """

    base_remote_uri = "none"
    """ The base remote uri """

    service_methods = []
    """ The service methods list """

    service_methods_map = {}
    """ The service methods map """

    def __init__(self, main_pyro_manager_plugin):
        """
        Constructor of the class.
        
        @type main_pyro_manager_plugin: MainPyroManagerPlugin
        @param main_pyro_manager_plugin: The main pyro manager plugin.
        """

        self.main_pyro_manager_plugin = main_pyro_manager_plugin

        self.service_objects = []
        self.service_methods_map = {}

        # creates the pyro daemon
        self.create_pyro_daemon()

    def is_active(self):
        return True

    def get_handler_name(self):
        return HANDLER_NAME

    def activate_server(self):
        """
        Activates the server.
        """

        self.pyro_daemon.requestLoop()

    def create_pyro_daemon(self):
        """
        Creates the pyro daemon creating the base object and connecting it.
        """

        # creates the pyro daemon instance
        self.pyro_daemon = Pyro.core.Daemon()

        # creates the base remote instance
        base_remote = BaseRemote()

        # connects the base remote object, and retrieves the base proxy uri
        self.base_remote_uri = self.pyro_daemon.connect(base_remote, "base_remote")

    def update_service_methods(self, updated_rpc_service_plugin = None):

        if updated_rpc_service_plugin:
            updated_rpc_service_plugins = [updated_rpc_service_plugin]
        else:
            # clears the service methods list
            self.service_methods = []

            # clears the service map
            self.service_methods_map = {}

            # retrieves the updated rpc service plugins
            updated_rpc_service_plugins = self.main_pyro_manager_plugin.rpc_service_plugins

        for rpc_service_plugin in updated_rpc_service_plugins:
            # retrieves all the method names for the current rpc service
            available_rpc_methods = rpc_service_plugin.get_available_rpc_methods()

            # retrieves all the method alias for the current rpc service
            available_rpc_methods_alias = rpc_service_plugin.get_rpc_methods_alias()

            # in case the plugin contains the rpc method metadata
            if rpc_service_plugin.contains_metadata_key("rpc_method"):
                # retrieves the metadata values for the rpc method
                metadata_values = rpc_service_plugin.get_metadata_key("rpc_method")

                # iterates over all the metadata values
                for metadata_value in metadata_values:
                    # retrieves the method name of the rpc method
                    method_name = metadata_value["method_name"]

                    # retrieves the alias for the rpc method
                    alias = metadata_value["alias"]

                    # retrieves the method for the rpc method from the plugin instance
                    method = getattr(rpc_service_plugin, method_name)

                    # adds the method to the list of available rpc methods
                    available_rpc_methods.append(method)

                    # adds the alias to the list of available rpc methods alias
                    available_rpc_methods_alias[method] = alias

            # retrieves the list of all the available rpc methods
            available_rpc_methods_string = [value.__name__ for value in available_rpc_methods]

            # iterates over all the rpc method alias keys
            for available_rpc_method_alias_key in available_rpc_methods_alias:
                available_rpc_methods_alias_string = available_rpc_methods_alias[available_rpc_method_alias_key]
                available_rpc_methods_string.extend(available_rpc_methods_alias_string)

            self.service_methods.extend(available_rpc_methods_string)

            # retrieves the service id
            service_id = rpc_service_plugin.get_service_id()

            # retrieves the list of service alias
            service_alias = rpc_service_plugin.get_service_alias()

            # creates a list with all the possible service names
            service_names = [service_id] + service_alias

            # iterates over all the possible service names
            for service_name in service_names:
                for available_rpc_method_string in available_rpc_methods_string:
                    composite_available_rpc_method_string = service_name + "." + available_rpc_method_string
                    self.service_methods.append(composite_available_rpc_method_string)

            # iterates over all the available rpc methods to generate the service methods map
            for available_rpc_method in available_rpc_methods:
                # creates the service method names list
                service_method_names = []

                # creates the service method basic names list
                service_method_basic_names = []

                # adds the available rpc method to the service method names list
                service_method_names.append(available_rpc_method.__name__)

                # adds the available rpc method to the service basic method names list
                service_method_basic_names.append(available_rpc_method.__name__)

                # retrieves all the alias to the current service methods
                alias_service_method_names = [value for value in available_rpc_methods_alias[available_rpc_method]]

                # adds the available rpc method alias to the service method names list
                service_method_names.extend(alias_service_method_names)

                # adds the available rpc method alias to the service basic method names list
                service_method_basic_names.extend(alias_service_method_names)

                # iterates over all the service names
                for service_name in service_names:
                    for service_method_basic_name in service_method_basic_names:
                        service_method_complex_name = service_name + "." + service_method_basic_name
                        service_method_names.append(service_method_complex_name)

                # iterates over all the service method names
                for service_method_name in service_method_names:
                    # adds the available rpc method to the map with the service method name as key
                    self.service_methods_map[service_method_name] = available_rpc_method

        self.update_pyro_proxies()

    def update_pyro_service_proxies(self):
        """
        Updates the pyro service proxies.
        """

        # iterates over all the available service methods
        for service_method in self.service_methods:
            # retrieves the service class
            service_class = self.get_service_class(service_method)

            if service_class:
                pass

    def get_service_class(self, service_method):
        """
        Retrieves the service class for the given service method.
        
        @type service_method: String
        @param service_method: The service method to retrieve the service class.
        @rtype: String
        @return: The service class for the given service method.
        """

        # splits the service method
        service_method_splitted = service_method.split(".")

        if len(service_method_splitted) == 2:
            return service_method_splitted[0]
        else:
            return

class BaseRemote(Pyro.core.ObjBase):
    """
    The base remote class.
    """

    name_proxy_uri_map = {}
    """ The map relating the name of the object and the proxy uri """

    def __init__(self):
        """
        Constructor of the class.
        """

        Pyro.core.ObjBase.__init__(self)
        self.name_proxy_uri_map = {}

    def add_proxy_uri(self, name, proxy_uri):
        """
        Adds a new proxy uri to the base remote.
        
        @type name: String
        @param name: The name of the proxy uri to be added.
        @type proxy_uri: String
        @param proxy_uri: The proxy uri to be added.
        @rtype: bool
        @return: The result of the addiction (if successful or not).
        """

        if name in self.name_proxy_uri_map:
            return False
        else:
            self.name_proxy_uri_map[name] = proxy_uri
            return True

    def get_proxy_uri(self, name):
        """
        Retrieves the proxy uri for the given object name.
        
        @type name: String
        @param name: The object name to retrieve the proxy uri.
        @rtype: String
        @return: The proxy uri for the given object name.
        """

        if name in self.name_proxy_uri_map:
            return self.name_proxy_uri_map[name]

class GenericRemote(Pyro.core.ObjBase):
    """
    The base remote class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass
