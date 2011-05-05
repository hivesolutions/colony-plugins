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
    "DOCTYPE",
    "CDATA",
    "TAG_SIMPLE",
    "TAG_INIT",
    "TAG_END",
    "COMMENT",
    "NAME",
    "STRING"
)

# the reserved keywords
reserved = {
}

reserved_values = {
}

def t_XML(t):
    r"\<\?xml(.|\n)*?\?\>"
    return t

def t_DOCTYPE(t):
    r"\<\!DOCTYPE (.|\n)*?\>"
    return t

def t_CDATA(t):
    r"\<\!\[CDATA\[(.|\n)*?\]\]\>"
    return t

def t_TAG_SIMPLE(t):
    r"\<[^/]([^\0\>]*?[^/])?/\>"
    return t

def t_TAG_INIT(t):
    r"\<[\w]+?([^\0\>]*?[^/])?\>"
    return t

def t_TAG_END(t):
    r"\</[\w]+?([^/\>]*?[^/])?\>"
    return t

def t_COMMENT(t):
    r"<!--(.|\n)*?-->"
    return t

def t_NAME(t):
    r"[^\<]+"
    t.type = reserved.get(t.value, "NAME")
    t.value = reserved_values.get(t.value, t.value)
    return t

# string definition
def t_STRING(t):
    r"\"([^\\\n]|(\\.)|\\n\\\r?\n)*?\""

    t.value = t.value[1:-1]

    return t
# ignored characters
t_ignore = " \t\r\n"

# other character
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
