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

import settler_query_visitor
import settler_query_ast

class QueryStructuresGenerationVisitor(settler_query_visitor.Visitor):
    """
    The query structures generation visitor class.
    """

    def __init__(self):
        settler_query_visitor.Visitor.__init__(self)

    @settler_query_visitor._visit(settler_query_ast.AstNode)
    def visit_ast_node(self, node):
        print "AstNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        print "AstSequenceNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.AstSequenceEndNode)
    def visit_ast_sequence_end_node(self, node):
        print "AstSequenceEndNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.AstEnumerationNode)
    def visit_ast_enumeration_node(self, node):
        print "AstEnumerationNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.RootNode)
    def visit_root_node(self, node):
        print "RootNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.ProgramNode)
    def visit_program_node(self, node):
        print "ProgramNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.StatementsNode)
    def visit_statements_node(self, node):
        print "StatementsNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.StatementNode)
    def visit_statement_node(self, node):
        print "StatementNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.PassNode)
    def visit_pass_node(self, node):
        print "PassNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.SelectNode)
    def visit_select_node(self, node):
        print "SelectNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.OptionalAllDistinctNode)
    def visit_optional_all_distinct_node(self, node):
        print "OptionalAllDistinctNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.SelectionNode)
    def visit_selection_node(self, node):
        print "SelectionNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.ScalarExpressionCommalistNode)
    def visit_scalar_expression_commalist_node(self, node):
        print "ScalarExpressionCommalistNode: " + str(node)

    @settler_query_visitor._visit(settler_query_ast.ScalarExpressionNode)
    def visit_scalar_expression_node(self, node):
        print "ScalarExpressionNode: " + str(node)
