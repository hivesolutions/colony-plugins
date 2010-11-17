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

import settler_query_ast

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

    visit_childs = True
    """ The visit childs flag """

    visit_next = True
    """ The visit next flag """

    def __init__(self):
        self.node_method_map = {}
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

    @dispatch_visit()
    def visit(self, node):
        print "unrecognized element node of type " + node.__class__.__name__

    def before_visit(self, node):
        self.visit_childs = True
        self.visit_next = True

    def after_visit(self, node):
        pass

    @_visit(settler_query_ast.AstNode)
    def visit_ast_node(self, node):
        print "AstNode: " + str(node)

    @_visit(settler_query_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        print "AstSequenceNode: " + str(node)

    @_visit(settler_query_ast.AstSequenceEndNode)
    def visit_ast_sequence_end_node(self, node):
        print "AstSequenceEndNode: " + str(node)

    @_visit(settler_query_ast.AstEnumerationNode)
    def visit_ast_enumeration_node(self, node):
        print "AstEnumerationNode: " + str(node)

    @_visit(settler_query_ast.RootNode)
    def visit_root_node(self, node):
        print "RootNode: " + str(node)

    @_visit(settler_query_ast.ProgramNode)
    def visit_program_node(self, node):
        print "ProgramNode: " + str(node)

    @_visit(settler_query_ast.StatementsNode)
    def visit_statements_node(self, node):
        print "StatementsNode: " + str(node)

    @_visit(settler_query_ast.StatementNode)
    def visit_statement_node(self, node):
        print "StatementNode: " + str(node)

    @_visit(settler_query_ast.PassNode)
    def visit_pass_node(self, node):
        print "PassNode: " + str(node)

    @_visit(settler_query_ast.SelectNode)
    def visit_select_node(self, node):
        print "SelectNode: " + str(node)

    @_visit(settler_query_ast.OptionalAllDistinctNode)
    def visit_optional_all_distinct_node(self, node):
        print "OptionalAllDistinctNode: " + str(node)

    @_visit(settler_query_ast.SelectionNode)
    def visit_selection_node(self, node):
        print "SelectionNode: " + str(node)

    @_visit(settler_query_ast.ScalarExpressionCommalistNode)
    def visit_scalar_expression_commalist_node(self, node):
        print "ScalarExpressionCommalistNode: " + str(node)

    @_visit(settler_query_ast.ScalarExpressionNode)
    def visit_scalar_expression_node(self, node):
        print "ScalarExpressionNode: " + str(node)

    @_visit(settler_query_ast.AtomScalarExpressionNode)
    def visit_atom_scalar_expression_node(self, node):
        print "AtomScalarExpressionNode: " + str(node)

    @_visit(settler_query_ast.FieldReferenceScalarExpressionNode)
    def visit_field_reference_scalar_expression_node(self, node):
        print "FieldReferenceScalarExpressionNode: " + str(node)

    @_visit(settler_query_ast.AtomNode)
    def visit_atom_node(self, node):
        print "AtomNode: " + str(node)

    @_visit(settler_query_ast.LiteralNode)
    def visit_literal_node(self, node):
        print "LiteralNode: " + str(node)

    @_visit(settler_query_ast.StringLiteralNode)
    def visit_string_literal_node(self, node):
        print "StringLiteralNode: " + str(node)

    @_visit(settler_query_ast.NumberLiteralNode)
    def visit_number_literal_node(self, node):
        print "NumberLiteralNode: " + str(node)

    @_visit(settler_query_ast.IntegerLiteralNode)
    def visit_integer_literal_node(self, node):
        print "IntegerLiteralNode: " + str(node)

    @_visit(settler_query_ast.FieldRefereceNode)
    def visit_field_reference_node(self, node):
        print "FieldRefereceNode: " + str(node)

    @_visit(settler_query_ast.EntityExpressionNode)
    def visit_entity_expression_node(self, node):
        print "EntityExpressionNode: " + str(node)

    @_visit(settler_query_ast.FromClauseNode)
    def visit_from_clause_node(self, node):
        print "FromClauseNode: " + str(node)

    @_visit(settler_query_ast.EntityReferenceCommalistNode)
    def visit_entity_reference_commalist_node(self, node):
        print "EntityReferenceCommalistNode: " + str(node)

    @_visit(settler_query_ast.EntityReferenceNode)
    def visit_entity_reference_node(self, node):
        print "EntityReferenceNode: " + str(node)

    @_visit(settler_query_ast.EntityNode)
    def visit_entity_node(self, node):
        print "EntityNode: " + str(node)

    @_visit(settler_query_ast.EntityAsNameNode)
    def visit_entity_as_name_node(self, node):
        print "EntityAsNameNode: " + str(node)

    @_visit(settler_query_ast.QualifiedEntityNameNode)
    def visit_qualified_entity_name_node(self, node):
        print "QualifiedEntityNameNode: " + str(node)

    @_visit(settler_query_ast.OptionalWhereClauseNode)
    def visit_optional_where_clause_node(self, node):
        print "OptionalWhereClauseNode: " + str(node)

    @_visit(settler_query_ast.WhereClauseNode)
    def visit_where_clause_node(self, node):
        print "WhereClauseNode: " + str(node)

    @_visit(settler_query_ast.SearchConditionNode)
    def visit_search_condition_node(self, node):
        print "SearchConditionNode: " + str(node)

    @_visit(settler_query_ast.PredicateSearchConditionNode)
    def visit_predicate_search_condition_node(self, node):
        print "PredicateSearchConditionNode: " + str(node)

    @_visit(settler_query_ast.ExpressionSearchConditionNode)
    def visit_expression_search_condition_node(self, node):
        print "ExpressionSearchConditionNode: " + str(node)

    @_visit(settler_query_ast.BinaryExpressionSearchConditionNode)
    def visit_binary_wxpression_search_condition_node(self, node):
        print "BinaryExpressionSearchConditionNode: " + str(node)

    @_visit(settler_query_ast.AndExpressionSearchConditionNode)
    def visit_and_expression_search_condition_node(self, node):
        print "AndExpressionSearchConditionNode: " + str(node)

    @_visit(settler_query_ast.OrExpressionSearchConditionNode)
    def visit_or_expression_search_condition_node(self, node):
        print "OrExpressionSearchConditionNode: " + str(node)

    @_visit(settler_query_ast.UnaryExpressionSearchConditionNode)
    def visit_unary_expression_search_condition_node(self, node):
        print "UnaryExpressionSearchConditionNode: " + str(node)

    @_visit(settler_query_ast.NotExpressionSearchConditionNode)
    def visit_not_expression_search_condition_node(self, node):
        print "NotExpressionSearchConditionNode: " + str(node)

    @_visit(settler_query_ast.ParenthesisExpressionSearchConditionNode)
    def visit_parenthesis_expression_search_condition_node(self, node):
        print "ParenthesisExpressionSearchConditionNode: " + str(node)

    @_visit(settler_query_ast.PredicateNode)
    def visit_predicate_node(self, node):
        print "PredicateNode: " + str(node)

    @_visit(settler_query_ast.BinaryPredicateNode)
    def visit_binary_predicate_node(self, node):
        print "BinaryPredicateNode: " + str(node)

    @_visit(settler_query_ast.ComparisonPredicateNode)
    def visit_comparison_predicate_node(self, node):
        print "ComparisonPredicateNode: " + str(node)

    @_visit(settler_query_ast.EqualComparisonPredicateNode)
    def visit_equal_comparison_predicate_node(self, node):
        print "EqualComparisonPredicateNode: " + str(node)

    @_visit(settler_query_ast.GreaterComparisonPredicateNode)
    def visit_greater_comparison_predicate_node(self, node):
        print "GreaterComparisonPredicateNode: " + str(node)

    @_visit(settler_query_ast.GreaterEqualComparisonPredicateNode)
    def visit_greater_equal_comparison_predicate_node(self, node):
        print "GreaterEqualComparisonPredicateNode: " + str(node)

    @_visit(settler_query_ast.BetweenPredicateNode)
    def visit_between_predicate_node(self, node):
        print "BetweenPredicateNode: " + str(node)

    @_visit(settler_query_ast.NotBetweenPredicateNode)
    def visit_not_between_predicate_node(self, node):
        print "NotBetweenPredicateNode: " + str(node)

    @_visit(settler_query_ast.LikePredicateNode)
    def visit_like_predicate_node(self, node):
        print "LikePredicateNode: " + str(node)

    @_visit(settler_query_ast.NotLikePredicateNode)
    def visit_not_like_predicate_node(self, node):
        print "NotLikePredicateNode: " + str(node)

    @_visit(settler_query_ast.UnaryPredicateNode)
    def visit_unary_predicate_node(self, node):
        print "UnaryPredicateNode: " + str(node)

    @_visit(settler_query_ast.IsNullPredicateNode)
    def visit_is_null_predicate_node(self, node):
        print "IsNullPredicateNode: " + str(node)

    @_visit(settler_query_ast.IsNotNullPredicateNode)
    def visit_is_not_null_predicate_node(self, node):
        print "IsNotNullPredicateNode: " + str(node)

    @_visit(settler_query_ast.InPredicateNode)
    def visit_in_predicate_node(self, node):
        print "InPredicateNode: " + str(node)

    @_visit(settler_query_ast.NotInPredicateNode)
    def visit_not_in_predicate_node(self, node):
        print "NotInPredicateNode: " + str(node)

    @_visit(settler_query_ast.InSubqueryPredicateNode)
    def visit_in_subquery_predicate_node(self, node):
        print "InSubqueryPredicateNode: " + str(node)

    @_visit(settler_query_ast.NotInSubqueryPredicateNode)
    def visit_not_in_subquery_predicate_node(self, node):
        print "NotInSubqueryPredicateNode: " + str(node)

    @_visit(settler_query_ast.AllOrAnyPredicateNode)
    def visit_all_or_any_predicate_node(self, node):
        print "AllOrAnyPredicateNode: " + str(node)

    @_visit(settler_query_ast.AnyAllSomeNode)
    def visit_any_all_some_node(self, node):
        print "AnyAllSomeNode: " + str(node)

    @_visit(settler_query_ast.ExistenceTestNode)
    def visit_existence_test_node(self, node):
        print "ExistenceTestNode: " + str(node)

    @_visit(settler_query_ast.ScalarExpressionPredicateNode)
    def visit_scalar_expression_predicate_node(self, node):
        print "ScalarExpressionPredicateNode: " + str(node)

    @_visit(settler_query_ast.SubqueryNode)
    def visit_subquery_node(self, node):
        print "SubqueryNode: " + str(node)
