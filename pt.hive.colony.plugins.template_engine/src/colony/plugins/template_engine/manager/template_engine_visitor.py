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

import colony.libs.string_buffer_util

import template_engine_ast
import template_engine_exceptions

FUNCTION_TYPES = (types.MethodType, types.FunctionType, types.BuiltinMethodType, types.BuiltinFunctionType)
""" The function types """

VALUE_VALUE = "value"
""" The value value """

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

XML_ESCAPE_VALUE = "xml_escape"
""" The xml escape value """

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
        getattr(self, "process_" + name)(node)

    def process_out(self, node):
        """
        Processes the out node.

        @type node: SingleNode
        @param node: The single node to be processed as out.
        """

        attributes_map = node.get_attributes_map()
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)

        if FORMAT_VALUE in attributes_map:
            format_string = attributes_map[FORMAT_VALUE]
            format_string_value = self.get_value(format_string)
            attribute_value_value = format_string_value % attribute_value_value

        if XML_ESCAPE_VALUE in attributes_map:
            attribute_xml_escape = attributes_map[XML_ESCAPE_VALUE]
            attribute_xml_escape_value = self.get_boolean_value(attribute_xml_escape)
        else:
            attribute_xml_escape_value = False

        # in case the variable encoding is defined
        if self.variable_encoding:
            # re-encodes the variable value
            attribute_value_value = unicode(attribute_value_value).encode(self.variable_encoding)
        else:
            # converts the value into unicode (in case it's necessary)
            attribute_value_value = unicode(attribute_value_value)

        if attribute_xml_escape_value:
            attribute_value_value = xml.sax.saxutils.escape(attribute_value_value)

        # writes the attribute value value to the string buffer
        self.string_buffer.write(attribute_value_value)

    def process_out_none(self, node):
        """
        Processes the out none node.

        @type node: SingleNode
        @param node: The single node to be processed as out none.
        """

        attributes_map = node.get_attributes_map()
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)

        if FORMAT_VALUE in attributes_map:
            format_string = attributes_map[FORMAT_VALUE]
            format_string_value = self.get_value(format_string)
            attribute_value_value = format_string_value % attribute_value_value

        if XML_ESCAPE_VALUE in attributes_map:
            attribute_xml_escape = attributes_map[XML_ESCAPE_VALUE]
            attribute_xml_escape_value = self.get_boolean_value(attribute_xml_escape)
        else:
            attribute_xml_escape_value = False

        if not attribute_value_value == None:
            # in case the variable encoding is defined
            if self.variable_encoding:
                # re-encodes the variable value
                attribute_value_value = unicode(attribute_value_value).encode(self.variable_encoding)
            else:
                # converts the value into unicode (in case it's necessary)
                attribute_value_value = unicode(attribute_value_value)

            if attribute_xml_escape_value:
                attribute_value_value = xml.sax.saxutils.escape(attribute_value_value)

            self.string_buffer.write(attribute_value_value)

    def process_var(self, node):
        """
        Processes the var node.

        @type node: SingleNode
        @param node: The single node to be processed as var.
        """

        attributes_map = node.get_attributes_map()
        attribute_item = attributes_map[ITEM_VALUE]
        attribute_item_literal_value = self.get_literal_value(attribute_item)
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)

        self.global_map[attribute_item_literal_value] = attribute_value_value

    def process_foreach(self, node):
        """
        Processes the foreach node.

        @type node: SingleNode
        @param node: The single node to be processed as foreach.
        """

        attributes_map = node.get_attributes_map()
        attribute_from = attributes_map[FROM_VALUE]
        attribute_from_value = self.get_value(attribute_from)
        attribute_item = attributes_map[ITEM_VALUE]
        attribute_item_literal_value = self.get_literal_value(attribute_item)

        if INDEX_VALUE in attributes_map:
            attribute_index = attributes_map[INDEX_VALUE]
            attribute_index_literal_value = self.get_literal_value(attribute_index)
        else:
            attribute_index_literal_value = None

        if KEY_VALUE in attributes_map:
            attribute_key = attributes_map[KEY_VALUE]
            attribute_key_literal_value = self.get_literal_value(attribute_key)
        else:
            attribute_key_literal_value = None

        if START_INDEX_VALUE in attributes_map:
            attribute_start_index = attributes_map[START_INDEX_VALUE]
            attribute_start_index_literal_value = self.get_literal_value(attribute_start_index)

            # sets the initial index
            index = int(attribute_start_index_literal_value[1:-1])
        else:
            # sets the default initial index
            index = 1

        # in case the attribute does not have the iterator method
        # it's not iterable
        if not hasattr(attribute_from_value, "__iter__"):
            # retrieves the attribute from value
            attribute_from_value = attribute_from[VALUE_VALUE]

            # raises the variable not iterable exception
            raise template_engine_exceptions.VariableNotIterable("value not iterable: " + attribute_from_value)

        # retrieves the attribute from value type
        attribute_from_value_type = type(attribute_from_value)

        if attribute_from_value_type == types.DictType:
            for attribute_from_value_key, attribute_from_value_value in attribute_from_value.items():
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
        else:
            for attribute_from_value_item in attribute_from_value:
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

        attributes_map = node.get_attributes_map()
        attribute_item = attributes_map[ITEM_VALUE]
        attribute_item_value = self.get_value(attribute_item)
        attribute_value = attributes_map[VALUE_VALUE]
        attribute_value_value = self.get_value(attribute_value)
        attribute_operator = attributes_map[OPERATOR_VALUE]
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

        # in case the result is valid
        if result:
            if self.visit_childs:
                for node_child_node in node.child_nodes:
                    node_child_node.accept(self)

    def process_else(self, node):
        """
        Processes the else node.

        @type node: SingleNode
        @param node: The single node to be processed as else.
        """

        pass

    def process_count(self, node):
        """
        Processes the count node.

        @type node: SingleNode
        @param node: The single node to be processed as count.
        """

        attributes_map = node.get_attributes_map()
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

        attributes_map = node.get_attributes_map()

        if FILE_VALUE in attributes_map:
            attribute_file = attributes_map[FILE_VALUE]
            attribute_file_literal_value = self.get_literal_value(attribute_file)

        if FILE_VALUE_VALUE in attributes_map:
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
        year_value = current_date_time.strftime("%Y")

        # writes the year value
        self.string_buffer.write(year_value)

    def process_date(self, node):
        """
        Processes the date node.

        @type node: SingleNode
        @param node: The single node to be processed as date.
        """

        attributes_map = node.get_attributes_map()

        if FORMAT_VALUE in attributes_map:
            attribute_format = attributes_map[FORMAT_VALUE]
            attribute_format_literal_value = self.get_literal_value(attribute_format)

            # converts the attribute format literal value to string, in order
            # to avoid possible problems with string formatting
            attribute_format_literal_value = str(attribute_format_literal_value)
        else:
            attribute_format_literal_value = "%d/%m/%y"

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

        attributes_map = node.get_attributes_map()

        if FORMAT_VALUE in attributes_map:
            attribute_format = attributes_map[FORMAT_VALUE]
            attribute_format_literal_value = self.get_literal_value(attribute_format)

            # converts the attribute format literal value to string, in order
            # to avoid possible problems with string formatting
            attribute_format_literal_value = str(attribute_format_literal_value)
        else:
            attribute_format_literal_value = "%H:%M:%S"

        # retrieves the current date time
        current_date_time = datetime.datetime.now()

        # formats the time value
        date_value = current_date_time.strftime(attribute_format_literal_value)

        # writes the time value
        self.string_buffer.write(date_value)

    def process_datetime(self, node):
        attributes_map = node.get_attributes_map()

        if FORMAT_VALUE in attributes_map:
            attribute_format = attributes_map[FORMAT_VALUE]
            attribute_format_literal_value = self.get_literal_value(attribute_format)

            # converts the attribute format literal value to string, in order
            # to avoid possible problems with string formatting
            attribute_format_literal_value = str(attribute_format_literal_value)
        else:
            attribute_format_literal_value = "%d/%m/%y %H:%M:%S"

        # retrieves the current date time
        current_date_time = datetime.datetime.now()

        # formats the datetime value
        datetime_value = current_date_time.strftime(attribute_format_literal_value)

        # writes the datetime value
        self.string_buffer.write(datetime_value)

    def process_format_datetime(self, node):
        attributes_map = node.get_attributes_map()

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

    def get_value(self, attribute_value):
        """
        Retrieves the value (variable or literal) of the given
        value.
        The process of retrieving the variable value is iterative
        and may consume some time in resolution.

        @type attribute_value: Dictionary
        @param attribute_value: A map describing the attribute value.
        @rtype: Object
        @return: The resolved attribute value.
        """

        # in case the attribute value is of type variable
        if attribute_value[TYPE_VALUE] == VARIABLE_VALUE:
            # retrieves the variable name
            variable_name = attribute_value[VALUE_VALUE]

            # in case the variable name is none
            if variable_name == "None":
                value = None
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
                        # retrieves the current variable type
                        current_variable_type = type(current_variable)

                        # in case the variable is of type dictionary
                        if current_variable_type == types.DictType:
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
