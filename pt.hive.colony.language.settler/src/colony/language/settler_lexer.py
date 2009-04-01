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

import ply.lex

# the token definitions
tokens = ("NAME", "NUMBER", "STRING", "BOOL", "PLUS",
          "MINUS", "TIMES", "DIVIDE", "POWER",
          "EQUALS", "EQUALEQUAL", "GREATER",
          "GREATEREQUAL", "LESS", "LESSEQUAL",
          "NOT", "AND", "OR", "LPAREN", "RPAREN",
          "LBRACK", "RBRACK", "FUNCTION", "RETURN",
          "COLON", "COMA", "DOT", "IF", "ELSE", "ELIF",
          "END", "NEWLINE", "WHILE", "FOR", "IN", "IMPORT",
          "CLASS", "EXTENDS", "IMPLEMENTS", "INTERFACE",
          "PLUGIN", "CAPABILITY", "ALLOWS", "PASS", "STATIC",
          "GLOBAL")

# the reserved keywords
reserved = {
    "not" : "NOT",
    "and" : "AND",
    "or" : "OR",
    "True" : "BOOL",
    "False" : "BOOL",
    "function" : "FUNCTION",
    "return" : "RETURN",
    "if" : "IF",
    "else" : "ELSE",
    "elif" : "ELIF",
    "end" : "END",
    "while" : "WHILE",
    "for" : "FOR",
    "in" : "IN",
    "import" : "IMPORT",
    "class" : "CLASS",
    "interface" : "INTERFACE",
    "extends" : "EXTENDS",
    "implements" : "IMPLEMENTS",
    "plugin" : "PLUGIN",
    "capability": "CAPABILITY",
    "allows" : "ALLOWS",
    "pass" : "PASS",
    "static" : "STATIC",
    "global" : "GLOBAL"
}

reserved_values = {
    "True" : True,
    "False" : False
}

# token definition
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_POWER = r"\^"
t_EQUALS = r"="

t_EQUALEQUAL = r"=="
t_GREATER = r">"
t_GREATEREQUAL = r">="
t_LESS = r"<"
t_LESSEQUAL = r"<="

t_LPAREN = r"\("
t_RPAREN = r"\)"

t_LBRACK = r"\["
t_RBRACK = r"\]"

t_COLON = r":"
t_COMA = r","
t_DOT = r"\."

def t_NAME(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "NAME")
    t.value = reserved_values.get(t.value, t.value)
    return t

# number definition
def t_NUMBER(t):
    r"\d+"

    try:
        t.value = int(t.value)
    except ValueError:
        print "Integer value too large", t.value
        t.value = 0

    return t

# string definition
def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\""

    t.value = t.value[1:-1]

    return t

# the new line character
def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")
    return t

# single line comments
def t_comment(t):
    r"\#[^\n]*\n+"
    pass

# ignored characters
t_ignore = " \t"

# other character
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# creates the lexer
ply.lex.lex()
