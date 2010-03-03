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

import os.path

import wiki_parser
import wiki_extension_system

import wiki_html_generation.wiki_html_generation

GENERATION_TYPE = "html"
""" The generation type """

WIKI_EXTENSIONS = ("wiki", "wik")
""" The valid wiki extensions list """

BASE_FILES = {"resources/css/main.css" : "/css",
              "resources/js/main.js" : "/js",
              "resources/images/link_icon.png" : "/images",
              "resources/images/console_icon.png" : "/images",
              "resources/images/header.png" : "/images",
              "resources/images/tick_icon.png" : "/images",
              "resources/images/arrow_icon.png" : "/images",
              "resources/images/wikipedia_icon.png" : "/images",
              "resources/images/colony_logo.png" : "/images",
              "resources/images/powered_by_colony.png" : "/images",
              "resources/images/separator.png" : "/images",
              "resources/images/quote.png" : "/images",
              "resources/images/document_information_note.gif" : "/images",
              "resources/images/warning_note.gif" : "/images",
              "resources/images/error_note.gif" : "/images",
              "resources/images/info_note.gif" : "/images",
              "resources/images/quote_note.gif" : "/images",
              "resources/images/code_note.gif" : "/images",
              "resources/images/image_note.gif" : "/images",
              "resources/images/video_note.gif" : "/images",
              "resources/images/checkbox_note.gif" : "/images",
              "resources/images/resources_note.gif" : "/images",
              "resources/images/diagram_note.gif" : "/images"}
""" The base files """

DEFAULT_CONFIGURATION_MAP = {"auto_numbered_sections" : True, "generate_footer" : True}
""" The default configuration map """

class WikiHtmlGenerator(wiki_extension_system.WikiExtension):
    """
    The wiki html generator class.
    """

    id = "pt.hive.colony.language.wiki.extensions.html_generation"
    """ The extension id """

    name = "Html Documentation Generation Plugin"
    """ The name of the extension """

    short_name = "Html Documentation Generation"
    """ The short name of the extension """

    description = "Extension for html documentation generation"
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

        # retrieves the target path
        target_path = properties.get("target_path", None)

        # creates the extra resources paths list
        extra_resources_paths_list = []

        # creates the full target path
        full_target_path = file_path + "/" + target_path

        # in case the target directory does not exist
        if not os.path.exists(full_target_path):
            # creates the directory
            os.mkdir(full_target_path)

        # walks the file path
        os.path.walk(file_path, self.generate_wiki_file, (full_target_path, extra_resources_paths_list))

        # copies the base files
        self._copy_base_files(full_target_path)

        # copies the extra files
        self._copy_extra_files(file_path, full_target_path, extra_resources_paths_list)

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

        # retrieves the full target path and the extra resources paths list from the args
        full_target_path, extra_resources_paths_list = args

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
                self.info("Processing in html: %s" % full_file_path)

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
                generation_visitor = wiki_html_generation.wiki_html_generation.HtmlGenerationVisitor()
                generation_visitor.set_parser(wiki_parser.parser)
                generation_visitor.set_extension_manager(self.manager)
                generation_visitor.set_configuration_map(DEFAULT_CONFIGURATION_MAP)

                # accepts the double visit
                parse_result.accept_double(generation_visitor)

                # retrieves the string buffer from the generation visitor
                string_buffer = generation_visitor.get_string_buffer()

                # retrieves the resources paths list
                resources_paths_list = generation_visitor.get_resources_paths_list()

                # extends the extra resources paths list with the resources paths list
                extra_resources_paths_list.extend(resources_paths_list)

                # retrieves the html value from the string buffer
                html_value = string_buffer.getvalue()

                # opens the html file
                html_file = open(full_target_name + ".xhtml", "w+")

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

            # copies the base file to the target path
            self._copy_files((base_file_path,), target_path + base_target_path)

    def _copy_extra_files(self, base_path, target_path, extra_resources_paths_list):
        """
        Copies the extra files to the given target path.

        @type base_path: String
        @param base_path: The base path.
        @type target_path: String
        @param target_path: The target path.
        @type extra_resources_paths_list: List
        @param extra_resources_paths_list: The extra resources paths list.
        """

        # generates the full extra resources paths list
        full_extra_resources_paths_list = [base_path + "/" + extra_resources_path for extra_resources_path in extra_resources_paths_list]

        # copies the extra files to the target path
        self._copy_files(full_extra_resources_paths_list, target_path)

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

            # creates the target full path
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
