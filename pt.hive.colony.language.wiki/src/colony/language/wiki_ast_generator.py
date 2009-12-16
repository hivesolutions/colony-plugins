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
import logging

import os.path

import wiki_parser
import wiki_generator

WIKI_EXTENSIONS = ("wiki", "wik")
""" The valid wiki extensions list """

class WikiAstGenerator(wiki_generator.WikiGenerator):
    """
    The wiki ast generator class.
    """

    parse_results_list = []
    """ The parse results list """

    configuration_map = {}
    """ The configuration map """

    def __init__(self, logger = logging):
        """
        Constructor of the class.
        """

        wiki_generator.WikiGenerator.__init__(self, logger)

        # creates the parse results list
        self.parse_results_list = []

        # creates the configuration map
        self.configuration_map = {}

    def generate_wiki(self, file_path):
        """
        Generates the wiki structure for the given file path,
        and options.

        @type file_path: String
        @param file_path:  The file path to generate the wiki structure.
        """

        # walks the file path
        os.path.walk(file_path, self.generate_wiki_file, None)

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

        # retrieves the full target path from the args
        full_target_path, = args

        # iterates over all the names
        for name in names:
            # splits the name
            name_splitted = name.split(".")

            # retrieves the name extension
            name_extension = name_splitted[-1]

            # in case the name extension is valid
            if name_extension in WIKI_EXTENSIONS:
                # creates the full file name
                full_file_path = file_path + "/" + name

                # retrieves the partial name
                partial_name = "".join(name_splitted[:-1])

                # creates the full target name
                full_target_name = full_target_path + "/" + partial_name

                # prints an info message
                self.logger.info("Processing: %s" % full_file_path)

                # opens the wiki file
                wiki_file = open(full_file_path)

                # reads the wiki file contents
                wiki_file_contents = wiki_file.read()

                # closes the wiki file
                wiki_file.close()

                # strips the wiki file contents (to remove extra spaces and lines)
                wiki_file_contents = wiki_file_contents.strip()

                # parses the javascript file retrieving the result
                parse_result = wiki_parser.parser.parse(wiki_file_contents)

                # adds the parse result to the parse results list
                self.parse_results_list.append(parse_result)
