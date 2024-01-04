#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import re

import colony

from . import ast
from . import visitor
from . import exceptions

OUTPUT_REGEX_VALUE = "\{\{[^\}]*\}\}"
""" The regular expression value for the matching of the
output (print) operations, these are specialized nodes
that are only meant to print variable/literal values """

EVAL_REGEX_VALUE = "\{\%[^\}]*\%\}"
""" Regular expression that matched the complex evaluation
expression that allow the control flow of the template this
is the regular expression to be used under simple mode """

START_TAG_REGEX_VALUE = "\$\{[^\/\{}\{}][^\{\}][^\/\{}\{}]*\}"
""" The start tag regular expression value that should
match the starting tag of an expression """

END_TAG_REGEX_VALUE = "\$\{\/[^\{\}][^\/\{}\{}]*\}"
""" The end tag regular expression value """

SINGLE_TAG_REGEX_VALUE = "\$\{[^\{\}]*\/\}"
""" The single tag regular expression value """

ATTRIBUTE_REGEX_VALUE = "[a-zA-Z_]+=[a-zA-Z_][a-zA-Z0-9_\-\.\/\(\)\:,'\"\|]*"
""" The attribute regular expression value, this
regular expression value should be able to match
the complete set of attribute matches """

QUOTED_SINGLE_REGEX_VALUE = "[a-zA-Z_]+=['][^']+[']"
""" The attribute quoted single regular expression value """

QUOTED_DOUBLE_REGEX_VALUE = "[a-zA-Z_]+=[\"][^\"]+[\"]"
""" The attribute quoted double regular expression value """

FLOAT_REGEX_VALUE = "[a-zA-Z_]+=-?[0-9]+\.[0-9]*"
""" The attribute float regular expression value """

INTEGER_REGEX_VALUE = "[a-zA-Z_]+=-?[0-9]+"
""" The attribute integer regular expression value """

BOOL_TRUE_REGEX_VALUE = "[a-zA-Z_]+=True"
""" The attribute true boolean regular expression value """

BOOL_FALSE_REGEX_VALUE = "[a-zA-Z_]+=False"
""" The attribute false boolean regular expression value """

NONE_REGEX_VALUE = "[a-zA-Z_]+=None"
""" The attribute none regular expression value """

OUTPUT_VALUE = 1
""" The output value """

EVAL_VALUE = 2
""" The eval value """

START_VALUE = 3
""" The start value """

END_VALUE = 4
""" The end value """

SINGLE_VALUE = 5
""" The single value """

LITERAL_VALUE = 6
""" The literal value """

OUTPUT_REGEX = re.compile(OUTPUT_REGEX_VALUE)
""" Regular expression used to match the simple output
nodes it should be wide enough to handle all kinds of
variable values """

EVAL_REGEX = re.compile(EVAL_REGEX_VALUE)
""" Compiled regular expression used for the matching
of the evaluation expressions that allow the control of
flow contents for the template """

START_TAG_REGEX = re.compile(START_TAG_REGEX_VALUE)
""" The start tag regular expression, used to
match the start tag of a complete expression """

END_TAG_REGEX = re.compile(END_TAG_REGEX_VALUE)
""" The end tag regular expression """

SINGLE_TAG_REGEX = re.compile(SINGLE_TAG_REGEX_VALUE)
""" The single tag regular expression """

ATTRIBUTE_REGEX = re.compile(ATTRIBUTE_REGEX_VALUE)
""" The attribute regular expression """

ATTRIBUTE_LITERAL_REGEX = re.compile(
    "(?P<quoted_single>" + QUOTED_SINGLE_REGEX_VALUE + ")|" + \
    "(?P<quoted_double>" + QUOTED_DOUBLE_REGEX_VALUE + ")|" + \
    "(?P<float>" + FLOAT_REGEX_VALUE + ")|" + \
    "(?P<integer>" + INTEGER_REGEX_VALUE + ")|" + \
    "(?P<true_boolean>" + BOOL_TRUE_REGEX_VALUE + ")|" + \
    "(?P<false_boolean>" + BOOL_FALSE_REGEX_VALUE + ")|" + \
    "(?P<none>" + NONE_REGEX_VALUE + ")"
)
""" The literal regular expression that matches all the literals, there
are matching groups for each of the data types """

ESCAPE_EXTENSIONS = (
    ".xml",
    ".html",
    ".xhtml",
    ".liquid",
    ".xml.tpl",
    ".html.tpl",
    ".xhtml.tpl"
)
""" The sequence containing the various extensions
for which the autoescape mode will be enabled  by
default as expected by the end developer """

class TemplateEngine(colony.System):
    """
    The template engine class, responsible for the processing
    of template files according to the current template engine
    based file specification. Its internal working should be
    based on a visitor strategy.
    """

    def parse_file_path(
        self,
        file_path,
        base_path = None,
        encoding = None,
        process_methods_list = [],
        locale_bundles = None
    ):
        # verifies that the template file requested exists in the
        # file system in case it does not raises an exception
        if not os.path.exists(file_path):
            raise exceptions.RuntimeError("'%s' template file not found" % file_path)

        # opens the file for the reading of its contents
        # the complete data will be read
        file = open(file_path, "rb")

        try:
            # parses the file, retrieving the template file structure
            # that can be used for the execution of it
            template_file = self.parse_file(
                file,
                file_path = file_path,
                base_path = base_path,
                encoding = encoding,
                process_methods_list = process_methods_list,
                locale_bundles = locale_bundles
            )
        finally:
            # closes the file no further reading operations
            # will be done for the file (avoids leaks)
            file.close()

        # returns the template file
        return template_file

    def parse_file_path_variable_encoding(
        self,
        file_path,
        base_path = None,
        encoding = None,
        variable_encoding = None,
        process_methods_list = [],
        locale_bundles = None
    ):
        # parses the file for the given file path with the
        # given encoding retrieving the template file and
        # then sets the variable encoding in it returning
        # then the resulting template file object to the
        # caller method (as expected by definition)
        template_file = self.parse_file_path(
            file_path,
            base_path = base_path,
            encoding = encoding,
            process_methods_list = process_methods_list,
            locale_bundles = locale_bundles
        )
        template_file.set_variable_encoding(variable_encoding)
        return template_file

    def parse_file(
        self,
        file,
        file_path = None,
        base_path = None,
        encoding = None,
        process_methods_list = [],
        locale_bundles = None
    ):
        # in case the locale bundles list is not defined must
        # create a new list reference to handle it correctly
        if locale_bundles == None: locale_bundles = []

        # retrieves the proper extension of the template's file
        # path and then uses it to try to determine if the template
        # output operation should be automatically escaped
        extension = self._extension(file_path)
        xml_escape = self._extension_in(extension, ESCAPE_EXTENSIONS)

        # reads the complete set of file contents and in case an
        # encoding is defined decodes the provided file contents
        # using the encoding value (may raise exception)
        file_contents = file.read()
        is_bytes = type(file_contents) == colony.legacy.BYTES
        if encoding and is_bytes: file_contents = file_contents.decode(encoding)

        # creates the match orderer list, this list will hold the various
        # definitions of matched tokens for the current template, and is
        # meant to be ordered two times for processing
        match_orderer_l = []

        # retrieves the output matches iterator
        output_matches = OUTPUT_REGEX.finditer(file_contents)

        # iterates over all the output matches
        for output_match in output_matches:
            # retrieves the reference to the start and end matching indexed
            # to the output match and uses it to retrieve the literal value
            # for the match (going to be used in the match orderer)
            match_start = output_match.start()
            match_end = output_match.end()
            match_value = file_contents[match_start:match_end]

            # creates the match orderer for the current (output) match
            # signaling it as a output value (for later reference)
            match_orderer = MatchOrderer(output_match, OUTPUT_VALUE, match_value)
            match_orderer_l.append(match_orderer)

        # retrieves the eval matches iterator
        eval_matches = EVAL_REGEX.finditer(file_contents)

        # iterates over all the eval matches
        for eval_match in eval_matches:
            # retrieves the reference to the start and end matching indexed
            # to the eval match and uses it to retrieve the literal value
            # for the match (going to be used in the match orderer)
            match_start = eval_match.start()
            match_end = eval_match.end()
            match_value = file_contents[match_start:match_end]

            # creates the match orderer for the current (eval) match
            # signaling it as a eval value (for later reference)
            match_orderer = MatchOrderer(eval_match, EVAL_VALUE, match_value)
            match_orderer_l.append(match_orderer)

        # retrieves the start matches iterator
        start_matches = START_TAG_REGEX.finditer(file_contents)

        # iterates over all the start matches
        for start_match in start_matches:
            # retrieves the match start and end values and uses them to
            # construct the match value that is going to be used for the
            # construction of the match orderer structure to be added
            match_start = start_match.start()
            match_end = start_match.end()
            match_value = file_contents[match_start:match_end]

            # creates the match orderer for the current (start) match
            # signaling it as a start value (for later reference)
            math_orderer = MatchOrderer(start_match, START_VALUE, match_value)
            match_orderer_l.append(math_orderer)

        # retrieves the end matches iterator
        end_matches = END_TAG_REGEX.finditer(file_contents)

        # iterates over all the end matches
        for end_match in end_matches:
            # retrieves the match start and end values and uses them to
            # construct the match value that is going to be used for the
            # construction of the match orderer structure to be added
            match_start = end_match.start()
            match_end = end_match.end()
            match_value = file_contents[match_start:match_end]

            # creates the match orderer for the current (end) match
            # signaling it as a end value (for later reference)
            match_orderer = MatchOrderer(end_match, END_VALUE, match_value)
            match_orderer_l.append(match_orderer)

        # retrieves the single matches iterator
        single_matches = SINGLE_TAG_REGEX.finditer(file_contents)

        # iterates over all the single matches
        for single_match in single_matches:
            # retrieves the match start and end values and uses them to
            # construct the match value that is going to be used for the
            # construction of the match orderer structure to be added
            match_start = single_match.start()
            match_end = single_match.end()
            match_value = file_contents[match_start:match_end]

            # creates the match orderer for the current (single) match
            # signaling it as a single value (for later reference)
            match_orderer = MatchOrderer(single_match, SINGLE_VALUE, match_value)
            match_orderer_l.append(match_orderer)

        # orders the match orderer list so that the items are ordered from
        # the beginning to the latest as their are meant to be sorted
        match_orderer_l.sort(reverse = True)

        # creates the temporary literal match orderer list
        literal_orderer_l = []

        # creates the initial previous end
        previous_end = 0

        # iterates over all the matches in the match orderer list
        # to be able to create the complete set of literal parts
        # of the template with pure contents
        for match_orderer in match_orderer_l:
            # retrieves the match orderer match start position
            # as the "original" match start value
            match_start_o = match_orderer.match.start()

            # in case the current match orderer value start is not the same
            # as the previous end plus one, this means that there's a literal
            # value in between both matches and so that literal value must be
            # added to the current match orderer container
            if not match_start_o == previous_end:
                # calculates the both the start and the end of the literal value
                # in between and then retrieves the same value from the current
                # file buffer/contents so that a orderer value may be created
                match_start = previous_end
                match_end = match_start_o
                match_value = file_contents[match_start:match_end]

                # creates the literal match object with the match start and
                # and end values and then uses it to create the orderer
                literal_match = LiteralMatch(match_start, match_end)
                match_orderer_lit = MatchOrderer(literal_match, LITERAL_VALUE, match_value)

                # appends the match orderer object to the list of literal match
                # orderer list, this list will later be fused with the "normal"
                # match orderer list (as expected)
                literal_orderer_l.append(match_orderer_lit)

            # updates the previous end value with the end of the current
            # literal value, this is considered to be the iteration housekeeping
            previous_end = match_orderer.match.end()

        # in case there is still a final literal to be processed, it
        # must be processed as a special case with special requirements
        if not previous_end == len(file_contents):
            # calculates the literal match start as the previous end
            # value and the end as the final index of the file contents
            # data and then retrieves the value as that chunk
            match_start = previous_end
            match_end = len(file_contents)
            match_value = file_contents[match_start:match_end]

            # creates the literal match object with the match start and
            # and end values and then uses it to create the orderer
            literal_match = LiteralMatch(match_start, match_end)
            match_orderer = MatchOrderer(literal_match, LITERAL_VALUE, match_value)

            # appends the match orderer object to the list of literal match
            # orderer list, this list will later be fused with the "normal"
            # match orderer list (as expected)
            literal_orderer_l.append(match_orderer)

        # adds the elements of the literal math orderer list
        # to the match orderer list and then re-sorts the
        # match ordered list one more time in the reverse order
        match_orderer_l += literal_orderer_l
        match_orderer_l.sort(reverse = True)

        # creates the root node and starts the stack of tree nodes
        # with the root node inserted in it, the stack will be used
        # for the proper handling of start and end values
        root_node = ast.RootNode()
        stack = [root_node]

        # iterates over all the matches in the match orderer list
        # to create the complete abstract syntax tree representing
        # the template that has just been parsed, this same tree
        # may be latter percolated for the generation process
        for match_orderer in match_orderer_l:

            # retrieves the match orderer type for the
            # current iteration, this value will condition
            # the way the nodes are going to be created
            mtype = match_orderer.get_type()

            if mtype == OUTPUT_VALUE:
                value = match_orderer.get_value()
                node = ast.OutputNode(value, xml_escape = xml_escape)
                parent_node = stack[-1]
                parent_node.add_child(node)

            elif mtype == EVAL_VALUE:
                value = match_orderer.get_value()
                node = ast.EvalNode(value)
                parent_node = stack[-1]
                is_end = node.is_end()
                is_open = node.is_open()
                if is_end:
                    node.assert_end(parent_node.type)
                    stack.pop()
                else:
                    parent_node.add_child(node)
                    if is_open: stack.append(node)

            elif mtype == START_VALUE:
                node = ast.CompositeNode(
                    [match_orderer],
                    regex = ATTRIBUTE_REGEX,
                    literal_regex = ATTRIBUTE_LITERAL_REGEX
                )
                parent_node = stack[-1]
                parent_node.add_child(node)
                stack.append(node)

            elif mtype == END_VALUE:
                node = stack.pop()
                node.value.append(match_orderer)

            elif mtype == SINGLE_VALUE:
                node = ast.SingleNode(
                    match_orderer,
                    regex = ATTRIBUTE_REGEX,
                    literal_regex = ATTRIBUTE_LITERAL_REGEX
                )
                parent_node = stack[-1]
                parent_node.add_child(node)

            elif mtype == LITERAL_VALUE:
                node = ast.LiteralNode(match_orderer)
                parent_node = stack[-1]
                parent_node.add_child(node)

        # creates the template file structure that is going to be
        # used to represent the template in a abstract way this is
        # going to be the interface structure with the end user
        template_file = TemplateFile(
            manager = self,
            base_path = base_path,
            file_path = file_path,
            encoding = encoding,
            root_node = root_node
        )

        # attaches the currently given process methods and locale
        # bundles to the template file so that they may be used
        # latter for the processing of the file
        template_file.attach_process_methods(process_methods_list)
        template_file.attach_locale_bundles(locale_bundles)

        # loads the system variable in the template file, this
        # will allow access to the global system status from inside
        # the template file (for diagnosis and debugging)
        template_file.load_system_variable()

        # loads the complete set of based functions that should be
        # made accessible to the template for be able to perform
        # common operations like conversion and localization
        template_file.load_functions()

        # returns the final template file template file to the caller
        # method so that it may be used for rendering
        return template_file

    def _extension(self, file_path):
        _head, tail = os.path.split(file_path)
        tail_s = tail.split(".", 1)
        if len(tail_s) > 1: return "." + tail_s[1]
        return None

    def _extension_in(self, extension, sequence):
        for item in sequence:
            valid = extension.endswith(item)
            if not valid: continue
            return True
        return False

class MatchOrderer(object):
    """
    The match orderer class, that is used to re-sort
    the various matched of the template engine in
    the proper order.
    """

    match = None
    """ The match object to be ordered, this value
    should be the internal regex library value for
    the match operation """

    type = None
    """ The type of the match object to be ordered,
    this value should reflect the kind of match that
    has been accomplished for the value """

    value = None
    """ The value of the match object to be ordered
    this should be a literal string value of it """

    def __init__(self, match, type, value):
        self.match = match
        self.type = type
        self.value = value

    def __cmp__(self, other):
        return other.match.start() - self.match.start()

    def __lt__(self, other):
        return self.match.start() > other.match.start()

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

class LiteralMatch(object):

    start_index = None
    """ The start index value, this should be an offset
    position inside the current document's string data value """

    end_index = None
    """ The end index value, that should close the
    current literal value starting in the start index """

    def __init__(self, start_index = None, end_index = None):
        self.start_index = start_index
        self.end_index = end_index

    def start(self):
        return self.start_index

    def end(self):
        return self.end_index

class TemplateFile(object):
    """
    The template file class, this is the most abstract
    representation of the template and also the entry
    level for the user level operations.
    """

    manager = None
    """ The manager of the template file, this is considered to
    be the owner and generator instance """

    base_path = None
    """ The base path to be used in the resolution of template
    files, this value may or may not be defined and in case it's
    not defined only the default (relative path) resolution approach
    is used for the include and extends operations """

    file_path = None
    """ The path to the file from which the contents of the template
    are loaded, this is the original reference """

    encoding = None
    """ The encoding used in the file, this is the main encoding
    to be used both in the loading and storage of it """

    variable_encoding = None
    """ The encoding that is going to be used to encode the value
    of the various variables to be expanded in the template """

    strict_mode = False
    """ The strict mode flag, that controls if the an error in a
    variable resolution should raise an exception, usage of this
    value should be done with care to avoid unwanted behavior """

    root_node = None
    """ The root node from which the visitor will start the visiting
    using a recursive approach """

    visitor = None
    """ The visitor object that will be used for the visiting of the
    various nodes that make part of the abstract syntax tree defined
    from the provided root node """

    locale_bundles = []
    """ The list that contains the various bundles to be searched for
    localization, the order set is going to be the priority for template
    value resolution (from first to last list element) """

    nodes = {}
    """ The dictionary that associates the identifiable node id with
    the node reference that it corresponds, this map may be used for
    abstract syntax tree manipulations (eg: inheritance manipulation) """

    def __init__(
        self,
        manager = None,
        base_path = None,
        file_path = None,
        encoding = None,
        root_node = None,
        eval = False
    ):
        """
        Constructor of the class.

        :type manager: TemplateEngine
        :param manager: The manager to be used.
        :type base_path: String
        :param base_path: The base file system path that is going to be
        used for processing templates in the include and extends operation.
        :type file_path: String
        :param file_path: The path to the file to be used, this value may or
        may not be defined depending on how the template is created.
        :type encoding: String
        :param encoding: The encoding used in the file, in case this value
        is not defined the encoding is assumed to be the default one.
        :type root_node: AstNode
        :param root_node: The root node to be used.
        :type eval: bool
        :param eval: If the evaluation based visitor should be used instead
        of the normal (and safe) interpreter based visitor. Care should be
        taking while deciding which visitor to be used.
        """

        self.manager = manager
        self.base_path = base_path
        self.file_path = file_path
        self.encoding = encoding
        self.root_node = root_node

        self.visitor = visitor.EvalVisitor(self) if eval else visitor.Visitor(self)
        self.locale_bundles = []
        self.nodes = {}

        self.index_nodes()

    @classmethod
    def format(cls, template, *args):
        """
        Custom format operation that takes a template value and
        a variable set of arguments and formats it according to
        the C definition of string templating.

        :type template: String
        :param template: The template string to be used in the
        C like format operation.
        :rtype: String
        :returns: The "final" formated string value.
        """

        try: return template % args
        except Exception: return None

    @classmethod
    def convert(cls, value, mode):
        """
        Converts the provided value according to the requested "modification"
        operation.

        The final converted value should be a "plain" string value.

        :type value: String
        :param value: The base value that is going to be converted
        according to the provided/requested mode.
        :type mode: String
        :param mode: The mode that described the operation that is
        going to be applied to the "base" value.
        :rtype: String
        :return: The final converted value according to the requested
        mode.
        """

        conversion_method = visitor.CONVERSION_MAP.get(mode, None)
        if not conversion_method: return value
        try: return conversion_method(value)
        except Exception: return None

    def index_nodes(self):
        """
        Runs the indexing stage of the identifiable nodes, this is
        required for the inheritance of blocks to properly work.

        More that one execution of this method may be required if
        the abstract syntax tree changed in response to the processing
        of one or more file inclusion (sub tree inclusion).
        """

        self._index_node(self.root_node)

    def assign(self, name, value):
        """
        Assigns a variable to a value. This assignment
        allows the usage of the value internally in the template.

        The assigned variable value may assume any given data
        type that is accessible by the template language.

        :type name: String
        :param name: The name of the variable to assign a value.
        :type value: Object
        :param value: The value to be assigned to the variable
        """

        self.visitor.set_global(name, value)

    def set_global_map(self, global_map):
        """
        Sets the global map to the current template file.
        The global map should be used as the support for the variable
        assignment.

        :type global_map: Dictionary
        :param global_map: The global map containing all the variable values.
        """

        self.visitor.set_global_map(global_map)

    def set_string_buffer(self, string_buffer):
        """
        Updates the underlying string buffer that is going to be
        used by the visitor to the provided one.

        The string buffer should be an opened file like object that
        accepts the typical calls.

        In case a typical file object is used this may reduce the
        amount of memory used by the visitor by an order of magnitude
        so this method may be very useful for long output generation
        in the template engine.

        :type string_buffer: File
        :param string_buffer: The file like object that is going to
        be used by the underlying visitor object.
        """

        self.visitor.string_buffer = string_buffer

    def attach_process_methods(self, process_methods_list):
        """
        Attaches a series of process methods to the visitor
        currently being used.

        This will allow for the usage of many more process
        methods that the ones available by default (extension).

        :type process_methods_list: List
        :param process_methods_list: The list of tuples containing the
        method name and method (function).
        """

        # iterates over all the process methods in the list unpacking
        # the tuples and then attaching each of these methods to the
        # currently defined visitor so that they may be used
        for method_name, method in process_methods_list:
            self.visitor.attach_process_method(method_name, method)

    def attach_locale_bundles(self, locale_bundles):
        """
        Attaches a series of locale bundles methods to the visitor
        currently being used.

        This method also attaches the locale bundles to the current
        instance (for context retrieval).

        :type locale_bundles: List
        :param locale_bundles: The list of locale bundles to be used
        for resolution in the current context.
        """

        self.locale_bundles = locale_bundles
        self.visitor.locale_bundles = locale_bundles

    def load_system_variable(self, name = "_system"):
        """
        Loads a system information variable to the template
        file. This variable would allow for access to the
        status of the current manager/system.

        :type name: String
        :param name: The name of the variable used
        to retain the system wide information.
        """

        # retrieves the template engine plugin
        # in order to obtain the plugin manager
        template_engine_plugin = self.manager.plugin
        plugin_manager = template_engine_plugin.manager

        # retrieves the map containing the "global" system information
        system_information_map = plugin_manager.get_system_information_map()

        # assigns the system information map variable to
        # the template so that it may be used to retrieve
        # global information about the system
        self.assign(name, system_information_map)

    def load_functions(self):
        """
        Loads the complete set of base functions that are going to be
        used at template runtime to perform common operations.

        These functions will be exposed on the global dictionary.
        """

        # retrieves the reference to the class associated with the
        # current instance to be able to access class variables
        cls = self.__class__

        # runs the assign operation for the complete set of functions
        # that are considered part of the global namespace
        self.assign("colony", colony)
        self.assign("format", cls.format)
        self.assign("convert", cls.convert)

    def load_visitor(self):
        """
        Runs the various loading/prepare operations in the currently
        set visitor so that it becomes reading for the visit of AST
        based nodes (prepare operation).

        This operation should always be called before any accepting
        operation of a visitor is performed (processing), otherwise
        unexpected behavior may occur in the visit.
        """

        self.visitor.set_encoding(self.encoding)
        self.visitor.set_base_path(self.base_path)
        self.visitor.set_file_path(self.file_path)
        self.visitor.set_template_engine(self.manager)
        self.visitor.set_variable_encoding(self.variable_encoding)
        self.visitor.set_strict_mode(self.strict_mode)

    def process(self, get_value = True):
        """
        Processes the template file running the visitor
        and returning the result value.

        This is considered to be the main method for the
        processing of the template and should only be called
        when the complete set of attribute are set in the
        current template structure (to avoid errors).

        The resulting value from this operation should always
        be a valid unicode string that may be used in any kind
        of transform operation. Alternatively and if the get value
        flag is not set the buffer is returned, but this option
        should be used carefully to avoid any encoding problems.

        :type get_value: bool
        :param get_value: If the final string value of
        the contents should be retrieved as a result.
        :rtype: String/Buffer
        :return: The result value from the visitor or the
        string buffer in case the get value flag was set
        to a false value.
        """

        # sets the complete set of attributes in the visitor
        # that is currently set in the template and then runs
        # the accept operation in the root node, this will
        # trigger the generation of the template contents
        self.load_visitor()
        self.root_node.accept(self.visitor)

        # retrieves the visitor string buffer, that should now
        # contains the final contents from template generation
        string_buffer = self.visitor.string_buffer

        # retrieves the visitor string buffer value, in case
        # the value should be retrieved from the underlying string
        # buffer, otherwise retrieves the string buffer as the value
        if get_value: value = string_buffer.get_value()
        else: value = string_buffer

        # in case the returned value from the string buffer is not
        # a valid unicode string it must be decoded using the currently
        # defined encoding or the default one in case it's not defined
        is_bytes = type(value) == colony.legacy.BYTES
        if is_bytes: value = value.decode(self.encoding or "utf-8")

        # returns the final value to the caller method, this may
        # either have the reference to the string buffer of the
        # generated string value contents
        return value

    def get_variable_encoding(self):
        """
        Retrieves the variable encoding.

        :rtype: String
        :return: The variable encoding.
        """

        return self.variable_encoding

    def set_variable_encoding(self, variable_encoding):
        """
        Sets the variable encoding.

        :type variable_encoding: String
        :param variable_encoding: The variable encoding.
        """

        self.variable_encoding = variable_encoding

    def get_strict_mode(self):
        """
        Retrieves the strict mode.
        In strict mode, variables referenced but node defined
        raise exceptions.

        :rtype: String
        :return: The strict mode.
        """

        return self.strict_mode

    def set_strict_mode(self, strict_mode):
        """
        Sets the strict mode.
        In strict mode, variables referenced but node defined
        raise exceptions.

        :type strict_mode: bool
        :param strict_mode: The strict mode.
        """

        self.strict_mode = strict_mode

    def add_bundle(self, bundle):
        """
        Adds a new locale bundle to the current
        context, the bundle will be added both
        to the current instance and to the visitor.

        :type bundle: Dictionary
        :param bundle: The locale bundle to be added to
        the current template processing context.
        """

        self.locale_bundles.append(bundle)
        self.visitor.add_bundle(bundle)

    def _index_node(self, node):
        """
        Index the provided template node, making sure that
        its identifier is present in the nodes map and associated
        with the node, this is a relevant operation for the
        inheritance infra-structure.

        :type node: Node
        :param node: The node that should be indexed under the
        current template infra-structure.
        """

        type = node.get_type()
        id = node.get_id()
        if type == "block": self.nodes[id] = node
        for node in node.children: self._index_node(node)
