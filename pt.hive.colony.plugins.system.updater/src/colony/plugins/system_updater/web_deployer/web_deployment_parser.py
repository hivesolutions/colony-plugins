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

class WebDeployerConfigurationFileParser(Parser):

    file_path = None

    web_deployer_configuration = None

    def __init__(self, file_path = None):
        Parser.__init__(self)
        self.file_path = file_path

    def parse(self):
        self.load_web_deployer_configuration_file(self.file_path)

    def get_value(self):
        return self.web_deployer_configuration

    def get_web_deployer_configuration(self):
        return self.web_deployer_configuration

    def load_web_deployer_configuration_file(self, file_path):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parse(file_path)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.web_deployer_configuration = self.parse_web_deployer_configuration(child_node)

    def parse_web_deployer_configuration(self, web_deployer_configuration):
        web_deployer_configuration_structure = WebDeployerConfiguration()
        child_nodes = web_deployer_configuration.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_web_deployer_configuration_element(child_node, web_deployer_configuration_structure)

        return web_deployer_configuration_structure

    def parse_web_deployer_configuration_element(self, web_deployer_configuration_element, web_deployer_configuration):
        node_name = web_deployer_configuration_element.nodeName

        if node_name == "web_apps_path":
            web_deployer_configuration.web_apps_path = self.parse_web_deployer_configuration_web_apps_path(web_deployer_configuration_element)
        elif node_name == "project_path":
            web_deployer_configuration.project_path = self.parse_web_deployer_configuration_project_path(web_deployer_configuration_element)
        elif node_name == "plugins_path":
            web_deployer_configuration.plugins_path = self.parse_web_deployer_configuration_plugins_path(web_deployer_configuration_element)

    def parse_web_deployer_configuration_web_apps_path(self, configuration_web_apps_path):
        web_deployer_configuration_web_apps_path = configuration_web_apps_path.firstChild.data.strip()
        return web_deployer_configuration_web_apps_path

    def parse_web_deployer_configuration_project_path(self, configuration_project_path):
        web_deployer_configuration_project_path = configuration_project_path.firstChild.data.strip()
        return web_deployer_configuration_project_path

    def parse_web_deployer_configuration_plugins_path(self, configuration_plugins_path):
        web_deployer_configuration_plugins_path = configuration_plugins_path.firstChild.data.strip()
        return web_deployer_configuration_plugins_path

class WebDeployerConfiguration:
    web_apps_path = "none"
    project_path = "none"
    plugins_path = "none"

    def __init__(self, web_apps_path = "none", project_path = "none", plugins_path = "none"):
        self.web_apps_path = web_apps_path
        self.project_path = project_path
        self.plugins_path = plugins_path

    def __repr__(self):
        return "<%s, %s, %s, %s>" % (
            self.__class__.__name__,
            self.web_apps_path,
            self.plugins_path,
            self.plugins_path
        )

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
