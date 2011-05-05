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

import os

import language_wiki.wiki_parser
import language_wiki.wiki_extension_system

GENERATION_TYPE = "ast"
""" The generation type """

WIKI_EXTENSIONS = (
    "wiki",
    "wik"
)
""" The valid wiki extensions list """

class WikiAstGenerator(language_wiki.wiki_extension_system.WikiExtension):
    """
    The wiki ast generator class.
    """

    id = "pt.hive.colony.language.wiki.extensions.ast_generation"
    """ The extension id """

    name = "Ast Documentation Generation Plugin"
    """ The name of the extension """

    short_name = "Ast Documentation Generation"
    """ The short name of the extension """

    description = "Extension for ast documentation generation"
    """ The description of the extension """

    version = "1.0.0"
    """ The version of the extension """

    capabilities = ["generation"]
    """ The capabilities of the extension """

    capabilities_allowed = []
    """ The capabilities allowed by the extension """

    dependencies = []
    """ The dependencies of the extension """

    def get_generation_type(self):
        """
        Retrieves the generation type.

        @rtype: String
        @return: The generation type.
        """

        return GENERATION_TYPE

    def generate_wiki(self, properties):
        """
        Generates the wiki structure for the given file path,
        and options.

        @type properties: Dictionary
        @param properties:  The properties for wiki generation.
        @rtype: Object
        @return: The result of the wiki generation.
        """

        # retrieves the file path
        file_path = properties.get("file_path", None)

        # creates the parse results list
        parse_results_list = []

        # walks the file path
        os.path.walk(file_path, self.generate_wiki_file, (parse_results_list,))

        # returns the parse results list
        return parse_results_list

    def generate_wiki_file(self, args, file_path, names):
        """
        Generates the wiki for the given file and arguments.

        @type args: List
        @param args:  The arguments for the generation.
        @type file_path: String
        @param file_path: The file path for the generation.
        @type names: List
        @param names: The list of name for the current file path.
        """

        # retrieves the parse results list from the args
        parse_results_list, = args

        # iterates over all the names
        for name in names:
            # splits the name
            name_splitted = name.rsplit(".", 1)

            # retrieves the name extension
            name_extension = name_splitted[-1]

            # in case the name extension is valid
            if name_extension in WIKI_EXTENSIONS:
                # creates the full file name
                full_file_path = file_path + "/" + name

                # prints an info message
                self.info("Processing in ast: %s" % full_file_path)

                # opens the wiki file
                wiki_file = open(full_file_path)

                # reads the wiki file contents
                wiki_file_contents = wiki_file.read()

                # closes the wiki file
                wiki_file.close()

                # strips the wiki file contents (to remove extra spaces and lines)
                wiki_file_contents = wiki_file_contents.strip()

                # parses the javascript file retrieving the result
                parse_result = language_wiki.wiki_parser.parser.parse(wiki_file_contents)

                # adds the parse result to the parse results list
                parse_results_list.append(parse_result)
