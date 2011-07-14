#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import ply.yacc

import search_query_interpreter_ast

from search_query_interpreter_lexer import * #@UnusedWildImport

precedence = (
    ("left", "OR"),
    ("left", "AND")
)

def p_query(t):
    "query : term"

    # retrieves the term node
    term_node = t[1]

    simple_query_node = search_query_interpreter_ast.SimpleQueryNode()

    simple_query_node.set_term_node(term_node)

    t[0] = simple_query_node

def p_query_and(t):
    "query : query AND query"

    first_query_node = t[1]

    second_query_node = t[3]

    and_boolean_query_node = search_query_interpreter_ast.AndBooleanQueryNode()

    and_boolean_query_node.set_first_query_node(first_query_node)

    and_boolean_query_node.set_second_query_node(second_query_node)

    t[0] = and_boolean_query_node

def p_query_or(t):
    "query : query OR query"

    first_query_node = t[1]

    second_query_node = t[3]

    or_boolean_query_node = search_query_interpreter_ast.OrBooleanQueryNode()

    or_boolean_query_node.set_first_query_node(first_query_node)

    or_boolean_query_node.set_second_query_node(second_query_node)

    t[0] = or_boolean_query_node

def p_term_multiple_NAME(t):
    "term : NAME term"

    first_term_value = t[1]

    first_term_node = search_query_interpreter_ast.TermNode()

    first_term_node.set_term_value(first_term_value)

    second_term_node = t[2]

    multiple_term_node = search_query_interpreter_ast.MultipleTermNode()

    multiple_term_node.set_first_term_node(first_term_node)

    multiple_term_node.set_second_term_node(second_term_node)

    t[0] = multiple_term_node

def p_term_multiple_QUOTED(t):
    "term : QUOTED term"

    first_term_value = t[1]

    first_term_node = search_query_interpreter_ast.QuotedNode()

    first_term_node.set_term_value(first_term_value)

    second_term_node = t[2]

    multiple_term_node = search_query_interpreter_ast.MultipleTermNode()

    multiple_term_node.set_first_term_node(first_term_node)

    multiple_term_node.set_second_term_node(second_term_node)

    t[0] = multiple_term_node

def p_term(t):
    "term : NAME"

    term_value = t[1]

    term_node = search_query_interpreter_ast.TermNode()

    term_node.set_term_value(term_value)

    t[0] = term_node

def p_term_quoted(t):
    "term : QUOTED"

    term_value = t[1]

    quoted_node = search_query_interpreter_ast.QuotedNode()

    quoted_node.set_term_value(term_value)

    t[0] = quoted_node

def p_error(t):
    print "Syntax error at '%s'" % t

# creates the parser
ply.yacc.yacc()

# sets the query parser
query_parser = ply.yacc
