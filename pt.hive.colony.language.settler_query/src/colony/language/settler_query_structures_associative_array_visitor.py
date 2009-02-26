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

import settler_query_structures_visitor
import settler_query_structures

VALUE_TYPE = "value"
""" The value type value """

FIELD_TYPE = "field"
""" The field type value """ 

class AssociativeArrayVisitor(settler_query_structures_visitor.Visitor):
    """
    The associative array visitor class.
    """
    
    associative_array = {}
    """ The associative array """

    data_stack = []
    """ The resulting data stack """
    
    selected_fields = []
    """ The selected fields """

    selected_entities = []
    """ The selected entities """

    values_stack = []
    """ The values stack """

    types_stack = []
    """ The types stack """

    def __init__(self):
        settler_query_structures_visitor.Visitor.__init__(self)

        self.data_stack = []
        self.selected_fields = []
        self.selected_entities = []
        self.values_stack = []
        self.types_stack = []

        # initializes the data stack
        self.init_data_stack()

    def init_data_stack(self):
        self.data_stack.append({})

    def get_associative_array(self):
        return self.associative_array

    def set_associative_array(self, associative_array):
        self.associative_array = associative_array

    @settler_query_structures_visitor._visit(settler_query_structures.Query)
    def visit_query_node(self, node):
        pass

    @settler_query_structures_visitor._visit(settler_query_structures.SelectQuery)
    def visit_select_query_node(self, node):
        pass

    @settler_query_structures_visitor._visit(settler_query_structures.Field)
    def visit_field_node(self, node):
        pass

    @settler_query_structures_visitor._visit(settler_query_structures.SimpleField)
    def visit_simple_field_node(self, node):
        self.selected_fields.append(node)

    @settler_query_structures_visitor._visit(settler_query_structures.Entity)
    def visit_entity_node(self, node):
        pass

    @settler_query_structures_visitor._visit(settler_query_structures.SimpleEntity)
    def visit_simple_entity_node(self, node):
        # retrieves the entity name
        entity_name = node.entity_name

        self.selected_entities.append(entity_name)

        self.data_stack[-1][entity_name] = self.associative_array[entity_name]

    @settler_query_structures_visitor._visit(settler_query_structures.Filter)
    def visit_filter_node(self, node):
        pass

    @settler_query_structures_visitor._visit(settler_query_structures.BinaryTermFilter)
    def visit_binary_term_filter_node(self, node):
        pass

    @settler_query_structures_visitor._visit(settler_query_structures.BooleanTermFilter)
    def visit_boolean_term_filter_node(self, node):
        pass

    @settler_query_structures_visitor._visit(settler_query_structures.EqualTermFilter)
    def visit_equal_term_filter_node(self, node):
        # retrieves the first operand value
        first_operand_value = self.values_stack.pop();

        # retrieves the second operand value
        second_operand_value = self.values_stack.pop();

        # retrieves the first operand type
        first_operand_type = self.types_stack.pop();

        # retrieves the second operand type
        second_operand_type = self.types_stack.pop();

        # in case is a join
        if(first_operand_type == FIELD_TYPE and second_operand_type == FIELD_TYPE):
            pass
        # in case it's a filter
        elif(first_operand_type == FIELD_TYPE and second_operand_type == VALUE_TYPE):
            data = self.data_stack[-1]

            for entity_elements in data.values():
                removal_list = []

                for entity_element in entity_elements:
                    if entity_element[first_operand_value] != second_operand_value:
                        removal_list.append(entity_element)

                for removal_element in removal_list:
                    entity_elements.remove(removal_element)

        # in case it's a filter
        elif(first_operand_type == VALUE_TYPE and second_operand_type == FIELD_TYPE):
            data = self.data_stack[-1]

            for entity_elements in data.values():
                removal_list = []

                for entity_element in entity_elements:
                    if entity_element[second_operand_value] != first_operand_value:
                        removal_list.append(entity_element)

                for removal_element in removal_list:
                    entity_elements.remove(removal_element)
        # in case it's a simple value comparison
        elif(first_operand_type == VALUE_TYPE and second_operand_type == VALUE_TYPE):
            pass

    @settler_query_structures_visitor._visit(settler_query_structures.GreaterTermFilter)
    def visit_greater_term_filter_node(self, node):
        # retrieves the first operand value
        first_operand_value = self.values_stack.pop();

        # retrieves the second operand value
        second_operand_value = self.values_stack.pop();

        # retrieves the first operand type
        first_operand_type = self.types_stack.pop();

        # retrieves the second operand type
        second_operand_type = self.types_stack.pop();

        # in case is a join
        if(first_operand_type == FIELD_TYPE and second_operand_type == FIELD_TYPE):
            pass
        # in case it's a filter
        elif(first_operand_type == FIELD_TYPE and second_operand_type == VALUE_TYPE):
            data = self.data_stack[-1]

            for entity_elements in data.values():
                removal_list = []

                for entity_element in entity_elements:
                    if entity_element[first_operand_value] <= second_operand_value:
                        removal_list.append(entity_element)

                for removal_element in removal_list:
                    entity_elements.remove(removal_element)

        # in case it's a filter
        elif(first_operand_type == VALUE_TYPE and second_operand_type == FIELD_TYPE):
            data = self.data_stack[-1]

            for entity_elements in data.values():
                removal_list = []

                for entity_element in entity_elements:
                    if entity_element[second_operand_value] <= first_operand_value:
                        removal_list.append(entity_element)

                for removal_element in removal_list:
                    entity_elements.remove(removal_element)
        # in case it's a simple value comparison
        elif(first_operand_type == VALUE_TYPE and second_operand_type == VALUE_TYPE):
            pass

    @settler_query_structures_visitor._visit(settler_query_structures.UnaryTermFilter)
    def visit_unary_term_filter_node(self, node):
        pass

    @settler_query_structures_visitor._visit(settler_query_structures.FieldReference)
    def visit_field_reference_node(self, node):
        pass

    @settler_query_structures_visitor._visit(settler_query_structures.SimpleFieldReference)
    def visit_simple_field_reference_node(self, node):
        self.values_stack.append(node.field_name)
        self.types_stack.append(FIELD_TYPE)

    @settler_query_structures_visitor._visit(settler_query_structures.Value)
    def visit_value_node(self, node):
        self.values_stack.append(node.value)
        self.types_stack.append(VALUE_TYPE)
