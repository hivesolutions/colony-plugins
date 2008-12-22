#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Omni ERP
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2087 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-20 22:25:42 +0100 (Mon, 20 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

import unittest

CRAWL_TARGET = "/remote_home/lmartinho/workspace/pocketgoogle/light-docs"
INDEX_TYPE = "file_system"

INDEX_PERSISTENCE_TARGET_FILE_PATH = "/remote_home/lmartinho/workspace/pocketgoogle/light-docs/t.dmp"
PERSISTENCE_TYPE = "file_system"
SERIALIZER_TYPE = "cpickle"

CRAWL_TARGET_INDEX_CREATION_BENCHMARK = 0.050
""" The benchmark for performance regression testing for index creation using CRAWL TARGET in seconds"""

TEST_QUERY = "ford"
""" The test query for index querying """

TEST_QUERY_FIRST_RESULT = "/remote_home/lmartinho/workspace/pocketgoogle/light-docs/cars.txt"
""" The first result expected for the test query """

QUERY_EVALUATOR_TYPE_VALUE = "query_evaluator_type"
""" The key for the properties map, to access the query evaluator type """

SEARCH_SCORER_FORMULA_TYPE_VALUE = "search_scorer_formula_type"
""" The search scorer formula intended for testing """

class SearchTest:
    """
    The Search plugin unit test class.
    The search plugin represents the centralized interface to the search infrastructure, 
    and is used as entry point for the search features.
    This test suite exercises the plugin's façade, exercising any attached plugins in the process.
    """

    search_plugin = None
    """ The Search plugin unit test plugin. """

    def __init__(self, search_plugin):
        """
        Constructor of the class
        
        @type search_plugin: SearchPlugin
        @param search_plugin: The search plugin.
        """

        self.search_plugin = search_plugin

    def get_plugin_test_case_bundle(self):
        return [SearchPluginTestCase]

class SearchTestCase(unittest.TestCase):
    """
    This test case targets the Search core.
    """

    def setUp(self):
        self.plugin.logger.info("Setting up Search Test Case...")
    
    def test_method_create_index(self):
        """
        This method targets the index creation using an available test path.
        """

        test_index = self.plugin.create_index({"start_path" : CRAWL_TARGET, "type" : INDEX_TYPE})
        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

    def test_method_persist_index(self):
        """
        This method targets the index persistence façade method of the search plugin.
        """

        # creates the test index
        test_index = self.plugin.create_index({"start_path" : CRAWL_TARGET, "type" : INDEX_TYPE})
        
        # persists the index to defined storage
        properties = {"file_path" : INDEX_PERSISTENCE_TARGET_FILE_PATH, "persistence_type" : PERSISTENCE_TYPE, "serializer_type": SERIALIZER_TYPE}
        persistence_sucess = self.plugin.persist_index(test_index, properties)
        self.assertTrue(persistence_sucess)

    def test_method_performance_create_index(self):
        """
        This test times the execution of the create index method, and fails if the specified benchmark is not met.
        """

        # gather start time
        start_time = time.time()

        # creates in-memory index
        test_index = self.plugin.create_index({"start_path" : CRAWL_TARGET, "type" : INDEX_TYPE})

        # gather end time
        end_time = time.time()

        # compute duration
        duration = end_time - start_time

        # asserts that the duration is inferior to the declared benchmark
        self.assertTrue(duration <= CRAWL_TARGET_INDEX_CREATION_BENCHMARK)

        # asserts that the index was successfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

    def test_method_query_index(self):
        """
        This test exercises the query index of the search plugin's façade. 
        The test begins by indexing small document repository containing only '.txt' files, and then query the resulting index.
        """

        # creates in-memory index
        test_index = self.plugin.create_index({"start_path" : CRAWL_TARGET, "type" : INDEX_TYPE})

        query_results = self.plugin.query_index(test_index, TEST_QUERY, {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_formula_type" : "term_frequency_formula_type"})

        first_result = query_results[0]
        first_result_document_id = first_result[0]

        self.assertEqual(first_result_document_id, TEST_QUERY_FIRST_RESULT)

    def test_method_query_index_sort_results_term_frequency_formula(self):
        """
        This test exercises querying the index, scoring the results and 
        sorting according to the term frequency score.        
        """

        crawl_target = "/remote_home/lmartinho/workspace/pocketgoogle/scorer_test"

        query = "luis"
        """ The query for the tf query test """

        term_frequency_scorer_first_result = "/remote_home/lmartinho/workspace/pocketgoogle/scorer_test/ficheiro_10.txt"
        """ The expected result for the tf query test """

        # creates in-memory index
        test_index = self.plugin.create_index({"start_path" : crawl_target, "type" : INDEX_TYPE})

        # queries the index and retrieves scored and sorted results
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_formula_type": "term_frequency_formula_type", SEARCH_SCORER_FORMULA_TYPE_VALUE : "term_frequency_formula_type"}
        query_results = self.plugin.query_index_sort_results(test_index, query, properties)
        
        self.assertTrue(query_results)

        # asserts that the top result was the expected one
        first_result = query_results[0]
        # gets the document id from the sortable search result
        first_result_document_id = first_result.document_id

        self.assertEqual(first_result_document_id, term_frequency_scorer_first_result)        

    def test_method_create_index_with_identifier(self):
        """
        This method targets the index creation using an available test path 
        and saving to the search index repository with a specified identifier.
        """
        
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.test_index_identifier", {"start_path" : CRAWL_TARGET, "type" : INDEX_TYPE})
        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_formula_type": "term_frequency_formula_type", SEARCH_SCORER_FORMULA_TYPE_VALUE : "term_frequency_formula_type"}
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.test_index_identifier", "ford", properties)
        # asserts that the index was sucessfully created
        first_result = test_results[0]
        first_result_document_id = first_result[0]

        self.assertEqual(first_result_document_id, TEST_QUERY_FIRST_RESULT)


class SearchPluginTestCase:

    @staticmethod
    def get_related_class():
        return pt.hive.colony.plugins.search_plugin.SearchPlugin

    @staticmethod
    def get_test_case():
        return SearchTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Search Plugin test case covering the server side plug-in's facade"
