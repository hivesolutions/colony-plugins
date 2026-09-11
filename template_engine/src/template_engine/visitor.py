#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import re
import os
import uuid
import types
import calendar
import datetime

import xml.sax.saxutils

import colony

from . import ast
from . import util
from . import exceptions

FUNCTION_TYPES = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinMethodType,
    types.BuiltinFunctionType,
)
""" The complete set of types that are going to be
considered function types during runtime """

SERIALIZERS = ("json", "pickle")
""" The list to hold the various serializers
in order of preference for serialization """

SERIALIZERS_MAP = None
""" The map associating the encoding type for
the serialization with the appropriate serializer
object to handle it """

LITERAL_ESCAPE_REGEX_VALUE = r"\$\\\\(?=\\\\*\{)"
""" The literal escape regular expression value """

FUNCTION_ARGUMENTS_REGEX_VALUE = r"\([^\)]+\)"
""" The function arguments regular expression value
that will match any possible (variable or constant) value """

NAMES_REGEX_VALUE = r"([^\.]+\([^\)]+\))|([^\.]+)"
""" The regular expression that is going to be used for the
splitting of the various names for a variable based value that
is going to be evaluated at runtime, this value may contain
method calls with literal an non literal values """

LITERAL_ESCAPE_REGEX = re.compile(LITERAL_ESCAPE_REGEX_VALUE)
""" The literal escape regular expression """

FUNCTION_ARGUMENTS_REGEX = re.compile(FUNCTION_ARGUMENTS_REGEX_VALUE)
""" The function arguments regular expression """

NAMES_REGEX = re.compile(NAMES_REGEX_VALUE)
""" The compiled version of names regular expression used for the
matching of the various components of a variable template value """

CACHE_LIMIT = 4096
""" The maximum number of entries to be kept in each of the global
(process wide) parsing caches, once this value is reached the cache
is completely flushed (avoids unbounded memory growth) """

NAMES_CACHE = {}
""" The cache that associates the complete name of a variable with the
sequence of the partial names that compose it, as this operation is a
pure one its result may be safely re-used between resolutions """

ARGUMENTS_CACHE = {}
""" The cache that associates the name of a method call with the sequence
of the (already processed) argument structures for it, avoiding the
re-parsing of the arguments for every single call resolution """

NODE_METHOD_CACHE = {}
""" The cache that associates a visitor class with the map of the AST node
classes to the (visit) methods that handle them, this structure is static
for a class and so it's only built once per class """

VISIT_CACHE = {}
""" The cache that associates a visitor class with the map that resolves
an AST node class into the proper visit method, this avoids the walking
of the class hierarchy for each one of the node visits """

EMPTY_FILTERS = ()
""" The empty filters sequence, re-used for every attribute that does not
define any filtering pipeline (avoids extra allocations) """


DEFAULT_DATE_FORMAT = "%d/%m/%y"
""" The default date format """

DEFAULT_TIME_FORMAT = "%H:%M:%S"
""" The default time format """

DEFAULT_DATE_TIME_FORMAT = "%d/%m/%y %H:%M:%S"
""" The default date time format """

SEQUENCE_TYPES = (list, tuple)
""" The tuple containing the types considered to be sequences """

SERIALIZABLE_TYPES = (list, tuple)
""" The tuple containing the set of types that can be
"serializable" in a custom manner """

RESOLVABLE_TYPES = (str, colony.legacy.UNICODE, colony.FormatTuple)
""" The tuple containing the set of types that can be
"resolved" in the localization context """

BUILTINS = {"True": True, "False": False, "len": len}
""" The base builtins structure that is going to be re-used
for every parsing operation to be done by the visitor, this
should contain the minimum amount of symbols required for the
parsing of the template file (to avoid security issues) """

CONVERSION_MAP = {"2_of_5": colony.encode_2_of_5}
""" The map associating the name of the conversion
function with the conversion function symbol reference """

COMPARISION_FUNCTIONS = {
    "not": lambda item, value: not item,
    "eq": lambda item, value: item == value,
    "neq": lambda item, value: not item == value,
    "gte": lambda item, value: item >= value,
    "gt": lambda item, value: item > value,
    "lte": lambda item, value: item <= value,
    "lt": lambda item, value: item < value,
    "len": lambda item, value: len(item) == value,
    "lengt": lambda item, value: len(item) > value,
    "lenlt": lambda item, value: len(item) < value,
    "in": lambda item, value: item and value in item or False,
    "nin": lambda item, value: False if item == None else not value in item,
}
""" The map containing the comparison functions (lambda) these
are going to be used "inside" the visitor execution logic """

FILTERS = dict(
    e=lambda v, a, t: v if v == None else xml.sax.saxutils.escape(t._to_string(v)),
    s=lambda v, a, t: a.update(xml_escape=False) or v,
    escape=lambda v, a, t: v if v == None else xml.sax.saxutils.escape(t._to_string(v)),
    safe=lambda v, a, t: a.update(xml_escape=False) or v,
    default=lambda v, a, t, default="", boolean=False: (
        default if boolean and not v or v == None else v
    ),
    double=lambda v, a, t: v if v == None else v * 2,
    append=lambda v, a, t, extra: v + extra,
    prepend=lambda v, a, t, extra: extra + v,
    format=lambda v, a, t, format, default=None: default if v == None else format % v,
    nl_to_br=lambda v, a, t: v.replace("\n", "<br/>"),
    split=lambda v, a, t, separator="\n": v.split(separator),
    timestamp=lambda v, a, t, default="": (
        str(calendar.timegm(v.utctimetuple())) if v else default
    ),
    range=lambda v, a, t: range(int(v)),
    locale=lambda v, a, t: t._resolve_locale(v),
)
""" The dictionary containing the complete set
of base filters to be exposed to the visitor,
this dictionary may be extended at runtime """

EXTRAS = dict(
    date=lambda format="%d/%m/%y": datetime.datetime.now().strftime(format),
    format_datetime=lambda v, format="%Y/%m/%d %H:%M:%S": (
        None if v == None else v.strftime(format)
    ),
)
""" Dictionary that contains the set of symbols
that are going to extend the base ones (builtins)
in the process of name resolution """

BUILTINS_EXTRAS = dict(BUILTINS)
BUILTINS_EXTRAS.update(EXTRAS)
""" The complete set of builtins, resulting from the extension of the base
ones with the extra symbols, this map is shared by the various visitor
instances and so it must not be changed at runtime """


def escape_literal(literal_value):
    """
    Escapes the given literal value, allowing the template engine to
    skip the interpretation of template tags.

    This operation is meant to be run at "parse time" so that no extra
    processing of the literal values is required at template rendering
    time (performance oriented).

    :type literal_value: String
    :param literal_value: The literal value to be escaped.
    :rtype: String
    :return: The escaped literal value.
    """

    return LITERAL_ESCAPE_REGEX.sub("$", literal_value)


def split_filters(original):
    """
    Splits the provided original (attribute) value around the filter
    separator token, returning both the base name of the value and the
    sequence of the filters that should be applied to it.

    The result of this operation is meant to be stored in the attribute
    structure itself so that no string splitting is required for each
    one of the value resolutions (performance oriented).

    :type original: String
    :param original: The original (unprocessed) value of the attribute
    that is going to be split around the filter separator.
    :rtype: Tuple
    :return: A tuple containing both the base name of the attribute and
    the sequence of filters to be applied to its value.
    """

    # in case the provided original value is not a string based value
    # it's not possible to split it, returning the "original" value
    # and an empty set of filters (as expected)
    if not hasattr(original, "split"):
        return original, EMPTY_FILTERS

    # in case there's no filter separator in the value the complete
    # value is considered to be the name of the attribute, this is
    # considered to be the most common (and fast) scenario
    if not "|" in original:
        return original.strip(), EMPTY_FILTERS

    # splits the value around the filter separator using the first
    # part as the name of the attribute and the remaining ones as
    # the various filters to be applied (in sequence)
    parts = original.split("|")
    return parts[0].strip(), tuple(part.strip() for part in parts[1:])


def split_arguments(value):
    """
    Splits the provided arguments string around the argument separator
    token, taking into account the quoted sequences so that a separator
    contained inside a string literal does not split it.

    :type value: String
    :param value: The (complete) arguments string that is going to be
    split around the argument separator.
    :rtype: List
    :return: The list containing the various arguments resulting from
    the split operation.
    """

    # creates the list that is going to hold the various arguments and
    # the buffer of characters for the argument currently being built
    arguments = []
    current = []

    # creates the value that holds the quote character that has started
    # the sequence currently open (invalid in case none is open)
    quote = None

    # iterates over the complete set of characters of the arguments
    # string to split it around the (unquoted) separator characters
    for char in value:
        if quote:
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == ",":
            arguments.append("".join(current))
            del current[:]
            continue
        current.append(char)

    # adds the remaining (pending) characters as the final argument of
    # the sequence and returns the complete set of arguments
    arguments.append("".join(current))
    return arguments


def node_method_map(cls):
    """
    Builds (or retrieves from cache) the map that associates the various
    AST node classes with the methods of the provided visitor class that
    are annotated to handle them.

    :type cls: Class
    :param cls: The visitor class for which the node method map is going
    to be built.
    :rtype: Dictionary
    :return: The map associating the AST node classes with the proper
    visit methods of the provided class.
    """

    # tries to retrieve the already built map for the class, avoiding
    # the (expensive) listing of the complete set of class elements
    map = NODE_METHOD_CACHE.get(cls, None)
    if not map == None:
        return map

    # iterates over the complete set of elements (attributes) defined
    # for the provided class trying to find the ones that are annotated
    # with the AST node class value, associating them in the map
    map = dict()
    for name in dir(cls):
        element = getattr(cls, name)
        if not hasattr(element, "ast_node_class"):
            continue
        map[element.ast_node_class] = element

    # stores the newly built map under the class key so that any further
    # request for the same class is immediately resolved
    NODE_METHOD_CACHE[cls] = map
    return map


class Visitor(object):
    """
    The visitor class for the template engine. This is the abstract
    implementation and more concrete implementations may exists if
    the default behavior should be replaced.
    """

    owner = None
    """ The owner object for the visitor, this object may be used
    for external state changes that are processed upon visit
    (eg: inheritance processing) """

    node_method_map = {}
    """ The node method map structure that is going to be used
    by the visitor decorators for proper polymorphic visit """

    encoding = None
    """ The encoding used the file, this is a meta-information
    value that is not going to be used for any practical usage """

    base_path = None
    """ The base path to be used for the resolution of template
    files that are going to be either included or extended, this
    value is not mandatory and in case it's not defined only
    the relative path resolution strategy is going to be used """

    file_path = None
    """ The path to the file that generated the abstract syntax
    tree that is going to be visited by this visitor """

    template_engine = None
    """ The reference template engine system object that handles
    and manages this visitor (owner object) """

    variable_encoding = None
    """ The variable encoding value this is the name of the encoding
    that is going to be used for the output of their string value
    to the currently set string buffer """

    strict_mode = False
    """ The strict mode, that controls if the processing should
    be done in a strict way meaning that exceptions should be
    raised whenever an unexpected value is received/processed """

    visit_childs = True
    """ The visit childs flag, that controls if the children
    of a note should also be visited when a node is visited """

    global_map = {}
    """ The global map, containing the global (interpreter wide)
    names that are going to be used at the time of template
    evaluation note that this map may be shared among the
    sub templates in both the extension and inclusion operations """

    string_buffer = None
    """ Buffer to where the complete set of output data will be
    written as part of the processing of the template, this object
    should comply with the typical file orations interface so that
    no runtime problems occur during the template processing """

    process_methods_list = []
    """ The list of process methods (tuples) that contains the
    complete set of extra methods that are going to be used in
    the processing of "complex" nodes """

    locale_bundles = []
    """ The list that contains the various bundles to be searched for
    localization, the order set is going to be the priority for template
    value resolution (from first to last list element) """

    def __init__(self, owner=None, string_buffer=None):
        """
        Constructor of the class.

        :type owner: Template
        :param owner: The owner object of the visitor, this object is
        expected to comply with the template interface as some of the
        visitor operations will change the object with that assumption.
        :type string_buffer: File
        :param string_buffer: The file like object that is going to be
        used for the underlying buffering of the template process. In
        case no value is provided the default string buffer object is used.
        """

        self.owner = owner
        self.node_method_map = {}
        self.visit_childs = True
        self.global_map = dict()
        self.string_buffer = string_buffer or colony.StringBuffer()
        self.process_methods_list = []
        self.locale_bundles = []
        self.filters = FILTERS
        self.extras = EXTRAS
        self.builtins = BUILTINS_EXTRAS
        self.process_map = dict()

        self.global_map["__builtins__"] = self.builtins
        self.update_node_method_map()

    def update_node_method_map(self):
        # retrieves both the node method map and the visit resolution
        # map for the class of the current instance, note that these
        # structures are static for a class and so they are built only
        # once and then shared by every instance of it
        cls = self.__class__
        self.node_method_map = node_method_map(cls)
        self.visit_map = VISIT_CACHE.setdefault(cls, dict())

    def attach_process_method(self, method_name, method):
        # creates the process method instance, that is attached to
        # the general visitor class and sets it the current instance
        method_instance = types.MethodType(method, self)
        setattr(self, method_name, method_instance)

        # invalidates the process method cache as a new method may be
        # shadowing a previously resolved (and cached) one
        self.process_map.clear()

        # creates the process method tuple that contains both the
        # name of the method and the method reference and adds the
        # tuple to the list of process method, this is going to be
        # used in the initial stage of the template creation
        process_method_tuple = (method_name, method)
        self.process_methods_list.append(process_method_tuple)

    def get_global_map(self):
        return self.global_map

    def write(self, data, *args, **kwargs):
        if not self.string_buffer:
            return
        is_unicode = type(data) == colony.legacy.UNICODE
        if is_unicode and self.encoding:
            data = data.encode(self.encoding)
        self.string_buffer.write(data, *args, **kwargs)

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

    def add_filter(self, name, filter):
        # copies the currently set filters map before changing it, this is
        # required as the default one is shared between the various visitor
        # instances (copy on write strategy)
        self.filters = dict(self.filters)
        self.filters[name] = filter

    def get_encoding(self):
        return self.encoding

    def set_encoding(self, encoding):
        self.encoding = encoding

    def get_base_path(self):
        return self.base_path

    def set_base_path(self, base_path):
        self.base_path = base_path

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

    def visit(self, node):
        # tries to resolve the visit method for the class of the node
        # that is going to be visited using the class level cache, in
        # case it's not there the "slow" resolution is performed
        node_class = node.__class__
        visit_map = self.visit_map
        if node_class in visit_map:
            method = visit_map[node_class]
        else:
            method = self._resolve_visit(node_class)

        # in case no method was found for the node class the fallback
        # operation is performed, notifying about the unknown node
        if method == None:
            return self.visit_default(node)

        # runs the complete set of visit operations, note that both the
        # before and after visit calls are performed so that the proper
        # "notification" of the visit exists (as expected)
        self.before_visit(node)
        method(self, node)
        self.after_visit(node)

    def visit_default(self, node):
        print("unrecognized element node of type " + node.__class__.__name__)

    def _resolve_visit(self, node_class):
        """
        Resolves the visit method that should be used for the provided
        AST node class, walking the class hierarchy from the bottom to
        the top so that the most specific method is used.

        The result of the resolution is stored in the class level cache
        so that this (expensive) operation is only run once per class.

        :type node_class: Class
        :param node_class: The AST node class for which the visit method
        is going to be resolved.
        :rtype: Method
        :return: The visit method for the provided node class or an
        invalid value in case no method is able to handle it.
        """

        # iterates over the complete class hierarchy for the provided
        # node class (from bottom to top) so that the best match for
        # the visit operation is found and then cached
        node_method_map = self.node_method_map
        method = None
        for mro_item in node_class.mro():
            if not mro_item in node_method_map:
                continue
            method = node_method_map[mro_item]
            break

        # stores the resolved method (that may be invalid) under the node
        # class key so that any further visit is immediately resolved
        self.visit_map[node_class] = method
        return method

    def before_visit(self, node):
        self.visit_childs = True

    def after_visit(self, node):
        pass

    @colony.visit(ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @colony.visit(ast.RootNode)
    def visit_root_node(self, node):
        pass

    @colony.visit(ast.LiteralNode)
    def visit_literal_node(self, node):
        # retrieves the match value from the current node's value, note
        # that this value is already escaped (at parse time) and so it
        # may be written directly into the current string buffer
        self.write(node.value.value)

    @colony.visit(ast.MatchNode)
    def visit_match_node(self, node):
        pass

    @colony.visit(ast.SingleNode)
    def visit_single_node(self, node):
        pass

    @colony.visit(ast.CompositeNode)
    def visit_composite_node(self, node):
        pass

    def process_accept(self, node, name):
        # tries to retrieve the process method for the requested tag name
        # from the instance level cache, avoiding the (repeated) dynamic
        # resolution of the method for every single node visit
        process_map = self.process_map
        if name in process_map:
            process_method = process_map[name]
        else:
            process_method = getattr(self, "process_" + name, None)
            process_map[name] = process_method

        # in case the process method is not defined, raises an exception
        # indicating tha the tag is not supported
        if process_method == None:
            raise exceptions.InvalidTagName(name)

        # runs the process method with the current node as the argument
        # so that the proper tag operation is performed
        process_method(node)

    def process_out(self, node):
        """
        Processes the out none node, that outputs a processed
        data to the current processing context/buffer.

        In case the resolved value is invalid/none the resulting
        data is printed as an empty string.

        :type node: SingleNode
        :param node: The single node to be processed as out none.
        """

        # retrieves the attributes map for the current node that
        # is going to be used to process the data that is going
        # to be printed to the current context
        attributes = node.get_attributes()

        # verifies if only the minimum set of attributes is defined for
        # the node, if that's the case (by far the most common one) the
        # simplified processing of the node is performed instead
        simple = node.simple
        if simple == None:
            simple = self._is_simple(attributes)
            node.simple = simple
        if simple:
            return self._process_out_simple(attributes)

        # retrieves the localization value, this is going to be used
        # for a lot of sub-operation in retrieval and must be gathered
        # before the rest of the attributes for such purpose
        localize = attributes.get("localize", None)
        localize = self.get_boolean_value(localize, True)

        # retrieves the complete set of attributes from the attributes
        # defined for the current node, it's an extensive list and
        # the range of usage and data types are vast
        value = attributes["value"]
        value = self.get_value(value, meta=attributes, localize=localize)
        prefix = attributes.get("prefix", None)
        prefix = self.get_value(prefix, localize=localize, default="")
        format = attributes.get("format", None)
        format = self.get_value(format)
        quote = attributes.get("quote", None)
        quote = self.get_boolean_value(quote)
        xml_escape = attributes.get("xml_escape", None)
        xml_escape = self.get_boolean_value(xml_escape)
        xml_quote = attributes.get("xml_quote", None)
        xml_quote = self.get_boolean_value(xml_quote, xml_escape)
        newline_convert = attributes.get("newline_convert", None)
        newline_convert = self.get_boolean_value(newline_convert)
        convert = attributes.get("convert", None)
        convert = self.get_value(convert)
        allow_empty = attributes.get("allow_empty", None)
        allow_empty = self.get_value(allow_empty, default=True)
        default = attributes.get("default", None)
        default = self.get_value(default, localize=localize)
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
        if value in invalid_values:
            value = default

        # in case the attribute value value is invalid and the default
        # value is not set (no need to show the value) must return
        # immediately nothing will be printed
        if value in invalid_values and default == None:
            return

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
        is_unicode = type(value) == colony.legacy.UNICODE
        value = is_unicode and value or colony.legacy.UNICODE(value)

        # in case the attribute convert value is set
        if convert:
            # retrieves the conversion method for the string
            # value representing it and uses it to convert
            # the attribute value to the target encoding
            conversion_method = CONVERSION_MAP.get(convert, None)
            value = conversion_method(value) if conversion_method else value

        # in case the attribute quote value is set must quote the
        # value using the provided colony utility
        if quote:
            value = value.encode("utf-8")
            value = colony.quote(value, safe="/")

        # runs the final transformation on the value according to
        # the provided flags (custom operations)
        if xml_escape:
            value = xml.sax.saxutils.escape(value)
        if xml_quote:
            value = value.replace('"', "&quot;")
        if newline_convert:
            value = value.replace("\n", "<br/>")

        # runs the final appending of the prefix value to the value
        value = prefix + value

        # in case the variable encoding is defined must re-encode the
        # variable according to the current variable encoding, note that
        # this is the last operation to be performed as the resulting
        # value is no longer a valid (unicode) string value
        if self.variable_encoding:
            value = value.encode(self.variable_encoding)

        # writes the final string/unicode value to the buffer
        self.write(value)

    def process_set(self, node):
        return self.process_var(node)

    def process_var(self, node):
        """
        Processes the var node, this is the operation that
        allows the attribute of a value in the current context
        the required attributes are the item (literal) and the
        value.

        :type node: Node
        :param node: The single node to be processed as var.
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
        # value otherwise the index start at one
        if not start_index == None:
            index = int(start_index)
        else:
            index = 1

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
                raise exceptions.VariableNotIterable(
                    "value not iterable: " + from_value
                )

            # otherwise avoids exception in case the object
            # is not an invalid one (possible problems) by
            # "casting" the attribute from value to a list it
            # will create an iterable object that may be used
            elif not iterable == None:
                iterable = [iterable]

            # otherwise in case the object is considered invalid
            # the best match for the cast is an empty list
            else:
                iterable = []

        # saves the previous values of the loop related globals so that
        # they may be restored at the end of the iteration, this is what
        # allows the proper nesting of loop operations
        global_map = self.global_map
        previous_loop = global_map.get("loop", None)
        previous_first = global_map.get("is_first", None)
        previous_last = global_map.get("is_last", None)

        # creates the map that holds the loop related values for the
        # current loop operation, this map is created only once as it's
        # going to be updated for each one of the iterations
        loop = dict()
        global_map["loop"] = loop

        # sets the various global wide values relates with the
        # current loop operation that is going to be performed
        # this values are not related with each iteration
        length = len(iterable)
        loop["length"] = length
        loop["cycle"] = self._loop_cycle

        # verifies if the iterable currently in use is of type
        # map (dictionary) this will condition the way the loop
        # part of the operation will be performed
        is_map = colony.is_dictionary(iterable)

        # in case the current structure is not map based and the
        # item value naming is not defined, sets the key reference
        # as the item value and unsets both the key and index
        # reference (non map iteration requires value assign)
        if not is_map and not item:
            item = key_ref
            key_ref = None
            index_ref = None

        # creates the ordinal value that is going to be used for the
        # detection of both the first and the last iterations, note that
        # this value is independent from the (visible) index one as that
        # one may start at any value (start index attribute)
        ordinal = 1

        # iterates over the complete set of elements in the iterable,
        # note that the value contained in the item will not be the
        # same if the iterable is a map or if it is a sequence
        try:
            for element in iterable:
                is_first = ordinal == 1
                is_last = ordinal == length

                loop["index"] = index
                loop["index0"] = index - 1
                loop["first"] = is_first
                loop["last"] = is_last
                global_map["is_first"] = is_first
                global_map["is_last"] = is_last

                key = element if is_map else index
                value = iterable[element] if is_map else element

                if item:
                    global_map[item] = value
                if index_ref:
                    global_map[index_ref] = index
                if key_ref:
                    global_map[key_ref] = key

                if self.visit_childs:
                    for child in node.children:
                        child.accept(self)

                ordinal += 1
                index += 1

        # restores the previous values of the loop related globals so that
        # an outer loop is not affected by the one that has just finished
        finally:
            global_map["loop"] = previous_loop
            global_map["is_first"] = previous_first
            global_map["is_last"] = previous_last

    def process_if(self, node):
        # evaluates the current node comparison, this is the default
        # acceptance behavior for all the nodes that do not require
        # an extra evaluation process (evaluation nodes)
        accept_node = self._evaluate_comparison_node(node)

        # in case the visit child flag is not set the method must
        # return immediately as there's nothing remaining to be done
        if not self.visit_childs:
            return

        # iterates over all the child nodes for the current if node
        # to evaluate or process them according to their type
        for child in node.children:
            # validates the accept node, so that if the node is "eval"
            # the evaluation is done otherwise the default evaluation
            # result for the if node is applied
            accept_node = self._validate_accept_node(child, accept_node)

            # in case the accept node is set to invalid
            # the evaluation is over (nothing to be done)
            if accept_node == None:
                return

            # in case the accept node flag is set accepts the node
            # child node as it is considered to be valid
            accept_node and child.accept(self)

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
            if current_index == values_length - 1:
                current_index = 0
            else:
                current_index += 1
        else:
            current_index = 0

        node.current_index = current_index
        current_value = values[current_index]
        self.write(current_value)

    def process_count(self, node):
        # retrieves the current nodes's attributes and gathers the value
        # field from the dictionary retrieving then it's value
        attributes = node.get_attributes()
        value = attributes["value"]
        value = self.get_value(value)

        # in case the retrieved value is invalid the length of it is considered
        # to be zero otherwise measures its size and sets accordingly
        if value == None:
            value_length = 0
        else:
            value_length = len(value)

        # checks if the attribute value length contains a unicode string
        # in such case there's no need to re-decode it
        is_unicode = type(value_length) == colony.legacy.UNICODE
        value_length = (
            is_unicode and value_length or colony.legacy.UNICODE(value_length)
        )

        # in case the variable encoding value is defined encodes the string
        # value using the currently defined encoding (as expected) and then
        # writes the resulting string value to the current buffer
        if self.variable_encoding:
            value_length = value_length.encode(self.variable_encoding)
        self.write(value_length)

    def process_include(self, node):
        # in case the current include node already contains children nodes it
        # is considered to be processed and so there's no need to re-process
        # again the same structure (time to visit the children nodes instead)
        if node.children:
            children = node.children if self.visit_childs else ()
            for child in children:
                child.accept(self)
            return

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

        # parses the file retrieving the template file structure, note
        # that any path existence validation will be done at this stage,
        # after this loading operation the visitor is loaded into the
        # template engine and only the extends nodes are accepted, this
        # is going to create a partial abstract syntax tree that is going
        # to be appended to the current node as subtree, the contents of
        # it are generated by the (owner) visitor afterwards
        template_file = self._get_template(node, file_path)
        template_file.set_global_map(self.global_map)
        template_file.load_visitor()
        template_file.root_node.accept_extends(template_file.visitor)

        # updates the current node's children sequence with the complete
        # set of root children of the processed file (propagation) and
        # then sets the parent node of the complete set of children with
        # the current include node (parent reference update)
        node.children = template_file.root_node.children
        for child in node.children:
            child.parent = node

        # runs the visit operation in the complete set of child nodes
        # so that they get update with the proper include files if they
        # have ones (normal recursive step operation)
        children = node.children if self.visit_childs else ()
        for child in children:
            child.accept(self)

    def process_extends(self, node):
        # retrieves the current node's attributes and uses them to unpack
        # the information for the template to be extended
        attributes = node.get_attributes()
        file = attributes.get("file", None)
        file = self.get_literal_value(file)
        file_value = attributes.get("file_value", None)
        file_value = self.get_value(file_value)

        # retrieves the initial file path value from either the file
        # or the file value attributes (whatever is defined)
        file_path = file or file_value

        # parses the file retrieving the template file structure, note
        # that any path existence validation will be done at this stage,
        # after this loading operation the visitor is loaded into the
        # template engine and only the extends nodes of the parent are
        # accepted, this resolves the complete inheritance chain without
        # generating any contents (they are generated by the owner)
        template_file = self._get_template(node, file_path)
        template_file.set_global_map(self.global_map)
        template_file.load_visitor()
        template_file.root_node.accept_extends(template_file.visitor)
        template_file.index_nodes()

        # "transfers" the children nodes of the super template file to
        # the current visitor owner root node (base inheritance)
        self.owner.root_node.children = template_file.root_node.children
        for child in self.owner.root_node.children:
            child.parent = self.owner.root_node

        # retrieves both the current template owner nodes map and the nodes
        # map of the "super" template file as there structures are going
        # to be used for the replacing of the various blocks
        nodes = self.owner.nodes
        super_nodes = template_file.nodes

        # iterates over the complete set of globally index nodes to try to find
        # the ones that are defined and switch them so that the most specific
        # (concrete templates) are defined and reference the most abstract ones
        for name, node in colony.legacy.items(nodes):
            # tries to retrieve a super node for the current block name in
            # iteration and in case there's one switches the current node
            # with the previous one, otherwise adds the current node as a
            # child to the root node (fallback operation) then updates the
            # global nodes map with the current node
            super_node = super_nodes.get(name, None)
            if super_node:
                super_node.switch(node)
            else:
                self.owner.root_node.add_child(node)
            super_nodes[name] = node

        # sets the global nodes map of the super node (already updated) as
        # the nodes map of the visitor's owner
        self.owner.nodes = super_nodes

    def process_block(self, node):
        def super():
            if not node.super:
                return
            node.super.accept(self)

        self.set_global("super", super)

        if self.visit_childs:
            for child in node.children:
                child.accept(self)

    def process_uuid(self, node):
        # creates a new uuid value and converts it into a string
        # value to be used in the string buffer
        uuid_value = uuid.uuid4()
        uuid_string_value = str(uuid_value)
        self.write(uuid_string_value)

    def process_year(self, node):
        # retrieves the current date time formats it according to
        # the default year format and writes the value to buffer
        current_date_time = datetime.datetime.now()
        year_value = current_date_time.strftime("%Y")
        self.write(year_value)

    def process_date(self, node):
        attributes = node.get_attributes()
        format = attributes.get("format", None)
        format = self.get_literal_value(format, default=DEFAULT_DATE_FORMAT)
        format = str(format)

        current_date_time = datetime.datetime.now()
        date_value = current_date_time.strftime(format)
        self.write(date_value)

    def process_time(self, node):
        attributes = node.get_attributes()
        format = attributes.get("format", None)
        format = self.get_literal_value(format, default=DEFAULT_TIME_FORMAT)
        format = str(format)

        current_date_time = datetime.datetime.now()
        time_value = current_date_time.strftime(format)
        self.write(time_value)

    def process_datetime(self, node):
        attributes = node.get_attributes()
        format = attributes.get("format", None)
        format = self.get_literal_value(format, default=DEFAULT_DATE_TIME_FORMAT)
        format = str(format)

        current_date_time = datetime.datetime.now()
        date_time_value = current_date_time.strftime(format)
        self.write(date_time_value)

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
            if value:
                self.write(value)
            return

        format = str(format)
        value_format = value.strftime(format)
        self.write(value_format)

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
            if value:
                self.write(value)
            return

        format = str(format)
        date_time = datetime.datetime.utcfromtimestamp(value)
        value_format = date_time.strftime(format)
        self.write(value_format)

    def process_timestamp(self, node):
        attributes = node.get_attributes()
        localize = attributes.get("localize", None)
        localize = self.get_boolean_value(localize, True)
        value = attributes.get("value", None)
        value = self.get_value(value, default=datetime.datetime.now())
        default = attributes.get("default", None)
        default = self.get_value(default, localize=localize)

        if value == None:
            value = default if default else value
            if value:
                self.write(value)
            return

        time_tuple = value.utctimetuple()
        timestamp = calendar.timegm(time_tuple)
        timestamp_s = str(timestamp)
        self.write(timestamp_s)

    def get_value(self, attribute, meta=None, localize=False, default=None):
        """
        Retrieves the value (variable or literal) of the given
        value. The process of retrieving the variable value is
        iterative and may consume some time in resolution.

        An optional localize flag may be set of the value should
        be localized using the current local bundles.

        :type attribute: Dictionary
        :param attribute: A map describing the attribute structure.
        :type meta: Dictionary
        :param meta: The map containing the meta-information related with
        the attribute in question (eg: XML escaping).
        :type localize: bool
        :param localize: If the value must be localized using the currently
        available locale bundles.
        :type default: Object
        :param default: The default (fallback) value to be returned if
        no valid attribute is provided or in case it is invalid.
        :rtype: Object
        :return: The resolved attribute value.
        """

        # in case the passed attribute is not valid the default must
        # be returned immediately as no resolution is possible, this
        # is the default and expected behavior (fallback procedure)
        if not attribute:
            return default

        # retrieves the (processed) value of the attribute and then the
        # base name and filters sequence, note that these values are
        # computed only once and then stored in the attribute structure
        # so that any further resolution of it is immediate
        value = attribute["value"]
        filters = attribute.get("filters", None)
        if filters == None:
            base, filters = split_filters(attribute["original"])
            attribute["base"] = base
            attribute["filters"] = filters

        # in case the attribute value is of type variable, must be
        # properly handled (stripping the value from extra lines)
        if attribute["type"] == "variable":
            # retrieves the pre-computed base name of the attribute, this
            # is the name of the variable stripped from any filter
            variable_name = attribute["base"]

            # in case the variable name is none sets the final value
            # with the invalid value as that's requested by the template
            if variable_name == "None":
                value = None

            # otherwise the value must be processed according to the currently
            # defined template rules (may required method invocation)
            else:
                # resolves the variable name using the multiple parts
                # approach so that the final value is retrieved according
                # to the current state of the template engine
                value = self.resolve_many(variable_name)

        # resolves the current "variable" value, trying to
        # localize it using the current locale bundles only
        # do this in case the localize flag is set
        value = self._resolve_locale(value) if localize else value

        # iterates over the complete set of filter definition to
        # resolve the final value according to the filter
        for filter in filters:
            value = self.resolve_many(
                filter, value, meta, self, global_map=self.filters
            )

        # returns the processed value to the caller method, this is the
        # considered to be the value for the requested attribute
        return value

    def get_literal_value(self, attribute, default=None):
        if attribute == None:
            return default
        return attribute["value"]

    def get_boolean_value(self, attribute, default=False):
        # in case the provided attribute structure is not
        # defined the boolean value is assumed to be the
        # provided default value (as defined is specification)
        if attribute == None:
            return default

        # verifies if the attribute is in itself a boolean (allows
        # polymorphic values) if that's the case returns the value
        # immediately as it's the one that is expected
        if type(attribute) == bool:
            return attribute

        # retrieves the literal value of the provided
        # attribute, retrieving then the data type for it
        value = attribute["value"]
        value_type = type(value)

        # in case the "literal" value is a boolean returns the same
        # value as the result, otherwise raises an exception indicating
        # the problem with the processing of the boolean value
        if value_type == bool:
            return value
        raise exceptions.InvalidBooleanValue("invalid boolean " + value)

    def resolve_many(self, name, *args, **kwargs):
        # tries to retrieve the sequence of partial names for the requested
        # (complete) variable name from the global cache, as the splitting
        # of a name is a pure operation its result may be safely re-used
        names = NAMES_CACHE.get(name, None)
        if names == None:
            names = tuple(match.group() for match in NAMES_REGEX.finditer(name))
            if len(NAMES_CACHE) > CACHE_LIMIT:
                NAMES_CACHE.clear()
            NAMES_CACHE[name] = names

        # sets the initial value of the resolution process as the current
        # global map and then starts the resolution running it for the
        # complete set of "partial" attribute names (iterative resolution),
        # note that the resolution is guarded in the same way as the one
        # of the resolve method (inline for performance reasons)
        value = kwargs.pop("global_map", self.global_map)
        try:
            for name in names:
                value = self._resolve(value, name, *args, **kwargs)
        except exceptions.UndefinedVariable:
            if self.strict_mode:
                raise
            value = None

        # return the final resolved value, this value should be a result
        # of the iteration around the various partial names
        return value

    def resolve(self, value, name, *args, **kwargs):
        try:
            result = self._resolve(value, name, *args, **kwargs)
        except exceptions.UndefinedVariable:
            if self.strict_mode:
                raise
            else:
                result = None
        return result

    def _resolve(self, value, name, *args, **kwargs):
        # saves the original attribute name under the original variable
        # as it's going to be used latter for some processing operations
        name_o = name

        # filters the variable name so that if it's a complete method
        # call the arguments part is removed, this way only the name of
        # the attribute is guaranteed
        index = name.find("(")
        if index > -1:
            name = name[:index]

        # verifies if the base value refers a dictionary, if that's the
        # case a normal get operation will be performed
        is_dictionary = True if type(value) == dict else colony.is_dictionary(value)

        # in case the variable is of type dictionary, the normal recursive
        # iteration step will be executed
        if is_dictionary:
            # verifies if the name is present in the map itself and only in
            # case it's not there falls back to the builtins, note that the
            # builtins are only retrieved when they are required
            if name in value:
                result = value[name]
            else:
                builtins = value.get("__builtins__", None)
                if builtins and name in builtins:
                    result = builtins[name]
                else:
                    raise exceptions.UndefinedVariable(
                        "variable is not defined: " + name
                    )

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
                if name:
                    kwargs[name] = value
                else:
                    args.append(value)

            # runs the calling of the method/function/callable with the complete set
            # of arguments, this should include both the default ones and the ones
            # parsed from the string (as expected by specification)
            result = result(*args, **kwargs)

        # retrieves the current results's class and in case the class is of
        # type file reference the contents should be read (the file is closed properly)
        # and set as the current variable (as the new result of it)
        result_class = getattr(result, "__class__", None)
        if result_class == colony.FileReference:
            result = result.read_all()

        # returns the final resolved result value to the caller method, no extra
        # processing should be required for this values is resolved
        return result

    def resolve_args(self, name):
        # tries to retrieve the already processed sequence of arguments for
        # the provided name, as the parsing of the arguments depends only
        # on the name itself its result may be safely re-used
        arguments_c = ARGUMENTS_CACHE.get(name, None)
        if not arguments_c == None:
            return arguments_c

        # runs the "effective" parsing of the arguments for the name and
        # then stores the result in the cache so that any further call
        # for the same name is resolved without any extra processing
        arguments_t = self._resolve_args(name)
        if len(ARGUMENTS_CACHE) > CACHE_LIMIT:
            ARGUMENTS_CACHE.clear()
        ARGUMENTS_CACHE[name] = arguments_t
        return arguments_t

    def _resolve_args(self, name):
        # tries to match the complete variable name split against
        # the arguments regular expression, to find out if the call
        # is of type simple or complex (arguments present)
        arguments_match = FUNCTION_ARGUMENTS_REGEX.search(name)

        # in case there is no valid arguments match, no processing
        # of arguments will occur and an empty sequence is returned
        # immediately as there's nothing remaining to be done
        if not arguments_match:
            return ()

        # retrieves the complete group match from the arguments
        # match and removes the calling parentheses
        arguments_s = arguments_match.group()
        arguments_s = arguments_s[1:-1]

        # splits the arguments string into the various arguments
        # names and then treats them, converting them into the
        # normal form, note that the split operation is aware of
        # the quoted sequences (avoids breaking string literals)
        arguments = split_arguments(arguments_s)
        arguments = [argument.strip() for argument in arguments]

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
            if len(parts) == 2:
                name, argument = parts
            else:
                (argument,) = parts
                name = None

            # in case the argument or the name are defined and valid strips
            # their values to avoid any extra space character in them
            if argument:
                argument = argument.strip()
            if name:
                name = name.strip()

            # saves the original value under the original value so that
            # it may be used latter for the creation of the argument
            original = argument

            # retrieves the first character of the argument to be used
            # to try to guess the argument type
            first_char = argument[0]

            # checks the type of the argument, using the first character for
            # so, then sets the literal flag in case the value is a number or
            # a string (literal types)
            is_string = first_char == "'" or first_char == '"'
            is_number = ord(first_char) > 0x2F and ord(first_char) < 0x3A
            is_bool = argument in ("True", "False")
            is_literal = is_string or is_number or is_bool
            _type = "literal" if is_literal else "variable"

            # in case the current argument is a literal some of its tokens
            # must be replaced to provide proper compatibility
            if not is_literal:
                argument = argument.replace(":", ".")

            # retrieves the correct value taking into account the various
            # type based flags
            if is_string:
                value = argument[1:-1]
            elif is_number:
                value = int(argument)
            elif is_bool:
                value = argument == "True"
            else:
                value = argument

            # creates the argument type map with both the type and the value
            # for the argument then adds it to the list of argument types
            argument_t = dict(type=_type, value=value, original=original, name=name)
            arguments_t.append(argument_t)

        # returns the complete list of processed arguments, this is a list of
        # argument dictionary values that are meant to be latter recursively
        # resolved to obtain the real/final argument values
        return arguments_t

    def _is_simple(self, attributes):
        """
        Verifies if the provided attributes map defines only the minimum
        set of attributes required for an out operation, meaning that no
        extra transformation of the value is going to be required.

        :type attributes: Dictionary
        :param attributes: The map containing the attributes defined for
        the node that is going to be verified.
        :rtype: bool
        :return: If the provided attributes allow the simplified (and
        faster) processing of the out operation.
        """

        # in case there are more attributes than the value and the auto
        # escaping ones the node is not considered to be a simple one
        if not len(attributes) == 2:
            return False

        # the auto escaping attribute must be a "plain" boolean value as
        # otherwise its resolution would be required
        if not type(attributes.get("xml_escape", None)) == bool:
            return False

        # retrieves the value attribute and in case it's not defined the
        # node is not considered to be a simple one
        value = attributes.get("value", None)
        if not value:
            return False

        # computes (and stores) the base name and the filters for the value
        # attribute, as the presence of filters requires the complete
        # processing of the node (the filters may change the attributes)
        filters = value.get("filters", None)
        if filters == None:
            base, filters = split_filters(value["original"])
            value["base"] = base
            value["filters"] = filters
        return not filters

    def _process_out_simple(self, attributes):
        """
        Processes the out operation for a node that defines only the
        minimum set of attributes, this is the most common scenario and
        so it's handled in an optimized fashion.

        :type attributes: Dictionary
        :param attributes: The map containing the attributes defined for
        the node that is going to be processed.
        """

        # resolves the value of the node localizing it (the default
        # behavior) and in case it's an invalid one returns immediately
        # as there's nothing to be printed to the current buffer
        value = self.get_value(attributes["value"], localize=True)
        if value == None:
            return

        # serializes the value into the correct visual representation
        # and makes sure that a valid unicode string is used
        value = self._serialize_value(value)
        if not type(value) == colony.legacy.UNICODE:
            value = colony.legacy.UNICODE(value)

        # runs the final transformation on the value according to the
        # auto escaping mode that is defined for the node
        if attributes["xml_escape"]:
            value = xml.sax.saxutils.escape(value)
            value = value.replace('"', "&quot;")

        # in case the variable encoding is defined must re-encode the
        # variable according to the current variable encoding
        if self.variable_encoding:
            value = value.encode(self.variable_encoding)

        # writes the final string/unicode value to the buffer
        self.write(value)

    def _get_template(self, node, file_path):
        """
        Retrieves and loads a (partial) template file under the ownership
        of the provided node and for the requested file path.

        This operations takes into account the current system state to
        run the loading process of the template.

        :type node: Node
        :param node: The node to be used as owner of this operation, it's
        going to be used in case the operation fails.
        :type file_path: String
        :param file_paht: Absolute or relative path to the template file
        that is going to be loaded/retrieved.
        :rtype: Template
        :return: The loaded template file, resulting from the creation
        of the file path according to the local rules.
        """

        # in case the file path was not able to be resolved an
        # exception must be raised indicating the undefined reference
        # to the template to be included
        if not file_path:
            # retrieves the node type and raises an exception with
            # the value that was just retrieved
            node_type = node.get_type()
            raise exceptions.UndefinedReference(node_type)

        # in case the provided file path is not absolute a resolution
        # process must be started to try to find the final template
        # path that is going to be retrieved, this is done using both
        # the current template path (relative inclusion) and the defined
        # base path (in case it's defined)
        if not os.path.isabs(file_path):
            file_base = os.path.dirname(self.file_path)
            for base_path in (file_base, self.base_path):
                if base_path == None:
                    continue
                _file_path = os.path.join(base_path, file_path)
                if not os.path.exists(_file_path):
                    continue
                file_path = _file_path
                break

        # normalizes the resolved template path so that it becomes compliant
        # with the current operative system "rules" and then runs the parsing
        # of the template file so that a proper template structure is returned
        # as the result of this method (as defined in specification)
        file_path = os.path.normpath(file_path)
        return self.template_engine.parse_file_path(
            file_path,
            base_path=self.base_path,
            encoding=self.encoding,
            process_methods_list=self.process_methods_list,
            locale_bundles=self.locale_bundles,
        )

    def _validate_accept_node(self, node, accept_node):
        """
        Validates the accept node flag in accordance with the if
        specification.

        :type node: Node
        :param node: The child node to be evaluated, this may either
        be a node that is able to be evaluated or not.
        :type accept_node: bool
        :param accept_node: The accept node flag value, this is
        the fallback value for nodes that are not able (or required)
        to be evaluated for acceptance.
        :rtype: bool
        :return: The new value for the accept node flag.
        """

        # verifies if the current node is mean to be evaluated and
        # if that's not the case returns the passed fallback value
        eval_node = isinstance(node, ast.MatchNode) or isinstance(node, ast.EvalNode)
        if not eval_node:
            return accept_node

        # retrieves the value type for the current node and uses
        # this value to decide to either process it or not
        type = node.get_type()
        if type in ("else", "elif", "endif"):
            # in case the accept node
            # flag is already set (the result is
            # already been evaluated positively)
            if accept_node:
                return None

            # in case the type is plain, the node should always
            # be accepted, and no extra evaluation process is
            # performed (node is accepted by default)
            if type in ("else", "endif"):
                accept_node = True

            # in case the type is elif, the node should be
            # accepted in case of positive evaluation
            elif type == "elif":
                result = self._evaluate_comparison_node(node)
                accept_node = result

        # returns the accept node final result so that the caller
        # may decide to either visit the node or not
        return accept_node

    def _evaluate_comparison_node(self, node):
        """
        Evaluates the given (comparison) node, retrieving
        the result of the evaluation.

        :type node: Node
        :param node: The comparison node to be evaluated.
        :rtype: bool
        :return: The result of the evaluation of the
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
        # and then evaluates the item against the value, note that the
        # result is normalized into a boolean value as the invalid value
        # is used by the caller method as the "stop" sentinel and so it
        # may not be used to represent a negative evaluation
        comparison = COMPARISION_FUNCTIONS.get(operator, None)
        result = comparison(item, value) if comparison else item
        return True if result else False

    def _escape_literal(self, literal_value):
        """
        Escapes the given literal value.
        Allow the template engine to skip interpretation
        of template tags.

        :type literal_value: String
        :param literal_value: The literal value to be escaped.
        :rtype: String
        :return: The escaped literal value
        """

        # escapes the literal value and returns it
        return escape_literal(literal_value)

    def _resolve_locale(self, value):
        """
        Resolves the given value using the currently available
        locale bundles to archive the resolution of the value.

        The resolution of the value is only possible to string
        values, although no exception is raises otherwise, the
        method fails silently.

        :type value: Object
        :param value: The value to be localized, it may be any
        type of data although only string are localizable.
        :rtype: String
        :return: The resolved locale value for the value or the
        original value in case no localization is possible.
        """

        # in case the value is invalid, not set or
        # an empty string no need to resolve it
        if not value:
            return value

        # in case there are no locale bundles defined there's no possible
        # resolution of the value, returns it immediately
        if not self.locale_bundles:
            return value

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
        if not type(value) in RESOLVABLE_TYPES:
            return value

        # iterates over all the present locale bundles
        # trying to find one that contains the locale
        # version of the value, in case none contains it
        # the value is literal and returned
        for locale_bundle in self.locale_bundles:
            # in case the value is not present in the locale
            # bundle no need to process it, continues the loop
            if not value in locale_bundle:
                continue

            # in case the value is present in the locale bundle
            # retrieves the locale version for the updating of
            # the reference value
            _value = locale_bundle[value]

            # in case the (private) replace method is present in
            # the value the substitution of the value must be done
            # through it otherwise the value reference is replaced
            # by the newly retrieved value
            if hasattr(value, "__replace__"):
                value.__replace__(_value)
            else:
                value = _value

            # breaks the loop because the first locale
            # is considered to be the highest priority
            break

        # returns the locale value or the literal value in case
        # no localization bundle is available for the value
        return value

    def _to_string(self, value):
        value = self._serialize_value(value)
        is_string = type(value) in colony.legacy.STRINGS
        if not is_string:
            value = colony.legacy.UNICODE(value)
        return value

    def _serialize_value(self, value):
        # retrieves the data type for the given value
        # to be checked against the various "checkings"
        value_type = type(value)

        # in case the current value is not "serializable"
        # it must be returned immediately
        if not value_type in SERIALIZABLE_TYPES:
            return value

        # in case the value value is a sequence it must be
        # "serializable" using the serialization of sequences
        # "mechanism" (the proper way of presenting the value)
        if value_type in SEQUENCE_TYPES:
            return self._serialize_sequence(value)

    def _serialize_sequence(self, value):
        # retrieves the data type for the given value
        # to be checked against the various "checkings"
        value_type = type(value)

        # in case the current value is not a sequence
        # it must be returned immediately
        if not value_type in SEQUENCE_TYPES:
            return value

        # creates the string buffer to hold the serialization values
        # and writes the initial list open token into it
        string_buffer = colony.StringBuffer()
        string_buffer.write(colony.legacy.u("["))

        # unsets the is first flag so that the comma separator
        # is not written in the first iteration
        is_first = True

        # iterates over all the list values to serialize them into
        # the correct representation
        for _value in value:
            # checks if this is the first iteration in case it's
            # not the comma separator is written to the string buffer
            if is_first:
                is_first = False
            else:
                string_buffer.write(colony.legacy.u(", "))

            # retrieves the type of the value before its serialization
            # (as it's the original type that conditions the writing
            # into the string buffer) and then serializes the value
            _value_type = type(_value)
            _value = self._serialize_value(_value)

            # checks if the value contains a unicode string
            # in such case there's no need to re-decode it
            is_unicode = _value_type == colony.legacy.UNICODE
            _value = is_unicode and _value or colony.legacy.UNICODE(_value)

            # in case the type of the current value is resolvable the
            # value must be written as an escaped string otherwise
            # the value is written literally
            if _value_type in RESOLVABLE_TYPES:
                string_buffer.write(
                    colony.legacy.u("'") + _value + colony.legacy.u("'")
                )
            else:
                string_buffer.write(_value)

        # writes the "final" end of list token into the string buffer
        # that holds the serialization of the sequence and then retrieves
        # the final value of the serialization from the string buffer
        string_buffer.write(colony.legacy.u("]"))
        value = string_buffer.get_value()

        # returns the final serialized value of the sequence
        return value

    def _get_serializer(self, name=None):
        # in case the serializers map is not defined triggers the
        # initial loading of the serializer, then in case the serializers
        # list is empty (or invalid) raises the no serializer error
        if SERIALIZERS_MAP == None:
            self._load_serializers()
        if not SERIALIZERS:
            raise exceptions.InvalidSerializer("no serializer available")

        # in case no (serializer) name is provided the first
        # (and preferred) serializer name is used then retrieves
        # the associated serializer object and in case it fails
        # raises an error
        name = name or SERIALIZERS[0]
        serializer = SERIALIZERS_MAP.get(name, None)
        if not serializer:
            raise exceptions.InvalidSerializer(
                "no serializer available for '%s'" % name
            )

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
            try:
                object = __import__(name)
            except ImportError:
                removal.append(name)
            else:
                SERIALIZERS_MAP[name] = object

        # iterates over all the (serializer) names to be
        # removed and removes them from the serializers list
        for name in removal:
            SERIALIZERS.remove(name)

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

    Attention should also be taken to the fact that using the eval
    function may create some multithreading lock issues where a
    thread gets blocked by other's gil (global interpreter lock).

    Overall this is also a slower evaluator of values as the eval
    function required the creation of new contexts (slow operations).
    """

    def get_value(self, attribute, meta=None, localize=False, default=None):
        # in case the passed attribute is not valid the default must
        # be returned immediately as no resolution is possible, this
        # is the default and expected behavior (fallback procedure)
        if not attribute:
            return default

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
        globals["__builtins__"] = self.builtins
        try:
            value = eval(name, globals, globals)
        except AttributeError:
            value = None
        except NameError:
            value = None
        except SyntaxError:
            value = None

        # verifies if the currently returned value is an accessor value and
        # in case it is retrieves the reference values as the value so that
        # the inner type of it as respected and the proxy is not used
        is_accessor = isinstance(value, util.Accessor)
        if is_accessor:
            value = value.ref

        # in case the returned value is callable it must be called
        # with no arguments to be able to retrieve the final value
        # for the current evaluation (simple callable)
        is_callable = hasattr(value, "__call__")
        if is_callable:
            value = value()

        # resolves the current "variable" value, trying to
        # localize it using the current locale bundles only
        # do this in case the localize flag is set
        value = self._resolve_locale(value) if localize else value

        # iterates over the complete set of filter definition to
        # resolve the final value according to the filters
        for filter in filters:
            value = self.resolve_many(
                filter, value, meta, self, global_map=self.filters
            )

        # returns the final value according to the eval based value
        # retrieval that uses the python interpreter for evaluation
        return value
