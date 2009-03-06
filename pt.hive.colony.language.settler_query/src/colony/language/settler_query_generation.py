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

import settler_query_structures
import settler_query_visitor
import settler_query_ast

class QueryStructuresGenerationVisitor(settler_query_visitor.Visitor):
    """
    The query structures generation visitor class.
    """

    query = None
    """ The query """

    context_information_stack = []
    """ The context information stack """

    context_information_map = {}
    """ The context information map """

    context_element_stack = []
    """ The context element stack """

    def __init__(self):
        settler_query_visitor.Visitor.__init__(self)

        self.context_information_stack = []
        self.context_information_map = {}
        self.context_element_stack = []

    def add_context(self, context_name):
        self.context_information_stack.append(context_name)
        self.context_information_map[context_name] = True

    def is_valid_context(self, context_name):
        return self.context_information_map.get(context_name, False)

    def is_sublcass_node(self, node, super_class):
        # retrieves the node class
        node_class = node.__class__

        # retrieves the mro list from the node class
        node_class_mro = node_class.mro()

        # iterates over all the node class mro elements
        for node_class_mro_element in node_class_mro:
            if node_class_mro_element == super_class:
                return True

        return False

    @settler_query_visitor._visit(settler_query_ast.AstNode)
    def visit_ast_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.AstSequenceNode)
    def visit_ast_sequence_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.AstSequenceEndNode)
    def visit_ast_sequence_end_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.AstEnumerationNode)
    def visit_ast_enumeration_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.RootNode)
    def visit_root_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.ProgramNode)
    def visit_program_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.StatementsNode)
    def visit_statements_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.StatementNode)
    def visit_statement_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.PassNode)
    def visit_pass_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.SelectNode)
    def visit_select_node(self, node):
        self.query = settler_query_structures.SelectQuery()

        for context_element in self.context_element_stack:
            if context_element.__class__ == settler_query_structures.SimpleField:
                self.query.select_fields.append(context_element)
            elif context_element.__class__ == settler_query_structures.SimpleEntity:
                self.query.select_entities.append(context_element)
            elif self.is_sublcass_node(context_element, settler_query_structures.Filter):
                self.query.select_filters.append(context_element)

        self.context_element_stack = []

    @settler_query_visitor._visit(settler_query_ast.OptionalAllDistinctNode)
    def visit_optional_all_distinct_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.SelectionNode)
    def visit_selection_node(self, node):
        self.add_context("selection")

    @settler_query_visitor._visit(settler_query_ast.ScalarExpressionCommalistNode)
    def visit_scalar_expression_commalist_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.ScalarExpressionNode)
    def visit_scalar_expression_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.AtomScalarExpressionNode)
    def visit_atom_scalar_expression_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.FieldReferenceScalarExpressionNode)
    def visit_field_reference_scalar_expression_node(self, node):
        if self.is_valid_context("selection"):
            # creates the simple field reference instance
            simple_field_reference = settler_query_structures.SimpleFieldReference()
        else:
            # creates the simple field instance
            simple_field_reference = settler_query_structures.SimpleField()

        # sets the simple filed reference field name
        simple_field_reference.field_name = node.field_reference_node.field_reference_name

        # appends the simple field reference to the context element stack
        self.context_element_stack.append(simple_field_reference)

    @settler_query_visitor._visit(settler_query_ast.AtomNode)
    def visit_atom_node(self, node):
        # creates the value instance
        value = settler_query_structures.Value()

        # sets the value value
        value.value = self.context_element_stack.pop()

        self.context_element_stack.append(value)

    @settler_query_visitor._visit(settler_query_ast.LiteralNode)
    def visit_literal_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.StringLiteralNode)
    def visit_string_literal_node(self, node):
        self.context_element_stack.append(node.string_value)

    @settler_query_visitor._visit(settler_query_ast.NumberLiteralNode)
    def visit_number_literal_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.IntegerLiteralNode)
    def visit_integer_literal_node(self, node):
        self.context_element_stack.append(node.integer_value)

    @settler_query_visitor._visit(settler_query_ast.FieldRefereceNode)
    def visit_field_reference_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.EntityExpressionNode)
    def visit_entity_expression_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.FromClauseNode)
    def visit_from_clause_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.EntityReferenceCommalistNode)
    def visit_entity_reference_commalist_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.EntityReferenceNode)
    def visit_entity_reference_node(self, node):
        # creates the simple entity instance
        simple_entity = settler_query_structures.SimpleEntity()

        # sets the simple entity entity name
        simple_entity.entity_name = node.entity_node.qualified_entity_name_node.qualified_entity_name_value

        # appends the simple entity to the context element stack
        self.context_element_stack.append(simple_entity)

    @settler_query_visitor._visit(settler_query_ast.EntityNode)
    def visit_entity_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.EntityAsNameNode)
    def visit_entity_as_name_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.QualifiedEntityNameNode)
    def visit_qualified_entity_name_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.OptionalWhereClauseNode)
    def visit_optional_where_clause_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.WhereClauseNode)
    def visit_where_clause_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.SearchConditionNode)
    def visit_search_condition_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.PredicateSearchConditionNode)
    def visit_predicate_search_condition_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.ExpressionSearchConditionNode)
    def visit_expression_search_condition_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.BinaryExpressionSearchConditionNode)
    def visit_binary_wxpression_search_condition_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.AndExpressionSearchConditionNode)
    def visit_and_expression_search_condition_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.OrExpressionSearchConditionNode)
    def visit_or_expression_search_condition_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.UnaryExpressionSearchConditionNode)
    def visit_unary_expression_search_condition_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.NotExpressionSearchConditionNode)
    def visit_not_expression_search_condition_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.ParenthesisExpressionSearchConditionNode)
    def visit_parenthesis_expression_search_condition_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.PredicateNode)
    def visit_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.BinaryPredicateNode)
    def visit_binary_predicate_node(self, node):
        binary_term_filter = self.context_element_stack.pop()

        binary_term_filter.second_operand = self.context_element_stack.pop()
        binary_term_filter.first_operand = self.context_element_stack.pop()

        self.context_element_stack.append(binary_term_filter)

    @settler_query_visitor._visit(settler_query_ast.ComparisonPredicateNode)
    def visit_comparison_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.EqualComparisonPredicateNode)
    def visit_equal_comparison_predicate_node(self, node):
        equal_term_filter = settler_query_structures.EqualTermFilter()

        self.context_element_stack.append(equal_term_filter)

        self.visit_binary_predicate_node(node)

    @settler_query_visitor._visit(settler_query_ast.GreaterComparisonPredicateNode)
    def visit_greater_comparison_predicate_node(self, node):
        greater_term_filter = settler_query_structures.GreaterTermFilter()

        self.context_element_stack.append(greater_term_filter)

        self.visit_binary_predicate_node(node)

    @settler_query_visitor._visit(settler_query_ast.GreaterEqualComparisonPredicateNode)
    def visit_greater_equal_comparison_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.BetweenPredicateNode)
    def visit_between_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.NotBetweenPredicateNode)
    def visit_not_between_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.LikePredicateNode)
    def visit_like_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.NotLikePredicateNode)
    def visit_not_like_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.UnaryPredicateNode)
    def visit_unary_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.IsNullPredicateNode)
    def visit_is_null_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.IsNotNullPredicateNode)
    def visit_is_not_null_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.InPredicateNode)
    def visit_in_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.NotInPredicateNode)
    def visit_not_in_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.InSubqueryPredicateNode)
    def visit_in_subquery_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.NotInSubqueryPredicateNode)
    def visit_not_in_subquery_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.AllOrAnyPredicateNode)
    def visit_all_or_any_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.AnyAllSomeNode)
    def visit_any_all_some_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.ExistenceTestNode)
    def visit_existence_test_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.ScalarExpressionPredicateNode)
    def visit_scalar_expression_predicate_node(self, node):
        pass

    @settler_query_visitor._visit(settler_query_ast.SubqueryNode)
    def visit_subquery_node(self, node):
        pass
