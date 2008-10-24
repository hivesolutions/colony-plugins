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

class ResourcesFileParser(Parser):
    """
    The resources file parser class.
    """

    file_path = None
    """ The file path """

    resource_list = []
    """ The resource list """

    def __init__(self, file_path = None):
        Parser.__init__(self)
        self.file_path = file_path

    def parse(self):
        self.load_resource_file(self.file_path)

    def get_value(self):
        return self.resource_list

    def get_resource_list(self):
        return self.resource_list

    def load_resource_file(self, file_path):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parse(file_path)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.resource_list = self.parse_resources(child_node)

    def parse_resources(self, resources):
        resource_list = []        
        child_nodes = resources.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                resource_list.append(self.parse_resource(child_node))

        return resource_list

    def parse_resource(self, resource):
        resource_structure = Resource()
        child_nodes = resource.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_resource_element(child_node, resource_structure)

        return resource_structure

    def parse_resource_element(self, resource_element, resource):
        node_name = resource_element.nodeName

        if node_name == "namespace":
            resource.namespace = self.parse_namespace(resource_element)
        elif node_name == "name":
            resource.name = self.parse_name(resource_element)
        elif node_name == "type":
            resource.type = self.parse_type(resource_element)
        elif node_name == "data":
            resource.data = self.parse_data(resource_element)

    def parse_namespace(self, namespace):
        resource_namespace = namespace.firstChild.data.strip()
        return resource_namespace

    def parse_name(self, name):
        resource_name = name.firstChild.data.strip()
        return resource_name

    def parse_type(self, type):
        resource_type = type.firstChild.data.strip()
        return resource_type

    def parse_data(self, data):
        resource_data = data.firstChild.data.strip()
        return resource_data

class Resource:
    """
    The resource class.
    """

    namespace = "none"
    name = "none"
    type = "none"
    data = "none"

    def __init__(self, namespace = "none", name = "none", type = "none", data = "none"):
        self.namespace = namespace
        self.name = name
        self.type = type
        self.data = data

def valid_node(node):
    """
    Gets if a node is valid or not for parsing
    
    @type node: Node
    @param node: The Xml node to be validated
    @rtype: bool
    @return: The valid or not valid value
    """

    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        return True
    else:
        return False
