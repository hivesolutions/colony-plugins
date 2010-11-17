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

import settler_ast

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
        @param: The decorator interceptor function.
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
        @param: The decorator interceptor function.
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

    current_context_stack = ["global"]
    """ The current context stack """

    current_context_type_stack = ["function"]
    """ The current context type stack """

    visit_childs = True
    """ The visit childs flag """

    visit_next = True
    """ The visit next flag """

    def __init__(self):
        self.node_method_map = {}
        self.current_context_stack = ["global"]
        self.current_context_type_stack = ["global"]
        self.visit_childs = True
        self.visit_next = True

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

    def get_current_context(self):
        return self.current_context_stack[-1]

    def pop_current_context(self):
        self.current_context_stack.pop()

    def push_current_context(self, context):
        self.current_context_stack.append(context)

    def get_current_context_type(self):
        return self.current_context_type_stack[-1]

    def get_current_context_type_stack(self):
        return self.current_context_type_stack

    def pop_current_context_type(self, node):
        self.current_context_type_stack.pop()

    def push_current_context_type(self, context_type, node):
        self.current_context_type_stack.append(context_type)

    def valid_context_type(self, context_type, node):
        return True

    @dispatch_visit()
    def visit(self, node):
        print "unrecognized element node of type " + node.__class__.__name__

    def before_visit(self, node):
        self.visit_childs = True
        self.visit_next = True

    def after_visit(self, node):
        pass

    @_visit(settler_ast.AstNode)
    def visit_ast_node(self, node):
        print "AstNode: " + str(node)

    @_visit(settler_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        print "AstSequenceNode: " + str(node)

    @_visit(settler_ast.RootNode)
    def visit_root_node(self, node):
        print "RootNode: " + str(node)

    @_visit(settler_ast.ProgramNode)
    def visit_program_node(self, node):
        print "ProgramNode: " + str(node)

    @_visit(settler_ast.StatementsNode)
    def visit_statements_node(self, node):
        print "StatementsNode: " + str(node)

    @_visit(settler_ast.StatementNode)
    def visit_statement_node(self, node):
        print "StatementNode: " + str(node)

    @_visit(settler_ast.PassNode)
    def visit_pass_node(self, node):
        print "PassNode: " + str(node)

    @_visit(settler_ast.AssignNode)
    def visit_assign_node(self, node):
        print "AssignNode: " + str(node)

    @_visit(settler_ast.ReturnNode)
    def visit_return_node(self, node):
        print "ReturnNode: " + str(node)

    @_visit(settler_ast.GlobalNode)
    def visit_global_node(self, node):
        print "GlobalNode: " + str(node)

    @_visit(settler_ast.IfConditionNode)
    def visit_if_condition_node(self, node):
        print "IfConditionNode: " + str(node)

    @_visit(settler_ast.ElseConditionNode)
    def visit_else_condition_node(self, node):
        print "ElseConditionNode: " + str(node)

    @_visit(settler_ast.ElseIfConditionNode)
    def visit_else_if_condition_node(self, node):
        print "ElseIfConditionNode: " + str(node)

    @_visit(settler_ast.WhileNode)
    def visit_while_node(self, node):
        print "WhileNode: " + str(node)

    @_visit(settler_ast.ForNode)
    def visit_for_node_node(self, node):
        print "ForNode: " + str(node)

    @_visit(settler_ast.ExpressionNode)
    def visit_expression_node(self, node):
        print "ExpressionNode: " + str(node)

    @_visit(settler_ast.NumberExpressionNode)
    def visit_num_expression_node(self, node):
        print "NumberExpressionNode: " + str(node)

    @_visit(settler_ast.IntegerExpressionNode)
    def visit_integer_expression_node(self, node):
        print "IntegerExpressionNode: " + str(node)

    @_visit(settler_ast.StringExpressionNode)
    def visit_string_expression_node(self, node):
        print "StringExpressionNode: " + str(node)

    @_visit(settler_ast.BoolExpressionNode)
    def visit_bool_expression_node(self, node):
        print "BoolExpressionNode: " + str(node)

    @_visit(settler_ast.NameExpressionNode)
    def visit_name_expression_node(self, node):
        print "NameExpressionNode: " + str(node)

    @_visit(settler_ast.ListExpressionNode)
    def visit_list_expression_node(self, node):
        print "ListExpressionNode: " + str(node)

    @_visit(settler_ast.ListContentsNode)
    def visit_list_contents_node(self, node):
        print "ListContentsNode: " + str(node)

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

    @_visit(settler_ast.NameReferenceNode)
    def visit_name_reference_node(self, node):
        print "NameReferenceNode: " + str(node)

    @_visit(settler_ast.ImportNode)
    def visit_import_node(self, node):
        print "ImportNode: " + str(node)

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

    @_visit(settler_ast.FunctionCallNode)
    def visit_function_call_node(self, node):
        print "FunctionCallNode: " + str(node)

    @_visit(settler_ast.ArgumentValuesNode)
    def visit_argument_values_node(self, node):
        print "ArgumentValuesNode: " + str(node)

    @_visit(settler_ast.ArgumentValueNode)
    def visit_argument_value_node(self, node):
        print "ArgumentValueNode: " + str(node)

    @_visit(settler_ast.ClassNode)
    def visit_class_node(self, node):
        print "ClassNode: " + str(node)

    @_visit(settler_ast.ExtendsNode)
    def visit_extends_node(self, node):
        print "ExtendsNode: " + str(node)

    @_visit(settler_ast.ExtendsValuesNode)
    def visit_extends_values_node(self, node):
        print "ExtendsValuesNode: " + str(node)

    @_visit(settler_ast.ImplementsNode)
    def visit_implements_node(self, node):
        print "ImplementsNode: " + str(node)

    @_visit(settler_ast.ImplementsValuesNode)
    def visit_implements_values_node(self, node):
        print "ImplementsValuesNode: " + str(node)

    @_visit(settler_ast.InterfaceNode)
    def visit_interface_node(self, node):
        print "InterfaceNode: " + str(node)

    @_visit(settler_ast.PluginNode)
    def visit_plugin_node(self, node):
        print "PluginNode: " + str(node)

    @_visit(settler_ast.AllowsNode)
    def visit_allows_node(self, node):
        print "AllowsNode: " + str(node)

    @_visit(settler_ast.AllowsValuesNode)
    def visit_allows_values_node(self, node):
        print "AllowsValuesNode: " + str(node)

    @_visit(settler_ast.CapabilityNode)
    def visit_capability_node(self, node):
        print "CapabilityNode: " + str(node)
