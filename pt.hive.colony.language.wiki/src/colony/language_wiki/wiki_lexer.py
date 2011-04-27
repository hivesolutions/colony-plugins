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

ESCAPE_REGEX = re.compile(r"%%(.*?)%%", re.UNICODE)
""" The escape regex value """

# the token definitions
tokens = ("LBRACK", "RBRACK", "LBRACE", "RBRACE", "PIPE",
          "BOLD", "BOLD_END", "ITALIC", "ITALIC_END",
          "UNDERLINE", "UNDERLINE_END", "MONOSPACE", "MONOSPACE_END",
          "SECTION", "SECTION_END", "TAG",
          "SPACE", "FORCED_NEWLINE", "BULLET_LIST",
          "ORDERED_LIST", "LINK_NAME", "NAME", "NEWLINE")

# the reserved keywords
reserved = {
}

reserved_values = {
}

t_PIPE = r"\|"

t_SPACE = r"[ \t\r]+"

t_FORCED_NEWLINE = r"\\\\"

states_map = {
    "BOLD" : False,
    "ITALIC" : False,
    "UNDERLINE" : False,
    "MONOSPACE" : False,
    "SECTION" : False
}

def t_NAME_ESCAPED(t):
    r"%%.*?%%"
    # retrieves the current value
    current_value = t.value

    # retrieves the escape characters
    current_value = ESCAPE_REGEX.sub("\g<1>", current_value)

    t.type = "NAME"
    t.value = current_value
    return t

# the new line character
def t_NEWLINE(t):
    r"(\r?\n)+"
    # retrieves the number of newline
    newline_count = t.value.count("\n")
    t.lexer.lineno += newline_count
    t.value = newline_count
    return t

def t_BOLD(t):
    r"\*\*"

    # in case the current bold state is valid
    if states_map["BOLD"]:
        # sets the type as bold end
        t.type = "BOLD_END"
    else:
        # sets the type as bold
        t.type = "BOLD"

    # changes the bold state
    change_state("BOLD")

    return t

def t_ITALIC(t):
    r"//"

    # in case the current italic state is valid
    if states_map["ITALIC"]:
        # sets the type as italic end
        t.type = "ITALIC_END"
    else:
        # sets the type as italic
        t.type = "ITALIC"

    # changes the italic state
    change_state("ITALIC")

    return t

def t_UNDERLINE(t):
    r"__"

    # in case the current underline state is valid
    if states_map["UNDERLINE"]:
        # sets the type as underline end
        t.type = "UNDERLINE_END"
    else:
        # sets the type as underline
        t.type = "UNDERLINE"

    # changes the underline state
    change_state("UNDERLINE")

    return t

def t_MONOSPACE(t):
    r"\'\'"

    # in case the current monospace state is valid
    if states_map["MONOSPACE"]:
        # sets the type as monospace end
        t.type = "MONOSPACE_END"
    else:
        # sets the type as monospace end
        t.type = "MONOSPACE"

    # changes the monospace state
    change_state("MONOSPACE")

    return t

def t_SECTION(t):
    r"==+"

    # in case the current section state is valid
    if states_map["SECTION"]:
        # sets the type as section end
        t.type = "SECTION_END"
    else:
        # sets the type as section
        t.type = "SECTION"

    # changes the section state
    change_state("SECTION")

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
    r"(http\://|www.)([^\\\n\# \t\r\%\*/_\'\{\}\[\]\|=]|[\%\*/_\'\{\}\[\]=][^\\\n\# \t\r\%\*/_\'\{\}\[\]\|=])+"
    return t

def t_LBRACK(t):
    r"\[\["
    return t

def t_RBRACK(t):
    r"\]\]"
    return t

def t_LBRACE(t):
    r"\{\{"
    return t

def t_RBRACE(t):
    r"\}\}"
    return t

def t_TAG(t):
    r"\<(?P<tag>[\w]+)([^/]|/[^\>])*?\>[^\0]*?\</(?P=tag)\>"
    return t

def t_EXTENDED_NAME(t):
    r"[\%\*/_\'\{\}\[\]=]"

    # sets the type as name
    t.type = "NAME"

    return t

def t_NAME(t):
    r"([^\\\n\# \t\r\%\*/_\'\{\}\[\]\|=]|[\%\*/_\'\{\}\[\]=][^\\\n\# \t\r\%\*/_\'\{\}\[\]\|=]|%%.*?%%)+"
    # retrieves the current value
    current_value = t.value

    # retrieves the escape characters
    current_value = ESCAPE_REGEX.sub("\g<1>", current_value)

    t.value = current_value
    return t

# single line comments
def t_comment(t):
    r"\#[^\n]*\n+"
    t.lexer.lineno += t.value.count("\n")

# ignored characters
t_ignore = ""

# other character
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def change_state(state_name):
    """
    Changes the current state (for the given state name),
    in the states map.

    @type state_name: String
    @param state_name: The name of the state to be changed.
    """

    if states_map[state_name]:
        states_map[state_name] = False
    else:
        states_map[state_name] = True
