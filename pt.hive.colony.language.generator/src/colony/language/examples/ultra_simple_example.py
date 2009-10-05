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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

# token definition
t_PLUS = r"\+"

t_1 = r"1"
t_0 = r"0"

# single line comments
def t_comment(t):
    r"\#[^\n]*\n+"
    pass

# ignored characters
t_ignore = " "

# other character
def t_error(t):
    print "Illegal character '%s'" % t.value[0]

    # skips the character
    t.lexer.skip(1)

def p_program(t):
    "program : E"

    print "program : " + str(t[1])

    t[0] = t[1]

def p_expression_sum(t):
    "E : E PLUS B"

    print "E : " + str(t[1]) + " PLUS " + str(t[3])

    t[0] = t[1] + t[3]

def p_expression_value(t):
    "E : B"

    print "E : " + str(t[1])

    t[0] = t[1]

def p_zero_terminal(t):
    "B : 0"

    print "B : " + t[1]

    t[0] = int(t[1])

def p_one_terminal(t):
    "B : 1"

    print "B : " + t[1]

    t[0] = int(t[1])

# sets the example
example = locals()
