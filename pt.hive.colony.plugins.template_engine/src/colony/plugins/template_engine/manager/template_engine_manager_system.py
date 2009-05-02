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

START_TAG_VALUE = "\$\{[^\/\{}\{}][^\{\}][^\/\{}\{}]*\}"
""" The start tag value """

END_TAG_VALUE = "\$\{\/[^\{\}][^\/\{}\{}]*\}"
""" The end tag value """

SINGLE_TAG_VALUE = "\$\{[^\{\}]*\/\}"
""" The single tag value """

ATTRIBUTE_VALUE = "[a-zA-Z]+=[a-zA-Z0-9]+"
""" The attribute value """

ATTRIBUTE_QUOTED_VALUE = "[a-zA-Z]+=\".+\""
""" The attribute quoted value """

START_VALUE = "start"
""" The start value """

END_VALUE = "end"
""" The end value """

SINGLE_VALUE = "single"
""" The single value """

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

    def parse_file_path(self, file_path):
        # opens the file for reading
        file = open(file_path, "r")

        # parses the file
        result = self.parse_file(file)

        # closes the file
        file.close()

        return result

    def parse_file(self, file):
        # reads the file contents
        file_contents = file.read()

        # creates the template start regex
        template_start_regex = re.compile(START_TAG_VALUE)

        # creates the template end regex
        template_end_regex = re.compile(END_TAG_VALUE)

        # creates the template single regex
        template_single_regex = re.compile(SINGLE_TAG_VALUE)

        # retrieves the start matches iterator
        start_matches_iterator = template_start_regex.finditer(file_contents)

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
        end_matches_iterator = template_end_regex.finditer(file_contents)

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
        single_matches_iterator = template_single_regex.finditer(file_contents)

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

        # creates the match pairs list
        match_pairs_tree_root_node = TreeNode(("root", "root"))

        tree_node_stack = [match_pairs_tree_root_node]

        # iterates over all the matches in
        # the match orderer list
        for match_orderer in match_orderer_list:
            match_orderer_type = match_orderer.get_match_type()

            # in case the match order is of type start
            if match_orderer_type == START_VALUE:
                parent_tree_node = tree_node_stack[-1]
                match_pair_tree_node = CompositeTreeNode([match_orderer], parent_tree_node)
                parent_tree_node.get_childs().append(match_pair_tree_node)
                tree_node_stack.append(match_pair_tree_node)
            # in case the match order is of type end
            elif match_orderer_type == END_VALUE:
                match_pair_tree_node = tree_node_stack.pop()
                match_pair_tree_node.value.append(match_orderer)
                tuple(match_pair_tree_node.value)
            # in case the match order is of type single
            elif match_orderer_type == SINGLE_VALUE:
                parent_tree_node = tree_node_stack[-1]
                match_pair_tree_node = SingleTreeNode(match_orderer, parent_tree_node)
                parent_tree_node.get_childs().append(match_pair_tree_node)

        # iterates over all the match pairs tree root node child nodes
        for match_pairs_tree_root_node_child_node in match_pairs_tree_root_node.childs:
            self.visit_node(match_pairs_tree_root_node_child_node)

    def visit_node(self, node):
        # retrieves the node class
        node_class = node.__class__

        # in case the node is of type single tree node class
        if node_class == SingleTreeNode:
            single_match_value = node.value

            print "single: " + single_match_value.match_value
            print "type:   " + node.get_value_type()

            node_value_type = node.get_value_type()

            process_method = getattr(self, "process_" + node_value_type)

            process_method("", node)

        elif node_class == CompositeTreeNode:
            start_match_value, end_match_value = node.value

            print "start:  " + start_match_value.match_value
            print "end:    " + end_match_value.match_value
            print "type:   " + node.get_value_type()

            node_value_type = node.get_value_type()

            process_method = getattr(self, "process_" + node_value_type)

            for node_child in node.childs:
                self.visit_node(node_child)

    def process_out(self, inside_buffer, node):
        pass

    def process_var(self, inside_buffer, node):
        pass

    def process_foreach(self, inside_buffer, node):
        pass

    def process_foreach1(self, inside_buffer, node):
        pass

    def process_foreach2(self, inside_buffer, node):
        pass

    def process_foreach3(self, inside_buffer, node):
        pass

    def process_foreach4(self, inside_buffer, node):
        pass

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

class TreeNode:
    """
    The tree node class.
    """

    value = None
    """ The tree node value """

    parent = None
    """ The tree node parent node """

    childs = []
    """ The tree node child nodes """

    def __init__(self, value = None, parent = None):
        self.value = value
        self.parent = parent
        self.childs = []

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_parent(self):
        return self.childs

    def set_parent(self, parent):
        self.parent = parent

    def get_childs(self):
        return self.childs

    def set_childs(self, childs):
        self.childs = childs

class MatchTreeNode(TreeNode):
    """
    The match tree node class.
    """

    value_type = None
    """ The value type """

    attributes_map = {}
    """ The attributes map """

    def __init__(self, value = None, parent = None):
        TreeNode.__init__(self, value, parent)
        self.attributes_map = {}

        self.process_value_type()
        self.process_value_attributes()

    def process_value_type(self):
        # retrieve the start match value
        start_match_value = self.get_start_match_value()

        # retrieves the start match value match value
        start_match_value_match_value = start_match_value.get_match_value()

        # splits the start match value match value
        start_match_value_match_value_splitted = start_match_value_match_value.split()

        # retrieves the value type from the start match value match value splitted
        self.value_type = start_match_value_match_value_splitted[0][2:]

    def process_value_attributes(self):
        # retrieve the start match value
        start_match_value = self.get_start_match_value()

        # retrieves the start match value match value
        start_match_value_match_value = start_match_value.get_match_value()

        # creates the attribute regex
        attribute_regex = re.compile(ATTRIBUTE_VALUE)

        # creates the attribute quoted single regex
        attribute_quoted_regex = re.compile(ATTRIBUTE_QUOTED_VALUE)

        # finds all the attributes
        attributes = attribute_regex.findall(start_match_value_match_value)

        # finds all the attributes quoted
        attributes_quoted = attribute_quoted_regex.findall(start_match_value_match_value)

        for attribute in attributes:
            attribute_splitted = attribute.split("=")

            attribute_name, attribute_value = attribute_splitted

            self.attributes_map[attribute_name] = {"value" : attribute_value, type : "variable"}

        for attribute_quoted in attributes_quoted:
            attribute_quoted_splitted = attribute_quoted.split("=")

            attribute_quoted_name, attribute_quoted_value = attribute_quoted_splitted

            self.attributes_map[attribute_quoted_name] = {"value" : attribute_quoted_value, type : "literal"}

    def get_value_type(self):
        return self.value_type

    def set_value_type(self, value_type):
        self.value_type = value_type

    def get_value_type(self):
        return self.value_type

    def set_value_type(self, value_type):
        self.value_type = value_type

class SingleTreeNode(MatchTreeNode):
    """
    The single tree node class.
    """

    def __init__(self, value = None, parent = None):
        TreeNode.__init__(self, value, parent)

        self.attributes_map = {}

        self.process_value_type()
        self.process_value_attributes()

    def get_start_match_value(self):
        return self.value

class CompositeTreeNode(MatchTreeNode):
    """
    The composite tree node class.
    """

    def __init__(self, value = None, parent = None):
        MatchTreeNode.__init__(self, value, parent)

    def get_start_match_value(self):
        return self.value[0]
