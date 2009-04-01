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

import settler_visitor

class SemanticVisitor(settler_visitor.Visitor):
    """
    The semantic visitor class.
    """

    processing_structure = None
    """ The processing structure """

    def __init__(self):
        settler_visitor.Visitor.__init__(self)

    def set_processing_structure(self, processing_structure):
        self.processing_structure = processing_structure

    @_visit(settler_ast.AstNode)
    def visit_ast_node(self, node):
        print "AstNode: " + str(node)

    @_visit(settler_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        print "AstSequenceNode: " + str(node)

    @_visit(settler_ast.RootNode)
    def visit_root_node(self, node):
        print "RootNode: " + str(node)

    @_visit(settler_ast.AssignNode)
    def visit_assign_node(self, node):
        print "AssignNode: " + str(node)

    @_visit(settler_ast.ExpressionNode)
    def visit_expression_node(self, node):
        print "ExpressionNode: " + str(node)

    @_visit(settler_ast.NumberExpressionNode)
    def visit_number_expression_node(self, node):
        print "NumberExpressionNode: " + str(node)

    @_visit(settler_ast.IntegerExpressionNode)
    def visit_integer_expression_node(self, node):
        print "IntegerExpressionNode: " + str(node)

    @_visit(settler_ast.BoolExpressionNode)
    def visit_bool_expression_node(self, node):
        print "BoolExpressionNode: " + str(node)

    @_visit(settler_ast.NameExpressionNode)
    def visit_name_expression_node(self, node):
        print "NameExpressionNode: " + str(node)

    @_visit(settler_ast.UnaryExpressionNode)
    def visit_unary_expression_node(self, node):
        print "UnaryExpressionNode: " + str(node)

    @_visit(settler_ast.BinaryExpressionNode)
    def visit_binary_expression_node(self, node):
        print "BinaryExpressionNode: " + str(node)

    @_visit(settler_ast.ArithmethicExpressionNode)
    def visit_arithmethic_expression_node(self, node):
        print "ArithmethicExpressionNode: " + str(node)

    @_visit(settler_ast.SummationExpressionNode)
    def visit_summation_expression_node(self, node):
        print "SummationExpressionNode: " + str(node)

    @_visit(settler_ast.SubtractionExpressionNode)
    def visit_subtraction_expression_node(self, node):
        print "SubtractionExpressionNode: " + str(node)

    @_visit(settler_ast.MultiplicationExpressionNode)
    def visit_multiplication_expression_node(self, node):
        print "MultiplicationExpressionNode: " + str(node)

    @_visit(settler_ast.DivisionExpressionNode)
    def visit_division_expression_node(self, node):
        print "DivisionExpressionNode: " + str(node)

    @_visit(settler_ast.PowerExpressionNode)
    def visit_power_expression_node(self, node):
        print "PowerExpressionNode: " + str(node)

    @_visit(settler_ast.BooleanExpressionNode)
    def visit_boolean_expression_node(self, node):
        print "BooleanExpressionNode: " + str(node)

    @_visit(settler_ast.EqualExpressionNode)
    def visit_equal_expression_node(self, node):
        print "EqualExpressionNode: " + str(node)

    @_visit(settler_ast.GreaterExpressionNode)
    def visit_greater_expression_node(self, node):
        print "GreaterExpressionNode: " + str(node)

    @_visit(settler_ast.GreaterEqualExpressionNode)
    def visit_greater_equal_expression_node(self, node):
        print "GreaterEqualExpressionNode: " + str(node)

    @_visit(settler_ast.AndExpressionNode)
    def visit_and_expression_node(self, node):
        print "AndExpressionNode: " + str(node)

    @_visit(settler_ast.OrExpressionNode)
    def visit_or_expression_node(self, node):
        print "OrExpressionNode: " + str(node)

    @_visit(settler_ast.NotExpressionNode)
    def visit_not_expression_node(self, node):
        print "NotExpressionNode: " + str(node)

    @_visit(settler_ast.ParenthesisExpressionNode)
    def visit_parenthesis_expression_node(self, node):
        print "ParenthesisExpressionNode: " + str(node)

    @_visit(settler_ast.NegativeExpressionNode)
    def visit_negative_expression_node(self, node):
        print "NegativeExpressionNode: " + str(node)

    @_visit(settler_ast.FunctionNode)
    def visit_function_node(self, node):
        print "FunctionNode: " + str(node)

    @_visit(settler_ast.ArgumentsNode)
    def visit_arguments_node(self, node):
        print "ArgumentsNode: " + str(node)

    @_visit(settler_ast.ArgumentNode)
    def visit_argument_node(self, node):
        print "ArgumentNode: " + str(node)

    @_visit(settler_ast.DefaultValueArgumentNode)
    def visit_default_argument_node(self, node):
        print "DefaultValueArgumentNode: " + str(node)
