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

import sys

import wiki_code.wiki_code_extension_system

from python_highlighting.python_lexer import * #@UnusedWildImport

COLONY_GENERATOR_PATH = "../../pt.hive.colony.language.generator/src/colony"
""" The colony generator path """

# appends the colony language generator path
sys.path.append(COLONY_GENERATOR_PATH)

# imports the colony generator package
import language_generator.lexer_generator

HIGHLIGHTING_TYPE = "python"
""" The highlighting type """

CLASS_DEFINITION = {
    "CLASS" : "kw5",
    "DEF" : "kw5",
    "IF" : "kw5",
    "ELSE" : "kw5",
    "ELIF" : "kw5",
    "FOR" : "kw5",
    "IN" : "kw5",
    "END" : "kw5",
    "PASS" : "kw5",
    "RETURN" : "kw5",
    "IMPORT" : "kw5",
    "FROM" : "kw5",
    "TRY" : "kw5",
    "EXCEPT" : "kw5",
    "FINALLY" : "kw5",
    "RAISE" : "kw5",
    "DECORATOR_NAME" : "kw1",
    "BOOL" : "kw5",
    "STRING" : "st0",
    "STRING_QUOTES" : "st0",
    "NUMBER" : "kw6",
    "GLOBAL" : "kw5",
    "COMMENT" : "kw4"
}
""" The class definition map """

class PythonHighlightingExtension(wiki_code.wiki_code_extension_system.WikiCodeExtension):
    """
    The python highlighting extension class.
    """

    id = "pt.hive.colony.language.wiki.code.extensions.python_highlighting"
    """ The extension id """

    name = "Python Highlighting Code Plugin"
    """ The name of the extension """

    short_name = "Python Highlighting Code"
    """ The short name of the extension """

    description = "Extension for python code highlighting"
    """ The description of the extension """

    version = "1.0.0"
    """ The version of the extension """

    capabilities = [
        "code_highlighting"
    ]
    """ The capabilities of the extension """

    capabilities_allowed = []
    """ The capabilities allowed by the extension """

    dependencies = []
    """ The dependencies of the extension """

    def get_highlighting_type(self):
        """
        Retrieves the highlighting type.

        @rtype: String
        @return: The highlighting type.
        """

        return HIGHLIGHTING_TYPE

    def get_tokens_list(self, contents):
        # starts the tokens list
        tokens_list = []

        # strips the contents
        contents_stripped = contents.strip()

        # creates a new lexer
        lexer = language_generator.lexer_generator.LexerGenerator()

        # constructs the lexer
        lexer.construct(globals())

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
            token_tuple = (
                token_type,
                token_value,
                token_position,
                token_end_position,
                token_line,
                token_class
            )

            # appends the token tuple to the tokens list
            tokens_list.append(token_tuple)

            # retrieves the token
            token = lexer.token()

        # returns the tokens list
        return tokens_list

    def _get_real_value(self, token):
        # retrieves the token type
        token_type = token.type

        # retrieves the token value
        token_value = token.value

        # in case the token type is string
        if token_type == "STRING":
            return "\"" + token_value + "\""
        # in case the token type is string with quotes
        elif token_type == "STRING_QUOTES":
            return "'" + token_value + "'"

        # returns the token value
        return token_value
