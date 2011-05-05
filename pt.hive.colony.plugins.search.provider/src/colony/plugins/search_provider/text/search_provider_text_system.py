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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import re

import search_provider_text_exceptions

DEFAULT_FILE_EXTENSIONS = [
    "txt",
    "text",
    "TXT",
    "TEXT"
]
""" Default file extensions for the plugin to crawl for """

FILE_EXTENSIONS_VALUE = "file_extensions"
""" Key to retrieve the file extensions to consider from the properties map """

WORD_REGEX = "(?u)\w+"

class SearchProviderText:
    """
    The search provider text class.
    """

    search_provider_text_plugin = None
    """ The search provider text plugin """

    def __init__(self, search_provider_text_plugin):
        """
        Constructor of the class.

        @type search_provider_text_plugin: SearchProviderTextPlugin
        @param search_provider_text_plugin: The search provider text plugin.
        """

        self.search_provider_text_plugin = search_provider_text_plugin

    def is_file_provider(self, properties):

        if not "file_path" in properties:
            return False

        # retrieves the file path
        file_path = properties["file_path"]

        # check if the path corresponds to a file
        if not os.path.isfile(file_path):
            return False

        if FILE_EXTENSIONS_VALUE in properties:
            file_extensions = properties[FILE_EXTENSIONS_VALUE]
        else:
            file_extensions = DEFAULT_FILE_EXTENSIONS

        # retrieves the file extension
        file_extension = file_path.split(".")[-1]

        # in case the file extension is compatible
        if file_extension in file_extensions:
            return True

        return False

    def get_tokens(self, properties):
        if not "file_path" in properties:
            raise search_provider_text_exceptions.MissingProperty("file_path")

        # retrieves the file path
        file_path = properties["file_path"]

        # retrieves the file size (in bytes)
        file_size = os.path.getsize(file_path)

        # opens the file
        file = open(file_path, "r")

        # reads the file contents
        file_contents = file.read()

        # closes the file
        file.close()

        # compiles the word regular expression
        compiled_regex = re.compile(WORD_REGEX)

        # retrieves the list of words in the file
        words_list = compiled_regex.findall(file_contents)

        words_list_length = len(words_list)

        # generates the words metadata list
        words_metadata_list = [{"position" : value} for value in range(words_list_length)]

        # creates the document information map
        document_information_map = {
            "document_id": file_path,
            "file_path" : file_path,
            "file_size" : file_size
        }

        return [
            words_list,
            words_metadata_list,
            document_information_map
        ]
