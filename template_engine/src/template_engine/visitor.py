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

import re
import os
import uuid
import types
import calendar
import datetime

import xml.sax.saxutils

import colony

import ast
import util
import exceptions

FUNCTION_TYPES = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinMethodType,
    types.BuiltinFunctionType
)
""" The function types """

SERIALIZERS = (
    "json",
    "pickle"
)
""" The list to hold the various serializers
in order of preference for serialization """

SERIALIZERS_MAP = None
""" The map associating the encoding type for
the serialization with the appropriate serializer
object to handle it """

LITERAL_ESCAPE_REGEX_VALUE = "\$\\\\(?=\\\\*\{)"
""" The literal escape regular expression value """

FUCNTION_ARGUMENTS_REGEX_VALUE = "\([a-zA-Z0-9_\-,\.\:'\/\" ]+\)"
""" The function arguments regular expression value """

NAMES_REGEX_VALUE = "([^\.]+\([^\)]+\))|([^\.]+)"
""" The regular expression that is going to be used for the
splitting of the various names for a variable based value that
is going to be evaluated at runtime, this value may contain
method calls with literal an non literal values """

LITERAL_ESCAPE_REGEX = re.compile(LITERAL_ESCAPE_REGEX_VALUE)
""" The literal escape regular expression """

FUCNTION_ARGUMENTS_REGEX = re.compile(FUCNTION_ARGUMENTS_REGEX_VALUE)
""" The function arguments regular expression """

NAMES_REGEX = re.compile(NAMES_REGEX_VALUE)
""" The compiled version of names regular expression used for the
matching of the various components of a variable template value """

START_INDEX_VALUE = "start_index"
""" The start index value """

KEY_MAP_VALUE = "key_map"
""" The key map value """

KEY_ORDER_LIST_VALUE = "key_order_list"
""" The key order list value """

XML_ESCAPE_VALUE = "xml_escape"
""" The xml escape value """

XML_QUOTE_VALUE = "xml_quote"
""" The xml quote value """

NEWLINE_CONVERT_VALUE = "newline_convert"
""" The newline convert value """

CONVERT_VALUE = "convert"
""" The convert value """

DEFAULT_VALUE = "default"
""" The default value """

ALLOW_EMPTY_VALUE = "allow_empty"
""" The allow empty value """

SERIALIZER_VALUE = "serializer"
""" The serializer value """

KEY_SEPARATOR_VALUE = "key_separator"
""" The key separator value """

ITEM_SEPARATOR_VALUE = "item_separator"
""" The item separator value """

ELSE_VALUE = "else"
""" The else value """

ELIF_VALUE = "elif"
""" The elif value """

ITER_VALUE = "__iter__"
""" The iter value """

DEFAULT_YEAR_FORMAT = "%Y"
""" The default year format """

DEFAULT_DATE_FORMAT = "%d/%m/%y"
""" The default date format """

DEFAULT_TIME_FORMAT = "%H:%M:%S"
""" The default time format """

DEFAULT_DATE_TIME_FORMAT = "%d/%m/%y %H:%M:%S"
""" The default date time format """

NEWLINE_CHARACTER = "\n"
""" The newline character """

LINE_BREAK_TAG = "<br/>"
""" The line break tag """

SEQUENCE_TYPES = (types.ListType, types.TupleType)
""" The tuple containing the types considered to be sequences """

SERIALIZABLE_TYPES = (types.ListType, types.TupleType)
""" The tuple containing the set of types that can be
"serializable" in a custom manner """

RESOLVABLE_TYPES = (types.StringType, types.UnicodeType, colony.FormatTuple)
""" The tuple containing the set of types that can be
"resolved" in the localization context """

BUILTINS = {
    "True" : True,
    "False" : False
}
""" The base builtins structure that is going to be re-used
for every parsing operation to be done by the visitor, this
should contain the minimum amount of symbols required for the
parsing of the template file (to avoid security issues) """

CONVERSION_MAP = {
    "2_of_5" : colony.encode_2_of_5
}
""" The map associating the name of the conversion
function with the conversion function symbol reference """

COMPARISION_FUNCTIONS = {
    "eq" : lambda attribute_item, attribute_value: attribute_item == attribute_value,
    "neq" : lambda attribute_item, attribute_value: not attribute_item == attribute_value,
    "gte" : lambda attribute_item, attribute_value: attribute_item >= attribute_value,
    "gt" : lambda attribute_item, attribute_value: attribute_item > attribute_value,
    "lte" : lambda attribute_item, attribute_value: attribute_item <= attribute_value,
    "lt" : lambda attribute_item, attribute_value: attribute_item < attribute_value,
    "len" : lambda attribute_item, attribute_value: len(attribute_item) == attribute_value,
    "lengt" : lambda attribute_item, attribute_value: len(attribute_item) > attribute_value,
    "lenlt" : lambda attribute_item, attribute_value: len(attribute_item) < attribute_value,
    "in" : lambda attribute_item, attribute_value: attribute_item and attribute_value in attribute_item or False,
    "nin" : lambda attribute_item, attribute_value: attribute_item and not attribute_value in attribute_item or False
}
""" The map containing the comparison functions (lambda) these
are going to be used "inside" the visitor execution logic """

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
        @return: The decorator interceptor function.
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

            # in case of failure to find the proper callback
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
        @return: The decorator interceptor function.
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
    """ The encoding used the file, this is a meta-information
    value that is not going to be used for any practical usage """

    file_path = None
    """ The path to the file that generated the abstract syntax
    tree that is going to be visited by this visitor """

    template_engine = None
    """ The reference template engine system object that handles
    and manages this visitor (owner object) """

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

    process_methods_list = []
    """ The list of process methods (tuples) """

    locale_bundles = []
    """ The list that contains the various bundles to be searched for
    localization, the order set is going to be the priority for template
    value resolution (from first to last list element) """

    def __init__(self, string_buffer = None):
        """
        Constructor of the class.

        @type string_buffer: File
        @param string_buffer: The file like object that is going to be
        used for the underlying buffering of the template process. In
        case no value is provided the default string buffer object is used.
        """

        self.node_method_map = {}
        self.visit_childs = True
        self.visit_next = True
        self.global_map = dict(__builtins__ = BUILTINS)
        self.string_buffer = string_buffer or colony.StringBuffer()
        self.process_methods_list = []
        self.locale_bundles = []

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

    def attach_process_method(self, process_method_name, process_method):
        # creates the process method instance
        process_method_instance = types.MethodType(process_method, self, Visitor)

        # sets the process method in the visitor
        setattr(self, process_method_name, process_method_instance)

        # creates the process method tuple
        process_method_tuple = (process_method_name, process_method)

        # adds the process method tuple to the list of process methods
        self.process_methods_list.append(process_method_tuple)

    def get_global_map(self):
        return self.global_map

    def set_global_map(self, global_map):
        self.global_map = global_map

    def add_global_variable(self, variable_name, variable_value):
        self.global_map[variable_name] = variable_value

    def remove_global_variable(self, variable_name):
        del self.global_map[variable_name]

    def add_bundle(self, bundle):
        self.locale_bundles.append(bundle)

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

    def get_template_engine(self):
        """
        Retrieves the template engine.

        @rtype: TemplateEngine
        @return: The template engine.
        """

        return self.template_engine

    def set_template_engine(self, template_engine):
        """
        Sets the template engine.

        @type template_engine: TemplateEngine
        @param template_engine: The template engine.
        """

        self.template_engine = template_engine

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

    @_visit(ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @_visit(ast.RootNode)
    def visit_root_node(self, node):
        pass

    @_visit(ast.LiteralNode)
    def visit_literal_node(self, node):
        # retrieves the match value from the current node's
        # value escaping it to avoid any problem and then
        # writes the value into the current string buffer
        match_value = node.value.value
        match_value = self._escape_literal(match_value)
        self.string_buffer.write(match_value)

    @_visit(ast.MatchNode)
    def visit_match_node(self, node):
        pass

    @_visit(ast.SingleNode)
    def visit_single_node(self, node):
        pass

    @_visit(ast.CompositeNode)
    def visit_composite_node(self, node):
        pass

    def process_accept(self, node, name):
        # retrieves the process method for the name and runs the
        # same method with the current node as the argument
        process_method = getattr(self, "process_" + name)
        process_method(node)

    def process_out(self, node):
        """
        Processes the out none node, that outputs a processed
        data to the current processing context/buffer.

        In case the resolved value is invalid/none the resulting
        data is printed as an empty string.

        @type node: SingleNode
        @param node: The single node to be processed as out none.
        """

        # retrieves the attributes map for the current node that
        # is going to be used to process the data that is going
        # to be printed to the current context
        attributes = node.get_attributes()

        # retrieves the attributes map values
        attribute_value = attributes["value"]
        attribute_value_value = self.get_value(attribute_value, localize = True)

        # in case the prefix exists in the attributes map
        if "prefix" in attributes:
            # retrieves attribute prefix value
            attribute_prefix = attributes["prefix"]
            attribute_prefix_value = self.get_value(attribute_prefix, localize = True)
        # otherwise
        else:
            # sets the default prefix value
            attribute_prefix_value = ""

        # in case the format exists in the attributes map
        if "format" in attributes:
            # retrieves attribute value value
            format_string = attributes["format"]
            format_string_value = self.get_value(format_string)
            is_valid = format_string_value and not attribute_value_value == None
            attribute_value_value = is_valid and\
                format_string_value % attribute_value_value or attribute_value_value

        # in case the quote exists in the attributes map
        if "quote" in attributes:
            # retrieves attribute quote value
            attribute_quote = attributes["quote"]
            attribute_quote_value = self.get_boolean_value(attribute_quote)
        # otherwise
        else:
            # unsets the attribute quote value
            attribute_quote_value = False

        # in case the xml escape exists in the attributes map
        if XML_ESCAPE_VALUE in attributes:
            # retrieves attribute xml escape value
            attribute_xml_escape = attributes[XML_ESCAPE_VALUE]
            attribute_xml_escape_value = self.get_boolean_value(attribute_xml_escape)
        # otherwise
        else:
            # unsets the attribute xml escape value
            attribute_xml_escape_value = False

        # in case the xml quote exists in the attributes map
        if XML_QUOTE_VALUE in attributes:
            # retrieves attribute xml quote value
            attribute_xml_quote = attributes[XML_QUOTE_VALUE]
            attribute_xml_quote_value = self.get_boolean_value(attribute_xml_quote)
        # otherwise
        else:
            # unsets the attribute xml quote value
            attribute_xml_quote_value = False

        # in case the new line convert exists in the attributes map
        if NEWLINE_CONVERT_VALUE in attributes:
            # retrieves attribute newline convert value
            attribute_newline_convert = attributes[NEWLINE_CONVERT_VALUE]
            attribute_newline_convert_value = self.get_boolean_value(attribute_newline_convert)
        # otherwise
        else:
            # unsets the attribute newline convert value
            attribute_newline_convert_value = False

        # in case the convert exists in the attributes map
        if CONVERT_VALUE in attributes:
            # retrieves attribute convert value
            attribute_convert = attributes[CONVERT_VALUE]
            attribute_convert_value = self.get_value(attribute_convert)
        # otherwise
        else:
            # unsets the attribute convert value
            attribute_convert_value = None

        # in case the allow empty exists in the attributes map
        if ALLOW_EMPTY_VALUE in attributes:
            # retrieves attribute allow empty value
            attribute_allow_empty = attributes[ALLOW_EMPTY_VALUE]
            attribute_allow_empty_value = self.get_value(attribute_allow_empty)
        # otherwise
        else:
            # sets the attribute allow empty value
            attribute_allow_empty_value = True

        # in case the default exists in the attributes map
        if DEFAULT_VALUE in attributes:
            # retrieves attribute default value
            attribute_default = attributes[DEFAULT_VALUE]
            attribute_default_value = self.get_value(attribute_default, localize = True)
        # otherwise
        else:
            # unsets the attribute default value
            attribute_default_value = None

        # in case the serializer exists in the attributes map
        if SERIALIZER_VALUE in attributes:
            # retrieves attribute serializer value
            attribute_serializer = attributes[SERIALIZER_VALUE]
            attribute_serializer_value = self.get_literal_value(attribute_serializer)
        # otherwise
        else:
            # unsets the attribute serializer value
            attribute_serializer_value = None

        # creates the invalid values tuple
        invalid_values = attribute_allow_empty_value and (None,) or (None, "")

        # changes the attribute value value to the default attribute
        # value in case the value of it is invalid
        if attribute_value_value in invalid_values: attribute_value_value = attribute_default_value

        # in case the attribute value value is invalid and the default
        # value is not set (no need to show the value) must return immediately
        # nothing will be printed
        if attribute_value_value in invalid_values and attribute_default_value == None:
            return

        # in case the serializer value is set must try to gather
        # the serializer and serialize the attribute value using it
        if attribute_serializer_value:
            serializer, _name = self._get_serializer(attribute_serializer_value)
            attribute_value_value = serializer.dumps(attribute_value_value)

        # serializes the value into the correct visual representation
        # (in case the attribute type is "serializable", eg: lists, tuples, etc.)
        attribute_value_value = self._serialize_value(attribute_value_value)

        # checks if the attribute value contains a unicode string
        # in such case there's no need to re-decode it
        is_unicode = type(attribute_value_value) == types.UnicodeType
        attribute_value_value = is_unicode and attribute_value_value or unicode(attribute_value_value)

        # in case the attribute convert value is set
        if attribute_convert_value:
            # retrieves the conversion method for the string
            # value representing it and uses it to convert
            # the attribute value to the target encoding
            conversion_method = CONVERSION_MAP.get(attribute_convert_value, None)
            attribute_value_value = conversion_method and conversion_method(attribute_value_value) or attribute_convert_value

        # in case the variable encoding is defined
        if self.variable_encoding:
            # re-encodes the variable value
            attribute_value_value = attribute_value_value.encode(self.variable_encoding)

        # in case the attribute quote value is set
        if attribute_quote_value:
            # re-encodes the value
            attribute_value_value = attribute_value_value.encode("utf-8")

            # quotes the attribute value value
            attribute_value_value = colony.quote(attribute_value_value, "/")

        # in case the attribute xml escape value is set
        if attribute_xml_escape_value:
            # escapes the attribute value value using xml escaping
            attribute_value_value = xml.sax.saxutils.escape(attribute_value_value)

        # in case the attribute xml quote value is set
        if attribute_xml_quote_value:
            # escapes the (double) quotes using the xml base approach
            attribute_value_value = attribute_value_value.replace("\"", "&quot;")

        # in case the attribute newline convert value is set
        if attribute_newline_convert_value:
            # converts the attribute value value newlines
            attribute_value_value = attribute_value_value.replace(NEWLINE_CHARACTER, LINE_BREAK_TAG)

        # adds the attribute prefix value to the attribute value value
        attribute_value_value = attribute_prefix_value + attribute_value_value

        # writes the attribute value value in the string buffer
        self.string_buffer.write(attribute_value_value)

    def process_out_map(self, node):
        """
        Processes the out none node.

        @type node: SingleNode
        @param node: The single node to be processed as out map.
        """

        # retrieves the attributes map
        attributes = node.get_attributes()

        # retrieves the attributes map values
        attribute_value = attributes["value"]
        attribute_value_value = self.get_value(attribute_value, localize = True)

        # in case the key map exists in the attributes map
        if KEY_MAP_VALUE in attributes:
            # retrieves attribute key map value
            attribute_key_map = attributes[KEY_MAP_VALUE]
            attribute_key_map_value = self.get_value(attribute_key_map)
        # otherwise
        else:
            # sets the attribute key map value
            attribute_key_map_value = {}

        # in case the key order list exists in the attributes map
        if KEY_ORDER_LIST_VALUE in attributes:
            # retrieves attribute key order list value
            attribute_key_order_list = attributes[KEY_ORDER_LIST_VALUE]
            attribute_key_order_list_value = self.get_value(attribute_key_order_list)
        # otherwise
        else:
            # sets the attribute key order list value
            attribute_key_order_list_value = attribute_value_value.keys()

        # in case the key separator exists in the attributes map
        if KEY_SEPARATOR_VALUE in attributes:
            # retrieves attribute key separator value
            attribute_key_separator = attributes[KEY_SEPARATOR_VALUE]
            attribute_key_separator_value = self.get_value(attribute_key_separator)
        # otherwise
        else:
            # sets the attribute key separator value
            attribute_key_separator_value = ": "

        # in case the item separator exists in the attributes map
        if ITEM_SEPARATOR_VALUE in attributes:
            # retrieves attribute item separator value
            attribute_item_separator = attributes[ITEM_SEPARATOR_VALUE]
            attribute_item_separator_value = self.get_value(attribute_item_separator)
        # otherwise
        else:
            # sets the attribute item separator value
            attribute_item_separator_value = NEWLINE_CHARACTER

        # in case the xml escape exists in the attributes map
        if XML_ESCAPE_VALUE in attributes:
            # retrieves attribute xml escape value
            attribute_xml_escape = attributes[XML_ESCAPE_VALUE]
            attribute_xml_escape_value = self.get_boolean_value(attribute_xml_escape)
        # otherwise
        else:
            # unsets the attribute xml escape value
            attribute_xml_escape_value = False

        # in case the xml quote exists in the attributes map
        if XML_QUOTE_VALUE in attributes:
            # retrieves attribute xml quote value
            attribute_xml_quote = attributes[XML_QUOTE_VALUE]
            attribute_xml_quote_value = self.get_boolean_value(attribute_xml_quote)
        # otherwise
        else:
            # unsets the attribute xml quote value
            attribute_xml_quote_value = False

        # in case the new line convert exists in the attributes map
        if NEWLINE_CONVERT_VALUE in attributes:
            # retrieves attribute newline convert value
            attribute_newline_convert = attributes[NEWLINE_CONVERT_VALUE]
            attribute_newline_convert_value = self.get_boolean_value(attribute_newline_convert)
        # otherwise
        else:
            # unsets the attribute newline convert value
            attribute_newline_convert_value = False

        # in case the allow empty exists in the attributes map
        if ALLOW_EMPTY_VALUE in attributes:
            # retrieves attribute allow empty value
            attribute_allow_empty = attributes[ALLOW_EMPTY_VALUE]
            attribute_allow_empty_value = self.get_value(attribute_allow_empty)
        # otherwise
        else:
            # sets the attribute allow empty value
            attribute_allow_empty_value = True

        # creates the invalid values tuple
        invalid_values = attribute_allow_empty_value and (None,) or (None, "")

        # iterates over all the attribute value key items
        for key in attribute_key_order_list_value:
            # retrieves the attribute value value for
            # the current key
            value = attribute_value_value[key]

            # in case the value is invalid
            if value in invalid_values:
                # skips the iteration
                continue

            # tries to retrieve the key from the attribute
            # key map value
            key = attribute_key_map_value.get(key, key)

            # serializes the value into the correct visual representation
            # (in case the attribute type is "serializable", eg: lists, tuples, etc.)
            value = self._serialize_value(value)

            # checks if the value contains a unicode string
            # in such case there's no need to re-decode it
            is_unicode = type(value) == types.UnicodeType
            value = is_unicode and value or unicode(value)

            # in case the variable encoding is defined
            if self.variable_encoding:
                # re-encodes the variable value
                value = value.encode(self.variable_encoding)

            # in case the attribute xml escape value is set
            if attribute_xml_escape_value:
                # escapes the key using xml escaping
                key = xml.sax.saxutils.escape(key)

                # escapes the value using xml escaping
                value = xml.sax.saxutils.escape(value)

            # in case the attribute xml quote value is set
            if attribute_xml_quote_value:
                # escapes the key using xml (quote) escaping
                key = key.replace("\"", "&quot;")

                # escapes the value using xml (quote) escaping
                value = value.replace("\"", "&quot;")

            # in case the attribute newline convert value is set
            if attribute_newline_convert_value:
                # converts the key newlines
                key = key.replace(NEWLINE_CHARACTER, LINE_BREAK_TAG)

                # converts the value newlines
                value = value.replace(NEWLINE_CHARACTER, LINE_BREAK_TAG)

            # writes the attribute value value in the string buffer
            self.string_buffer.write(key + attribute_key_separator_value + value + attribute_item_separator_value)

    def process_var(self, node):
        """
        Processes the var node.

        @type node: SingleNode
        @param node: The single node to be processed as var.
        """

        # retrieves the attributes map
        attributes = node.get_attributes()

        # retrieves the attributes map values
        attribute_item = attributes["item"]
        attribute_item_literal_value = self.get_literal_value(attribute_item)
        attribute_value = attributes["value"]
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
        attributes = node.get_attributes()

        # retrieves the attributes map values
        attribute_from = attributes["from"]
        attribute_from_value = self.get_value(attribute_from)
        attribute_item = attributes["item"]
        attribute_item_literal_value = self.get_literal_value(attribute_item)

        # in case the index exists in the attributes map
        if "index" in attributes:
            # retrieves the attribute index literal value
            attribute_index = attributes["index"]
            attribute_index_literal_value = self.get_literal_value(attribute_index)
        else:
            # sets the attribute index literal value as none
            attribute_index_literal_value = None

        # in case the key exists in the attributes map
        if "key" in attributes:
            # retrieves the attribute key literal value
            attribute_key = attributes["key"]
            attribute_key_literal_value = self.get_literal_value(attribute_key)
        else:
            # sets the attribute key literal value as none
            attribute_key_literal_value = None

        # in case the start index exists in the attributes map
        if START_INDEX_VALUE in attributes:
            # retrieves the attribute start index literal value
            attribute_start_index = attributes[START_INDEX_VALUE]
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
                attribute_from_value = attribute_from["value"]

                # raises the variable not iterable exception
                raise exceptions.VariableNotIterable("value not iterable: " + attribute_from_value)
            # otherwise avoids exception in case the object
            # is not an invalid one (possible problems)
            elif not attribute_from_value == None:
                # "casts" the attribute from value to a list it
                # will create an iterable object that may be used
                attribute_from_value = [attribute_from_value]
            # otherwise in case the object is considered invalid
            # the best match for the cast is an empty list
            else:
                # "casts" the "invalid" attribute to an empty list
                # considers it the best representation
                attribute_from_value = []

        # in case the type of the attribute from value is dictionary
        if colony.is_dictionary(attribute_from_value):
            # iterates over all the attribute from value items
            for attribute_from_value_key, attribute_from_value_value in attribute_from_value.items():
                # sets the attribute from value value in the global map
                self.global_map[attribute_item_literal_value] = attribute_from_value_value

                is_last = index == len(attribute_from_value)
                self.global_map["is_last"] = is_last

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

                is_last = index == len(attribute_from_value)
                self.global_map["is_last"] = is_last

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
                # the evaluation is over (nothing to be done)
                if accept_node == None: return

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
        attributes = node.get_attributes()

        # retrieves the attributes map values
        attribute_values = attributes["values"]
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
        attributes = node.get_attributes()

        # retrieves the attributes map values
        attribute_value = attributes["value"]
        attribute_value_value = self.get_value(attribute_value)

        # in case the attribute value value is not valid the
        # default empty value should be considered
        if attribute_value_value == None:
            # sets the attribute value length as zero because
            # a non iterable value should be considered empty
            attribute_value_length = 0
        # otherwise the attribute value value must be considered
        # as iterable and so the length must be calculated
        else:
            # retrieves the attribute value value length and sets it
            # as the attribute value length
            attribute_value_length = len(attribute_value_value)

        # checks if the attribute value length contains a unicode string
        # in such case there's no need to re-decode it
        is_unicode = type(attribute_value_length) == types.UnicodeType
        attribute_value_length = is_unicode and attribute_value_length or unicode(attribute_value_length)

        # in case the variable encoding is defined
        if self.variable_encoding:
            # re-encodes the variable value
            attribute_value_length = attribute_value_length.encode(self.variable_encoding)

        # writes the attribute value value to the string buffer
        self.string_buffer.write(attribute_value_length)

    def process_include(self, node):
        """
        Processes the include node.

        @type node: SingleNode
        @param node: The single node to be processed as include.
        """

        # retrieves the attributes map
        attributes = node.get_attributes()

        # in case the file exists in the attributes map
        if "file" in attributes:
            # retrieves the attribute file literal value
            attribute_file = attributes["file"]
            attribute_file_literal_value = self.get_literal_value(attribute_file)

        # in case the file value exists in the attributes map
        if "file_value" in attributes:
            # retrieves the attribute file literal value
            attribute_file_value = attributes["file_value"]
            attribute_file_literal_value = self.get_value(attribute_file_value)

        # in case the attribute file literal value is not valid
        if not attribute_file_literal_value:
            # retrieves the node value type
            node_value_type = node.get_value_type()

            # raises the undefined reference exception
            raise exceptions.UndefinedReference(node_value_type)

        # in case the path is absolute
        if os.path.isabs(attribute_file_literal_value):
            # sets the file path as absolute
            file_path = attribute_file_literal_value
        # in case the path is relative to the current file
        else:
            # retrieves the file directory from the file path and then
            # sets the file path as relative to the file directory, after
            # the join operations normalizes the path so that it represents
            # the proper path with the proper operative system representation
            file_directory = os.path.dirname(self.file_path)
            file_path = os.path.join(file_directory, attribute_file_literal_value)
            file_path = os.path.normpath(file_path)

        # parses the file retrieving the template file structure, note
        # that any path existence validation will be done at this stage
        template_file = self.template_engine.parse_file_path(
            file_path,
            self.encoding,
            self.process_methods_list,
            self.locale_bundles
        )

        # sets the global map and the variable(s) encoding in the loaded
        # template file structure to be used in the process stage
        template_file.set_global_map(self.global_map)
        template_file.set_variable_encoding(self.variable_encoding)

        # processes the template file and writes the processed template
        # file (resulting template data) to the string buffer
        processed_template_file = template_file.process()
        self.string_buffer.write(processed_template_file)

    def process_uuid(self, node):
        """
        Processes the uuid node.

        @type node: SingleNode
        @param node: The single node to be processed as uuid.
        """

        # creates a new uuid value and converts it into a string
        # value to be used in the string buffer
        uuid_value = uuid.uuid4()
        uuid_string_value = str(uuid_value)

        # writes the time value
        self.string_buffer.write(uuid_string_value)

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
        attributes = node.get_attributes()

        # in case the format exists in the attributes map
        if "format" in attributes:
            # retrieves the attributes map values
            attribute_format = attributes["format"]
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
        attributes = node.get_attributes()

        # in case the format exists in the attributes map
        if "format" in attributes:
            # retrieves the attributes map values
            attribute_format = attributes["format"]
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
        """
        Processes the datetime node.

        @type node: SingleNode
        @param node: The single node to be processed as datetime.
        """

        # retrieves the attributes map
        attributes = node.get_attributes()

        # in case the format exists in the attributes map
        if "format" in attributes:
            # retrieves the attributes map values
            attribute_format = attributes["format"]
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
        attributes = node.get_attributes()

        # retrieves the attributes map values
        attribute_value = attributes["value"]
        attribute_value_value = self.get_value(attribute_value)
        attribute_format = attributes["format"]
        attribute_format_literal_value = self.get_literal_value(attribute_format)

        # in case the default exists in the attributes map
        if DEFAULT_VALUE in attributes:
            # retrieves attribute default value
            attribute_default = attributes[DEFAULT_VALUE]
            attribute_default_value = self.get_value(attribute_default, localize = True)
        # otherwise
        else:
            # unsets the attribute default value
            attribute_default_value = None

        # in case the value is not defined, the default
        # value must be used instead
        if attribute_value_value == None:
            # writes the default attribute value to
            # the string buffer and returns immediately
            attribute_default_value = not attribute_default_value == None and str(attribute_default_value)
            attribute_default_value and self.string_buffer.write(attribute_default_value)
            return

        # converts the attribute format literal value to string, in order
        # to avoid possible problems with string formatting
        attribute_format_literal_value = str(attribute_format_literal_value)

        # date formats the attribute value (datetime)
        attribute_value_formatted = attribute_value_value.strftime(attribute_format_literal_value)

        # writes the attribute value formatted
        self.string_buffer.write(attribute_value_formatted)

    def process_format_timestamp(self, node):
        """
        Processes the format datetime node.

        @type node: SingleNode
        @param node: The single node to be processed as format datetime.
        """

        # retrieves the attributes map
        attributes = node.get_attributes()

        # retrieves the attributes map values
        attribute_value = attributes["value"]
        attribute_value_value = self.get_value(attribute_value)
        attribute_format = attributes["format"]
        attribute_format_literal_value = self.get_literal_value(attribute_format)

        # in case the default exists in the attributes map
        if DEFAULT_VALUE in attributes:
            # retrieves attribute default value
            attribute_default = attributes[DEFAULT_VALUE]
            attribute_default_value = self.get_value(attribute_default, localize = True)
        # otherwise
        else:
            # unsets the attribute default value
            attribute_default_value = None

        # in case the value is not defined, the default
        # value must be used instead
        if attribute_value_value == None:
            # writes the default attribute value to
            # the string buffer and returns immediately
            attribute_default_value = not attribute_default_value == None and str(attribute_default_value)
            attribute_default_value and self.string_buffer.write(attribute_default_value)
            return

        # converts the attribute format literal value to string, in order
        # to avoid possible problems with string formatting
        attribute_format_literal_value = str(attribute_format_literal_value)

        # converts the attribute value value to date time
        attribute_date_time = datetime.datetime.utcfromtimestamp(attribute_value_value)

        # date formats the attribute value (in datetime format)
        attribute_value_formatted = attribute_date_time.strftime(attribute_format_literal_value)

        # writes the attribute value formatted
        self.string_buffer.write(attribute_value_formatted)

    def process_timestamp(self, node):
        """
        Processes the timestamp node.
        This node provides a way to print the a timestamp
        representation of a given date time value.
        In case no date time is provided the current date
        is used.

        @type node: SingleNode
        @param node: The single node to be processed as timestamp.
        """

        # retrieves the attributes map
        attributes = node.get_attributes()

        # in case the format exists in the attributes map
        if "value" in attributes:
            # retrieves the attributes map values
            attribute_value = attributes["value"]
            attribute_value_value = self.get_value(attribute_value)
        # otherwise
        else:
            # sets the current data time as the attribute
            # value value
            attribute_value_value = datetime.datetime.now()

        # in case the default exists in the attributes map
        if DEFAULT_VALUE in attributes:
            # retrieves attribute default value
            attribute_default = attributes[DEFAULT_VALUE]
            attribute_default_value = self.get_value(attribute_default, localize = True)
        # otherwise
        else:
            # unsets the attribute default value
            attribute_default_value = None

        # in case the value is not defined, the default
        # value must be used instead
        if attribute_value_value == None:
            # writes the default attribute value to
            # the string buffer and returns immediately
            attribute_default_value = not attribute_default_value == None and str(attribute_default_value)
            attribute_default_value and self.string_buffer.write(attribute_default_value)
            return

        # retrieves the time tuple from the date time
        # attribute and then converts it to timestamp
        # and then into a string
        time_tuple_value = attribute_value_value.utctimetuple()
        timestamp_value = calendar.timegm(time_tuple_value)
        timestamp_string_value = str(timestamp_value)

        # writes the timestamp string value
        self.string_buffer.write(timestamp_string_value)

    def get_value(self, attribute_value, process_literal = False, localize = False):
        """
        Retrieves the value (variable or literal) of the given
        value.
        The process of retrieving the variable value is iterative
        and may consume some time in resolution.

        An optional localize flag may be set of the value should
        be localized using the current local bundles.

        @type attribute_value: Dictionary
        @param attribute_value: A map describing the attribute value.
        @type process_string: bool
        @param process_string: If the literal value should be processed.
        @type localize: bool
        @param localize: If the value must be localized using the currently
        available locale bundles.
        @rtype: Object
        @return: The resolved attribute value.
        """

        # in case the attribute value is of type variable
        if attribute_value["type"] == "variable":
            # retrieves the variable name
            variable_name = attribute_value["value"]

            # in case the variable name is none sets the final value
            # with the invalid value as that's requested by the template
            if variable_name == "None": value = None

            # otherwise the value must be processed according to the currently
            # defined template rules (may required method invocation)
            else:
                # splits the variable name into the various parts of
                # it, separating the proper variable name from the
                # various filters as defined in the specification
                parts = variable_name.split("|")
                variable_name = parts[0].strip()
                filters = [filter.strip() for filter in parts[1:]]

                # resolves the variable name using the multiple parts
                # approach so that the final value is retrieved according
                # to the current state of the template engine
                value = self.resolve_many(variable_name)

                # iterates over the complete set of filter definition to
                # resolve the final value according to the filter
                for filter in filters: value = self.resolve_many(filter, value)

                # resolves the current variable value, trying to
                # localize it using the current locale bundles only
                # do this in case the localize flag is set
                value = self._resolve_locale(value) if localize else value

        # in case the attribute value is of type literal the value must
        # be "read" using a literal based approach so that the proper and
        # concrete value is going to be returned as the value
        elif attribute_value["type"] == "literal":
            # retrieves the literal value from the attribute
            # this is going to be considered the proper value
            value = attribute_value["value"]

            # in case the process literal is sets and
            # the literal value contains commas, it
            # must be a sequence
            if process_literal and value.find(","):
                # sets the value as the list resulting
                # from the split around the separator
                value = value.split(",")

        # returns the processed value to the caller method, this is the
        # considered to be the value for the requested attribute
        return value

    def get_literal_value(self, attribute_value):
        return attribute_value["value"]

    def get_boolean_value(self, attribute_value):
        # retrieves the literal value of the provided
        # attribute, retrieving then the data type for it
        value = attribute_value["value"]
        value_type = type(value)

        # in case the "literal" value is a boolean returns the same
        # value as the result, otherwise raises an exception indicating
        # the problem with the processing of the boolean value
        if value_type == types.BooleanType: return value
        raise exceptions.InvalidBooleanValue("invalid boolean " + value)

    def resolve_many(self, name, *args, **kwargs):
        # creates the list that will hold the complete set of names
        # for the current (full) variable name, this partial names
        # will be retrieved using regex matching
        names = []

        # retrieves the various names matched for the current variable
        # name and then iterates over each of these matches to retrieve
        # it's literal value and store it under the names list
        matches = NAMES_REGEX.finditer(name)
        for match in matches:
            part = name[match.start():match.end()]
            names.append(part)

        # sets the initial value of the resolution process as the current
        # global map and then starts the resolution running it for the
        # complete set of "partial" attribute names (iterative resolution)
        value = self.global_map
        for name in names: value = self.resolve(value, name, *args, **kwargs)

        # return the final resolved value, this value should be a result
        # of the iteration around the various partial names
        return value

    def resolve(self, value, name, *args, **kwargs):
        try: result = self._resolve(value, name, *args, **kwargs)
        except exceptions.UndefinedVariable:
            if self.strict_mode: raise
            else: result = None
        return result

    def _resolve(self, value, name, *args, **kwargs):
        # saves the original attribute name under the original variable
        # as it's going to be used latter for some processing operations
        name_o = name

        # filters the variable name (split) so that if it's
        # a complete method call the arguments part is removed
        # this way only the name of the attribute is guaranteed
        name = name.split("(", 1)[0]

        # verifies if the base value refers a dictionary, if that's the
        # case a normal get operation will be performed
        is_dictionary = colony.is_dictionary(value)

        # in case the variable is of type dictionary, the normal recursive
        # iteration step will be executed
        if is_dictionary:
            if name in value: result = value[name]
            else: raise exceptions.UndefinedVariable("variable is not defined: " + name)

        # otherwise variable is of type object or other, then the more complex
        # recursive read of its attributes is executed
        else:
            # checks if the attribute name exists in the current variable
            # in iteration, and in case it does not exists raises an exception
            # indicating that the variable was not found in context
            has_attribute = hasattr(value, name)
            if not has_attribute:
                raise exceptions.UndefinedVariable("variable is not defined: " + name)

            # retrieves the result value from the current value as the attribute
            # of the same name in the passed value
            result = getattr(value, name)

        # retrieves the data type for the current result value as this
        # may affect some of the post processing operation to be done
        result_type = type(result)

        # in case its a variable of type function, must proceed
        # with the calling of it to retrieve the return value
        if result_type in FUNCTION_TYPES:
            # converts the provided list of arguments into a list so that it may
            # be changed to contains the "newly" parsed arguments
            args = list(args)

            # resolves the complete set of arguments defined in the original name
            # that was meant to be resolved for the current value, this should
            # returns a list of arguments that must be then re-retrieved as values
            # for the current template engine (recursive resolution)
            extra = self.resolve_args(name_o)

            # creates the list of argument values by retrieving the values of the
            # various argument types and uses these values in the function call
            args += [self.get_value(arg) for arg in extra]
            result = result(*args, **kwargs)

        # retrieves the current rsults's class and in case the class is of
        # type file reference the contents should be read (the file is closed properly)
        # and set as the current variable (as the new result of it)
        result_class = result.__class__ if hasattr(result, "__class__") else None
        if result_class == colony.FileReference: result = result.read_all()

        # returns the final resolved result value to the caller method, no extra
        # processing should be required for this values is resolved
        return result

    def resolve_args(self, name):
        # tries to match the complete variable name split against
        # the arguments regular expression, to find out if the call
        # is of type simple or complex (arguments present)
        arguments_match = FUCNTION_ARGUMENTS_REGEX.search(name)

        # in case there is no valid arguments match, no processing
        # of arguments will occur and an empty sequence is returned
        # immediately as there's nothing remaining to be done
        if not arguments_match: return ()

        # retrieves the complete group match from the arguments
        # match and removes the calling parentheses
        arguments_s = arguments_match.group()
        arguments_s = arguments_s[1:-1]

        # splits the arguments string into the various arguments
        # names and then treats them, converting them into the
        # normal form
        arguments = arguments_s.split(",")
        arguments = [argument.strip().replace(":", ".") for argument in arguments]

        # creates the list that will hold the various argument types
        # (maps) to be used to retrieve their value, then iterates over
        # all the arguments to populate the list
        arguments_t = []
        for argument in arguments:
            # saves the original value under the original value so that
            # it may be used latter for the creation of the argument
            original = argument

            # retrieves the first character of the argument to be used
            # to try to guess the argument type
            first_char = argument[0]

            # checks the type of the argument, using the first character for
            # so, then sets the literal flag in case the value is a number or
            # a string (literal types)
            is_string = first_char == "'" or first_char == "\""
            is_number = ord(first_char) > 0x2f and ord(first_char) < 0x3a
            is_bool = argument in ("True", "False")
            is_literal = is_string or is_number or is_bool
            _type = is_literal and "literal" or "variable"

            # retrieves the correct value taking into account the various
            # type based flags
            if is_string: value = argument[1:-1]
            elif is_number: value = int(argument)
            elif is_bool: value = argument == "True"
            else: value = argument

            # creates the argument type map with both the type and the value
            # for the argument then adds it to the list of argument types
            argument_t = dict(
                type = _type,
                value = value,
                original = original
            )
            arguments_t.append(argument_t)

        # returns the complete list of processed arguments, this is a list of
        # argument dictionary values that are meant to be latter recursively
        # resolved to obtain the real/final argument values
        return arguments_t

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
        if not isinstance(node, ast.MatchNode):
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

        # retrieves the attributes map and then uses it to retrieve the
        # item that is going to be compared the "target" value for the
        # comparison and the operator to be used for it
        attributes = node.get_attributes()
        item = attributes["item"]
        item = self.get_value(item)
        value = attributes.get("value", None)
        value = self.get_value(value) if value else value
        operator = attributes.get("operator", None)
        operator = self.get_literal_value(operator) if operator else operator

        # retrieves the comparison function from the requested operator
        # and then evaluates the item against the value, this should produce
        # a boolean result that is then returned as the result of the evaluation
        # of the comparison based node, to the caller method
        comparison = COMPARISION_FUNCTIONS.get(operator, None)
        result = comparison(item, value) if comparison else item
        return result

    def _escape_literal(self, literal_value):
        """
        Escapes the given literal value.
        Allow the template engine to skip interpretation
        of template tags.

        @type literal_value: String
        @param literal_value: The literal value to be escaped.
        @rtype: String
        @return: The escaped literal value
        """

        # escapes the literal value
        escaped_literal_value = LITERAL_ESCAPE_REGEX.sub("$", literal_value)

        # returns the escaped literal value
        return escaped_literal_value

    def _resolve_locale(self, value):
        """
        Resolves the given value using the currently available
        locale bundles to archive the resolution of the value.

        The resolution of the value is only possible to string
        values, although no exception is raises otherwise, the
        method fails silently.

        @type value: Object
        @param value: The value to be localized, it may be any
        type of data although only string are localizable.
        @rtype: String
        @return: The resolved locale value for the value or the
        original value in case no localization is possible.
        """

        # in case the value is invalid, not set or
        # an empty string no need to resolve it
        if not value: return value

        # in case the type of the value is a sequence the resolution
        # of the locale must be made for each of the elements of the
        # sequence (complete recursive resolution)
        if type(value) in SEQUENCE_TYPES:
            # runs the locale resolution for each of the sequence
            # items and then encapsulates the results into a list
            return [self._resolve_locale(item) for item in value]

        # in case the type of the value is not a string
        # or a format list type it's not possible to
        # resolve it (no string resolution available)
        if type(value) not in RESOLVABLE_TYPES: return value

        # iterates over all the present locale bundles
        # trying to find one that contains the locale
        # version of the value, in case none contains it
        # the value is literal and returned
        for locale_bundle in self.locale_bundles:
            # in case the value is not present in the locale
            # bundle no need to process it, continues the loop
            if not value in locale_bundle: continue

            # in case the value is present in the locale bundle
            # retrieves the locale version for the updating of
            # the reference value
            _value = locale_bundle[value]

            # in case the (private) replace method is present in
            # the value the substitution of the value must be done
            # through it otherwise the value reference is replaced
            # by the newly retrieved value
            if hasattr(value, "__replace__"): value.__replace__(_value)
            else: value = _value

            # breaks the loop because the first locale
            # is considered to be the highest priority
            break

        # returns the locale value or the literal value in case
        # no localization bundle is available for the value
        return value

    def _serialize_value(self, value):
        # retrieves the data type for the given value
        # to be checked against the various "checkings"
        value_type = type(value)

        # in case the current value is not "serializable"
        # it must be returned immediately
        if not value_type in SERIALIZABLE_TYPES: return value

        # in case the value value is a sequence it must be
        # "serializable" using the serialization of sequences
        # "mechanism"
        if value_type in SEQUENCE_TYPES: return self._serialize_sequence(value)

    def _serialize_sequence(self, value):
        # retrieves the data type for the given value
        # to be checked against the various "checkings"
        value_type = type(value)

        # in case the current value is not a sequence
        # it must be returned immediately
        if not value_type in SEQUENCE_TYPES: return value

        # creates the string buffer to hold the serialization values
        # and writes the initial list open token into it
        string_buffer = colony.StringBuffer()
        string_buffer.write(u"[")

        # unsets the is first flag so that the comma separator
        # is not written in the first iteration
        is_first = True

        # iterates over all the list values to serialize them into
        # the correct representation
        for _value in value:
            # checks if this is the first iteration in case it's
            # not the comma separator is written to the string buffer
            if is_first: is_first = False
            else: string_buffer.write(u", ")

            # serializes the current value and retrieves the type
            # of the value that will condition the writing into
            # the string buffer
            _value = self._serialize_value(_value)
            _value_type = type(_value)

            # checks if the value contains a unicode string
            # in such case there's no need to re-decode it
            is_unicode = _value_type == types.UnicodeType
            _value = is_unicode and _value or unicode(_value)

            # in case the type of the current value is resolvable the
            # value must be written as an escaped string otherwise
            # the value is written literally
            if _value_type in RESOLVABLE_TYPES: string_buffer.write(u"'" + _value + u"'")
            else: string_buffer.write(_value)

        # writes the "final" end of list token into the string buffer
        # that holds the serialization of the sequence and then retrieves
        # the final value of the serialization from the string buffer
        string_buffer.write(u"]")
        value = string_buffer.get_value()

        # returns the final serialized value of the sequence
        return value

    def _get_serializer(self, name = None):
        # in case the serializers map is not defined triggers the
        # initial loading of the serializer, then in case the serializers
        # list is empty (or invalid) raises the no serializer error
        if SERIALIZERS_MAP == None: self._load_serializers()
        if not SERIALIZERS: raise exceptions.InvalidSerializer("no serializer available")

        # in case no (serializer) name is provided the first
        # (and preferred) serializer name is used then retrieves
        # the associated serializer object and in case it fails
        # raises an error
        name = name or SERIALIZERS[0]
        serializer = SERIALIZERS_MAP.get(name, None)
        if not serializer: raise exceptions.InvalidSerializer("no serializer available for '%s'", name)

        # creates the serializer tuple containing both
        # the serializer object and the name
        serializer_tuple = (serializer, name)
        return serializer_tuple

    def _load_serializers(self):
        """
        Loads the various serializer objects according
        to the associated module names.

        This method ignores the import problems for non
        existent serializers, removing them from the
        associated data structures.
        """

        global SERIALIZERS_MAP

        # creates the list that will hold the various
        # names to be removed from the serializers list
        removal = []

        # initializes the serializers map that will associate
        # the name of the serializer with the object
        SERIALIZERS_MAP = {}

        # iterates over all the (serializer) names in the
        # serializers list to try to import the module and
        # alter the affected data structures
        for name in SERIALIZERS:
            # tries to import the module associated with the
            # serializer and in case it fails adds the name
            # to the removal list otherwise sets the serializer
            # in the associated map
            try: object = __import__(name)
            except: removal.append(name)
            else: SERIALIZERS_MAP[name] = object

        # iterates over all the (serializer) names to be
        # removed and removes them from the serializers list
        for name in removal: SERIALIZERS.remove(name)

class EvalVisitor(Visitor):

    def get_value(self, attribute_value, process_literal = False, localize = False):
        # retrieves the original value from the attribute and then
        # splits it around the filter operator, retrieving both the
        # base name value and the filter literal values
        original = attribute_value["original"]
        parts = original.split("|")
        name = parts[0].strip()
        filters = [filter.strip() for filter in parts[1:]]

        # creates the globals map accessor value from the current map
        # of global values and then uses it to evaluate the current
        # name literal value in the current python context, the resulting
        # value is nullified in case there's an exception in the evaluation
        globals = util.accessor(self.global_map)
        try: value = eval(name, globals, globals)
        except: value = None

        # in case the returned value is callable it must be called
        # with no arguments to be able to retrieve the final value
        # for the current evaluation (simple callable)
        is_callable = hasattr(value, "__call__")
        if is_callable: value = value()

        # iterates over the complete set of filter definition to
        # resolve the final value according to the filter and then
        # runs the final step of locale value resolution (auto locale)
        for filter in filters: value = self.resolve_many(filter, value)
        value = self._resolve_locale(value) if localize else value

        # returns the final value according to the eval based value
        # retrieval that uses the python interpreter for evaluation
        return value
