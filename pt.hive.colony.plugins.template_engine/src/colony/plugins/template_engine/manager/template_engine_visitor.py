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

import cStringIO

import xml.sax.saxutils

import template_engine_ast
import template_engine_exceptions

def _visit(ast_node_class):
    """
    Decorator for the visit of an ast node.

    @type ast_node_class: String
    @param ast_node_class: The target class for the visit.
    @rtype: function
    @return: The created decorator.
    """

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the visit decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The decorator interceptor function.
        """

        func.ast_node_class = ast_node_class

        return func

    # returns the created decorator
    return decorator

def dispatch_visit():
    """
    Decorator for the dispatch visit of an ast node.

    @rtype: function
    @return: The created decorator.
    """

    def create_decorator_interceptor(func):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type func: function
        @param func: The callback function.
        """

        def decorator_interceptor(*args, **kwargs):
            """
            The interceptor function for the dispatch visit decorator.

            @type args: pointer
            @param args: The function arguments list.
            @type kwargs: pointer pointer
            @param kwargs: The function arguments map.
            """

            # retrieves the self values
            self_value = args[0]

            # retrieves the node value
            node_value = args[1]

            # retrieves the node value class
            node_value_class = node_value.__class__

            # retrieves the mro list from the node value class
            node_value_class_mro = node_value_class.mro()

            # iterates over all the node value class mro elements
            for node_value_class_mro_element in node_value_class_mro:
                # in case the node method map exist in the current instance
                if hasattr(self_value, "node_method_map"):
                    # retrieves the node method map from the current instance
                    node_method_map = getattr(self_value, "node_method_map")

                    # in case the node value class exists in the node method map
                    if node_value_class_mro_element in node_method_map:
                        # retrieves the visit method for the given node value class
                        visit_method = node_method_map[node_value_class_mro_element]

                        # calls the before visit method
                        self_value.before_visit(*args[1:], **kwargs)

                        # calls the visit method
                        visit_method(*args, **kwargs)

                        # calls the after visit method
                        self_value.after_visit(*args[1:], **kwargs)

                        return

            # in case of failure to find the proper callbak
            func(*args, **kwargs)

        return decorator_interceptor

    def decorator(func, *args, **kwargs):
        """
        The decorator function for the dispatch visit decorator.

        @type func: function
        @param func: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: function
        @param: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(func)

        # returns the interceptor to be used
        return decorator_interceptor_function

    # returns the created decorator
    return decorator


class Visitor:
    """
    The visitor class.
    """

    node_method_map = {}
    """ The node method map """

    visit_childs = True
    """ The visit childs flag """

    visit_next = True
    """ The visit next flag """

    global_map = {}
    """ The global map """

    string_buffer = None
    """ The string buffer """

    def __init__(self):
        self.node_method_map = {}
        self.visit_childs = True
        self.visit_next = True
        self.global_map = {}
        self.string_buffer = cStringIO.StringIO()

        self.update_node_method_map()

    def update_node_method_map(self):
        # retrieves the class of the current instance
        self_class = self.__class__

        # retrieves the names of the elements for the current class
        self_class_elements = dir(self_class)

        # iterates over all the name of the elements
        for self_class_element in self_class_elements:
            # retrieves the real element value
            self_class_real_element = getattr(self_class, self_class_element)

            # in case the current class real element contains an ast node class reference
            if hasattr(self_class_real_element, "ast_node_class"):
                # retrieves the ast node class from the current class real element
                ast_node_class = getattr(self_class_real_element, "ast_node_class")

                self.node_method_map[ast_node_class] = self_class_real_element

    def get_global_map(self):
        return self.global_map

    def set_global_map(self, global_map):
        self.global_map = global_map

    def add_global_variable(self, variable_name, variable_value):
        self.global_map[variable_name] = variable_value

    def remove_global_variable(self, variable_name):
        del self.global_map[variable_name]

    @dispatch_visit()
    def visit(self, node):
        print "unrecognized element node of type " + node.__class__.__name__

    def before_visit(self, node):
        self.visit_childs = True
        self.visit_next = True

    def after_visit(self, node):
        pass

    @_visit(template_engine_ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @_visit(template_engine_ast.RootNode)
    def visit_root_node(self, node):
        pass

    @_visit(template_engine_ast.LiteralNode)
    def visit_literal_node(self, node):
        self.string_buffer.write(node.value.match_value)

    @_visit(template_engine_ast.MatchNode)
    def visit_match_node(self, node):
        pass

    @_visit(template_engine_ast.SingleNode)
    def visit_single_node(self, node):
        pass

    @_visit(template_engine_ast.CompositeNode)
    def visit_composite_node(self, node):
        pass

    def process_accept(self, node, name):
        getattr(self, "process_" + name)(node)

    def process_out(self, node):
        attributes_map = node.get_attributes_map()
        attribute_value = attributes_map["value"]
        attribute_value_value = self.get_value(attribute_value)

        if "format" in attributes_map:
            format_string = attributes_map["format"]
            format_string_value = self.get_value(format_string)
            attribute_value_value = format_string_value % attribute_value_value

        if "xml_escape" in attributes_map:
            attribute_xml_escape = attributes_map["xml_escape"]
            attribute_xml_escape_value = self.get_boolean_value(attribute_xml_escape)
        else:
            attribute_xml_escape_value = False

        attribute_value_value = unicode(attribute_value_value).encode("utf-8")

        if attribute_xml_escape_value:
            attribute_value_value = xml.sax.saxutils.escape(attribute_value_value)

        self.string_buffer.write(attribute_value_value)

    def process_out_none(self, node):
        attributes_map = node.get_attributes_map()
        attribute_value = attributes_map["value"]
        attribute_value_value = self.get_value(attribute_value)
        if "xml_escape" in attributes_map:
            attribute_xml_escape = attributes_map["xml_escape"]
            attribute_xml_escape_value = self.get_boolean_value(attribute_xml_escape)
        else:
            attribute_xml_escape_value = False

        if not attribute_value_value == None:
            attribute_value_value = unicode(attribute_value_value).encode("utf-8")

            if attribute_xml_escape_value:
                attribute_value_value = xml.sax.saxutils.escape(attribute_value_value)

            self.string_buffer.write(attribute_value_value)

    def process_var(self, node):
        attributes_map = node.get_attributes_map()
        attribute_item = attributes_map["item"]
        attribute_item_literal_value = self.get_literal_value(attribute_item)
        attribute_value = attributes_map["value"]
        attribute_value_value = self.get_value(attribute_value)

        self.global_map[attribute_item_literal_value] = attribute_value_value

    def process_foreach(self, node):
        attributes_map = node.get_attributes_map()
        attribute_from = attributes_map["from"]
        attribute_from_value = self.get_value(attribute_from)
        attribute_item = attributes_map["item"]
        attribute_item_literal_value = self.get_literal_value(attribute_item)

        for attribute_from_value_item in attribute_from_value:
            self.global_map[attribute_item_literal_value] = attribute_from_value_item

            if self.visit_childs:
                for node_child_node in node.child_nodes:
                    node_child_node.accept(self)

    def process_if(self, node):
        attributes_map = node.get_attributes_map()
        attribute_item = attributes_map["item"]
        attribute_item_value = self.get_value(attribute_item)
        attribute_value = attributes_map["value"]
        attribute_value_value = self.get_value(attribute_value)
        attribute_operator = attributes_map["operator"]
        attribute_operator_literal_value = self.get_literal_value(attribute_operator)

        if attribute_operator_literal_value == "eq":
            result = attribute_item_value == attribute_value_value
        elif attribute_operator_literal_value == "neq":
            result = not attribute_item_value == attribute_value_value
        elif attribute_operator_literal_value == "gte":
            result = attribute_item_value >= attribute_value_value
        elif attribute_operator_literal_value == "gt":
            result = attribute_item_value > attribute_value_value
        elif attribute_operator_literal_value == "lte":
            result = attribute_item_value <= attribute_value_value
        elif attribute_operator_literal_value == "lt":
            result = attribute_item_value < attribute_value_value

        if result:
            if self.visit_childs:
                for node_child_node in node.child_nodes:
                    node_child_node.accept(self)

    def get_value(self, attribute_value):
        # in case the attribute value is of type variable
        if attribute_value["type"] == "variable":
            # retrieves the variable name
            variable_name = attribute_value["value"]

            # in case the variable name is none
            if variable_name == "None":
                value = None
            else:
                # splits the variable name in the dots
                variable_name_splitted = variable_name.split(".")

                # retrieves the first variable name split
                first_variable_name_split = variable_name_splitted[0]

                # sets the current variable as the first split
                current_variable = self.global_map[first_variable_name_split]

                for variable_name_split in variable_name_splitted[1:]:
                    # retrieves the current variable
                    current_variable = getattr(current_variable, variable_name_split)

                # sets the value as the current variable value
                value = current_variable
        # in case the attribute value is of type literal
        elif attribute_value["type"] == "literal":
            # retrieves the literal value
            literal_value = attribute_value["value"]

            # strips the literal value
            literal_value_stripped = literal_value.strip("\"")

            # sets the value as the literal value stripped
            value = literal_value_stripped

        # returns the value
        return value

    def get_literal_value(self, attribute_value):
        literal_value = attribute_value["value"]

        return literal_value

    def get_boolean_value(self, attribute_value):
        literal_value = attribute_value["value"]

        if literal_value == "True":
            return True
        elif literal_value == "False":
            return False

        raise template_engine_exceptions.InvalidBooleanValue("invalid boolean " + literal_value)
