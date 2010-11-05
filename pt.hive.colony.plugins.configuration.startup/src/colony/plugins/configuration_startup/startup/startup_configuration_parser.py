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
    The abstract parser class
    """

    def __init__(self):
        """
        Constructor of the class
        """

        pass

    def parse(self):
        """
        Parses the defined file
        """

        pass

    def get_value(self):
        """
        Retrieves the result of the parse

        @rtype: Object
        @return: The result of the parse
        """

        pass

class StartupConfigurationParser(Parser):
    """
    The startup configuration parser class
    """

    file_path = None
    """ The path to the xml file """

    startup_configration = None
    """ The startup configuration structure """

    def __init__(self, file_path = None):
        """
        Constructor of the class

        @type file_path: String
        @param file_path: The path to the xml file
        """

        Parser.__init__(self)
        self.file_path = file_path

    def parse(self):
        self.load_startup_configuration_file(self.file_path)

    def get_value(self):
        return self.startup_configration

    def get_startup_configuration(self):
        return self.startup_configuration

    def load_startup_configuration_file(self, file_path):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parse(file_path)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.startup_configration = self.parse_startup_configuration(child_node)

    def parse_startup_configuration(self, startup_configuration):
        startup_configuration_structure = StartupConfiguration()
        child_nodes = startup_configuration.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_startup_configuration_element(child_node, startup_configuration_structure)

        return startup_configuration_structure

    def parse_startup_configuration_element(self, startup_configuration_element, startup_configuration):
        node_name = startup_configuration_element.nodeName

        if node_name == "plugins":
            startup_configuration.plugins = self.parse_startup_configuration_plugins(startup_configuration_element)

    def parse_startup_configuration_plugins(self, startup_configuration_plugins):
        startup_configuration_plugins_list = []
        child_nodes = startup_configuration_plugins.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                startup_configuration_plugin = self.parse_startup_configuration_plugin(child_node)
                startup_configuration_plugins_list.append(startup_configuration_plugin)

        return startup_configuration_plugins_list

    def parse_startup_configuration_plugin(self, startup_configuration_plugin):
        startup_configuration_plugin_structure = StartupConfigurationPlugin()
        child_nodes = startup_configuration_plugin.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_startup_configuration_plugin_element(child_node, startup_configuration_plugin_structure)

        return startup_configuration_plugin_structure

    def parse_startup_configuration_plugin_element(self, startup_configuration_plugin_element, startup_configuration_plugin):
        node_name = startup_configuration_plugin_element.nodeName

        if node_name == "name":
            startup_configuration_plugin.name = self.parse_startup_configuration_plugin_name(startup_configuration_plugin_element)
        elif node_name == "id":
            startup_configuration_plugin.id = self.parse_startup_configuration_plugin_id(startup_configuration_plugin_element)
        elif node_name == "version":
            startup_configuration_plugin.version = self.parse_startup_configuration_plugin_version(startup_configuration_plugin_element)
        elif node_name == "load":
            startup_configuration_plugin.load = self.parse_startup_configuration_plugin_load(startup_configuration_plugin_element)

    def parse_startup_configuration_plugin_name(self, configuration_plugin_name):
        startup_configuration_plugin_name = configuration_plugin_name.firstChild.data.strip()
        return startup_configuration_plugin_name

    def parse_startup_configuration_plugin_id(self, configuration_plugin_id):
        startup_configuration_plugin_id = configuration_plugin_id.firstChild.data.strip()
        return startup_configuration_plugin_id

    def parse_startup_configuration_plugin_version(self, configuration_plugin_version):
        startup_configuration_plugin_version = configuration_plugin_version.firstChild.data.strip()
        return startup_configuration_plugin_version

    def parse_startup_configuration_plugin_load(self, configuration_plugin_load):
        if configuration_plugin_load.firstChild.data == "true":
            startup_configuration_plugin_load = True
        elif configuration_plugin_load.firstChild.data == "false":
            startup_configuration_plugin_load = False

        return startup_configuration_plugin_load

class StartupConfiguration:

    plugins = []

    def __init__(self):
        self.plugins = []

    def __repr__(self):
        return "<%s>" % (
            self.__class__.__name__
        )

class StartupConfigurationPlugin:

    name = "none"
    id = "none"
    version = "none"
    load = True

    def __init__(self, name = "none", id = "none", version = "none", load = True):
        self.name = name
        self.id = id
        self.version = version
        self.load = load

    def __repr__(self):
        return "<%s, %s, %s, %s>" % (
            self.__class__.__name__,
            self.name,
            self.id,
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
