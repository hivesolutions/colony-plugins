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
import sys
import time
import getopt
import logging

import os.path

import libs.extension_system

import wiki_parser
import wiki_visitor
import wiki_html_generation
import wiki_extension_system

DEFAULT_TARGET_PATH = "generated"
""" The default target path """

WIKI_EXTENSIONS = ("wiki", "wik")
""" The valid wiki extensions list """

BASE_FILES = {"resources/css/main.css" : "/css",
              "resources/images/link_icon.gif" : "/images",
              "resources/images/colony_logo.png" : "/images",
              "resources/images/powered_by_colony.png" : "/images",
              "resources/images/separator.png" : "/images",
              "resources/images/quote.png" : "/images",
              "resources/images/document_information_note.gif" : "/images",
              "resources/images/warning_note.gif" : "/images",
              "resources/images/error_note.gif" : "/images",
              "resources/images/info_note.gif" : "/images",
              "resources/images/quote_note.gif" : "/images",
              "resources/images/code_note.gif" : "/images"}
""" The base files """

class WikiGenerator:
    """
    The wiki generator class.
    """

    extension_manager = None
    """ The extension manager """

    configuration_map = {}
    """ The configuration map """

    def __init__(self):
        """
        Constructor of the class.
        """

        # creates a new extension manager
        self.extension_manager = libs.extension_system.ExtensionManager(["./extensions"])
        self.extension_manager.set_extension_class(wiki_extension_system.WikiExtension)
        self.extension_manager.start_logger()
        self.extension_manager.load_system()

        # creates the configuration map
        self.configuration_map = {"auto_numbered_sections" : True, "generate_footer" : True}

    def generate_wiki(self, file_path, target_path, verbose, debug):
        """
        Generates the wiki structure for the given file path,
        and options.

        @type file_path: String
        @param file_path:  The file path to generate the wiki structure.
        @type target_path: String
        @param target_path:  The target path for the wiki generation.
        @type verbose: bool
        @param verbose: If the log is going to be of type verbose.
        @type debug: bool
        @param debug: If the log is going to be of type debug.
        """

        # creates the full target path
        full_target_path = file_path + "/" + target_path

        # in case the target directory does not exist
        if not os.path.exists(full_target_path):
            # creates the directory
            os.mkdir(full_target_path)

        # walks the file path
        os.path.walk(file_path, self.generate_wiki_file, (full_target_path,))

        # copies the base files
        self._copy_base_files(full_target_path)

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
                logging.error("Processing: %s" % full_file_path)

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

                # creates the generator visitor
                generation_visitor = wiki_html_generation.HtmlGenerationVisitor()
                generation_visitor.set_parser(wiki_parser.parser)
                generation_visitor.set_extension_manager(self.extension_manager)
                generation_visitor.set_configuration_map(self.configuration_map)

                # accepts the double visit
                parse_result.accept_double(generation_visitor)

                # retrieves the string buffer from the generation visitor
                string_buffer = generation_visitor.get_string_buffer()

                # retrieves the html value from the string buffer
                html_value = string_buffer.getvalue()

                # opens the html file
                html_file = open(full_target_name + ".html", "w+")

                # writes the html value to the html file
                html_file.write(html_value)

                # closes the html file
                html_file.close()

    def _copy_base_files(self, target_path):
        """
        Copies the base files to the given target path.

        @type target_path: String
        @param target_path: The target path.
        """

        # iterates over all the base files
        for base_file_path in BASE_FILES:
            # retrieves the base target path
            base_target_path = BASE_FILES[base_file_path]

            # copes the base file to the target path
            self._copy_files((base_file_path,), target_path + base_target_path)

    def _copy_files(self, file_paths, target_path):
        """
        Copies the files in the given file path to the target path.

        @type file_paths: List
        @param file_paths: The file paths of the files to be copied.
        @type target_path: String
        @param target_path: The target path for the file copy.
        """

        # in case the target path does not exist
        if not os.path.exists(target_path):
            # creates the directory
            os.mkdir(target_path)

        # iterates over all the file paths
        for file_path in file_paths:
            # retrieves the file name
            file_name = os.path.basename(file_path)

            target_full_path = target_path + "/" + file_name

            # opens the file for reading
            file = open(file_path, "rb")

            # reads the file contents
            file_contents = file.read()

            # closes the file
            file.close()

            # opens the target file for writing
            target_file = open(target_full_path, "wb+")

            # writes the file contents to the target file
            target_file.write(file_contents)

            # closes the target file
            target_file.close()

if __name__ == "__main__":
    # starts the verbose flag as false
    verbose = False

    # starts the debug flag as false
    debug = False

    # start the file path value as None
    file_path = None

    # start the target path as None
    target_path = DEFAULT_TARGET_PATH

    # retrieves the argument options
    opts, args = getopt.getopt(sys.argv[1:], "vdf:t:", ["verbose", "debug", "file=", "target="])

    # iterates over all the given options
    for option, value in opts:
        if option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-d", "--debug"):
            debug = True
        elif option in ("-f", "--file"):
            file_path = value
        elif option in ("-y", "--target"):
            target_path = value

    # creates the wiki generator
    wiki_generator = WikiGenerator()

    # retrieves the start time
    start_time = time.time()

    # generates the wiki
    wiki_generator.generate_wiki(file_path, target_path, verbose, debug)

    # retrieves the end time
    end_time = time.time()

    # calculates the time difference
    time_difference = end_time - start_time

    # rounds the time difference
    time_difference_rounded = round(time_difference, 2)

    logging.error("Processing took: %s secconds" % time_difference_rounded)
