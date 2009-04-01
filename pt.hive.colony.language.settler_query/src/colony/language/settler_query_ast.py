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

class AstNode(object):
    """
    The ast node class.
    """

    value = None
    """ The value """

    indent = False
    """ The indentation level """

    child_nodes = []
    """ The list of child nodes """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.child_nodes = []

    def __repr__(self):
        """
        Returns the default representation of the class.

        @rtype: String
        @return: The default representation of the class.
        """

        return "<ast_node indent:%s child_nodes:%s>" % (self.indent, len(self.child_nodes))

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

    def set_value(self, value):
        """
        Sets the value value.

        @type value: Object
        @para value: The value value.
        """

        self.value = value

    def set_indent(self, indent):
        """
        Sets the indent value.

        @type indent: int
        @param indent: The indent value.
        """

        self.indent = indent

    def add_child_node(self, child_node):
        """
        Adds a child node to the node.

        @type child_node: AstNode
        @param child_node: The child node to be added.
        """

        self.child_nodes.append(child_node)

    def remove_child_node(self, child_node):
        """
        Removes a child node from the node.

        @type child_node: AstNode
        @param child_node: The child node to be removed.
        """

        self.child_nodes.remove(child_node)

class AstSequenceNode(AstNode):
    """
    The ast sequence node class.
    """

    next_node = None
    """ The next node """

    valid = True
    """ The valid flag """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def __iter__(self):
        """
        Returns the iterator object for sequence iteration.

        @rtype: AstSequenceNodeIterator
        @return: The iterator object for sequence iteration.
        """

        # creates the ast sequence node iterator
        ast_sequence_node_iterator = AstSequenceNodeIterator(self)

        # returns the ast sequence node iterator
        return ast_sequence_node_iterator

    def set_next_node(self, next_node):
        """
        Sets the next node.

        @type next_node: AstSequenceNode
        @param next_node: The next node.
        """

        self.next_node = next_node

    def get_last_node(self):
        """
        Retrieves the last node.

        @rtype: AstSequenceNode
        @return: The last node.
        """

        # sets the current sequence node
        sequence_node = self

        # retrieves the next sequence node
        next_sequence_node = self.next_node

        while not next_sequence_node == None:
            sequence_node = next_sequence_node
            next_sequence_node = sequence_node.next_node

        return sequence_node

    def get_all_nodes(self):
        """
        Retrieves all the nodes in the sequence.

        @rtype: List
        @return: All the nodes in the sequence.
        """

        # constructs the nodes list
        nodes_list = [value for value in self]

        # returns the nodes list
        return nodes_list

    def count(self):
        """
        Counts the number of nodes in the sequence.

        @rtype: int
        @return: The number of nodes in the sequence.
        """

        # retrieve all nodes
        all_nodes = self.get_all_nodes()

        # calculates the length of all nodes
        length_all_nodes = len(all_nodes)

        # returns the length of all nodes
        return length_all_nodes

    def is_valid(self):
        """
        Retrieves if a node is valid or not.

        @rtype: bool
        @return: The is valid value.
        """

        return self.valid

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

        if self.next_node:
            if visitor.visit_next:
                self.next_node.accept(visitor)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

        if self.next_node:
            if visitor.visit_next:
                self.next_node.accept_post_order(visitor)

class AstSequenceEndNode(AstSequenceNode):
    """
    The ast sequence end node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)
        self.valid = False

class AstEnumerationNode(AstNode):
    """
    The ast enumeration node class.
    """

    enumeration_value = "none"
    """ The enumeration value """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_enumeration_value(self, enumeration_value):
        """
        Sets the enumeration value.

        @type enumeration_value: String
        @param enumeration_value: The enumeration value.
        """

        self.enumeration_value = enumeration_value

class RootNode(AstNode):
    """
    The root node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

class ProgramNode(RootNode):
    """
    The program node class.
    """

    statements_node = None
    """ The statements node """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootNode.__init__(self)

    def set_statements_node(self, statements_node):
        """
        Sets the statements node.

        @type statements_node: StatementsNode
        @param statements_node: The statements node.
        """

        self.statements_node = statements_node
        self.add_child_node(statements_node)

class StatementsNode(AstSequenceNode):
    """
    The statements node class.
    """

    statement_node = None
    """ The statement node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_statement_node(self, statement_node):
        """
        Sets the statement node.

        @type statement_node: StatementNode
        @param statement_node: The statement node.
        """

        self.statement_node = statement_node
        self.add_child_node(statement_node)

class StatementNode(AstNode):
    """
    The statement node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

class PassNode(StatementNode):
    """
    The pass node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

class SelectNode(StatementNode):
    """
    The select node class.
    """

    optional_all_distinct_node = None
    """ The optional all distinct node """

    selection_node = None
    """ The selection node """

    entity_expression = None
    """ The entity expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        StatementNode.__init__(self)

    def set_optional_all_distinct_node(self, optional_all_distinct_node):
        """
        Sets the optional all distinct node.

        @type optional_all_distinct_node: OptionalAllDistinctNode
        @param optional_all_distinct_node: The optional all distinct node.
        """

        self.optional_all_distinct_node = optional_all_distinct_node
        self.add_child_node(optional_all_distinct_node)

    def set_selection_node(self, selection_node):
        """
        Sets the selection node.

        @type selection_node: SelectionNode
        @param selection_node: The selection node.
        """

        self.selection_node = selection_node
        self.add_child_node(selection_node)

    def set_entity_expression_node(self, entity_expression_node):
        """
        Sets the entity expression node.

        @type entity_expression_node: EntityExpressionNode
        @param entity_expression_node: The entity expression node.
        """

        self.entity_expression_node = entity_expression_node
        self.add_child_node(entity_expression_node)

class OptionalAllDistinctNode(AstEnumerationNode):
    """
    The optional all distinct node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstEnumerationNode.__init__(self)

class SelectionNode(AstNode):
    """
    The selection node class.
    """

    scalar_expression_commalist_node = None
    """ The scalar expression commalist node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_scalar_expression_commalist_node(self, scalar_expression_commalist_node):
        """
        Sets the scalar expression commalist node.

        @type scalar_expression_commalist_node: ScalarExpressionCommalistNode
        @param scalar_expression_commalist_node: The scalar expression commalist node.
        """

        self.scalar_expression_commalist_node = scalar_expression_commalist_node
        self.add_child_node(scalar_expression_commalist_node)

class ScalarExpressionCommalistNode(AstSequenceNode):
    """
    The scalar expression commalist node class.
    """

    scalar_expression_node = None
    """ The scalar expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_scalar_expression_node(self, scalar_expression_node):
        """
        Sets the scalar expression node.

        @type scalar_expression_node: ScalarExpressionNode
        @param scalar_expression_node: The scalar expression node.
        """

        self.scalar_expression_node = scalar_expression_node
        self.add_child_node(scalar_expression_node)

class ScalarExpressionNode(AstNode):
    """
    The scalar expression node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

class AtomScalarExpressionNode(ScalarExpressionNode):
    """
    The atom scalar expression node class.
    """

    atom_node = None
    """ The atom node """

    def __init__(self):
        """
        Constructor of the class.
        """

        ScalarExpressionNode.__init__(self)

    def set_atom_node(self, atom_node):
        """
        Sets the atom node.

        @type atom_node: AtomNode
        @param atom_node: The atom node.
        """

        self.atom_node = atom_node
        self.add_child_node(atom_node)


class FieldReferenceScalarExpressionNode(ScalarExpressionNode):
    """
    The field reference scalar expression node class.
    """

    field_reference_node = None
    """ The field reference node """

    def __init__(self):
        """
        Constructor of the class.
        """

        ScalarExpressionNode.__init__(self)

    def set_field_reference_node(self, field_reference_node):
        """
        Sets the field reference node.

        @type field_reference_node: FieldReferenceNode
        @param field_reference_node: The field reference node.
        """

        self.field_reference_node = field_reference_node
        self.add_child_node(field_reference_node)

class AtomNode(AstNode):
    """
    The atom node class.
    """

    literal_node = None
    """ The literal node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_literal_node(self, literal_node):
        """
        Sets the literal node.

        @type literal_node: LiteralNode
        @param literal_node: The literal node.
        """

        self.literal_node = literal_node
        self.add_child_node(literal_node)

class LiteralNode(AstNode):
    """
    The literal node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

class StringLiteralNode(LiteralNode):
    """
    The string literal node class.
    """

    string_value = None
    """ The string value """

    def __init_(self):
        """
        Constructor of the class.
        """

        LiteralNode.__init__(self)

    def set_string_value(self, string_value):
        """
        Sets the string value.

        @type string_value: String
        @param string_value: The string value.
        """

        self.string_value = string_value

class NumberLiteralNode(LiteralNode):
    """
    The number literal node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        LiteralNode.__init__(self)

class IntegerLiteralNode(NumberLiteralNode):
    """
    The integer literal node class.
    """

    integer_value = None
    """ The integer value """

    def __init__(self):
        """
        Constructor of the class.
        """

        NumberLiteralNode.__init__(self)

    def set_integer_value(self, integer_value):
        """
        Sets the integer value.

        @type integer_value: int
        @param integer_value: The integer value.
        """

        self.integer_value = integer_value

class FieldRefereceNode(AstSequenceNode):
    """
    The field reference node class.
    """

    field_reference_name = "none"
    """ The filed reference name """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_field_reference_name(self, field_reference_name):
        """
        Sets the field reference name.

        @type field_reference_name: String
        @param field_reference_name: The field reference name.
        """

        self.field_reference_name = field_reference_name

class EntityExpressionNode(AstNode):
    """
    The entity expression node class.
    """

    from_clause_node = None
    """ The from clause node """

    optional_where_clause_node = None
    """ The optional where clause node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_from_clause_node(self, from_clause_node):
        """
        Sets the from clause node.

        @type from_clause_node: FromClauseNode
        @param from_clause_node: The from clause node.
        """

        self.from_clause_node = from_clause_node
        self.add_child_node(from_clause_node)

    def set_optional_where_clause_node(self, optional_where_clause_node):
        """
        Sets the optional where clause node.

        @type optional_where_clause_node: OptionalWhereClauseNode
        @param optional_where_clause_node: The optional where clause node.
        """

        self.optional_where_clause_node = optional_where_clause_node
        self.add_child_node(optional_where_clause_node)

class FromClauseNode(AstNode):
    """
    The from clause node class.
    """

    entity_reference_commalist_node = None
    """ The entity reference commalist node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_entity_reference_commalist_node(self, entity_reference_commalist_node):
        """
        Sets the entity reference commalist node.

        @type entity_reference_commalist_node: EntityReferenceCommalistNode
        @param entity_reference_commalist_node: The entity reference commalist node.
        """

        self.entity_reference_commalist_node = entity_reference_commalist_node
        self.add_child_node(entity_reference_commalist_node)

class EntityReferenceCommalistNode(AstSequenceNode):
    """
    The entity reference commalist node class.
    """

    entity_reference_node = None
    """ The filed reference name """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstSequenceNode.__init__(self)

    def set_entity_reference_node(self, entity_reference_node):
        """
        Sets the entity reference node.

        @type entity_reference_node: EntityReferenceNode
        @param entity_reference_node: The entity reference node.
        """

        self.entity_reference_node = entity_reference_node
        self.add_child_node(entity_reference_node)

class EntityReferenceNode(AstNode):
    """
    The entity reference node class.
    """

    entity_node = None
    """ The entity node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_entity_node(self, entity_node):
        """
        Sets the entity node.

        @type entity_node: EntityNode
        @param entity_node: The entity node.
        """

        self.entity_node = entity_node
        self.add_child_node(entity_node)

class EntityNode(AstNode):
    """
    The entity node class.
    """

    qualified_entity_name_node = None
    """ The qualified entity name node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_qualified_entity_name_node(self, qualified_entity_name_node):
        """
        Sets the qualified entity name node.

        @type qualified_entity_name_node: QualifiedEntityNameNode
        @param qualified_entity_name_node: The qualified entity name node.
        """

        self.qualified_entity_name_node = qualified_entity_name_node
        self.add_child_node(qualified_entity_name_node)

class EntityAsNameNode(EntityNode):
    """
    The entity as name node class.
    """

    entity_as_name_value = "none"
    """ The entity as name value """

    def __init__(self):
        """
        Constructor of the class.
        """

        EntityNode.__init__(self)

    def set_entity_as_name_value(self, entity_as_name_value):
        """
        Sets the entity as name value.

        @type entity_as_name_value: String
        @param entity_as_name_value: The entity as name value.
        """

        self.entity_as_name_value = entity_as_name_value

class QualifiedEntityNameNode(AstNode):
    """
    The qualified entity name node class.
    """

    qualified_entity_name_value = "none"
    """ The qualified entity name value """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_qualified_entity_name_value(self, qualified_entity_name_value):
        """
        Sets the qualified entity name value.

        @type qualified_entity_name_value: String
        @param qualified_entity_name_value: The qualified entity name value.
        """

        self.qualified_entity_name_value = qualified_entity_name_value

class OptionalWhereClauseNode(AstNode):
    """
    The optional where clause node class.
    """

    where_clause_node = None
    """ The where clause node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_where_clause_node(self, where_clause_node):
        """
        Sets the where clause node.

        @type where_clause_node: WhereClauseNode
        @param where_clause_node: The where clause node.
        """

        self.where_clause_node = where_clause_node
        self.add_child_node(where_clause_node)

class WhereClauseNode(AstNode):
    """
    The where clause node class.
    """

    search_condition_node = None
    """ The search condition node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_search_condition_node(self, search_condition_node):
        """
        Sets the search condition node.

        @type search_condition_node: SearchConditionNode
        @param search_condition_node: The search condition node.
        """

        self.search_condition_node = search_condition_node
        self.add_child_node(search_condition_node)

class SearchConditionNode(AstNode):
    """
    The search condition node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

class PredicateSearchConditionNode(SearchConditionNode):
    """
    The predicate search condition node class.
    """

    predicate_node = None
    """ The predicate node """

    def __init__(self):
        """
        Constructor of the class.
        """

        SearchConditionNode.__init__(self)

    def set_predicate_node(self, predicate_node):
        """
        Sets the predicate node.

        @type predicate_node: PredicateNode
        @param predicate_node: The predicate node.
        """

        self.predicate_node = predicate_node
        self.add_child_node(predicate_node)

class ExpressionSearchConditionNode(SearchConditionNode):
    """
    The expression search condition node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        SearchConditionNode.__init__(self)

class BinaryExpressionSearchConditionNode(ExpressionSearchConditionNode):
    """
    The binary expression search condition node class.
    """

    first_expression_search_condition_node = None
    """ The first expression search condition node """

    second_expression_search_condition_node = None
    """ The second expression search condition node """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionSearchConditionNode.__init__(self)

    def set_first_expression_search_condition_node(self, first_expression_search_condition_node):
        """
        Sets the first expression search condition node.

        @type first_expression_search_condition_node: SearchConditionNode
        @param first_expression_search_condition_node: The first expression search condition node.
        """

        self.first_expression_search_condition_node = first_expression_search_condition_node
        self.add_child_node(first_expression_search_condition_node)

    def set_second_expression_search_condition_node(self, second_expression_search_condition_node):
        """
        Sets the second expression search condition node.

        @type second_expression_search_condition_node: SearchConditionNode
        @param second_expression_search_condition_node: The second expression search condition node.
        """

        self.second_expression_search_condition_node = second_expression_search_condition_node
        self.add_child_node(second_expression_search_condition_node)

class AndExpressionSearchConditionNode(BinaryExpressionSearchConditionNode):
    """
    The and expression search condition node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryExpressionSearchConditionNode.__init__(self)

class OrExpressionSearchConditionNode(BinaryExpressionSearchConditionNode):
    """
    The or expression search condition node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryExpressionSearchConditionNode.__init__(self)

class UnaryExpressionSearchConditionNode(ExpressionSearchConditionNode):
    """
    The unary expression search condition node class.
    """

    expression_search_condition_node = None
    """ The expression search condition node """

    def __init__(self):
        """
        Constructor of the class.
        """

        ExpressionSearchConditionNode.__init__(self)

    def set_expression_search_condition_node(self, expression_search_condition_node):
        """
        Sets the expression search condition node.

        @type expression_search_condition_node: SearchConditionNode
        @param expression_search_condition_node: The expression search condition node.
        """

        self.expression_search_condition_node = expression_search_condition_node
        self.add_child_node(expression_search_condition_node)

class NotExpressionSearchConditionNode(UnaryExpressionSearchConditionNode):
    """
    The not expression search condition node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        UnaryExpressionSearchConditionNode.__init__(self)

class ParenthesisExpressionSearchConditionNode(UnaryExpressionSearchConditionNode):
    """
    The parenthesis expression search condition node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        UnaryExpressionSearchConditionNode.__init__(self)

class PredicateNode(AstNode):
    """
    The predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

class BinaryPredicateNode(PredicateNode):
    """
    The binary predicate node class.
    """

    first_scalar_expression_node = None
    """ The first scalar expression node """

    second_scalar_expression_node = None
    """ The second scalar expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_first_scalar_expression_node(self, first_scalar_expression_node):
        """
        Sets the first scalar expression node.

        @type first_scalar_expression_node: ScalarExpressionNode
        @param first_scalar_expression_node: The first scalar expression node.
        """

        self.first_scalar_expression_node = first_scalar_expression_node
        self.add_child_node(first_scalar_expression_node)

    def set_second_scalar_expression_node(self, second_scalar_expression_node):
        """
        Sets the second scalar expression node.

        @type second_scalar_expression_node: ScalarExpressionNode
        @param second_scalar_expression_node: The second scalar expression node.
        """

        self.second_scalar_expression_node = second_scalar_expression_node
        self.add_child_node(second_scalar_expression_node)

class ComparisonPredicateNode(BinaryPredicateNode):
    """
    The comparison predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryPredicateNode.__init__(self)

class EqualComparisonPredicateNode(ComparisonPredicateNode):
    """
    The equal comparison predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ComparisonPredicateNode.__init__(self)

class GreaterComparisonPredicateNode(ComparisonPredicateNode):
    """
    The greater comparison predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ComparisonPredicateNode.__init__(self)

class GreaterEqualComparisonPredicateNode(ComparisonPredicateNode):
    """
    The greater equal comparison predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        ComparisonPredicateNode.__init__(self)

class BetweenPredicateNode(BinaryPredicateNode):
    """
    The between predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryPredicateNode.__init__(self)

class NotBetweenPredicateNode(BinaryPredicateNode):
    """
    The between predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryPredicateNode.__init__(self)

class LikePredicateNode(BinaryPredicateNode):
    """
    The like predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryPredicateNode.__init__(self)

class NotLikePredicateNode(BinaryPredicateNode):
    """
    The like predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryPredicateNode.__init__(self)

class UnaryPredicateNode(PredicateNode):
    """
    The unary predicate node class.
    """

    scalar_expression_node = None
    """ The scalar expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_scalar_expression_node(self, scalar_expression_node):
        """
        Sets the scalar expression node.

        @type scalar_expression_node: ScalarExpressionNode
        @param scalar_expression_node: The scalar expression node.
        """

        self.scalar_expression_node = scalar_expression_node
        self.add_child_node(scalar_expression_node)

class IsNullPredicateNode(UnaryPredicateNode):
    """
    The is null predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        UnaryPredicateNode.__init__(self)

class IsNotNullPredicateNode(UnaryPredicateNode):
    """
    The is not null predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        UnaryPredicateNode.__init__(self)

class InPredicateNode(PredicateNode):
    """
    The in predicate node class.
    """

    scalar_expression_node = None
    """ The scalar expression node """

    scalar_expression_commalist_node = None
    """ The scalar expression commalist node """

    def __init__(self):
        """
        Constructor of the class.
        """

        PredicateNode.__init__(self)

    def set_scalar_expression_node(self, scalar_expression_node):
        """
        Sets the scalar expression node.

        @type scalar_expression_node: ScalarExpressionNode
        @param scalar_expression_node: The scalar expression node.
        """

        self.scalar_expression_node = scalar_expression_node
        self.add_child_node(scalar_expression_node)

    def set_scalar_expression_commalist_node(self, scalar_expression_commalist_node):
        """
        Sets the scalar expression commalist node.

        @type scalar_expression_commalist_node: ScalarExpressionNode
        @param scalar_expression_commalist_node: The scalar expression commalist node.
        """

        self.scalar_expression_commalist_node = scalar_expression_commalist_node
        self.add_child_node(scalar_expression_commalist_node)

class NotInPredicateNode(InPredicateNode):
    """
    The not in predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        InPredicateNode.__init__(self)

class InSubqueryPredicateNode(PredicateNode):
    """
    The in subquery predicate node class.
    """

    scalar_expression_node = None
    """ The scalar expression node """

    subquery_node = None
    """ The subquery node """

    def __init__(self):
        """
        Constructor of the class.
        """

        PredicateNode.__init__(self)

    def set_scalar_expression_node(self, scalar_expression_node):
        """
        Sets the scalar expression node.

        @type scalar_expression_node: ScalarExpressionNode
        @param scalar_expression_node: The scalar expression node.
        """

        self.scalar_expression_node = scalar_expression_node
        self.add_child_node(scalar_expression_node)

    def set_subquery_node(self, subquery_node):
        """
        Sets the subquery node.

        @type subquery_node: SubqueryNode
        @param subquery_node: The subquery node.
        """

        self.subquery_node = subquery_node
        self.add_child_node(subquery_node)

class NotInSubqueryPredicateNode(InSubqueryPredicateNode):
    """
    The not in subquery predicate node class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        InSubqueryPredicateNode.__init__(self)

class AllOrAnyPredicateNode(PredicateNode):
    """
    The all or any predicate node class.
    """

    scalar_expression_node = None
    """ The scalar expression node """

    any_all_some_node = None
    """ The any all some node """

    subquery_node = None
    """ The subquery node """

    def __init__(self):
        """
        Constructor of the class.
        """

        PredicateNode.__init__(self)

    def set_scalar_expression_node(self, scalar_expression_node):
        """
        Sets the scalar expression node.

        @type scalar_expression_node: ScalarExpressionNode
        @param scalar_expression_node: The scalar expression node.
        """

        self.scalar_expression_node = scalar_expression_node
        self.add_child_node(scalar_expression_node)

    def set_any_all_some_node(self, any_all_some_node):
        """
        Sets the any all some node.

        @type any_all_some_node: AnyAllSomeNode
        @param any_all_some_node: The any all some node.
        """

        self.any_all_some_node = any_all_some_node
        self.add_child_node(any_all_some_node)

    def set_subquery_node(self, subquery_node):
        """
        Sets the subquery node.

        @type subquery_node: SubqueryNode
        @param subquery_node: The subquery node.
        """

        self.subquery_node = subquery_node
        self.add_child_node(subquery_node)

class AnyAllSomeNode(AstNode):
    """
    The any all some predicate node class.
    """

    any_all_some_value = "none"
    """ The any all some value """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_any_all_some_value(self, any_all_some_value):
        """
        Sets the any all some value.

        @type any_all_some_value: String
        @param any_all_some_value: The any all some value.
        """

        self.any_all_some_value = any_all_some_value

class ExistenceTestNode(AstNode):
    """
    The existence node class.
    """

    subquery_node = None
    """ The subquery node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_subquery_node(self, subquery_node):
        """
        Sets the subquery node.

        @type subquery_node: SubqueryNode
        @param subquery_node: The subquery node.
        """

        self.subquery_node = subquery_node
        self.add_child_node(subquery_node)

class ScalarExpressionPredicateNode(PredicateNode):
    """
    The scalar expression predicate node class.
    """

    scalar_expression_node = None
    """ The scalar expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        PredicateNode.__init__(self)

    def set_scalar_expression_node(self, scalar_expression_node):
        """
        Sets the scalar expression node.

        @type scalar_expression_node: ScalarExpressionNode
        @param scalar_expression_node: The scalar expression node.
        """

        self.scalar_expression_node = scalar_expression_node
        self.add_child_node(scalar_expression_node)

class SubqueryNode(AstNode):
    """
    The subquery node class.
    """

    optional_all_distinct_node = None
    """ The optional all distinct node """

    selection_node = None
    """ The selection node """

    entity_expression_node = None
    """ The entity expression node """

    def __init__(self):
        """
        Constructor of the class.
        """

        AstNode.__init__(self)

    def set_optional_all_distinct_node(self, optional_all_distinct_node):
        """
        Sets the optional all distinct node.

        @type optional_all_distinct_node: OptionalAllDistinctNode
        @param optional_all_distinct_node: The optional all distinct node.
        """

        self.optional_all_distinct_node = optional_all_distinct_node
        self.add_child_node(optional_all_distinct_node)

    def set_selection_node(self, selection_node):
        """
        Sets the selection node.

        @type selection_node: SelectionNode
        @param selection_node: The selection node.
        """

        self.selection_node = selection_node
        self.add_child_node(selection_node)

    def set_entity_expression_node(self, entity_expression_node):
        """
        Sets the entity expression node.

        @type entity_expression_node: EntityExpressionNode
        @param entity_expression_node: The entity expression node.
        """

        self.entity_expression_node = entity_expression_node
        self.add_child_node(entity_expression_node)
