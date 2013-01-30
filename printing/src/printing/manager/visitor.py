#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

import ast

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

            # unpacks the provided arguments to the decorator
            # to be used in the processing
            self_value = args[0]
            node_value = args[1]

            # retrieves the node value class and uses it to
            # get the associated mro structure to be used in
            # the values iteration
            node_value_class = node_value.__class__
            node_value_class_mro = node_value_class.mro()

            # iterates over all the node value class mro elements
            for node_value_class_mro_element in node_value_class_mro:
                # in case the node method map does not exists in
                # the current instance must continue the loop
                if not hasattr(self_value, "node_method_map"): continue

                # retrieves the node method map from the current instance
                # and verifies that the node value class exists in the
                # node method map, otherwise continues the loop
                node_method_map = getattr(self_value, "node_method_map")
                if not node_value_class_mro_element in node_method_map: continue

                # retrieves the correct visit method for the element and
                # then calls it "enclosed" by calls to the before and after
                # visit handler methods
                visit_method = node_method_map[node_value_class_mro_element]
                self_value.before_visit(*args[1:], **kwargs)
                visit_method(*args, **kwargs)
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

        # creates the decorator interceptor with the given
        # function (creating the clojure) and returns the
        # resulting function to the caller method
        decorator_interceptor_function = create_decorator_interceptor(function)
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
        print "AstNode: " + str(node)

    @_visit(ast.GenericElement)
    def visit_generic_element(self, node):
        print "GenericElement: " + str(node)

    @_visit(ast.PrintingDocument)
    def visit_printing_document(self, node):
        print "PrintingDocument: " + str(node)

    @_visit(ast.Block)
    def visit_block(self, node):
        print "Block: " + str(node)

    @_visit(ast.Paragraph)
    def visit_paragraph(self, node):
        print "Paragraph: " + str(node)

    @_visit(ast.Line)
    def visit_line(self, node):
        print "Line: " + str(node)

    @_visit(ast.Text)
    def visit_text(self, node):
        print "Text: " + str(node)

    @_visit(ast.Image)
    def visit_image(self, node):
        print "Image: " + str(node)
