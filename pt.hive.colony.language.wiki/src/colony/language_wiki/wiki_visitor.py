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

import wiki_ast

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

    visit_childs = True
    """ The visit childs flag """

    visit_next = True
    """ The visit next flag """

    visit_index = 0
    """ The visit index, for multiple visits """

    parser = None
    """ The parser """

    def __init__(self):
        self.node_method_map = {}
        self.visit_childs = True
        self.visit_next = True
        self.visit_index = 0

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

    def get_parser(self):
        """
        Retrieves the parser.

        @rtype: Parser
        @return: The parser.
        """

        return self.parser

    def set_parser(self, parser):
        """
        Sets the parser.

        @type parser: Parser
        @param parser: The parser.
        """

        self.parser = parser

    def clone(self):
        """
        Clones the visitor.

        @rtype: Visitor
        @return: The cloned visitor.
        """

        # clones the current visitor
        cloned_visitor = self.__class__()

        # sets the visitor attributes in the cloned visitor
        cloned_visitor.set_parser(self.parser)

        # returns the cloned visitor
        return cloned_visitor

    @dispatch_visit()
    def visit(self, node):
        print "unrecognized element node of type " + node.__class__.__name__

    def before_visit(self, node):
        self.visit_childs = True
        self.visit_next = True

    def after_visit(self, node):
        pass

    @_visit(wiki_ast.AstNode)
    def visit_ast_node(self, node):
        print "AstNode: " + str(node)

    @_visit(wiki_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        print "AstSequenceNode: " + str(node)

    @_visit(wiki_ast.RootNode)
    def visit_root_node(self, node):
        print "RootNode: " + str(node)

    @_visit(wiki_ast.ProgramNode)
    def visit_program_node(self, node):
        print "ProgramNode: " + str(node)

    @_visit(wiki_ast.StatementsNode)
    def visit_statements_node(self, node):
        print "StatementsNode: " + str(node)

    @_visit(wiki_ast.StatementNode)
    def visit_statement_node(self, node):
        print "StatementNode: " + str(node)

    @_visit(wiki_ast.DecorationNode)
    def visit_decoration_node(self, node):
        print "DecorationNode: " + str(node)

    @_visit(wiki_ast.BoldNode)
    def visit_bold_node(self, node):
        print "BoldNode: " + str(node)

    @_visit(wiki_ast.ItalicNode)
    def visit_italic_node(self, node):
        print "ItalicNode: " + str(node)

    @_visit(wiki_ast.UnderlineNode)
    def visit_underline_node(self, node):
        print "UnderlineNode: " + str(node)

    @_visit(wiki_ast.MonospaceNode)
    def visit_monospace_node(self, node):
        print "MonospaceNode: " + str(node)

    @_visit(wiki_ast.SectionNode)
    def visit_section_node(self, node):
        print "SectionNode: " + str(node)

    @_visit(wiki_ast.NameNode)
    def visit_name_node(self, node):
        print "NameNode: " + str(node)

    @_visit(wiki_ast.NewLineNode)
    def visit_new_line_node(self, node):
        print "NewLineNode: " + str(node)

    @_visit(wiki_ast.SpaceNode)
    def visit_space_node(self, node):
        print "SpaceNode: " + str(node)

    @_visit(wiki_ast.ImageNode)
    def visit_image_node(self, node):
        print "ImageNode: " + str(node)

    @_visit(wiki_ast.LinkNode)
    def visit_link_node(self, node):
        print "LinkNode: " + str(node)

    @_visit(wiki_ast.ExternalLinkNode)
    def visit_external_link_node(self, node):
        print "ExternalLinkNode: " + str(node)

    @_visit(wiki_ast.InternalLinkNode)
    def visit_internal_link_node(self, node):
        print "InternalLinkNode: " + str(node)

    @_visit(wiki_ast.ListNode)
    def visit_list_node(self, node):
        print "ListNode: " + str(node)

    @_visit(wiki_ast.BulletListNode)
    def visit_bullet_list_node(self, node):
        print "BulletListNode: " + str(node)

    @_visit(wiki_ast.OrderedListNode)
    def visit_ordered_list_node(self, node):
        print "OrderedListNode: " + str(node)

    @_visit(wiki_ast.TagNode)
    def visit_tag_node(self, node):
        print "TagNode: " + str(node)
