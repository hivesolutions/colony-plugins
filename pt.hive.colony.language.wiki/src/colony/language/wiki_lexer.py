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

import re

ESCAPE_REGEX = re.compile(r"%%(.*?)%%")
""" The escape regex value """

# the token definitions
tokens = ("LPAREN", "RPAREN", "LBRACK", "RBRACK",
          "LBRACE", "RBRACE", "PIPE", "EXCLAMATION",
          "BOLD", "BOLD_END", "ITALIC", "ITALIC_END", "UNDERLINE", "UNDERLINE_END", "MONOSPACE", "MONOSPACE_END", "SECTION", "SECTION_END",
          "TAG_INIT", "TAG_END", "SPACE", "FORCED_NEWLINE",
          "NAME_NO_FORMATTING", "BULLET_LIST", "ORDERED_LIST", "LINK_NAME", "NAME", "NEWLINE")

# the reserved keywords
reserved = {
}

reserved_values = {
}

t_LPAREN = r"\("
t_RPAREN = r"\)"

t_LBRACK = r"\["
t_RBRACK = r"\]"

t_LBRACE = r"\{"
t_RBRACE = r"\}"

t_PIPE = r"\|"

t_EXCLAMATION = r"\?"

t_TAG_INIT = r"\<[a-zA-Z]+\>"
t_TAG_END = r"\<\/[a-zA-Z]+\>"

t_SPACE = r"[ \t\r]+"

t_FORCED_NEWLINE = r"\\\\"

states_map = {"BOLD" : False,
              "ITALIC" : False,
              "UNDERLINE" : False,
              "MONOSPACE" : False,
              "SECTION" : False}

# the new line character
def t_NEWLINE(t):
    r"\n+"
    # retrieves the number of newline
    newline_count = t.value.count("\n")
    t.lexer.lineno += newline_count
    t.value = newline_count
    return t

# single line comments
def t_comment(t):
    r"\#[^\n]*\n+"
    pass

def t_BOLD(t):
    r"\*\*"

    global states_map

    if states_map["BOLD"]:
        t.type = "BOLD_END"
        states_map["BOLD"] = False
    else:
        t.type = "BOLD"
        states_map["BOLD"] = True

    return t

def t_ITALIC(t):
    r"\/\/"

    if states_map["ITALIC"]:
        t.type = "ITALIC_END"
        states_map["ITALIC"] = False
    else:
        t.type = "ITALIC"
        states_map["ITALIC"] = True

    return t

def t_UNDERLINE(t):
    r"__"

    if states_map["UNDERLINE"]:
        t.type = "UNDERLINE_END"
        states_map["UNDERLINE"] = False
    else:
        t.type = "UNDERLINE"
        states_map["UNDERLINE"] = True

    return t

def t_MONOSPACE(t):
    r"\'\'"

    if states_map["MONOSPACE"]:
        t.type = "MONOSPACE_END"
        states_map["MONOSPACE"] = False
    else:
        t.type = "MONOSPACE"
        states_map["MONOSPACE"] = True

    return t

def t_SECTION(t):
    r"=+"

    if states_map["SECTION"]:
        t.type = "SECTION_END"
        states_map["SECTION"] = False
    else:
        t.type = "SECTION"
        states_map["SECTION"] = True

    # retrieves the number of equals
    equals_count = t.value.count("=")
    t.value = equals_count
    return t

def t_BULLET_LIST(t):
    r"([ ]{2})+\*"
    # retrieves the number of spaces
    space_count = t.value.count(" ")
    t.value = space_count
    return t

def t_ORDERED_LIST(t):
    r"([ ]{2})+\-"
    # retrieves the number of spaces
    space_count = t.value.count(" ")
    t.value = space_count
    return t

def t_LINK_NAME(t):
    r"(http\:\/\/|www.)[^\\\n\# \t\r\|]+"
    return t

def t_NAME(t):
    r"([^\\\n\# \t\r\%\*\/_\'\{\}\?\[\]\|=]|%%.*?%%)+"
    # retrieves the current value
    current_value = t.value

    # retrieves the escape characters
    current_value = ESCAPE_REGEX.sub("\g<1>", current_value)

    t.value = current_value
    return t

# ignored characters
t_ignore = ""

# other character
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
