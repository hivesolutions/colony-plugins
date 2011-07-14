#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import copy

SEARCH_INTERPRETER_ADAPTER_TYPE = "capitals"

class SearchInterpreterCapitalsAdapter:
    """
    The search interpreter capitals adapter class.
    """

    search_interpreter_capitals_adapter_plugin = None
    """ The search interpreter capitals adapter plugin """

    def __init__(self, search_interpreter_capitals_adapter_plugin):
        """
        Constructor of the class.

        @type search_interpreter_capitals_adapter_plugin: SearchInterpreterCapitalsAdapterPlugin
        @param search_interpreter_capitals_adapter_plugin: The search interpreter capitals adapter plugin.
        """

        self.search_interpreter_capitals_adapter_plugin = search_interpreter_capitals_adapter_plugin

    def get_type(self):
        return SEARCH_INTERPRETER_ADAPTER_TYPE

    def process_tokens_list(self, tokens_list, properties):
        # iterates over the tokens list
        for tokens_list_item in tokens_list:
            words_list, words_metadata_list, _file_information_map = tokens_list_item

            index = 0

            final_words_list = copy.copy(words_list)

            for word in words_list:
                lower_case_word = word.lower()

                if not word == lower_case_word:
                    original_metadata = words_metadata_list[index]
                    new_metadata = copy.copy(original_metadata)

                    new_metadata["original_word_index"] = index
                    new_metadata["lower_cased"] = True
                    new_metadata["processed"] = True

                    index += 1
                    final_words_list.insert(index, lower_case_word)
                    words_metadata_list.insert(index, new_metadata)

                index += 1

            tokens_list_item[0] = final_words_list
