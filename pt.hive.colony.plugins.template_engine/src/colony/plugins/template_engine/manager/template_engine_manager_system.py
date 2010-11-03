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

__revision__ = "$LastChangedRevision: 516 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-28 14:30:47 +0000 (Sex, 28 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

import template_engine_ast
import template_engine_visitor

START_TAG_REGEX_VALUE = "\$\{[^\/\{}\{}][^\{\}][^\/\{}\{}]*\}"
""" The start tag regular expression value """

END_TAG_REGEX_VALUE = "\$\{\/[^\{\}][^\/\{}\{}]*\}"
""" The end tag regular expression value """

SINGLE_TAG_REGEX_VALUE = "\$\{[^\{\}]*\/\}"
""" The single tag regular expression value """

ATTRIBUTE_REGEX_VALUE = "[a-zA-Z_]+=[a-zA-Z_][a-zA-Z0-9_\.\/]*"
""" The attribute regular expression value """

ATTRIBUTE_QUOTED_REGEX_VALUE = "[a-zA-Z_]+=\".+\""
""" The attribute quoted regular expression value """

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

DEFAULT_ENCODING_VALUE = None
""" The default encoding value """

DEFAULT_VARIABLE_ENCODING = "utf-8"
""" The default variable encoding """

START_TAG_REGEX = re.compile(START_TAG_REGEX_VALUE)
""" The start tag regular expression """

END_TAG_REGEX = re.compile(END_TAG_REGEX_VALUE)
""" The end tag regular expression """

SINGLE_TAG_REGEX = re.compile(SINGLE_TAG_REGEX_VALUE)
""" The single tag regular expression """

ATTRIBUTE_REGEX = re.compile(ATTRIBUTE_REGEX_VALUE)
""" The attribute regular expression """

ATTRIBUTE_LITERAL_REGEX = re.compile("(?P<quoted>" + ATTRIBUTE_QUOTED_REGEX_VALUE + ")|" + \
                                     "(?P<float>" + ATTRIBUTE_FLOAT_REGEX_VALUE + ")|" + \
                                     "(?P<integer>" + ATTRIBUTE_INTEGER_REGEX_VALUE + ")|" + \
                                     "(?P<true_boolean>" + ATTRIBUTE_TRUE_BOOLEAN_REGEX_VALUE + ")|" + \
                                     "(?P<false_boolean>" + ATTRIBUTE_FALSE_BOOLEAN_REGEX_VALUE + ")|" + \
                                     "(?P<none>" + ATTRIBUTE_NONE_REGEX_VALUE + ")")
""" The literal regular expression that matches all the literals """

class TemplateEngineManager:
    """
    The template engine manager class.
    """

    template_engine_manager_plugin = None
    """ The template engine manager plugin """

    def __init__(self, template_engine_manager_plugin):
        """
        Constructor of the class.

        @type template_engine_manager_plugin: TemplateEngineManagerPlugin
        @param template_engine_manager_plugin: The template engine manager plugin.
        """

        self.template_engine_manager_plugin = template_engine_manager_plugin

    def parse_file_path(self, file_path, encoding = DEFAULT_ENCODING_VALUE, variable_encoding = DEFAULT_ENCODING_VALUE):
        # opens the file for reading
        file = open(file_path, "r")

        try:
            # parses the file, retrieving the template file
            template_file = self.parse_file(file, file_path, encoding)
        finally:
            # closes the file
            file.close()

        # in case the variable encoding is valid sets the variable
        # encoding in the template file
        variable_encoding and template_file.set_variable_encoding(variable_encoding)

        # returns the template file
        return template_file

    def parse_file(self, file, file_path = None, encoding = DEFAULT_ENCODING_VALUE):
        # reads the file contents
        file_contents = file.read()

        # in case an encoding is defined
        if encoding:
            # decodes the file contents
            file_contents = file_contents.decode(encoding)

        # retrieves the start matches iterator
        start_matches_iterator = START_TAG_REGEX.finditer(file_contents)

        # creates the match orderer list
        match_orderer_list = []

        # iterates over all the start matches
        for start_match in start_matches_iterator:
            # retrieves the start match start
            start_match_start = start_match.start()

            # retrieves the start match end
            start_match_end = start_match.end()

            # retrieves the start match value
            start_match_value = file_contents[start_match_start:start_match_end]

            start_math_orderer = MatchOrderer(start_match, START_VALUE, start_match_value)
            match_orderer_list.append(start_math_orderer)

        # retrieves the end matches iterator
        end_matches_iterator = END_TAG_REGEX.finditer(file_contents)

        # iterates over all the end matches
        for end_match in end_matches_iterator:
            # retrieves the end match start
            end_match_start = end_match.start()

            # retrieves the end match end
            end_match_end = end_match.end()

            # retrieves the end match value
            end_match_value = file_contents[end_match_start:end_match_end]

            end_match_orderer = MatchOrderer(end_match, END_VALUE, end_match_value)
            match_orderer_list.append(end_match_orderer)

        # retrieves the single matches iterator
        single_matches_iterator = SINGLE_TAG_REGEX.finditer(file_contents)

        # iterates over all the single matches
        for single_match in single_matches_iterator:
            # retrieves the single match start
            single_match_start = single_match.start()

            # retrieves the single match end
            single_match_end = single_match.end()

            # retrieves the single match value
            single_match_value = file_contents[single_match_start:single_match_end]

            single_match_orderer = MatchOrderer(single_match, SINGLE_VALUE, single_match_value)
            match_orderer_list.append(single_match_orderer)

        # orders the match orderer list
        match_orderer_list.sort()

        # reverses the list so that it's ordered in ascending form
        match_orderer_list.reverse()

        # creates the temporary literal match orderer list
        literal_match_orderer_list = []

        # creates the initial previous end
        previous_end = 0

        # iterates over all the matches in
        # the match orderer list
        for match_orderer in match_orderer_list:
            # retrieves the match orderer match start
            match_orderer_match_start = match_orderer.match.start()

            # in case the current match orderer value start is not the same
            # as the previous end plus one
            if not match_orderer_match_start == previous_end:
                # calculates the literal match start
                literal_match_start = previous_end

                # calculates the literal match end
                literal_match_end = match_orderer_match_start

                # calculates the literal match value
                literal_match_value = file_contents[literal_match_start:literal_match_end]

                # creates the literal match object with the
                # literal match start and the literal match end
                literal_match = LiteralMatch(literal_match_start, literal_match_end)

                # creates a match orderer object for the literal match
                literal_match_orderer = MatchOrderer(literal_match, LITERAL_VALUE, literal_match_value)

                # appends the literal match orderer object to
                # the list of literal match orderer list
                literal_match_orderer_list.append(literal_match_orderer)

            # updates the previous end value
            previous_end = match_orderer.match.end()

        # in case there is still a final literal to be processed
        if not previous_end == len(file_contents):
            # calculates the literal match start
            literal_match_start = previous_end

            # calculates the literal match end
            literal_match_end = len(file_contents)

            # calculates the literal match value
            literal_match_value = file_contents[literal_match_start:literal_match_end]

            # creates the literal match object with the
            # literal match start and the literal match end
            literal_match = LiteralMatch(literal_match_start, literal_match_end)

            # creates a match orderer object for the literal match
            literal_match_orderer = MatchOrderer(literal_match, LITERAL_VALUE, literal_match_value)

            # appends the literal match orderer object to
            # the list of literal match orderer list
            literal_match_orderer_list.append(literal_match_orderer)

        # adds the elements of the literal math orderer list
        # to the match orderer list
        match_orderer_list += literal_match_orderer_list

        # orders the match orderer list
        match_orderer_list.sort()

        # reverses the list so that it's ordered in ascending form
        match_orderer_list.reverse()

        # creates the root node
        root_node = template_engine_ast.RootNode()

        # creates the tree node stack with the root node inserted
        tree_node_stack = [root_node]

        # iterates over all the matches in
        # the match orderer list
        for match_orderer in match_orderer_list:
            # retrieves the match orderer type
            match_orderer_type = match_orderer.get_match_type()

            # in case the match order is of type start
            if match_orderer_type == START_VALUE:
                # retrieves the parent node
                parent_node = tree_node_stack[-1]

                # creates the composite node from the match orderer
                composite_node = template_engine_ast.CompositeNode([match_orderer], ATTRIBUTE_REGEX, ATTRIBUTE_LITERAL_REGEX)

                # adds the composite node as a child to the parent node
                parent_node.add_child_node(composite_node)

                # adds the composite node to the tree node stack
                tree_node_stack.append(composite_node)
            # in case the match order is of type end
            elif match_orderer_type == END_VALUE:
                # retrieves the composite node
                composite_node = tree_node_stack.pop()

                # adds the match orderer to the value of the composite node
                composite_node.value.append(match_orderer)

                # converts the composite node value to a tuple
                tuple(composite_node.value)
            # in case the match order is of type single
            elif match_orderer_type == SINGLE_VALUE:
                # retrieves the parent node
                parent_node = tree_node_stack[-1]

                # creates the single node from the match orderer
                single_node = template_engine_ast.SingleNode(match_orderer, ATTRIBUTE_REGEX, ATTRIBUTE_LITERAL_REGEX)

                # adds the single node as a child to the parent node
                parent_node.add_child_node(single_node)
            # in case the match order is of type literal
            elif match_orderer_type == LITERAL_VALUE:
                # retrieves the parent node
                parent_node = tree_node_stack[-1]

                # creates the literal node from the match orderer
                literal_node = template_engine_ast.LiteralNode(match_orderer)

                # adds the literal node as a child to the parent node
                parent_node.add_child_node(literal_node)

        # creates the template file from the file path, encoding and root node
        template_file = TemplateFile(self, file_path, encoding, root_node)

        # returns the template file
        return template_file

class MatchOrderer:
    """
    The match orderer class.
    """

    match = None
    """ The match object to be ordered """

    match_type = "none"
    """ The type of the match object to be ordered """

    match_value = None
    """ The value of the match object to be ordered """

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
    The template file class.
    """

    manager = None
    """ The manager """

    file_path = None
    """ The path to the file to be used """

    encoding = None
    """ The encoding used in the file """

    variable_encoding = DEFAULT_VARIABLE_ENCODING
    """ The variable encoding """

    strict_mode = False
    """ The strict mode flag """

    root_node = None
    """ The root node """

    visitor = None
    """ The visitor """

    def __init__(self, manager = None, file_path = None, encoding = None, root_node = None):
        """
        Constructor of the class.

        @type manager: TemplateEngineManager
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

        self.visitor = template_engine_visitor.Visitor()

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

    def process(self):
        """
        Processes the template file running the visitor
        and returning the result value.

        @rtype: String
        @return: The result value from the visitor.
        """

        # sets the encoding in the visitor
        self.visitor.set_encoding(self.encoding)

        # sets the file path in the visitor
        self.visitor.set_file_path(self.file_path)

        # sets the template engine manager in the visitor
        self.visitor.set_template_engine_manager(self.manager)

        # sets the variable encoding in the visitor
        self.visitor.set_variable_encoding(self.variable_encoding)

        # sets the strict mode in the visitor
        self.visitor.set_strict_mode(self.strict_mode)

        # accepts the visitor in the root node
        self.root_node.accept(self.visitor)

        # retrieves the visitor string buffer
        visitor_string_buffer = self.visitor.string_buffer

        print "o valor e: " + str(visitor_string_buffer.string_list)

        # retrieves the visitor string buffer value
        visitor_string_buffer_value = visitor_string_buffer.get_value()

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
