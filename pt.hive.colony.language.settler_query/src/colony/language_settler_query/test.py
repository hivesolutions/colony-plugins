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
import settler_query_structures_visitor
import settler_query_structures_associative_array_visitor

ARRAY = {
    "Person" : [
        {
            "name" : "Tobias",
            "nationality" : "Portuguese",
            "age" : 12
        },
        {
            "name" : "Matias",
            "nationality" : "Portuguese",
            "age" : 56
        },
        {
            "name" : "Matias",
            "nationality" : "English",
            "age" : 23
        }
    ],
    "User" : [
        {
            "username" : "joamag",
            "password" : "123123"
        },
        {
            "username" : "tiagooo",
            "password" : "234"
        }
    ]
}

# creates a new select query
select_query = settler_query_structures.SelectQuery()

name_field = settler_query_structures.SimpleField()
name_field.field_name = "name"

# adds a new select field
select_query.add_select_field(name_field)

person_entity = settler_query_structures.SimpleEntity()
person_entity.entity_name = "Person"

# adds a new select entity
select_query.add_select_entity(person_entity)

nationality_field = settler_query_structures.SimpleFieldReference()
nationality_field.field_name = "nationality"

portuguese_value = settler_query_structures.Value()
portuguese_value.value = "Portuguese"

nationality_filter = settler_query_structures.EqualTermFilter()
nationality_filter.first_operand = nationality_field
nationality_filter.second_operand = portuguese_value

# adds a new select filter
select_query.add_select_filters(nationality_filter)

age_field = settler_query_structures.SimpleFieldReference()
age_field.field_name = "age"

age_value = settler_query_structures.Value()
age_value.value = 14

adult_age_filter = settler_query_structures.GreaterTermFilter()
adult_age_filter.first_operand = age_field
adult_age_filter.second_operand = age_value

# adds a new select filter
select_query.add_select_filters(adult_age_filter)

associative_array_visitor = settler_query_structures_associative_array_visitor.AssociativeArrayVisitor()

associative_array_visitor.set_associative_array(ARRAY)

visitor = settler_query_structures_visitor.Visitor()

#select_query.accept_post_order(visitor)
select_query.accept_post_order(associative_array_visitor)

print associative_array_visitor.data_stack[-1]

#print [value["age"] for value in ARRAY["Person"] if value["nationality"] == "Portuguese" and value["age"] > 14]
