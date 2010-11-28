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

import types

HELPER_NAME = "xmlrpc"
""" The helper name """

HTTP_PROTOCOL_PREFIX = "HTTP://"
""" The httpd protocol prefix """

FULL_CLASS_NAME_VALUE = "full_class_name"
""" The full class name value """

class DistributionXmlrpcHelper:
    """
    The distribution xmlrpc helper class.
    """

    distribution_xmlrpc_helper_plugin = None
    """ The distribution xmlrpc helper plugin """

    def __init__(self, distribution_xmlrpc_helper_plugin):
        """
        Constructor of the class.

        @type distribution_xmlrpc_helper_plugin: DistributionXmlrpcHelperPlugin
        @param distribution_xmlrpc_helper_plugin: The distribution xmlrpc helper plugin.
        """

        self.distribution_xmlrpc_helper_plugin = distribution_xmlrpc_helper_plugin

    def get_helper_name(self):
        return HELPER_NAME

    def create_client(self, remote_reference):
        """
        Creates a xmlrpc client proxy from a remote reference.

        @type remote_reference: RemoteReference
        @param remote_reference: The remote reference to retrieve the xmlrpc client proxy.
        @rtype: XmlrpcClientProxy
        @return: The xmlrpc client proxy retrieved from a remote reference.
        """

        # retrieves the main xmlrpc client plugin
        main_xmlrpc_client_plugin = self.distribution_xmlrpc_helper_plugin.main_xmlrpc_client_plugin

        # retrieves the remote reference hostname
        hostname = remote_reference.hostname

        # retrieves the remote reference port
        port = remote_reference.port

        # retrieves the remote reference properties list
        properties_list = remote_reference.properties_list

        # retrieves the xmlrpc handler base filename
        xmlrpc_handler_base_filename = properties_list[0]

        # retrieves the xmlrpc handler extension
        xmlrpc_handler_extension = properties_list[1]

        # creates the xmlrpc server address
        xmlrpc_server_address = HTTP_PROTOCOL_PREFIX + hostname + ":" + str(port) + "/" + xmlrpc_handler_base_filename + "." + xmlrpc_handler_extension

        # creates the xmlrpc remote client
        xmlrpc_remote_client = main_xmlrpc_client_plugin.create_remote_client({"xmlrpc_server_address" : xmlrpc_server_address})

        # creates the xmlrpc remote client proxy
        xmlrpc_remote_client_proxy = XmlrpcClientProxy(xmlrpc_remote_client, remote_reference)

        # returns the xmlrpc remote client proxy
        return xmlrpc_remote_client_proxy

    def create_client_host(self, hostname, port, properties):
        """
        Creates a xmlrpc client from an hostname, port and some properties.

        @type hostname: String
        @param hostname: The hostname to create the xmlrpc client.
        @type port: int
        @param port: The port to create the xmlrpc client.
        @type properties: Dictionary
        @param properties: The properties to create the xmlrpc client.
        @rtype: XmlrpcClient
        @return: The xmlrpc client retrieved from an hostname, port and some properties.
        """

        # retrieves the main xmlrpc client plugin
        main_xmlrpc_client_plugin = self.distribution_xmlrpc_helper_plugin.main_xmlrpc_client_plugin

        # retrieves the xmlrpc handler base filename
        xmlrpc_handler_base_filename = properties["handler_base_filename"]

        # retrieves the xmlrpc handler extension
        xmlrpc_handler_extension = properties["handler_extension"]

        # creates the xmlrpc server address
        xmlrpc_server_address = HTTP_PROTOCOL_PREFIX + hostname + ":" + str(port) + "/" + xmlrpc_handler_base_filename + "." + xmlrpc_handler_extension

        # creates the xmlrpc remote client
        xmlrpc_remote_client = main_xmlrpc_client_plugin.create_remote_client({"xmlrpc_server_address" : xmlrpc_server_address})

        # returns the xmlrpc remote client
        return xmlrpc_remote_client

class XmlrpcClientProxy:
    """
    The xmlrpc client proxy class.
    """

    xmlrpc_client = None
    """ The xmlrpc client """

    remote_reference = None
    """ The remote reference """

    def __init__(self, xmlrpc_client = None, remote_reference = None):
        """
        Constructor of the class.

        @type xmlrpc_client: XmlrpcClient
        @param xmlrpc_client: The xmlrpc client.
        @type remote_reference: RemoteReference
        @param remote_reference: The xmlrpc remote reference.
        """

        self.xmlrpc_client = xmlrpc_client
        self.remote_reference = remote_reference

    def __nonzero__(self):
        return True

    def __getattr__(self, name):
        if hasattr(self.xmlrpc_client, name):
            attribute = getattr(self.xmlrpc_client, name)

            # retrieves the attribute class
            attribute_class = attribute.__class__

            # in case the attribute class getattr method has not been replaced
            if not hasattr(attribute_class, "__replaced_getattr__"):
                new_getattr_method = self.create_getter_attr(attribute.__getattr__)
                attribute_class.__getattr__ = new_getattr_method
                attribute_class.__replaced_getattr__ = True

            # sets the attribute as class xmlrcp, in order to encapsulate the result into a class
            attribute.__class_xmlrpc__ = True

            # returns the attribute
            return attribute

        raise AttributeError()

    def create_getter_attr(self, method):
        """
        Creates a getattr method, that redirects the call method.

        @type method: Method
        @param method: The method to be modified.
        @rtype: Method
        @return: The modified method.
        """

        def getter_attr(self, name):
            # in case the name that is being retrieves id class xmlrpc
            # ignores it, otherwise a loop would be created
            if name == "__class_xmlrpc__":
                raise AttributeError()

            # calls the method retrieving the value
            return_value = method(name)

            # in case the returns is to be replaced to a class, and not a map
            if hasattr(self, "__class_xmlrpc__"):
                # updates the call method to allow creation of return classes
                return_value.__call__ = create_caller(return_value.__call__)

            # returns the return value
            return return_value

        # returns the getter attr method
        return getter_attr

def create_caller(method):
    """
    Creates the caller method for the colony xmlrpc specification.

    @type method: Method
    @param method: The method to be converted to the xmlrpc specification.
    @rtype: Method
    @return: The method converted to the xmlrpc specification.
    """

    def caller(*args, **kwargs):
        # calls the method retrieving the value
        return_value = method(*args, **kwargs)

        # in case the type of the return value is dictionary
        if type(return_value) == types.DictionaryType:
            # if the full class name value is defined in return value,
            # this is required by the colony specification of xmlrpc
            if FULL_CLASS_NAME_VALUE in return_value:
                # retrieves the full class name
                full_class_name = return_value[FULL_CLASS_NAME_VALUE]

                # splits the full class name
                full_class_name_splitted = full_class_name.split(".")

                # retrieves the module name
                module_name = ".".join(full_class_name_splitted[:-1])

                # the intermediate modules
                intermediate_modules = full_class_name_splitted[1:-1]

                # retrieves the class name
                class_name = full_class_name_splitted[-1]

                # import the class module
                module = __import__(module_name)

                # iterates over the intermediate module
                for intermediate_module in intermediate_modules:
                    # sets the module as the new intermediate module
                    module = getattr(module, intermediate_module)

                # retrieves the class reference
                class_reference = getattr(module, class_name)

                # creates a new class instance
                class_instance = class_reference()

                # sets the original (dictionary) value in the __original__ attribute,
                # this should be viewed as a backup of the original data
                class_instance.__original__ = return_value

                # iterates over all the key values in the map
                for key in return_value:
                    # sets the instance attributes as the map values
                    setattr(class_instance, key, return_value[key])

                # returns the class instance
                return class_instance
        else:
            # returns the return value
            return return_value

    # returns the caller method
    return caller
