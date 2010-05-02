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

import sys

import javascript_documentation_ast
import javascript_documentation_visitor

COLONY_DOCUMENTATION_PATH = "../../../../pt.hive.colony.documentation/src/colony"
""" The colony documentation path """

# appends the colony language generator path
sys.path.append(COLONY_DOCUMENTATION_PATH)

# imports the colony documentation
import documentation.documentation_ast

class JavascriptDocumentationGenerationVisitor(javascript_documentation_visitor.Visitor):
    """
    The javascript documentation generation visitor class.
    """

    documentation_project_node = None
    """ The documentation project node """

    current_element_node_stack = []
    """ The current element node stack """

    current_comment_node = None
    """ The current comment node """

    def __init__(self):
        javascript_documentation_visitor.Visitor.__init__(self)

        # starts the current element node stack
        self.current_element_node_stack = []

        # creates a new documentation project node
        self.documentation_project_node = documentation.documentation_ast.ProjectNode()

    def get_documentation_project_node(self):
        """
        Retrieves the documentation project node.

        @rtype: ProjectNode
        @return: The documentation project node.
        """

        return self.documentation_project_node

    def set_documentation_project_node(self, documentation_project_node):
        """
        Sets the documentation project node.

        @type documentation_project_node: ProjectNode
        @param documentation_project_node: The documentation project node.
        """

        self.documentation_project_node = documentation_project_node

    @javascript_documentation_visitor._visit(javascript_documentation_ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.RootNode)
    def visit_root_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ProgramNode)
    def visit_program_node(self, node):
        if self.visit_index == 0:
            self.current_element_node_stack.append(self.documentation_project_node)
        elif self.visit_index == 1:
            self.current_element_node_stack.pop()

    @javascript_documentation_visitor._visit(javascript_documentation_ast.StatementsNode)
    def visit_statements_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.StatementNode)
    def visit_statement_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.CommentNode)
    def visit_comment_node(self, node):
        # sets the current comment node
        self.current_comment_node = node

    @javascript_documentation_visitor._visit(javascript_documentation_ast.PassNode)
    def visit_pass_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.AssignNode)
    def visit_assign_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ReturnNode)
    def visit_return_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.GlobalNode)
    def visit_global_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.IfConditionNode)
    def visit_if_condition_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ElseConditionNode)
    def visit_else_condition_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ElseIfConditionNode)
    def visit_else_if_condition_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.WhileNode)
    def visit_while_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ForNode)
    def visit_for_node_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ExpressionNode)
    def visit_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.NumberExpressionNode)
    def visit_num_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.IntegerExpressionNode)
    def visit_integer_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.StringExpressionNode)
    def visit_string_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.BoolExpressionNode)
    def visit_bool_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.NameExpressionNode)
    def visit_name_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ListExpressionNode)
    def visit_list_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ListContentsNode)
    def visit_list_contents_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.UnaryExpressionNode)
    def visit_unary_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.BinaryExpressionNode)
    def visit_binary_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ArithmethicExpressionNode)
    def visit_arithmethic_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.SummationExpressionNode)
    def visit_summation_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.SubtractionExpressionNode)
    def visit_subtraction_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.MultiplicationExpressionNode)
    def visit_multiplication_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.DivisionExpressionNode)
    def visit_division_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.PowerExpressionNode)
    def visit_power_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.BooleanExpressionNode)
    def visit_boolean_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.EqualExpressionNode)
    def visit_equal_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.GreaterExpressionNode)
    def visit_greater_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.GreaterEqualExpressionNode)
    def visit_greater_equal_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.AndExpressionNode)
    def visit_and_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.OrExpressionNode)
    def visit_or_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.NotExpressionNode)
    def visit_not_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ParenthesisExpressionNode)
    def visit_parenthesis_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.NegativeExpressionNode)
    def visit_negative_expression_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.NameReferenceNode)
    def visit_name_reference_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ImportNode)
    def visit_import_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.FunctionNode)
    def visit_function_node(self, node):
        if self.visit_index == 0:
            # retrieves the current comment node
            current_comment_node = self.current_comment_node

            # creates a new function node
            function_node = documentation.documentation_ast.FunctionNode()

            # sets the name in the function node
            function_node.set_name(node.function_name)

            # sets the name in the function node
            function_node.set_description(current_comment_node.comment_value)

            self.current_element_node_stack[-1].add_child_node(function_node)

            self.current_element_node_stack.append(function_node)
        elif self.visit_index == 1:
            self.current_element_node_stack.pop()

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ArgumentsNode)
    def visit_arguments_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ArgumentNode)
    def visit_argument_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.DefaultValueArgumentNode)
    def visit_default_argument_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.FunctionCallNode)
    def visit_function_call_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ArgumentValuesNode)
    def visit_argument_values_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ArgumentValueNode)
    def visit_argument_value_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ClassNode)
    def visit_class_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ExtendsNode)
    def visit_extends_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ExtendsValuesNode)
    def visit_extends_values_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ImplementsNode)
    def visit_implements_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.ImplementsValuesNode)
    def visit_implements_values_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.InterfaceNode)
    def visit_interface_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.PluginNode)
    def visit_plugin_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.AllowsNode)
    def visit_allows_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.AllowsValuesNode)
    def visit_allows_values_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.CapabilityNode)
    def visit_capability_node(self, node):
        pass

    @javascript_documentation_visitor._visit(javascript_documentation_ast.SpaceNode)
    def visit_space_node(self, node):
        pass
