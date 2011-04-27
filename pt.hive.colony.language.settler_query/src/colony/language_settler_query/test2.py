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

import settler_query_parser
import settler_query_visitor
import settler_query_generation

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

rootNode = settler_query_parser.parser.parse("select age from Person where age > 22 and nationality = \"Portuguese\"\n")

query_visitor = settler_query_visitor.Visitor()
query_structures_generation_visitor = settler_query_generation.QueryStructuresGenerationVisitor()

rootNode.accept_post_order(query_visitor)
rootNode.accept_post_order(query_structures_generation_visitor)

query = query_structures_generation_visitor.query

associative_array_visitor = settler_query_structures_associative_array_visitor.AssociativeArrayVisitor()

associative_array_visitor.set_associative_array(ARRAY)

query.accept_post_order(associative_array_visitor)

print associative_array_visitor.data_stack[-1]
