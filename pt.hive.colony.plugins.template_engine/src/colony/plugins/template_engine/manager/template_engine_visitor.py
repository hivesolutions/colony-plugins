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

import os
import types
import datetime

import xml.sax.saxutils

import colony.libs.quote_util
import colony.libs.structures_util
import colony.libs.string_buffer_util

import template_engine_ast
import template_engine_exceptions

FUNCTION_TYPES = (types.MethodType, types.FunctionType, types.BuiltinMethodType, types.BuiltinFunctionType)
""" The function types """

VALUE_VALUE = "value"
""" The value value """

VALUES_VALUE = "values"
""" The values value """

TYPE_VALUE = "type"
""" The type value """

FORMAT_VALUE = "format"
""" The format value """

VARIABLE_VALUE = "variable"
""" The variable value """

LITERAL_VALUE = "literal"
""" The literal value """

FILE_VALUE = "file"
""" The file value """

FILE_VALUE_VALUE = "file_value"
""" The file value value """

ITEM_VALUE = "item"
""" The item value """

OPERATOR_VALUE = "operator"
""" The operator value """

FROM_VALUE = "from"
""" The from value """

INDEX_VALUE = "index"
""" The index value """

KEY_VALUE = "key"
""" The key value """

START_INDEX_VALUE = "start_index"
""" The start index value """

PREFIX_VALUE = "prefix"
""" The prefix value """

QUOTE_VALUE = "quote"
""" The quote value """

KEY_MAP_VALUE = "key_map"
""" The key map value """

XML_ESCAPE_VALUE = "xml_escape"
""" The xml escape value """

ALLOW_EMPTY_VALUE = "allow_empty"
""" The allow empty value """

KEY_SEPARATOR_VALUE = "key_separator"
""" The key separator value """

ITEM_SEPARATOR_VALUE = "item_separator"
""" The item separator value """

ELSE_VALUE = "else"
""" The else value """

ELIF_VALUE = "elif"
""" The elif value """

NONE_VALUE = "None"
""" The none value """

ITER_VALUE = "__iter__"
""" The iter value """

QUOTE_ENCODING = "utf-8"
""" The quote encoding """

PROCESS_METHOD_PREFIX = "process_"
""" The process method prefix """

DEFAULT_YEAR_FORMAT = "%Y"
""" The default year format """

DEFAULT_DATE_FORMAT = "%d/%m/%y"
""" The default date format """

DEFAULT_TIME_FORMAT = "%H:%M:%S"
""" The default time format """

DEFAULT_DATE_TIME_FORMAT = "%d/%m/%y %H:%M:%S"
""" The default date time format """

COMPARISION_FUNCTIONS = {"eq" : lambda attribute_item, attribute_value: attribute_item == attribute_value,
                         "neq" : lambda attribute_item, attribute_value: not attribute_item == attribute_value,
                         "gte" : lambda attribute_item, attribute_value: attribute_item >= attribute_value,
                         "gt" : lambda attribute_item, attribute_value: attribute_item > attribute_value,
                         "lte" : lambda attribute_item, attribute_value: attribute_item <= attribute_value,
                         "lte" : lambda attribute_item, attribute_value: attribute_item < attribute_value}
""" The map containing the comparison functions (lambda) """

def _visit(ast_node_class):
    """
    Decorator for the visit of an ast node.

    @type ast_node_class: String
    @param ast_node_class: The target class for the visit.
    @rtype: Function
    @return: The created decorator.
    """

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the visit decorator.

        @type function: Function
        @param function: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: Function
        @param: The decorator interceptor function.
        """

        function.ast_node_class = ast_node_class

        return function

    # returns the created decorator
    return decorator

def dispatch_visit():
    """
    Decorator for the dispatch visit of an ast node.

    @rtype: Function
    @return: The created decorator.
    """

    def create_decorator_interceptor(function):
        """
        Creates a decorator interceptor, that intercepts the normal function call.

        @type function: Function
        @param function: The callback function.
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
            function(*args, **kwargs)

        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        """
        The decorator function for the dispatch visit decorator.

        @type function: Function
        @param function: The function to be decorated.
        @type args: pointer
        @param args: The function arguments list.
        @type kwargs: pointer pointer
        @param kwargs: The function arguments map.
        @rtype: Function
        @param: The decorator interceptor function.
        """

        # creates the decorator interceptor with the given function
        decorator_interceptor_function = create_decorator_interceptor(function)

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

    encoding = None
    """ The encoding used the file """

    file_path = None
    """ The path to the file """

    template_engine_manager = None
    """ The template engine manager """

    variable_encoding = None
    """ The variable encoding """

    strict_mode = False
    """ The strict mode """

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
        self.string_buffer = colony.libs.string_buffer_util.StringBuffer()

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

    def get_encoding(self):
        """
        Retrieves encoding used in the file.

        @rtype: String
        @return: The encoding used in the file.
        """

        return self.encoding

    def set_encoding(self, encoding):
        """
        Sets the encoding used in the file.

        @type encoding: String
        @param encoding: The encoding used in the file.
        """

        self.encoding = encoding

    def get_file_path(self):
        """
        Retrieves path to the file.

        @rtype: String
        @return: The path to the file.
        """

        return self.file_path

    def set_file_path(self, file_path):
        """
        Sets the path to the file.

        @type file_path: String
        @param file_path: The path to the file.
        """

        self.file_path = file_path

    def get_template_engine_manager(self):
        """
        Retrieves the template engine manager.

        @rtype: TemplateEngineManager
        @return: The template engine manager.
        """

        return self.template_engine_manager

    def set_template_engine_manager(self, template_engine_manager):
        """
        Sets the template engine manager.

        @type template_engine_manager: TemplateEngineManager
        @param template_engine_manager: The template engine manager.
        """

        self.template_engine_manager = template_engine_manager

    def get_variable_encoding(self):
        """
        Retrieves the variable encoding.

        @rtype: String
        @return: The variable encoding.
        """

        return self.variable_encoding

    def set_variable_encoding(self, variable_encoding):
        """
        Sets the variable encoding.

        @type variable_encoding: String
        @param variable_encoding: The variable encoding.
        """

        self.variable_encoding = variable_encoding

    def get_strict_mode(self):
        """
        Retrieves the strict mode.

        @rtype: bool
        @return: The strict mode.
        """

        return self.strict_mode

    def set_strict_mode(self, strict_mode):
        """
        Sets the strict mode.

        @type strict_mode: String
        @param strict_mode: The strict mode.
        """

        self.strict_mode = strict_mode

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
        # retrieves the process method for the name
        process_method = getattr(self, PROCESS_METHOD_PREFIX + name)

        # calls the process method with the node
        process_method(node)

    def process_out(self, node):
        """
        Processes the out node.

        @type node: SingleNode
        @param node: The single node to be processed as out.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # retrieves the attributes map values
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)

        # in case the prefix exists in the attributes map
        if PREFIX_VALUE in attributes_map:
            # retrieves attribute prefix value
            attribute_prefix = attributes_map[PREFIX_VALUE]
            attribute_prefix_value = self.get_value(attribute_prefix)
        # otherwise
        else:
            # sets the default prefix value
            attribute_prefix_value = ""

        # in case the format exists in the attributes map
        if FORMAT_VALUE in attributes_map:
            # retrieves attribute value value
            format_string = attributes_map[FORMAT_VALUE]
            format_string_value = self.get_value(format_string)
            attribute_value_value = format_string_value % attribute_value_value

        # in case the quote exists in the attributes map
        if QUOTE_VALUE in attributes_map:
            # retrieves attribute quote value
            attribute_quote = attributes_map[QUOTE_VALUE]
            attribute_quote_value = self.get_boolean_value(attribute_quote)
        # otherwise
        else:
            # unsets the attribute quote value
            attribute_quote_value = False

        # in case the xml escape exists in the attributes map
        if XML_ESCAPE_VALUE in attributes_map:
            # retrieves the attribute xml escape value
            attribute_xml_escape = attributes_map[XML_ESCAPE_VALUE]
            attribute_xml_escape_value = self.get_boolean_value(attribute_xml_escape)
        # otherwise
        else:
            # unsets the attribute xml escape value
            attribute_xml_escape_value = False

        # in case the variable encoding is defined
        if self.variable_encoding:
            # re-encodes the variable value
            attribute_value_value = unicode(attribute_value_value).encode(self.variable_encoding)
        else:
            # converts the value into unicode (in case it's necessary)
            attribute_value_value = unicode(attribute_value_value)

        # in case the attribute quote value is set
        if attribute_quote_value:
            # re-encodes the value
            attribute_value_value = attribute_value_value.encode(QUOTE_ENCODING)

            # quotes the attribute value value
            attribute_value_value = colony.libs.quote_util.quote(attribute_value_value, "/")

        # in case the attribute xml escape value is set
        if attribute_xml_escape_value:
            # escapes the attribute value value using xml escaping
            attribute_value_value = xml.sax.saxutils.escape(attribute_value_value)

        # adds the attribute prefix value to the attribute value value
        attribute_value_value = attribute_prefix_value + attribute_value_value

        # writes the attribute value value to the string buffer
        self.string_buffer.write(attribute_value_value)

    def process_out_none(self, node):
        """
        Processes the out none node.

        @type node: SingleNode
        @param node: The single node to be processed as out none.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # retrieves the attributes map values
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)

        # in case the prefix exists in the attributes map
        if PREFIX_VALUE in attributes_map:
            # retrieves attribute prefix value
            attribute_prefix = attributes_map[PREFIX_VALUE]
            attribute_prefix_value = self.get_value(attribute_prefix)
        # otherwise
        else:
            # sets the default prefix value
            attribute_prefix_value = ""

        # in case the format exists in the attributes map
        if FORMAT_VALUE in attributes_map:
            # retrieves attribute value value
            format_string = attributes_map[FORMAT_VALUE]
            format_string_value = self.get_value(format_string)
            attribute_value_value = format_string_value % attribute_value_value

        # in case the quote exists in the attributes map
        if QUOTE_VALUE in attributes_map:
            # retrieves attribute quote value
            attribute_quote = attributes_map[QUOTE_VALUE]
            attribute_quote_value = self.get_boolean_value(attribute_quote)
        # otherwise
        else:
            # unsets the attribute quote value
            attribute_quote_value = False

        # in case the xml escape exists in the attributes map
        if XML_ESCAPE_VALUE in attributes_map:
            # retrieves attribute xml escape value
            attribute_xml_escape = attributes_map[XML_ESCAPE_VALUE]
            attribute_xml_escape_value = self.get_boolean_value(attribute_xml_escape)
        # otherwise
        else:
            # unsets the attribute xml escape value
            attribute_xml_escape_value = False

        # in case the allow empty exists in the attributes map
        if ALLOW_EMPTY_VALUE in attributes_map:
            # retrieves attribute allow empty value
            attribute_allow_empty = attributes_map[ALLOW_EMPTY_VALUE]
            attribute_allow_empty_value = self.get_value(attribute_allow_empty)
        # otherwise
        else:
            # sets the attribute allow empty value
            attribute_allow_empty_value = True

        # creates the invalid values tuple
        invalid_values = attribute_allow_empty_value and (None,) or (None, "")

        # in case the attribute value value is invalid
        if attribute_value_value in invalid_values:
            # returns immediately (no write)
            return

        # in case the variable encoding is defined
        if self.variable_encoding:
            # re-encodes the variable value
            attribute_value_value = attribute_value_value.encode(self.variable_encoding)
        else:
            # converts the value into unicode (in case it's necessary)
            attribute_value_value = unicode(attribute_value_value)

        # in case the attribute quote value is set
        if attribute_quote_value:
            # re-encodes the value
            attribute_value_value = attribute_value_value.encode(QUOTE_ENCODING)

            # quotes the attribute value value
            attribute_value_value = colony.libs.quote_util.quote(attribute_value_value, "/")

        # in case the attribute xml escape value is set
        if attribute_xml_escape_value:
            # escapes the attribute value value using xml escaping
            attribute_value_value = xml.sax.saxutils.escape(attribute_value_value)

        # adds the attribute prefix value to the attribute value value
        attribute_value_value = attribute_prefix_value + attribute_value_value

        # writes the attribute value value in the string buffer
        self.string_buffer.write(attribute_value_value)

    def process_out_map(self, node):
        """
        Processes the out none node.

        @type node: SingleNode
        @param node: The single node to be processed as out none.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # retrieves the attributes map values
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)

        # in case the key map exists in the attributes map
        if KEY_MAP_VALUE in attributes_map:
            # retrieves attribute key map value
            attribute_key_map = attributes_map[KEY_MAP_VALUE]
            attribute_key_map_value = self.get_value(attribute_key_map)
        # otherwise
        else:
            # sets the attribute key map value
            attribute_key_map_value = {}

        # in case the key separator exists in the attributes map
        if KEY_SEPARATOR_VALUE in attributes_map:
            # retrieves attribute key separator value
            attribute_key_separator = attributes_map[KEY_SEPARATOR_VALUE]
            attribute_key_separator_value = self.get_value(attribute_key_separator)
        # otherwise
        else:
            # sets the attribute key separator value
            attribute_key_separator_value = ": "

        # in case the item separator exists in the attributes map
        if ITEM_SEPARATOR_VALUE in attributes_map:
            # retrieves attribute item separator value
            attribute_item_separator = attributes_map[ITEM_SEPARATOR_VALUE]
            attribute_item_separator_value = self.get_value(attribute_item_separator)
        # otherwise
        else:
            # sets the attribute item separator value
            attribute_item_separator_value = "\n"

        # in case the xml escape exists in the attributes map
        if XML_ESCAPE_VALUE in attributes_map:
            # retrieves attribute xml escape value
            attribute_xml_escape = attributes_map[XML_ESCAPE_VALUE]
            attribute_xml_escape_value = self.get_boolean_value(attribute_xml_escape)
        # otherwise
        else:
            # unsets the attribute xml escape value
            attribute_xml_escape_value = False

        # in case the allow empty exists in the attributes map
        if ALLOW_EMPTY_VALUE in attributes_map:
            # retrieves attribute allow empty value
            attribute_allow_empty = attributes_map[ALLOW_EMPTY_VALUE]
            attribute_allow_empty_value = self.get_value(attribute_allow_empty)
        # otherwise
        else:
            # sets the attribute allow empty value
            attribute_allow_empty_value = True

        # creates the invalid values tuple
        invalid_values = attribute_allow_empty_value and (None,) or (None, "")

        # iterates over all the attribute value value items
        for key, value in attribute_value_value.items():
            # in case the value is invalid
            if value in invalid_values:
                # skips the iteration
                continue

            # tries to retrieve the key from the attribute
            # key map value
            key = attribute_key_map_value.get(key, key)

            # in case the variable encoding is defined
            if self.variable_encoding:
                # re-encodes the variable value
                value = value.encode(self.variable_encoding)
            else:
                # converts the value into unicode (in case it's necessary)
                value = unicode(value)

            # in case the attribute xml escape value is set
            if attribute_xml_escape_value:
                # escapes the key using xml escaping
                key = xml.sax.saxutils.escape(key)

                # escapes the value using xml escaping
                value = xml.sax.saxutils.escape(value)

            # writes the attribute value value in the string buffer
            self.string_buffer.write(key + attribute_key_separator_value + value + attribute_item_separator_value)

    def process_var(self, node):
        """
        Processes the var node.

        @type node: SingleNode
        @param node: The single node to be processed as var.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # retrieves the attributes map values
        attribute_item = attributes_map[ITEM_VALUE]
        attribute_item_literal_value = self.get_literal_value(attribute_item)
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)

        # sets the attribute value value in the global map
        self.global_map[attribute_item_literal_value] = attribute_value_value

    def process_foreach(self, node):
        """
        Processes the foreach node.

        @type node: SingleNode
        @param node: The single node to be processed as foreach.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # retrieves the attributes map values
        attribute_from = attributes_map[FROM_VALUE]
        attribute_from_value = self.get_value(attribute_from)
        attribute_item = attributes_map[ITEM_VALUE]
        attribute_item_literal_value = self.get_literal_value(attribute_item)

        # in case the index exists in the attributes map
        if INDEX_VALUE in attributes_map:
            # retrieves the attribute index literal value
            attribute_index = attributes_map[INDEX_VALUE]
            attribute_index_literal_value = self.get_literal_value(attribute_index)
        else:
            # sets the attribute index literal value as none
            attribute_index_literal_value = None

        # in case the key exists in the attributes map
        if KEY_VALUE in attributes_map:
            # retrieves the attribute key literal value
            attribute_key = attributes_map[KEY_VALUE]
            attribute_key_literal_value = self.get_literal_value(attribute_key)
        else:
            # sets the attribute key literal value as none
            attribute_key_literal_value = None

        # in case the start index exists in the attributes map
        if START_INDEX_VALUE in attributes_map:
            # retrieves the attribute start index literal value
            attribute_start_index = attributes_map[START_INDEX_VALUE]
            attribute_start_index_literal_value = self.get_literal_value(attribute_start_index)

            # sets the initial index
            index = int(attribute_start_index_literal_value[1:-1])
        else:
            # sets the default initial index
            index = 1

        # in case the attribute does not have the iterator method
        # it's not iterable
        if not hasattr(attribute_from_value, ITER_VALUE):
            # in case the strict mode is active
            if self.strict_mode:
                # retrieves the attribute from value
                attribute_from_value = attribute_from[VALUE_VALUE]

                # raises the variable not iterable exception
                raise template_engine_exceptions.VariableNotIterable("value not iterable: " + attribute_from_value)
            # otherwise avoids exception
            else:
                # "casts" the attribute from value to a list
                attribute_from_value = [attribute_from_value]

        # in case the type of the attribute from value is dictionary
        if colony.libs.structures_util.is_dictionary(attribute_from_value):
            # iterates over all the attribute from value items
            for attribute_from_value_key, attribute_from_value_value in attribute_from_value.items():
                # sets the attribute from value value in the global map
                self.global_map[attribute_item_literal_value] = attribute_from_value_value

                if attribute_index_literal_value:
                    self.global_map[attribute_index_literal_value] = index

                if attribute_key_literal_value:
                    self.global_map[attribute_key_literal_value] = attribute_from_value_key

                if self.visit_childs:
                    for node_child_node in node.child_nodes:
                        node_child_node.accept(self)

                # increments the index
                index += 1
        # otherwise it must be a sequence
        else:
            # iterates over all the attribute from value values
            for attribute_from_value_item in attribute_from_value:
                # sets the attribute from value item in the global map
                self.global_map[attribute_item_literal_value] = attribute_from_value_item

                if attribute_index_literal_value:
                    self.global_map[attribute_index_literal_value] = index

                if self.visit_childs:
                    for node_child_node in node.child_nodes:
                        node_child_node.accept(self)

                # increments the index
                index += 1

    def process_if(self, node):
        """
        Processes the if node.

        @type node: SingleNode
        @param node: The single node to be processed as if.
        """

        # evaluates the node as comparison
        result = self._evaluate_comparison_node(node)

        # sets the initial accept node value
        accept_node = result

        # in case the visit child is set
        if self.visit_childs:
            # iterates over all the node child nodes
            for node_child_node in node.child_nodes:
                # validates the accept node using the node child node
                # and the accept node
                accept_node = self._validate_accept_node(node_child_node, accept_node)

                # in case the accept node is set to invalid
                # the evaluation is over
                if accept_node == None:
                    # returns immediately
                    return

                # in case the accept node flag is set
                # accepts the node child node
                accept_node and node_child_node.accept(self)

    def process_else(self, node):
        """
        Processes the else node.

        @type node: SingleNode
        @param node: The single node to be processed as else.
        """

        pass

    def process_elif(self, node):
        """
        Processes the elif node.

        @type node: SingleNode
        @param node: The single node to be processed as elif.
        """

        pass

    def process_cycle(self, node):
        """
        Processes the cycle node.

        @type node: SingleNode
        @param node: The single node to be processed as cycle.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # retrieves the attributes map values
        attribute_values = attributes_map[VALUES_VALUE]
        attribute_values_value = self.get_value(attribute_values, True)

        if not hasattr(node, "current_index"):
            # sets the initial current index
            current_index = 0
        else:
            # retrieves the attribute values value length
            attribute_values_value_length = len(attribute_values_value)

            # retrieves the current index
            current_index = node.current_index

            # in case the current index overflows
            if current_index == attribute_values_value_length - 1:
                # resets the current index
                current_index = 0
            # otherwise
            else:
                # increments the current index
                current_index += 1

        # sets the current index in the node
        node.current_index = current_index

        # retrieves the current value from the attribute
        # values values
        current_value = attribute_values_value[current_index]

        # writes the current value to the string buffer
        self.string_buffer.write(current_value)

    def process_count(self, node):
        """
        Processes the count node.

        @type node: SingleNode
        @param node: The single node to be processed as count.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # retrieves the attributes map values
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)

        # retrieves the attribute value value length and sets it
        # as the attribute value length
        attribute_value_length = len(attribute_value_value)

        # in case the variable encoding is defined
        if self.variable_encoding:
            # re-encodes the variable value
            attribute_value_length = unicode(attribute_value_length).encode(self.variable_encoding)
        else:
            # converts the value into unicode (in case it's necessary)
            attribute_value_length = unicode(attribute_value_length)

        # writes the attribute value value to the string buffer
        self.string_buffer.write(attribute_value_length)

    def process_include(self, node):
        """
        Processes the include node.

        @type node: SingleNode
        @param node: The single node to be processed as include.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # in case the file exists in the attributes map
        if FILE_VALUE in attributes_map:
            # retrieves the attribute file literal value
            attribute_file = attributes_map[FILE_VALUE]
            attribute_file_literal_value = self.get_literal_value(attribute_file)

        # in case the file value exists in the attributes map
        if FILE_VALUE_VALUE in attributes_map:
            # retrieves the attribute file literal value
            attribute_file_value = attributes_map[FILE_VALUE_VALUE]
            attribute_file_literal_value = self.get_value(attribute_file_value)

        # in case the attribute file literal value is not valid
        if not attribute_file_literal_value:
            # retrieves the node value type
            node_value_type = node.get_value_type()

            # raises the undefined reference exception
            raise template_engine_exceptions.UndefinedReference(node_value_type)

        # in case the path is absolute
        if attribute_file_literal_value[0] == "/":
            # sets the file path as absolute
            file_path = attribute_file_literal_value
        # in case the path is relative to the current file
        else:
            # retrieves the file directory from the file path
            file_directory = os.path.dirname(self.file_path)

            # sets the file path as relative to the file directory
            file_path = file_directory + "/" + attribute_file_literal_value

        # parses the file retrieving the template file
        template_file = self.template_engine_manager.parse_file_path(file_path, self.encoding)

        # sets the global map in template file
        template_file.set_global_map(self.global_map)

        # sets the variable encoding in the template file
        template_file.set_variable_encoding(self.variable_encoding)

        # processes the template file
        processed_template_file = template_file.process()

        # writes the processed template file to the string buffer
        self.string_buffer.write(processed_template_file)

    def process_year(self, node):
        """
        Processes the year node.

        @type node: SingleNode
        @param node: The single node to be processed as year.
        """

        # retrieves the current date time
        current_date_time = datetime.datetime.now()

        # formats the year value
        year_value = current_date_time.strftime(DEFAULT_YEAR_FORMAT)

        # writes the year value
        self.string_buffer.write(year_value)

    def process_date(self, node):
        """
        Processes the date node.

        @type node: SingleNode
        @param node: The single node to be processed as date.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # in case the format exists in the attributes map
        if FORMAT_VALUE in attributes_map:
            # retrieves the attributes map values
            attribute_format = attributes_map[FORMAT_VALUE]
            attribute_format_literal_value = self.get_literal_value(attribute_format)

            # converts the attribute format literal value to string, in order
            # to avoid possible problems with string formatting
            attribute_format_literal_value = str(attribute_format_literal_value)
        else:
            # sets the attribute format literal value
            # as the default date format
            attribute_format_literal_value = DEFAULT_DATE_FORMAT

        # retrieves the current date time
        current_date_time = datetime.datetime.now()

        # formats the date value
        date_value = current_date_time.strftime(attribute_format_literal_value)

        # writes the date value
        self.string_buffer.write(date_value)

    def process_time(self, node):
        """
        Processes the time node.

        @type node: SingleNode
        @param node: The single node to be processed as time.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # in case the format exists in the attributes map
        if FORMAT_VALUE in attributes_map:
            # retrieves the attributes map values
            attribute_format = attributes_map[FORMAT_VALUE]
            attribute_format_literal_value = self.get_literal_value(attribute_format)

            # converts the attribute format literal value to string, in order
            # to avoid possible problems with string formatting
            attribute_format_literal_value = str(attribute_format_literal_value)
        # otherwise
        else:
            # sets the attribute format literal value
            # as the default time format
            attribute_format_literal_value = DEFAULT_TIME_FORMAT

        # retrieves the current date time
        current_date_time = datetime.datetime.now()

        # formats the time value
        date_value = current_date_time.strftime(attribute_format_literal_value)

        # writes the time value
        self.string_buffer.write(date_value)

    def process_datetime(self, node):
        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # in case the format exists in the attributes map
        if FORMAT_VALUE in attributes_map:
            # retrieves the attributes map values
            attribute_format = attributes_map[FORMAT_VALUE]
            attribute_format_literal_value = self.get_literal_value(attribute_format)

            # converts the attribute format literal value to string, in order
            # to avoid possible problems with string formatting
            attribute_format_literal_value = str(attribute_format_literal_value)
        # otherwise
        else:
            # sets the attribute format literal value as
            # the default date time format
            attribute_format_literal_value = DEFAULT_DATE_TIME_FORMAT

        # retrieves the current date time
        current_date_time = datetime.datetime.now()

        # formats the datetime value
        datetime_value = current_date_time.strftime(attribute_format_literal_value)

        # writes the datetime value
        self.string_buffer.write(datetime_value)

    def process_format_datetime(self, node):
        """
        Processes the format datetime node.

        @type node: SingleNode
        @param node: The single node to be processed as format datetime.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # retrieves the attributes map values
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)
        attribute_format = attributes_map[FORMAT_VALUE]
        attribute_format_literal_value = self.get_literal_value(attribute_format)

        # converts the attribute format literal value to string, in order
        # to avoid possible problems with string formatting
        attribute_format_literal_value = str(attribute_format_literal_value)

        # date formats the attribute value (datetime)
        attribute_value_formatted = attribute_value_value.strftime(attribute_format_literal_value)

        # writes the attribute value formatted
        self.string_buffer.write(attribute_value_formatted)

    def get_value(self, attribute_value, process_literal = False):
        """
        Retrieves the value (variable or literal) of the given
        value.
        The process of retrieving the variable value is iterative
        and may consume some time in resolution.

        @type attribute_value: Dictionary
        @param attribute_value: A map describing the attribute value.
        @type process_string: bool
        @param process_string: If the literal value should be processed.
        @rtype: Object
        @return: The resolved attribute value.
        """

        # in case the attribute value is of type variable
        if attribute_value[TYPE_VALUE] == VARIABLE_VALUE:
            # retrieves the variable name
            variable_name = attribute_value[VALUE_VALUE]

            # in case the variable name is none
            if variable_name == NONE_VALUE:
                # sets the value as none
                value = None
            # otherwise
            else:
                # splits the variable name in the dots
                variable_name_splitted = variable_name.split(".")

                # retrieves the first variable name split
                first_variable_name_split = variable_name_splitted[0]

                # sets the current variable as the first split
                current_variable = self.global_map.get(first_variable_name_split, None)

                # in case the current variable is defined
                if not current_variable == None:
                    # iterates over the sub values of the variable
                    for variable_name_split in variable_name_splitted[1:]:
                        # in case the variable is of type dictionary
                        if colony.libs.structures_util.is_dictionary(current_variable):
                            if variable_name_split in current_variable:
                                # retrieves the current variable (from the dictionary)
                                current_variable = current_variable[variable_name_split]
                            elif not self.strict_mode:
                                # sets the current variable as none
                                current_variable = None

                                # breaks the cycle
                                break
                            else:
                                # raises the undefined variable exception
                                raise template_engine_exceptions.UndefinedVariable("variable is not defined: " + variable_name)
                        # variable is of type object or other
                        else:
                            if hasattr(current_variable, variable_name_split):
                                # retrieves the current variable (from the object)
                                current_variable = getattr(current_variable, variable_name_split)

                                # retrieves the current variable type
                                current_variable_type = type(current_variable)

                                # in case its a variable of type function
                                if current_variable_type in FUNCTION_TYPES:
                                    # calls the function (without arguments) to
                                    # retrieve the variable
                                    current_variable = current_variable()

                            elif not self.strict_mode:
                                # sets the current variable as none
                                current_variable = None

                                # breaks the cycle
                                break
                            else:
                                # raises the undefined variable exception
                                raise template_engine_exceptions.UndefinedVariable("variable is not defined: " + variable_name)
                elif not self.strict_mode:
                    # sets the current variable as none
                    current_variable = None
                else:
                    # raises the undefined variable exception
                    raise template_engine_exceptions.UndefinedVariable("variable is not defined: " + variable_name)

                # sets the value as the current variable value
                value = current_variable
        # in case the attribute value is of type literal
        elif attribute_value[TYPE_VALUE] == LITERAL_VALUE:
            # retrieves the literal value
            literal_value = attribute_value[VALUE_VALUE]

            # in case the process literal is sets and
            # the literal value contains commas, it
            # must be a sequence
            if process_literal and literal_value.find(","):
                # sets the value as the list resulting
                # from the split around the separator
                value = literal_value.split(",")
            # otherwise it must be
            # a simple literal value
            else:
                # sets the value as the literal value
                value = literal_value

        # returns the value
        return value

    def get_literal_value(self, attribute_value):
        # retrieves the literal value
        literal_value = attribute_value[VALUE_VALUE]

        # returns the literal value
        return literal_value

    def get_boolean_value(self, attribute_value):
        # retrieves the literal value
        literal_value = attribute_value[VALUE_VALUE]

        # retrieves the literal value type
        literal_value_type = type(literal_value)

        # in case the literal value is a boolean
        if literal_value_type == types.BooleanType:
            # returns true literal value
            return literal_value

        # raises an invalid boolean value exception
        raise template_engine_exceptions.InvalidBooleanValue("invalid boolean " + literal_value)

    def _validate_accept_node(self, node, accept_node):
        """
        Validates the accept node flag in accordance with the if
        specification.

        @type node: Node
        @param node: The child node to be evaluated.
        @type accept_node: bool
        @param accept_node: The accept node flag value.
        @rtype: bool
        @return: The new value for the accept node flag.
        """

        # in case the current node is not a match node
        if not isinstance(node, template_engine_ast.MatchNode):
            # returns the accept node
            return accept_node

        # retrieves the value type
        value_type = node.get_value_type()

        # in case the value type is else
        if value_type in (ELSE_VALUE, ELIF_VALUE):
            # in case the accept node
            # flag is already set (the result is
            # already been evaluated positively)
            if accept_node:
                # returns invalid (to end evaluation)
                return None

            # in case the type is else, the
            # node should be accepted
            if value_type == ELSE_VALUE:
                # sets the accept node flag
                accept_node = True
            # in case the type is elif, the
            # node should be accepted in case
            # of positive evaluation
            elif ELIF_VALUE:
                # evaluates the node as comparison
                result = self._evaluate_comparison_node(node)

                # sets the accept node value
                accept_node = result

        # returns the accept node
        return accept_node

    def _evaluate_comparison_node(self, node):
        """
        Evaluates the given (comparison) node, retrieving
        the result of the evaluation.

        @type node: Node
        @param node: The comparison node to be evaluated.
        @rtype: bool
        @return: The result of the evaluation of the
        comparison node.
        """

        # retrieves the attributes map
        attributes_map = node.get_attributes_map()

        # retrieves the attributes map values
        attribute_item = attributes_map[ITEM_VALUE]
        attribute_item_value = self.get_value(attribute_item)
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)
        attribute_operator = attributes_map[OPERATOR_VALUE]
        attribute_operator_literal_value = self.get_literal_value(attribute_operator)

        # retrieves the comparison function
        comparison_function = COMPARISION_FUNCTIONS[attribute_operator_literal_value]

        # compares the values using the comparison function
        # and retrieves the results
        comparison_result = comparison_function(attribute_item_value, attribute_value_value)

        # returns the comparison result
        return comparison_result
