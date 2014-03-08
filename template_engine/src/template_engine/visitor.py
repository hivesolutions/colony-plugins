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

FUCNTION_ARGUMENTS_REGEX_VALUE = "\([\sa-zA-Z0-9_\-,\.\:\='\/\"]+\)"
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

DEFAULT_DATE_FORMAT = "%d/%m/%y"
""" The default date format """

DEFAULT_TIME_FORMAT = "%H:%M:%S"
""" The default time format """

DEFAULT_DATE_TIME_FORMAT = "%d/%m/%y %H:%M:%S"
""" The default date time format """

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
    "False" : False,
    "len" : len
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
    "not" : lambda  item, value: not item,
    "eq" : lambda item, value: item == value,
    "neq" : lambda item, value: not item == value,
    "gte" : lambda item, value: item >= value,
    "gt" : lambda item, value: item > value,
    "lte" : lambda item, value: item <= value,
    "lt" : lambda item, value: item < value,
    "len" : lambda item, value: len(item) == value,
    "lengt" : lambda item, value: len(item) > value,
    "lenlt" : lambda item, value: len(item) < value,
    "in" : lambda item, value: item and value in item or False,
    "nin" : lambda item, value: item and not value in item or False
}
""" The map containing the comparison functions (lambda) these
are going to be used "inside" the visitor execution logic """

def _visit(ast_node_class):

    def decorator(function, *args, **kwargs):
        function.ast_node_class = ast_node_class
        return function

    return decorator

def dispatch_visit():

    def create_interceptor(function):

        def decorator_interceptor(*args, **kwargs):
            # unpacks the first two "unnamed" arguments as the self
            # instance reference and the node element to be visited
            self = args[0]
            node = args[1]

            # verifies if the current instance contains the node method
            # map if that's the case retrieves otherwise falls back to an
            # empty dictionary (for code compatibility)
            has_map = hasattr(self, "node_method_map")
            node_method_map = self.node_method_map if has_map else dict()

            # retrieves the class for the node argument and then
            # gathers the complete mro class definition to be able
            # to iterate over the class hierarchy
            node_class = node.__class__
            mro = node_class.mro()

            # iterates over the complete class hierarchy for the provided
            # node (from bottom to up) so that the best match for the
            # visit operation is found and properly called
            for mro_item in mro:
                # in case the current mro item class level is nor found
                # skips the current iteration (cannot visit at this level)
                if not mro_item in node_method_map: continue

                # the current class level is valid and so the proper method
                # is retrieved from the map and then called with the provided
                # arguments, note that a before visit and an after visit calls
                # are done so that proper "notification" exists
                visit_method = node_method_map[mro_item]
                self.before_visit(*args[1:], **kwargs)
                visit_method(*args, **kwargs)
                self.after_visit(*args[1:], **kwargs)

                return

            function(*args, **kwargs)

        return decorator_interceptor

    def decorator(function, *args, **kwargs):
        interceptor = create_interceptor(function)
        return interceptor

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
    """ The strict mode, that controls if the processing should
    be done in a strict way meaning that exceptions should be
    raised whenever an unexpected value is received/processed """

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
        # retrieves the current instance class and list the
        # complete set of element for the current class so that
        # the proper node method map may be created
        cls = self.__class__
        cls_elements = dir(cls)

        # iterates over the complete set of elements (attributes)
        # defined for the current instance's class trying to find
        # the ones that are annotated with the ast node class value
        for name  in cls_elements:
            # retrieves the current element in iteration and verifies
            # if the current element is annotated with the asr node class
            # value, if that's not the case continues the loop
            element = getattr(cls, name)
            if not hasattr(element, "ast_node_class"): continue

            # retrieves the elements node class and associated the
            # current element with the node class in the node class
            # method map (to be used latter in runtime verification)
            ast_node_class = element.ast_node_class
            self.node_method_map[ast_node_class] = element

    def attach_process_method(self, method_name, method):
        # creates the process method instance, that is attached to
        # the general visitor class and sets it the current instance
        method_instance = types.MethodType(method, self, Visitor)
        setattr(self, method_name, method_instance)

        # creates the process method tuple that contains both the
        # name of the method and the method reference and adds the
        # tuple to the list of process method, this is going to be
        # used in the initial stage of the template creation
        process_method_tuple = (method_name, method)
        self.process_methods_list.append(process_method_tuple)

    def get_global_map(self):
        return self.global_map

    def set_global_map(self, global_map):
        self.global_map = global_map

    def get_global(self, name):
        return self.global_map[name]

    def set_global(self, name, value):
        self.global_map[name] = value

    def del_global(self, name):
        del self.global_map[name]

    def get_global_many(self, name):
        parts = name.split(".")
        last = parts[-1]
        current = self.global_map
        for part in parts[:-1]:
            current = current.get(part, {})
        return current.get(last, None)

    def set_global_many(self, name, value):
        parts = name.split(".")
        last = parts[-1]
        current = self.global_map
        for part in parts[:-1]:
            next = current.get(part, {})
            current[part] = next
            current = next
        current[last] = value

    def add_bundle(self, bundle):
        self.locale_bundles.append(bundle)

    def get_encoding(self):
        return self.encoding

    def set_encoding(self, encoding):
        self.encoding = encoding

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_template_engine(self):
        return self.template_engine

    def set_template_engine(self, template_engine):
        self.template_engine = template_engine

    def get_variable_encoding(self):
        return self.variable_encoding

    def set_variable_encoding(self, variable_encoding):
        self.variable_encoding = variable_encoding

    def get_strict_mode(self):
        return self.strict_mode

    def set_strict_mode(self, strict_mode):
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

        # retrieves the complete set of attributes from the attributes
        # defined for the current node, it's an extensive list and
        # the range of usage and data types are vast
        value = attributes["value"]
        value = self.get_value(value, localize = True)
        prefix = attributes.get("prefix", None)
        prefix = self.get_value(prefix, localize = True, default = "")
        format = attributes.get("format", None)
        format = self.get_value(format)
        quote = attributes.get("quote", None)
        quote = self.get_boolean_value(quote)
        xml_escape = attributes.get("xml_escape", None)
        xml_escape = self.get_boolean_value(xml_escape)
        xml_quote = attributes.get("xml_escape", None)
        xml_quote = self.get_boolean_value(xml_quote)
        newline_convert = attributes.get("newline_convert", None)
        newline_convert = self.get_boolean_value(newline_convert)
        convert = attributes.get("convert", None)
        convert = self.get_value(convert)
        allow_empty = attributes.get("allow_empty", None)
        allow_empty = self.get_value(allow_empty, default = True)
        default = attributes.get("default", None)
        default = self.get_value(default, localize = True)
        serializer = attributes.get("serializer", None)
        serializer = self.get_literal_value(serializer)

        # in case the format value is defined the provided value
        # must be formated according to the value specified in
        # that field using the default (python) formatter
        if format:
            is_valid = format and not value == None
            value = format % value if is_valid else value

        # creates the invalid values tuple according to the allow
        # empty flag and the verifies if the value is defined under
        # such value falling back to the default value for such case
        invalid_values = (None,) if allow_empty else (None, "")
        if value in invalid_values: value = default

        # in case the attribute value value is invalid and the default
        # value is not set (no need to show the value) must return
        # immediately nothing will be printed
        if value in invalid_values and default == None: return

        # in case the serializer value is set must try to gather
        # the serializer and serialize the attribute value using it
        if serializer:
            serializer, _name = self._get_serializer(serializer)
            value = serializer.dumps(value)

        # serializes the value into the correct visual representation
        # (in case the attribute type is "serializable", eg: lists, tuples, etc.)
        value = self._serialize_value(value)

        # checks if the attribute value contains a unicode string
        # in such case there's no need to re-decode it
        is_unicode = type(value) == types.UnicodeType
        value = is_unicode and value or unicode(value)

        # in case the attribute convert value is set
        if convert:
            # retrieves the conversion method for the string
            # value representing it and uses it to convert
            # the attribute value to the target encoding
            conversion_method = CONVERSION_MAP.get(convert, None)
            value = conversion_method(value) if conversion_method else value

        # in case the variable encoding is defined must re-encode
        # the variable according to the current variable encoding
        if self.variable_encoding: value = value.encode(self.variable_encoding)

        # in case the attribute quote value is set must quote the
        # value using the provided colony utility
        if quote:
            value = value.encode("utf-8")
            value = colony.quote(value, safe = "/")

        # runs the final transformation on the value according to
        # the provided flags (custom operations)
        if xml_escape: value = xml.sax.saxutils.escape(value)
        if xml_quote: value = value.replace("\"", "&quot;")
        if newline_convert: value = value.replace("\n", "<br/>")

        # runs the final appending of the prefix value to the value
        # and then writes the final string/unicode value to the buffer
        value = prefix + value
        self.string_buffer.write(value)

    def process_var(self, node):
        """
        Processes the var node, this is the operation that
        allow the attribute of a value in the current context
        the required attributes are the item (literal) and the
        value.

        @type node: Node
        @param node: The single node to be processed as var.
        """

        # retrieves the map that contains the attributes for the
        # current node and then unpacks each of this values
        attributes = node.get_attributes()
        item = attributes["item"]
        item = self.get_literal_value(item)
        value = attributes["value"]
        value = self.get_value(value)

        # sets the attribute value value in the global map, this
        # is considered to represent the assign operation, from
        # this moment the variable with the same name is available
        self.set_global(item, value)

    def process_for(self, node):
        return self.process_foreach(node)

    def process_foreach(self, node):
        attributes = node.get_attributes()
        iterable = attributes["from"]
        iterable = self.get_value(iterable)
        item = attributes.get("item", None)
        item = self.get_literal_value(item)
        index_ref = attributes.get("index", None)
        index_ref = self.get_literal_value(index_ref)
        key_ref = attributes.get("key", None)
        key_ref = self.get_literal_value(key_ref)
        start_index = attributes.get("start_index", None)
        start_index = self.get_literal_value(start_index)

        # in case the start index literal value is defined
        # retrieves the index as the integer cast of the
        # partial name otherwise the index start at one
        if start_index: index = int(start_index[1:-1])
        else: index = 1

        # in case the attribute does not have the iterator method
        # it's not iterable and a fallback strategy must performed
        if not hasattr(iterable, "__iter__"):

            # in case the strict mode is active, an exception must be
            # raised because it's not possible to perform the iteration
            if self.strict_mode:
                # retrieves the attribute from name (value) and uses
                # it to raise the proper exception with the description
                # for the variable that is not iterable
                from_value = attributes["from"]["value"]
                raise exceptions.VariableNotIterable("value not iterable: " + from_value)

            # otherwise avoids exception in case the object
            # is not an invalid one (possible problems) by
            # "casting" the attribute from value to a list it
            # will create an iterable object that may be used
            elif not iterable == None: iterable = [iterable]

            # otherwise in case the object is considered invalid
            # the best match for the cast is an empty list
            else: iterable = []

        # sets the various global wide values relates with the
        # current loop operation that is going to be performed
        # this values are not related with each iteration
        self.set_global_many("loop.length", len(iterable))
        self.set_global_many("loop.cycle", self._loop_cycle)

        # verifies if the iterable currently in use is of type
        # map (dictionary) this will condition the way the loop
        # part of the operation will be performed
        is_map = colony.is_dictionary(iterable)

        # iterates over the complete set of elements in the iterable,
        # note that the value contained in the item will not be the
        # same if the iterable is a map or if it is a sequence
        for element in iterable:
            is_first = index == 1
            is_last = index == len(iterable)

            self.set_global_many("loop.index", index)
            self.set_global_many("loop.index0", index - 1)
            self.set_global_many("loop.first", is_first)
            self.set_global_many("loop.last", is_last)
            self.set_global("is_first", is_first)
            self.set_global("is_last", is_last)

            key = element if is_map else index
            value = iterable[element] if is_map else element

            if item: self.set_global(item, value)
            if index_ref: self.set_global(index_ref, index)
            if key_ref: self.set_global(key_ref, key)

            if self.visit_childs:
                for node_child_node in node.child_nodes:
                    node_child_node.accept(self)

            index += 1

    def process_if(self, node):
        # evaluates the current node comparison, this is the default
        # acceptance behavior for all the nodes that do not require
        # an extra evaluation process (evaluation nodes)
        accept_node = self._evaluate_comparison_node(node)

        # in case the visit child flag is not set the method must
        # return immediately as there's nothing remaining to be done
        if not self.visit_childs: return

        # iterates over all the child nodes for the current if node
        # to evaluate or process them according to their type
        for child_node in node.child_nodes:
            # validates the accept node, so that if the node is "eval"
            # the evaluation is done otherwise the default evaluation
            # result for the if node is applied
            accept_node = self._validate_accept_node(child_node, accept_node)

            # in case the accept node is set to invalid
            # the evaluation is over (nothing to be done)
            if accept_node == None: return

            # in case the accept node flag is set accepts the node
            # child node as it is considered to be valid
            accept_node and child_node.accept(self)

    def process_else(self, node):
        pass

    def process_elif(self, node):
        pass

    def process_cycle(self, node):
        attributes = node.get_attributes()
        values = attributes["values"]
        values = self.get_value(values)
        values = values.split(",")

        if hasattr(node, "current_index"):
            values_length = len(values)
            current_index = node.current_index
            if current_index == values_length - 1: current_index = 0
            else: current_index += 1
        else:
            current_index = 0

        node.current_index = current_index
        current_value = values[current_index]
        self.string_buffer.write(current_value)

    def process_count(self, node):
        # retrieves the current nodes's attributes and gathers the value
        # field from the dictionary retrieving then it's value
        attributes = node.get_attributes()
        value = attributes["value"]
        value = self.get_value(value)

        # in case the retrieved value is invalid the length of it is considered
        # to be zero otherwise measures its size and sets accordingly
        if value == None: value_length = 0
        else: value_length = len(value)

        # checks if the attribute value length contains a unicode string
        # in such case there's no need to re-decode it
        is_unicode = type(value_length) == types.UnicodeType
        value_length = is_unicode and value_length or unicode(value_length)

        # in case the variable encoding value is defined encodes the string
        # value using the currently defined encoding (as expected) and then
        # writes the resulting string value to the current buffer
        if self.variable_encoding:
            value_length = value_length.encode(self.variable_encoding)
        self.string_buffer.write(value_length)

    def process_include(self, node):
        # retrieves the current node's attributes and uses them to unpack
        # the attributes that are relevant for the include processing
        attributes = node.get_attributes()
        file = attributes.get("file", None)
        file = self.get_literal_value(file)
        file_value = attributes.get("file_value", None)
        file_value = self.get_value(file_value)

        # retrieves the initial file path value from either the file
        # or the file value attributes (whatever is defined)
        file_path = file or file_value

        # in case the file path was not able to be resolved an
        # exception must be raised indicating the undefined reference
        # to the template to be included
        if not file_path:
            # retrieves the node type and raises an exception with
            # the value that was just retrieved
            node_type = node.get_type()
            raise exceptions.UndefinedReference(node_type)

        # in case the path provided file path is not absolute an extra
        # step must be performed to resolve the complete file path to
        # the template file using the current template's file path
        if not os.path.isabs(file_path):
            # retrieves the file directory from the file path and then
            # sets the file path as relative to the file directory, after
            # the join operations normalizes the path so that it represents
            # the proper path with the proper operative system representation
            file_directory = os.path.dirname(self.file_path)
            file_path = os.path.join(file_directory, file_path)
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
        # creates a new uuid value and converts it into a string
        # value to be used in the string buffer
        uuid_value = uuid.uuid4()
        uuid_string_value = str(uuid_value)
        self.string_buffer.write(uuid_string_value)

    def process_year(self, node):
        # retrieves the current date time formats it according to
        # the default year format and writes the value to buffer
        current_date_time = datetime.datetime.now()
        year_value = current_date_time.strftime("%Y")
        self.string_buffer.write(year_value)

    def process_date(self, node):
        attributes = node.get_attributes()
        format = attributes.get("format", None)
        format = self.get_literal_value(format, default = DEFAULT_DATE_FORMAT)
        format = str(format)

        current_date_time = datetime.datetime.now()
        date_value = current_date_time.strftime(format)
        self.string_buffer.write(date_value)

    def process_time(self, node):
        attributes = node.get_attributes()
        format = attributes.get("format", None)
        format = self.get_literal_value(format, default = DEFAULT_TIME_FORMAT)
        format = str(format)

        current_date_time = datetime.datetime.now()
        time_value = current_date_time.strftime(format)
        self.string_buffer.write(time_value)

    def process_datetime(self, node):
        attributes = node.get_attributes()
        format = attributes.get("format", None)
        format = self.get_literal_value(format, default = DEFAULT_DATE_TIME_FORMAT)
        format = str(format)

        current_date_time = datetime.datetime.now()
        date_time_value = current_date_time.strftime(format)
        self.string_buffer.write(date_time_value)

    def process_format_datetime(self, node):
        attributes = node.get_attributes()
        value = attributes["value"]
        value = self.get_value(value)
        format = attributes["format"]
        format = self.get_literal_value(format)
        default = attributes.get("default", None)
        default = self.get_value(default)

        if value == None:
            value = default if default else value
            if value: self.string_buffer.write(value)
            return

        format = str(format)
        value_format = value.strftime(format)
        self.string_buffer.write(value_format)

    def process_format_timestamp(self, node):
        attributes = node.get_attributes()
        value = attributes["value"]
        value = self.get_value(value)
        format = attributes["format"]
        format = self.get_literal_value(format)
        default = attributes.get("default", None)
        default = self.get_value(default)

        if value == None:
            value = default if default else value
            if value: self.string_buffer.write(value)
            return

        format = str(format)
        date_time = datetime.datetime.utcfromtimestamp(value)
        value_format = date_time.strftime(format)
        self.string_buffer.write(value_format)

    def process_timestamp(self, node):
        attributes = node.get_attributes()
        value = attributes.get("value", None)
        value = self.get_value(value, default = datetime.datetime.now())
        default = attributes.get("default", None)
        default = self.get_value(default, localize = True)

        if value == None:
            value = default if default else value
            if value: self.string_buffer.write(value)
            return

        time_tuple = value.utctimetuple()
        timestamp = calendar.timegm(time_tuple)
        timestamp_s = str(timestamp)
        self.string_buffer.write(timestamp_s)

    def get_value(self, attribute, localize = False, default = None):
        """
        Retrieves the value (variable or literal) of the given
        value. The process of retrieving the variable value is
        iterative and may consume some time in resolution.

        An optional localize flag may be set of the value should
        be localized using the current local bundles.

        @type attribute: Dictionary
        @param attribute: A map describing the attribute structure.
        @type localize: bool
        @param localize: If the value must be localized using the currently
        available locale bundles.
        @type default: Object
        @param default: The default (fallback) value to be returned if
        no valid attribute is provided or in case it is invalid.
        @rtype: Object
        @return: The resolved attribute value.
        """

        # in case the passed attribute is not valid the default must
        # be returned immediately as no resolution is possible, this
        # is the default and expected behavior (fallback procedure)
        if not attribute: return default

        # in case the attribute value is of type variable
        if attribute["type"] == "variable":
            # retrieves the variable name
            variable_name = attribute["value"]

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
        elif attribute["type"] == "literal":
            # retrieves the literal value from the attribute
            # this is going to be considered the proper value
            value = attribute["value"]

        # returns the processed value to the caller method, this is the
        # considered to be the value for the requested attribute
        return value

    def get_literal_value(self, attribute, default = None):
        if attribute == None: return default
        return attribute["value"]

    def get_boolean_value(self, attribute, default = False):
        # in case the provided attribute structure is not
        # defined the boolean value is assumed to be the
        # provided default value (as defined is specification)
        if attribute == None: return default

        # retrieves the literal value of the provided
        # attribute, retrieving then the data type for it
        value = attribute["value"]
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
            builtins = value.get("__builtins__", dict())
            if name in value: result = value[name]
            elif name in builtins: result = builtins[name]
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
            # be changed to contains the "newly" parsed arguments, and then creates
            # a copy of the passed keyword arguments so that a new dictionary may
            # be populated with the extra values to be added (by parsing)
            args = list(args)
            kwargs = kwargs.copy()

            # resolves the complete set of arguments defined in the original name
            # that was meant to be resolved for the current value, this should
            # returns a list of arguments that must be then re-retrieved as values
            # for the current template engine (recursive resolution)
            extra = self.resolve_args(name_o)

            # populates both the list of unnamed arguments and extends the map
            # containing the named arguments with the processed name arguments,
            # note that the argument type is defined by the presence of the name
            # argument in the dictionary that defined the same argument
            for arg in extra:
                name = arg["name"]
                value = self.get_value(arg)
                if name: kwargs[name] = value
                else: args.append(value)

            # runs the calling of the method/function/callable with the complete set
            # of arguments, this should include both the default ones and the ones
            # parsed from the string (as expected by specification)
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
            # tries to split the provided argument string into the two
            # possible parts (name and argument value) in case only one
            # value exists (unnamed argument) used the default invalid
            # attribute for the name value (expected behavior)
            parts = argument.split("=", 1)
            if len(parts) == 2: name, argument = parts
            else: argument, = parts; name = None

            # in case the argument or the name are defined and valid strips
            # their values to avoid any extra space character in them
            if argument: argument = argument.strip()
            if name: name = name.strip()

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
                original = original,
                name = name
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
        @param node: The child node to be evaluated, this may either
        be a node that is able to be evaluated or not.
        @type accept_node: bool
        @param accept_node: The accept node flag value, this is
        the fallback value for nodes that are not able (or required)
        to be evaluated for acceptance.
        @rtype: bool
        @return: The new value for the accept node flag.
        """

        # verifies if the current node is mean to be evaluated and
        # if that's not the case returns the passed fallback value
        eval_node = isinstance(node, ast.MatchNode) or\
            isinstance(node, ast.EvalNode)
        if not eval_node: return accept_node

        # retrieves the value type for the current node and uses
        # this value to decide to either process it or not
        type = node.get_type()
        if type in ("else", "elif", "endif"):
            # in case the accept node
            # flag is already set (the result is
            # already been evaluated positively)
            if accept_node: return None

            # in case the type is plain, the node should always
            # be accepted, and no extra evaluation process is
            # performed (node is accepted by default)
            if type in ("else", "endif"): accept_node = True

            # in case the type is elif, the node should be
            # accepted in case of positive evaluation
            elif "elif":
                result = self._evaluate_comparison_node(node)
                accept_node = result

        # returns the accept node final result so that the caller
        # may decide to either visit the node or not
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
        value = self.get_value(value)
        operator = attributes.get("operator", None)
        operator = self.get_literal_value(operator)

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
        if not type(value) in RESOLVABLE_TYPES: return value

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

    def _loop_cycle(self, odd, even):
        index = self.get_global_many("loop.index")
        is_odd = index % 2 == 1
        return odd if is_odd else even

class EvalVisitor(Visitor):
    """
    Specialized visitor infra-structure that uses the python
    eval call to evaluate the various attribute values/variables
    that are passed. Keep in mind that this is not a safe
    environment (not sandboxed) and should not be used to run
    arbitrary/unsafe code.
    """

    def get_value(self, attribute, localize = False, default = None):
        # in case the passed attribute is not valid the default must
        # be returned immediately as no resolution is possible, this
        # is the default and expected behavior (fallback procedure)
        if not attribute: return default

        # retrieves the original value from the attribute and then
        # splits it around the filter operator, retrieving both the
        # base name value and the filter literal values
        original = attribute["original"]
        parts = original.split("|")
        name = parts[0].strip()
        filters = [filter.strip() for filter in parts[1:]]

        # creates the globals map accessor value from the current map
        # of global values and then uses it to evaluate the current
        # name literal value in the current python context, the resulting
        # value is nullified in case there's an exception in the evaluation
        globals = util.accessor(self.global_map)
        globals["__builtins__"] = BUILTINS
        try: value = eval(name, globals, globals)
        except AttributeError: value = None
        except NameError: value = None
        except SyntaxError: value = None

        # verifies if the currently returned value is an accessor value and
        # in case it is retrieves the reference values as the value so that
        # the inner type of it as respected and the proxy is not used
        is_accessor = isinstance(value, util.Accessor)
        if is_accessor: value = value.ref

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
