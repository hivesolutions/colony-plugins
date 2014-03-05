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

import os
import re

import colony.base.system

import ast
import visitor
import exceptions

START_TAG_REGEX_VALUE = "\$\{[^\/\{}\{}][^\{\}][^\/\{}\{}]*\}"
""" The start tag regular expression value """

END_TAG_REGEX_VALUE = "\$\{\/[^\{\}][^\/\{}\{}]*\}"
""" The end tag regular expression value """

SINGLE_TAG_REGEX_VALUE = "\$\{[^\{\}]*\/\}"
""" The single tag regular expression value """

ATTRIBUTE_REGEX_VALUE = "[a-zA-Z_]+=[a-zA-Z_][a-zA-Z0-9_\.\/\(\)\:,'\"]*"
""" The attribute regular expression value """

ATTRIBUTE_QUOTED_SINGLE_REGEX_VALUE = "[a-zA-Z_]+=['][^']+[']"
""" The attribute quoted single regular expression value """

ATTRIBUTE_QUOTED_DOUBLE_REGEX_VALUE = "[a-zA-Z_]+=[\"][^\"]+[\"]"
""" The attribute quoted double regular expression value """

ATTRIBUTE_FLOAT_REGEX_VALUE = "[a-zA-Z_]+=-?[0-9]+\.[0-9]*"
""" The attribute float regular expression value """

ATTRIBUTE_INTEGER_REGEX_VALUE = "[a-zA-Z_]+=-?[0-9]+"
""" The attribute integer regular expression value """

ATTRIBUTE_TRUE_BOOLEAN_REGEX_VALUE = "[a-zA-Z_]+=True"
""" The attribute true boolean regular expression value """

ATTRIBUTE_FALSE_BOOLEAN_REGEX_VALUE = "[a-zA-Z_]+=False"
""" The attribute false boolean regular expression value """

ATTRIBUTE_NONE_REGEX_VALUE = "[a-zA-Z_]+=None"
""" The attribute none regular expression value """

START_VALUE = "start"
""" The start value """

END_VALUE = "end"
""" The end value """

SINGLE_VALUE = "single"
""" The single value """

LITERAL_VALUE = "literal"
""" The literal value """

START_TAG_REGEX = re.compile(START_TAG_REGEX_VALUE)
""" The start tag regular expression """

END_TAG_REGEX = re.compile(END_TAG_REGEX_VALUE)
""" The end tag regular expression """

SINGLE_TAG_REGEX = re.compile(SINGLE_TAG_REGEX_VALUE)
""" The single tag regular expression """

ATTRIBUTE_REGEX = re.compile(ATTRIBUTE_REGEX_VALUE)
""" The attribute regular expression """

ATTRIBUTE_LITERAL_REGEX = re.compile(
    "(?P<quoted_single>" + ATTRIBUTE_QUOTED_SINGLE_REGEX_VALUE + ")|" + \
    "(?P<quoted_double>" + ATTRIBUTE_QUOTED_DOUBLE_REGEX_VALUE + ")|" + \
    "(?P<float>" + ATTRIBUTE_FLOAT_REGEX_VALUE + ")|" + \
    "(?P<integer>" + ATTRIBUTE_INTEGER_REGEX_VALUE + ")|" + \
    "(?P<true_boolean>" + ATTRIBUTE_TRUE_BOOLEAN_REGEX_VALUE + ")|" + \
    "(?P<false_boolean>" + ATTRIBUTE_FALSE_BOOLEAN_REGEX_VALUE + ")|" + \
    "(?P<none>" + ATTRIBUTE_NONE_REGEX_VALUE + ")"
)
""" The literal regular expression that matches all the literals, there
are matching groups for each of the data types """

class TemplateEngine(colony.base.system.System):
    """
    The template engine class, responsible for the processing
    of template files according to the current template engine
    based file specification. Its internal working should be
    based on a visitor strategy.
    """

    def parse_file_path(
        self,
        file_path,
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
        file = open(file_path, "r")

        try:
            # parses the file, retrieving the template file structure
            # that can be used for the execution of it
            template_file = self.parse_file(
                file,
                file_path,
                encoding,
                process_methods_list,
                locale_bundles
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
        template_file = self.parse_file_path(file_path, encoding, process_methods_list, locale_bundles)
        template_file.set_variable_encoding(variable_encoding)
        return template_file

    def parse_file(
        self,
        file,
        file_path = None,
        encoding = None,
        process_methods_list = [],
        locale_bundles = None
    ):
        # in case the locale bundles list is not defined must
        # create a new list reference to handle it correctly
        if locale_bundles == None: locale_bundles = []

        # reads the complete set of file contents and in case an
        # encoding is defined decodes the provided file contents
        # using the encoding value (may raise exception)
        file_contents = file.read()
        if encoding: file_contents = file_contents.decode(encoding)

        # creates the match orderer list, this list will hold the various
        # definitions of matched tokens for the current template, and is
        # meant to be ordered two times for processing
        match_orderer_l = []

        # retrieves the start matches iterator
        start_matches_iterator = START_TAG_REGEX.finditer(file_contents)

        # iterates over all the start matches
        for start_match in start_matches_iterator:
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
        end_matches_iterator = END_TAG_REGEX.finditer(file_contents)

        # iterates over all the end matches
        for end_match in end_matches_iterator:
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
        single_matches_iterator = SINGLE_TAG_REGEX.finditer(file_contents)

        # iterates over all the single matches
        for single_match in single_matches_iterator:
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
            type = match_orderer.get_match_type()

            if type == START_VALUE:
                node = ast.CompositeNode(
                    [match_orderer],
                    regex = ATTRIBUTE_REGEX,
                    literal_regex = ATTRIBUTE_LITERAL_REGEX
                )
                parent_node = stack[-1]
                parent_node.add_child_node(node)
                stack.append(node)

            elif type == END_VALUE:
                node = stack.pop()
                node.value.append(match_orderer)

            elif type == SINGLE_VALUE:
                node = ast.SingleNode(
                    match_orderer,
                    regex = ATTRIBUTE_REGEX,
                    literal_regex = ATTRIBUTE_LITERAL_REGEX
                )
                parent_node = stack[-1]
                parent_node.add_child_node(node)

            elif type == LITERAL_VALUE:
                node = ast.LiteralNode(match_orderer)
                parent_node = stack[-1]
                parent_node.add_child_node(node)

        # creates the template file structure that is going to be
        # used to represent the template in a abstract way this is
        # going to be the interface structure with the end user
        template_file = TemplateFile(
            manager = self,
            file_path = file_path,
            encoding = encoding,
            root_node = root_node
        )

        # attaches the currently given process methods and locale
        # bundles to the template file
        template_file.attach_process_methods(process_methods_list)
        template_file.attach_locale_bundles(locale_bundles)

        # loads the system variable in the template file
        template_file.load_system_variable()

        # returns the final template file template file to the caller
        # method so that it may be used for rendering
        return template_file

class MatchOrderer:
    """
    The match orderer class, that is used to re-sort
    the various matched of the template engine in
    the proper order.
    """

    match = None
    """ The match object to be ordered, this value
    should be the internal regex library value for
    the match operation """

    match_type = None
    """ The type of the match object to be ordered,
    this value should reflect the kind of match that
    has been accomplished for the value """

    match_value = None
    """ The value of the match object to be ordered
    this should be a literal string value of it """

    def __init__(self, match, match_type, match_value):
        self.match = match
        self.match_type = match_type
        self.match_value = match_value

    def __cmp__(self, other):
        return other.match.start() - self.match.start()

    def get_match_type(self):
        return self.match_type

    def set_match_type(self, match_type):
        self.match_type = match_type

    def get_match_value(self):
        return self.match_value

    def set_match_value(self, match_value):
        self.match_value = match_value

class LiteralMatch:

    start_index = None
    """ The start index value """

    end_index = None
    """ The end index value """

    def __init__(self, start_index = None, end_index = None):
        self.start_index = start_index
        self.end_index = end_index

    def start(self):
        return self.start_index

    def end(self):
        return self.end_index

class TemplateFile:
    """
    The template file class, this is the most abstract
    representation of the template and also the entry
    level for the user level operations.
    """

    manager = None
    """ The manager """

    file_path = None
    """ The path to the file to be used """

    encoding = None
    """ The encoding used in the file """

    variable_encoding = None
    """ The variable encoding """

    strict_mode = False
    """ The strict mode flag """

    root_node = None
    """ The root node """

    visitor = None
    """ The visitor """

    locale_bundles = []
    """ The list that contains the various bundles to be searched for
    localization, the order set is going to be the priority for template
    value resolution (from first to last list element) """

    def __init__(self, manager = None, file_path = None, encoding = None, root_node = None):
        """
        Constructor of the class.

        @type manager: TemplateEngine
        @param manager: The manager to be used.
        @type file_path: String
        @param file_path: The path to the file to be used.
        @type encoding: String
        @param encoding: The encoding used in the file.
        @type root_node: AstNode
        @param root_node: The root node to be used.
        """

        self.manager = manager
        self.file_path = file_path
        self.encoding = encoding
        self.root_node = root_node

        self.visitor = visitor.Visitor()
        self.locale_bundles = []

    def assign(self, variable_name, variable_value):
        """
        Assigns a variable to a value. This assignment
        allows the usage of the value internally in the template.

        @type variable_name: String
        @param variable_name: The name of the variable to assign a value.
        @type variable_value: Object
        @param variable_value: The value to be assigned to the variable
        """

        self.visitor.add_global_variable(variable_name, variable_value)

    def set_global_map(self, global_map):
        """
        Sets the global map to the current template file.
        The global map should be used as the support for the variable
        assignment.

        @type global_map: Dictionary
        @param global_map: The global map containing all the variable values.
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

        @type string_buffer: File
        @param string_buffer: The file like object that is going to
        be used by the underlying visitor object.
        """

        self.visitor.string_buffer = string_buffer

    def attach_process_methods(self, process_methods_list):
        """
        Attaches a series of process methods to the visitor
        currently being used.

        @type process_methods_list: List
        @param process_methods_list: The list of tuples containing the
        method name and method (function).
        """

        # iterates over all the process methods in the list
        for process_method_name, process_method in process_methods_list:
            # attaches the process method to the visitor
            self.visitor.attach_process_method(process_method_name, process_method)

    def attach_locale_bundles(self, locale_bundles):
        """
        Attaches a series of locale bundles methods to the visitor
        currently being used.

        This method also attaches the locale bundles to the current
        instance (for context retrieval).

        @type locale_bundles: List
        @param locale_bundles: The list of locale bundles to be used
        for resolution in the current context.
        """

        self.locale_bundles = locale_bundles
        self.visitor.locale_bundles = locale_bundles

    def load_system_variable(self, variable_name = "_system"):
        """
        Loads a system information variable to the template
        file.

        @type variable_name: String
        @param variable_name: The name of the variable used
        to retain the system wide information.
        """

        # retrieves the template engine plugin
        # in order to obtain the plugin manager
        template_engine_plugin = self.manager.plugin
        plugin_manager = template_engine_plugin.manager

        # retrieves the map containing the "global" system information
        system_information_map = plugin_manager.get_system_information_map()

        # assigns the system information map variable
        # to the template
        self.assign(variable_name, system_information_map)

    def process(self, get_value = True):
        """
        Processes the template file running the visitor
        and returning the result value.

        @type get_value: bool
        @param get_value: If the final string value of
        the contents should be retrieved as a result.
        @rtype: String
        @return: The result value from the visitor.
        """

        # sets the encoding in the visitor
        self.visitor.set_encoding(self.encoding)

        # sets the file path in the visitor
        self.visitor.set_file_path(self.file_path)

        # sets the template engine in the visitor
        self.visitor.set_template_engine(self.manager)

        # sets the variable encoding in the visitor
        self.visitor.set_variable_encoding(self.variable_encoding)

        # sets the strict mode in the visitor
        self.visitor.set_strict_mode(self.strict_mode)

        # accepts the visitor in the root node
        self.root_node.accept(self.visitor)

        # retrieves the visitor string buffer
        visitor_string_buffer = self.visitor.string_buffer

        # retrieves the visitor string buffer value, in case
        # the value should be retrieved from the underlying string
        # buffer, otherwise retrieves the string buffer as the value
        if get_value: visitor_string_buffer_value = visitor_string_buffer.get_value()
        else: visitor_string_buffer_value = visitor_string_buffer

        # returns the visitor string buffer value
        return visitor_string_buffer_value

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
        In strict mode, variables referenced but node defined
        raise exceptions.

        @rtype: String
        @return: The strict mode.
        """

        return self.strict_mode

    def set_strict_mode(self, strict_mode):
        """
        Sets the strict mode.
        In strict mode, variables referenced but node defined
        raise exceptions.

        @type strict_mode: bool
        @param strict_mode: The strict mode.
        """

        self.strict_mode = strict_mode

    def add_bundle(self, bundle):
        """
        Adds a new locale bundle to the current
        context, the bundle will be added both
        to the current instance and to the visitor.

        @type bundle: Dictionary
        @param bundle: The locale bundle to be added to
        the current template processing context.
        """

        self.locale_bundles.append(bundle)
        self.visitor.add_bundle(bundle)
