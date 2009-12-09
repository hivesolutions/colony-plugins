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

import ply

import wiki_code.wiki_code_extension_system

from settler_highlighter.settler_lexer import *

HIGHLIGHTER_TYPE = "settler"
""" The highlighter type """

CLASS_DEFINITION = {"CLASS" : "kw5",
                    "FUNCTION" : "kw5",
                    "IF" : "kw5",
                    "ELSE" : "kw5",
                    "ELIF" : "kw5",
                    "END" : "kw5",
                    "PASS" : "kw5",
                    "RETURN" : "kw5",
                    "NAME" : "kw2",
                    "STRING" : "st0",
                    "NUMBER" : "kw6",
                    "COMMENT" : "kw4"}
""" The class definition map """

class SettlerHighlighterExtension(wiki_code.wiki_code_extension_system.WikiCodeExtension):
    """
    The settler highlighter extension class.
    """

    id = "pt.hive.colony.language.wiki.code.extensions.settler_highlighter"
    """ The extension id """

    name = "Settler Highlighter Code Plugin"
    """ The name of the extension """

    short_name = "Settler Highlighter Code"
    """ The short name of the extension """

    description = "Extension for settler code highlighting"
    """ The description of the extension """

    version = "1.0.0"
    """ The version of the extension """

    capabilities = ["code_highlighting"]
    """ The capabilities of the extension """

    capabilities_allowed = []
    """ The capabilities allowed by the extension """

    dependencies = []
    """ The dependencies of the extension """

    def get_highlighter_type(self):
        """
        Retrieves the highlighter type.

        @rtype: String
        @return: The highlighter type.
        """

        return HIGHLIGHTER_TYPE

    def get_tokens_list(self, contents):
        # starts the tokens list
        tokens_list = []

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

        # while there is a valid token
        while token:
            # retrieves the token type
            token_type = token.type

            # retrieves the token value
            token_value = self._get_real_value(token)

            # retrieve the token position
            token_position = token.lexpos

            # is case the lexer attribute is defined in the token
            if hasattr(token, "lexer"):
                token_end_position = token.lexer.lexpos
            else:
                token_end_position = token.lexpos + 1

            # retrieves the token line
            token_line = token.lineno

            # retrieves the token class for the given token type
            token_class = CLASS_DEFINITION.get(token_type, None)

            # creates the token tuple
            token_tuple = (token_type, token_value, token_position, token_end_position, token_line, token_class)

            # appends the token tuple to the tokens list
            tokens_list.append(token_tuple)

            # retrieves the token
            token = lexer.token()

        # returns the tokens list
        return tokens_list

    def _get_real_value(self, token):
        if token.type == "STRING":
            return "\"" + token.value + "\""

        # returns the token value
        return token.value
