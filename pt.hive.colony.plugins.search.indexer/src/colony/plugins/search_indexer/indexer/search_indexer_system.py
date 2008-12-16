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

class SearchIndexer:
    """
    The search indexer class.
    """

    search_indexer_plugin = None
    """ The search indexer plugin """

    def __init__(self, search_indexer_plugin):
        """
        Constructor of the class.
        
        @type search_indexer_plugin: SearchIndexerPlugin
        @param search_indexer_plugin: The search indexer plugin.
        """

        self.search_indexer_plugin = search_indexer_plugin

    def create_index(self, token_list, properties):
        """ Abstract factory method for index products """
        forward_index_map = self.create_forward_index(token_list, properties)
        inverted_index_map = self.create_inverted_index(forward_index_map, properties)
        
        # an index is a tuple composed of forward and inverted index
        return (forward_index_map, inverted_index_map)

    def create_forward_index(self, token_list, properties):
        # initialize the forward index data structure
        forward_index_map = {}

        # iterate through each document's token list
        for document_token_list in token_list:

            words_list, words_metadata_list, document_information_map = document_token_list

            document_id = document_information_map["document_id"]

            # initialize the document's word map, containing the list of hits for each word
            word_map = {}

            # the document tuple contains the document's metadata along with the word map with each word's hits in the document
            document_tuple = (document_information_map, word_map)

            # iterate through all word occurrences to generate the word_map
            length_words_list = len(words_list)
            for index in range(length_words_list):
                word = words_list[index]
                word_metadata = words_metadata_list[index]

                # the word hit structure holds the word metadata of the specific occurrence
                hit = word_metadata

                if not word in word_map:
                    word_map[word] = []
                
                word_hit_list = word_map[word]
                word_hit_list.append(hit)

            # place the document tuple in the forward index map
            forward_index_map[document_id] = document_tuple

        return forward_index_map

    def create_inverted_index(self, forward_index_map, properties):

        inverted_index_map = {}
 
        for document_id, document_tuple in forward_index_map.items():
            document_information_map, word_map = document_tuple

            for word_id, word_hit_list in word_map.items():
                if not word_id in inverted_index_map:
                    inverted_index_map[word_id] = {}

                document_map = inverted_index_map[word_id]
                document_map[document_id] = word_hit_list

        return inverted_index_map
