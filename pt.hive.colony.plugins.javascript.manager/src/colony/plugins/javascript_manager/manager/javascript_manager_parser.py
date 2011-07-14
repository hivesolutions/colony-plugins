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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
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

class PluginDescriptorParser(Parser):

    file_path = None

    plugin_descriptor = None

    def __init__(self, file_path = None):
        Parser.__init__(self)
        self.file_path = file_path

    def parse(self):
        self.load_plugin_descriptor_file(self.file_path)

    def get_value(self):
        return self.plugin_descriptor

    def get_plugin_descriptor(self):
        return self.plugin_descriptor

    def load_plugin_descriptor_file(self, file_path):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parse(file_path)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.plugin_descriptor = self.parse_plugin_descriptor(child_node)

    def parse_plugin_descriptor(self, plugin_descriptor):
        plugin_descriptor_structure = PluginDescriptor()
        child_nodes = plugin_descriptor.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_plugin_descriptor_element(child_node, plugin_descriptor_structure)

        return plugin_descriptor_structure

    def parse_plugin_descriptor_element(self, plugin_descriptor_element, plugin_descriptor):
        node_name = plugin_descriptor_element.nodeName

        if node_name == "id":
            plugin_descriptor.id = self.parse_plugin_descriptor_id(plugin_descriptor_element)
        elif node_name == "name":
            plugin_descriptor.name = self.parse_plugin_descriptor_name(plugin_descriptor_element)
        elif node_name == "short_name":
            plugin_descriptor.short_name = self.parse_plugin_descriptor_short_name(plugin_descriptor_element)
            plugin_descriptor.shortName = plugin_descriptor.short_name
        elif node_name == "description":
            plugin_descriptor.description = self.parse_plugin_descriptor_description(plugin_descriptor_element)
        elif node_name == "version":
            plugin_descriptor.version = self.parse_plugin_descriptor_version(plugin_descriptor_element)
        elif node_name == "author":
            plugin_descriptor.author = self.parse_plugin_descriptor_author(plugin_descriptor_element)
        elif node_name == "main_class":
            plugin_descriptor.main_class = self.parse_plugin_descriptor_main_class(plugin_descriptor_element)
            plugin_descriptor.mainClass = plugin_descriptor.main_class
        elif node_name == "main_file":
            plugin_descriptor.main_file = self.parse_plugin_descriptor_main_file(plugin_descriptor_element)
            plugin_descriptor.mainFile = plugin_descriptor.main_file
        elif node_name == "zip_file":
            plugin_descriptor.zip_file = self.parse_plugin_descriptor_zip_file(plugin_descriptor_element)
            plugin_descriptor.zipFile = plugin_descriptor.zip_file

    def parse_plugin_descriptor_id(self, descriptor_id):
        plugin_descriptor_id = descriptor_id.firstChild.data.strip()
        return plugin_descriptor_id

    def parse_plugin_descriptor_name(self, descriptor_name):
        plugin_descriptor_name = descriptor_name.firstChild.data.strip()
        return plugin_descriptor_name

    def parse_plugin_descriptor_short_name(self, descriptor_name):
        plugin_descriptor_short_name = descriptor_name.firstChild.data.strip()
        return plugin_descriptor_short_name

    def parse_plugin_descriptor_description(self, descriptor_description):
        plugin_descriptor_description = descriptor_description.firstChild.data.strip()
        return plugin_descriptor_description

    def parse_plugin_descriptor_version(self, descriptor_description):
        plugin_descriptor_version = descriptor_description.firstChild.data.strip()
        return plugin_descriptor_version

    def parse_plugin_descriptor_author(self, descriptor_description):
        plugin_descriptor_author = descriptor_description.firstChild.data.strip()
        return plugin_descriptor_author

    def parse_plugin_descriptor_main_class(self, descriptor_description):
        plugin_descriptor_main_class = descriptor_description.firstChild.data.strip()
        return plugin_descriptor_main_class

    def parse_plugin_descriptor_main_file(self, descriptor_description):
        plugin_descriptor_main_file = descriptor_description.firstChild.data.strip()
        return plugin_descriptor_main_file

    def parse_plugin_descriptor_zip_file(self, descriptor_description):
        plugin_descriptor_zip_file = descriptor_description.firstChild.data.strip()
        return plugin_descriptor_zip_file

class PluginDescriptor:

    id = None
    """ The id of the plugin """

    name = "none"
    """ The name of the plugin """

    short_name = "none"
    """ The short name of the plugin """

    shortName = "none"
    """ The short name (compatibility) of the plugin """

    description = "none"
    """ The description of the plugin """

    version = "none"
    """ The version of the plugin """

    author = "none"
    """ The author of the plugin """

    main_class = "none"
    """ The main class of the plugin """

    mainClass = "none"
    """ The main class (compatibility) of the plugin """

    main_file = "none"
    """ The main file of the plugin """

    mainFile = "none"
    """ The main file (compatibility) of the plugin """

    zip_file = "none"
    """ The zip file of the plugin """

    zipFile = "none"
    """ The zip file (compatibility) of the plugin """

    def __init__(self, id = "none", name = "none", short_name = "none", description = "none", version = "none", author = "none", main_class = "none", main_file = "none", zip_file = "none"):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.description = description
        self.version = version
        self.author = author
        self.main_class = main_class
        self.main_file = main_file
        self.zip_file = zip_file

    def __repr__(self):
        return "<%s, %s, %s>" % (
            self.__class__.__name__,
            self.name,
            self.version
        )

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
