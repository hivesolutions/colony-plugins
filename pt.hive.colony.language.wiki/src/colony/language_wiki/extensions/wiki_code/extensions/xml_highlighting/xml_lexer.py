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
    "XML",
    "CDATA",
    "TAG_INIT",
    "TAG_END",
    "TAG_END_END",
    "ATTRIBUTION",
    "COMMENT",
    "NAME",
    "STRING",
    "STRING_QUOTES",
    "NEWLINE",
    "EQUALS"
)

# the reserved keywords
reserved = {
}

reserved_values = {
}

# token definition
t_EQUALS = r"="

def t_XML(t):
    r"\<\?xml(.|\n)*?\?\>"

    return t

def t_CDATA(t):
    r"\<\!\[CDATA\[(.|\n)*?\]\]\>"

    return t

def t_TAG_INIT(t):
    r"\<[^\!\?\> ]+"

    return t

def t_TAG_END(t):
    r"\>"

    return t

def t_TAG_END_END(t):
    r"/\>"

    return t

def t_ATTRIBUTION(t):
    r"[a-zA-Z_\$\.0-9][a-zA-Z_\$\.\:0-9]*="

    return t

def t_COMMENT(t):
    r"<!--(.|\n)*?-->"

    return t

def t_NAME(t):
    r"[\w\$\.,:/#+\-\{\}]+"

    t.type = reserved.get(t.value, "NAME")
    t.value = reserved_values.get(t.value, t.value)

    return t

# string definition
def t_STRING(t):
    r"\"([^\\\n]|(\\.)|\\n\\\r?\n)*?\""

    t.value = t.value[1:-1]

    return t

# string quotes definition
def t_STRING_QUOTES(t):
    r"\'([^\\\n]|(\\.)|\\n\\\r?\n)*?\'"

    t.type = "STRING_QUOTES"
    t.value = t.value[1:-1]

    return t

# the new line character
def t_NEWLINE(t):
    r"(\r?\n)+"

    t.lexer.lineno += t.value.count("\n")

    return t

# ignored characters
t_ignore = " \t\r"

# other character
def t_error(t):

    print "Illegal character '%s'" % t.value[0]

    t.lexer.skip(1)
