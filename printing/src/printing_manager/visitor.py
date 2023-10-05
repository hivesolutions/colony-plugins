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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import ast

class Visitor(object):
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

            # in case the current class real element does not contain
            # an AST node class reference must continue the loop
            if not hasattr(self_class_real_element, "ast_node_class"): continue

            # retrieves the AST node class from the current class real element
            # and sets it in the node method map
            ast_node_class = getattr(self_class_real_element, "ast_node_class")
            self.node_method_map[ast_node_class] = self_class_real_element

    @colony.dispatch_visit()
    def visit(self, node):
        print("unrecognized element node of type " + node.__class__.__name__)

    def before_visit(self, node):
        self.visit_childs = True
        self.visit_next = True

    def after_visit(self, node):
        pass

    @colony.visit(ast.AstNode)
    def visit_ast_node(self, node):
        print("AstNode: " + str(node))

    @colony.visit(ast.GenericElement)
    def visit_generic_element(self, node):
        print("GenericElement: " + str(node))

    @colony.visit(ast.PrintingDocument)
    def visit_printing_document(self, node):
        print("PrintingDocument: " + str(node))

    @colony.visit(ast.Block)
    def visit_block(self, node):
        print("Block: " + str(node))

    @colony.visit(ast.Paragraph)
    def visit_paragraph(self, node):
        print("Paragraph: " + str(node))

    @colony.visit(ast.Line)
    def visit_line(self, node):
        print("Line: " + str(node))

    @colony.visit(ast.Text)
    def visit_text(self, node):
        print("Text: " + str(node))

    @colony.visit(ast.Image)
    def visit_image(self, node):
        print("Image: " + str(node))
