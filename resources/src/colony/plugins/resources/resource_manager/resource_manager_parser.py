#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
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
                resource_list.append(self.parse_resource_element(child_node))

        return resource_list

    def parse_resource_element(self, resource_element):
        node_name = resource_element.nodeName

        if node_name == "plugin_configuration":
            resource = self.parse_plugin_configuration(resource_element)
        elif node_name == "resource":
            resource = self.parse_resource(resource_element)
        elif node_name == "validation":
            resource = self.parse_validation(resource_element)

        return resource

    def parse_plugin_configuration(self, plugin_configuration):
        plugin_configuration_structure = PluginConfiguration()
        child_nodes = plugin_configuration.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_plugin_configuration_element(child_node, plugin_configuration_structure)

        return plugin_configuration_structure

    def parse_plugin_configuration_element(self, plugin_configuration_element, plugin_configuration):
        node_name = plugin_configuration_element.nodeName

        if node_name == "plugin_id":
            plugin_configuration.plugin_id = self.parse_plugin_id(plugin_configuration_element)
        elif node_name == "resource":
            plugin_configuration.resources_list.append(self.parse_resource(plugin_configuration_element))

    def parse_plugin_id(self, plugin_id):
        plugin_configuration_plugin_id = plugin_id.firstChild.data.strip()
        return plugin_configuration_plugin_id

    def parse_resource(self, resource):
        resource_structure = Resource()
        child_nodes = resource.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_base_resource_element(child_node, resource_structure)

        return resource_structure

    def parse_base_resource_element(self, resource_element, resource):
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
        # retrieves the resource type
        resource_type = type.firstChild.data.strip()

        # returns the resource type
        return resource_type

    def parse_data(self, data):
        # in case there is a child available
        if data.firstChild:
            # strips the resource data from extra space
            resource_data = data.firstChild.data.strip()
        # in case the field is empty
        else:
            # sets the resource data as an empty string
            resource_data = ""

        # returns the resource data
        return resource_data

    def parse_validation(self, validation):
        validation_structure = Validation()
        child_nodes = validation.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_validation_element(child_node, validation_structure)

        return validation_structure

    def parse_validation_element(self, validation_element, validation):
        node_name = validation_element.nodeName

        if node_name == "equals_expression":
            validation.expression = self.parse_equals_expression(validation_element)

    def parse_equals_expression(self, equals_expression):
        equals_expression_structure = EqualsExpression()
        child_nodes = equals_expression.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_equals_expression_element(child_node, equals_expression_structure)

        return equals_expression_structure

    def parse_equals_expression_element(self, equals_expression_element, equals_expression):
        node_name = equals_expression_element.nodeName

        if node_name == "first_operand":
            equals_expression.first_operand = self.parse_operand(equals_expression_element)
        elif node_name == "second_operand":
            equals_expression.second_operand = self.parse_operand(equals_expression_element)

    def parse_operand(self, operand):
        operand_structure = Operand()
        child_nodes = operand.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_operand_element(child_node, operand_structure)

        return operand_structure

    def parse_operand_element(self, operand_element, operand):
        node_name = operand_element.nodeName

        if node_name == "type":
            operand.type = self.parse_type(operand_element)
        elif node_name == "data":
            operand.data = self.parse_data(operand_element)

class PluginConfiguration:
    """
    The plugin configuration class.
    """

    plugin_id = "none"
    """ The plugin configuration plugin id """

    resources_list = []
    """ The plugin configuration resources list """

    def __init__(self, plugin_id = "none"):
        self.plugin_id = plugin_id
        self.resources_list = []

class Resource:
    """
    The resource class.
    """

    namespace = "none"
    """ The resource namespace """

    name = "none"
    """ The resource name """

    type = "none"
    """ The resource type """

    data = "none"
    """ The resource data """

    process_resouce = None
    """ The process resource handler """

    def __init__(self, namespace = "none", name = "none", type = "none", data = "none"):
        self.namespace = namespace
        self.name = name
        self.type = type
        self.data = data

    def get_data(self):
        if self.parse_resource_data:
            if self.parse_resource_data(self):
                self.parse_resource_data = None
            else:
                return None

        return self.data

class Validation:
    """
    The validation class.
    """

    expression = None
    """ The validation expression """

    def __init__(self, expression = None):
        self.expression = expression

class Expression:
    """
    The expression class.
    """

    def __init__(self):
        pass

class UnaryExpressionNode(Expression):
    """
    The unary expression class.
    """

    operand = None
    """ The expression node """

    def __init__(self, operand = None):
        """
        Constructor of the class.

        @type operand: Expression
        @param operand: The operand of the binary expression.
        """

        Expression.__init__(self)

        self.operand = operand

class BinaryExpression(Expression):
    """
    The binary expression class.
    """

    first_operand = None
    """ The binary expression first operand """

    second_operand = None
    """ The binary expression second operand """

    def __init__(self, first_operand = None, second_operand = None):
        """
        Constructor of the class.

        @type first_operand: Expression
        @param first_operand:  The first operand of the binary expression.
        @type second_operand: Expression
        @param second_operand:  The second operand of the binary expression.
        """

        Expression.__init__(self)

        self.first_operand = first_operand
        self.second_operand = second_operand

class Operand:
    """
    The operand class.
    """

    type = "none"
    """ The operand type """

    data = "none"
    """ The operand data """

    def __init__(self, type = "none", data = "none"):
        """
        Constructor of the class.

        @type name: String
        @param name:  The operand type.
        @type data: Expression
        @param data:  The operand data.
        """

        self.type = type
        self.data = data

class EqualsExpression(BinaryExpression):
    """
    The equals expression class.
    """

    def __init__(self, first_operand = None, second_operand = None):
        """
        Constructor of the class.

        @type first_operand: Expression
        @param first_operand:  The first operand of the equals expression.
        @type second_operand: Expression
        @param second_operand:  The second operand of the equals expression.
        """

        BinaryExpression.__init__(self, first_operand, second_operand)

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
