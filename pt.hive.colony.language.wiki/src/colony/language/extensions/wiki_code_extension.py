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

import ply

import wiki_extension

from settler_lexer import *

GENERATOR_TYPE = "code"
""" The generator type """

CLASS_DEFINITION = {"CLASS" : "kw4",
                    "FUNCTION" : "kw4",
                    "IF" : "kw4",
                    "ELSE" : "kw4",
                    "ELIF" : "kw4",
                    "END" : "kw4",
                    "PASS" : "kw4",
                    "NAME" : "kw2",
                    "STRING" : "st0",
                    "NUMBER" : "kw6"}
""" The class definition map """

class WikiCodeExtension(wiki_extension.WikiExtension):
    """
    The wiki code extension class.
    """

    extension_id = "pt.hive.colony.language.wiki.extensions.code"
    """ The extension id """

    extension_version = "1.0.0"
    """ The extension version """

    def __init__(self):
        """
        The class constructor.
        """

        pass

    def get_generator_type(self):
        """
        Retrieves the generator type.

        @rtype: String
        @return: The generator type.
        """

        return GENERATOR_TYPE

    def generate_html(self, tag_node):
        """
        Generates the html code for the given tag node.

        @rtype: String
        @return: The generated html code.
        """

        import libs.string_buffer_util

        # creates the string buffer
        string_buffer = libs.string_buffer_util.StringBuffer()

        # retrieves the tag contents
        contents = tag_node.contents

        # strips the contents
        contents_stripped = contents.strip()

        # creates the lexer
        ply.lex.lex()

        # sets the python lexer
        lexer = ply.lex.lexer

        # sets the input in the lexer
        lexer.input(contents_stripped)

        # retrieves the current token from the lexer
        token = lexer.token()

        # writes the start div code tag
        string_buffer.write("<div class=\"code\">")

        # writes the start code tag
        string_buffer.write("<code>")

        current_lex_pos = 0
        current_lex_line = 1

        # while there is a valid token
        while token:
            # prints the token
            print token

            # retrieves the token type
            token_type = token.type

            # retrieves the token class for the given token type
            token_class = CLASS_DEFINITION.get(token_type, None)

            # retrieves the line delta value
            line_delta = token.lineno - current_lex_line

            # retrieves the position delta
            position_delta = token.lexpos - current_lex_pos

            if line_delta > 0:
                for index in range(line_delta):
                    string_buffer.write("<br/>")

            for index in range(position_delta):
                string_buffer.write("&nbsp;")

            if hasattr(token, "lexer"):
                current_lex_pos = token.lexer.lexpos
            else:
                current_lex_pos = token.lexpos + 1
            current_lex_line = token.lineno

            # in case the token class is defined
            if token_class:
                string_buffer.write("<span class=\"" + token_class + "\">")
                string_buffer.write(str(self._get_real_value(token)))
                string_buffer.write("</span>")
            else:
                string_buffer.write(str(self._get_real_value(token)))

            # retrieves the token
            token = lexer.token()

        # writes the end code tag
        string_buffer.write("</code>")

        # writes the end div code tag
        string_buffer.write("</div>")

        # retrieves the string balue
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value

    def _get_real_value(self, token):
        if token.type == "STRING":
            return "\"" + token.value + "\""

        # returns the token value
        return token.value
