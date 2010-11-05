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

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import xml.dom.minidom

class Parser:
    """
    The abstract parser class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def parse(self):
        """
        Parses the defined file.
        """

        pass

    def get_value(self):
        """
        Retrieves the result of the parse.

        @rtype: Object
        @return: The result of the parse.
        """

        pass

class ResourceDescriptorParser(Parser):
    """
    The resource descriptor parser class.
    """

    file_path = None
    """ The file path """

    resources_list = []
    """ The resources list """

    def __init__(self, file_path = None):
        Parser.__init__(self)
        self.file_path = file_path

    def parse(self):
        self.load_resource_file(self.file_path)

    def get_value(self):
        return self.resources_list

    def get_resources_list(self):
        return self.resources_list

    def load_yadis_file(self, file_path):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parse(file_path)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.resources_list = self.parse_resources(child_node)

    def load_yadis_contents(self, file_contents):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parseString(file_contents)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.resources_list = self.parse_resources(child_node)

    def parse_resources(self, resources):
        resources_list = []
        child_nodes = resources.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                resources_list.append(self.parse_resources_element(child_node))

        return resources_list

    def parse_resources_element(self, resources_element):
        node_name = resources_element.nodeName

        if node_name == "XRD":
            resource = self.parse_resource(resources_element)

        return resource

    def parse_resource(self, resource):
        resource_structure = Resource()
        child_nodes = resource.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_resource_element(child_node, resource_structure)

        if resource.hasAttribute("version"):
            version = resource.getAttribute("version")
            resource_structure.version = version

        return resource_structure

    def parse_resource_element(self, resource_element, resource):
        node_name = resource_element.nodeName

        if node_name == "Service":
            resource.services_list.append(self.parse_service(resource_element))

    def parse_service(self, service):
        service_structure = Service()
        child_nodes = service.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_service_element(child_node, service_structure)

        if service.hasAttribute("priority"):
            priority = service.getAttribute("priority")
            service_structure.priority = priority

        return service_structure

    def parse_service_element(self, service_element, service):
        node_name = service_element.nodeName

        if node_name == "Type":
            service.types_list.append(self.parse_type(service_element))
        else:
            service.attributes_map[node_name] = self.parse_attribute(service_element)

    def parse_type(self, type):
        service_type = type.firstChild.data.strip()
        return service_type

    def parse_attribute(self, attribute):
        service_attribute = attribute.firstChild.data.strip()
        return service_attribute

class Resource:
    """
    Class that represent an xrd resource.
    """

    version = "none"
    """ The version of the resource """

    services_list = []
    """ The list of service for the resource """

    def __init__(self, version = "none"):
        """
        Constructor of the class.

        @type version: String
        @param version: The version of the resource.
        """

        self.version = version

        self.services_list = []

class Service:
    """
    The service class, describing a yadis service.
    """

    priority = None
    """ The priority of the service """

    types_list = []
    """ The list of types describing the service """

    attributes_map = {}
    """ The map containing all the attributes """

    def __init__(self, priority = "none"):
        """
        Constructor of the class.

        @type priority: String
        @param priority: The priority of the service.
        """

        self.priority = priority

        self.types_list = []
        self.attributes_map = {}

    def get_attribute(self, attribute_name):
        """
        Retrieves an attribute from the attributes map.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to retrieve.
        @rtype: Object
        @return: The retrieved attribute.
        """

        return self.attributes_map.get(attribute_name, None)

    def set_attribute(self, attribute_name, attribute_value):
        """
        Sets an attribute in the attributes map.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to set.
        @type attribute_value: Object
        @param attribute_value: The value of the attribute to set.
        """

        self.attributes_map[attribute_name] = attribute_value

def valid_node(node):
    """
    Gets if a node is valid or not for parsing.

    @type node: Node
    @param node: The Xml node to be validated.
    @rtype: bool
    @return: The valid or not valid value.
    """

    # in case the node is of type element
    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        # returns true (valid)
        return True
    # otherwise
    else:
        # returns false (invalid)
        return False
