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

# the token definitions
tokens = (
    "MULTI_LINE_COMMENT",
    "NAME",
    "DECORATOR_NAME",
    "NUMBER",
    "STRING",
    "STRING_QUOTES",
    "BOOL",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "POWER",
    "EQUALS",
    "EQUALEQUAL",
    "NOTEQUAL",
    "GREATER",
    "GREATEREQUAL",
    "LESS",
    "LESSEQUAL",
    "NOT",
    "AND",
    "OR",
    "LPAREN",
    "RPAREN",
    "LBRACK",
    "RBRACK",
    "LBRACE",
    "RBRACE",
    "DEF",
    "RETURN",
    "COLON",
    "SEMI_COLON",
    "COMA",
    "DOT",
    "IF",
    "ELSE",
    "ELIF",
    "END",
    "NEWLINE",
    "WHILE",
    "FOR",
    "IN",
    "IMPORT",
    "FROM",
    "RAISE",
    "TRY",
    "EXCEPT",
    "FINALLY",
    "CLASS",
    "EXTENDS",
    "IMPLEMENTS",
    "INTERFACE",
    "PLUGIN",
    "CAPABILITY",
    "ALLOWS",
    "PASS",
    "STATIC",
    "GLOBAL",
    "COMMENT"
)

# the reserved keywords
reserved = {
    "not" : "NOT",
    "and" : "AND",
    "or" : "OR",
    "True" : "BOOL",
    "False" : "BOOL",
    "def" : "DEF",
    "return" : "RETURN",
    "if" : "IF",
    "else" : "ELSE",
    "elif" : "ELIF",
    "end" : "END",
    "while" : "WHILE",
    "for" : "FOR",
    "in" : "IN",
    "import" : "IMPORT",
    "from" : "FROM",
    "raise" : "RAISE",
    "try" : "TRY",
    "except" : "EXCEPT",
    "finally" : "FINALLY",
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
t_NOTEQUAL = r"!="
t_GREATER = r">"
t_GREATEREQUAL = r">="
t_LESS = r"<"
t_LESSEQUAL = r"<="

t_LPAREN = r"\("
t_RPAREN = r"\)"

t_LBRACK = r"\["
t_RBRACK = r"\]"

t_LBRACE = r"\{"
t_RBRACE = r"\}"

t_COLON = r":"
t_SEMI_COLON = r";"
t_COMA = r","
t_DOT = r"\."

def t_NAME(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "NAME")
    t.value = reserved_values.get(t.value, t.value)
    return t

def t_DECORATOR_NAME(t):
    r"\@[a-zA-Z_.][a-zA-Z_0-9.]+"
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

def t_MULTI_LINE_COMMENT(t):
    r"\"{3}(.|\n)*?\"{3}"
    # sets the token type
    t.type = "COMMENT"

    return t

# string definition
def t_STRING(t):
    r"\"([^\\\n]|(\\.)|\\n\\\r?\n)*?\""

    t.value = t.value[1:-1]

    return t

# string quotes definition
def t_STRING_QUOTES(t):
    r"\'([^\\\n]|(\\.)|\\n\\\r?\n)*?\'"

    t.type = "STRING"
    t.value = t.value[1:-1]

    return t

# the new line character
def t_NEWLINE(t):
    r"(\r?\n)+"

    t.lexer.lineno += t.value.count("\n")

    return t

# single line comments
def t_COMMENT(t):
    r"\#[^\n]*\n*"

    t.lexer.lineno += 1

    return t

# ignored characters
t_ignore = " \t\r"

# other character
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
