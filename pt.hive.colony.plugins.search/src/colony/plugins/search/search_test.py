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

CRAWL_TARGET = "/remote_home/search/light-docs"
INDEX_TYPE = "file_system"

INDEX_PERSISTENCE_TARGET_FILE_PATH = "/remote_home/search/light-docs/t.dmp"
PERSISTENCE_TYPE = "file_system"
SERIALIZER_TYPE = "cpickle"

CRAWL_TARGET_INDEX_CREATION_BENCHMARK = 0.050
""" The benchmark for performance regression testing for index creation using CRAWL TARGET in seconds"""

TEST_QUERY = "ford"
""" The test query for index querying """

TEST_QUERY_FIRST_RESULT = "/remote_home/search/light-docs/cars.txt"
""" The first result expected for the test query """

QUERY_EVALUATOR_TYPE_VALUE = "query_evaluator_type"
""" The key for the properties map, to access the query evaluator type """

SEARCH_SCORER_FORMULA_TYPE_VALUE = "search_scorer_formula_type"
""" The search scorer formula intended for testing """

import cProfile

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

        search_results = self.plugin.query_index(test_index, "ford and jaguar", {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"})
        # FIXME: getting a memory problem here, the second time a run the query some of the data is messed up        
        search_results = self.plugin.query_index(test_index, "ford jaguar", {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"})

        first_result = search_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, TEST_QUERY_FIRST_RESULT)

    def test_method_query_index_sort_results_term_frequency_formula(self):
        """
        This test exercises querying the index, scoring the results and 
        sorting according to the term frequency score.        
        """

        crawl_target = "/remote_home/search/scorer_test"

        query = "luis"
        """ The query for the tf query test """

        term_frequency_scorer_first_result = "/remote_home/search/scorer_test/ficheiro_10.txt"
        """ The expected result for the tf query test """

        # creates in-memory index
        test_index = self.plugin.create_index({"start_path" : crawl_target, "type" : INDEX_TYPE})

        # queries the index and retrieves scored and sorted results
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}
        query_results = self.plugin.query_index_sort_results(test_index, query, properties)

        self.assertTrue(query_results)

        # asserts that the top result was the expected one
        first_result = query_results[0]
        # gets the document id from the sortable search result
        first_result_document_id = first_result["document_id"]

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

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.test_index_identifier", "ford", properties)
        # asserts that the index was sucessfully created
        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, TEST_QUERY_FIRST_RESULT)

    def test_term_frequency_metrics(self):
        """
        This method targets the index time computation. 
        """

        properties = {"start_path" : "/remote_home/search/scorer_test",
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["term_frequency_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.test_index_identifier", properties)

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        # assert that the term frequency scorer metric was correctly calculated for the word "luis"
        self.assertEquals(test_index.inverted_index_map["luis"]["metrics"]["term_frequency_scorer_metric"], 19)

    def test_word_document_level_metrics(self):
        """
        This method targets the index time computation of word-document combination level metrics. 
        """

        properties = {"start_path" : "/remote_home/search/scorer_test",
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["word_document_frequency_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.test_index_identifier", properties)

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        # assert that the term frequency scorer metric was correctly calculated for the word "luis" and the document
        file1_path = "/remote_home/search/scorer_test/ficheiro_1.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file1_path]["metrics"]["word_document_frequency_scorer_metric"], 1) 
        file10_path = "/remote_home/search/scorer_test/ficheiro_10.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file10_path]["metrics"]["word_document_frequency_scorer_metric"], 10)

    def test_document_level_metrics(self):
        """
        This method targets the index time computation of document level metrics. 
        """

        properties = {"start_path" : "/remote_home/search/scorer_test",
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["document_hits_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.test_index_identifier", properties)

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)
        
        file1_path = "/remote_home/search/scorer_test/ficheiro_1.txt"
        self.assertEquals(test_index.forward_index_map[file1_path]["metrics"]["document_hits_scorer_metric"], 6) 
        file10_path = "/remote_home/search/scorer_test/ficheiro_10.txt"
        self.assertEquals(test_index.forward_index_map[file10_path]["metrics"]["document_hits_scorer_metric"], 15)
 
    def test_word_document_level_metrics(self):
        """
        This method targets the index time computation of word-document combination level metrics. 
        """

        properties = {"start_path" : "/remote_home/search/scorer_test",
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["word_document_frequency_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.test_index_identifier", properties)

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        # assert that the term frequency scorer metric was correctly calculated for the word "luis" and the document
        file1_path = "/remote_home/search/scorer_test/ficheiro_1.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file1_path]["metrics"]["word_document_frequency_scorer_metric"], 1) 
        file10_path = "/remote_home/search/scorer_test/ficheiro_10.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file10_path]["metrics"]["word_document_frequency_scorer_metric"], 10)

    def test_hit_level_metrics(self):
        """
        This method targets the index time computation of hit level metrics. 
        """

        properties = {"start_path" : "/remote_home/search/scorer_test",
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["hit_distance_to_top_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.test_index_identifier", properties)

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        file1_path = "/remote_home/search/scorer_test/ficheiro_1.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file1_path]["hits"][0]["metrics"]["hit_distance_to_top_scorer_metric"], 0)

        file10_path = "/remote_home/search/scorer_test/ficheiro_10.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file10_path]["hits"][1]["metrics"]["hit_distance_to_top_scorer_metric"], 6)        

        file10_path = "/remote_home/search/scorer_test/ficheiro_10.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file10_path]["hits"][2]["metrics"]["hit_distance_to_top_scorer_metric"], 7)        

    def test_term_frequency_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF 
        """

        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.test_index_identifier", {"start_path" : "/remote_home/search/scorer_test", "type" : INDEX_TYPE})
        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.test_index_identifier", "luis pedro", properties)
        # asserts that the index was sucessfully created
        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, "/remote_home/search/scorer_test/ficheiro_5.txt") 

    def test_word_frequency_scoring_with_index_time_metrics(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        """

        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.test_index_identifier", 
                                                              {"start_path" : "/remote_home/search/scorer_test", 
                                                               "type" : INDEX_TYPE, 
                                                               "metrics_identifiers" : ["word_document_frequency_scorer_metric"]})
        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_frequency_scorer_function"}
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.test_index_identifier", "luis", properties)
        # asserts that the index was sucessfully created
        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, "/remote_home/search/scorer_test/ficheiro_10.txt") 

    def test_word_frequency_scoring_with_search_time_metrics(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        computing the metrics in search time.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.new_index_identifier", 
                                                              {"start_path" : "/remote_home/search/scorer_test", 
                                                               "type" : INDEX_TYPE})
        # asserts that the index was successfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_frequency_scorer_function"}
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", "luis", properties)

        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, "/remote_home/search/scorer_test/ficheiro_10.txt")
    
    def test_word_frequency_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        computing the metrics in index time.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.new_index_identifier", 
                                                              {"start_path" : "/remote_home/search/scorer_functions_test", 
                                                               "type" : INDEX_TYPE,
                                                               "metrics_identifiers" : ["word_document_frequency_scorer_metric"]})
        
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_frequency_scorer_function"}
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", "luis martinho", properties)

        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, "/remote_home/search/scorer_functions_test/word_frequency_best/word_frequency_best.txt")

    def test_document_location_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to Document Location.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.new_index_identifier", 
                                                              {"start_path" : "/remote_home/search/scorer_functions_test", 
                                                               "type" : INDEX_TYPE})
        
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "document_location_scorer_function"}
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", "luis martinho", properties)

        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, "/remote_home/search/scorer_functions_test/document_location_best.txt")

    def test_word_distance_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to Word Distance
        computing the metrics in index time.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.new_index_identifier", 
                                                              {"start_path" : "/remote_home/search/scorer_functions_test", 
                                                               "type" : INDEX_TYPE})

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_distance_scorer_function"}
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", "luis martinho", properties)

        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, "/remote_home/search/scorer_functions_test/word_distance_best.txt")

    def test_hive_source_code_indexing_compare_scorer_functions(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to Word Distance
        computing the metrics in index time.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.new_index_identifier", 
                                                              {"start_path" : "/remote_home/search/scorer_functions_test",
                                                               "type" : INDEX_TYPE,
                                                               "file_extensions" : ["py", "PY", "txt", "TXT"]})

        scorer_functions = ["word_frequency_scorer_function", "document_location_scorer_function", "word_distance_scorer_function"]
        
        for scorer_function in scorer_functions:
            properties = {"search_scorer_function_identifier" : scorer_function}
            test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", "luis martinho plugin", properties)

            # print top 5 results for each function method
            print scorer_function
            for result in test_results[0:5]:
                print result["document_id"], "score: ", result["score"]

    def test_hive_source_code_indexing_combined_scorer_verification(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to the Combined Scorer
        computing the metrics in index time.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.new_index_identifier", 
                                                              {"start_path" : "/remote_home/search/scorer_functions_test",
                                                               "type" : INDEX_TYPE,
                                                               "file_extensions" : ["py", "PY", "txt", "TXT"]})
        test_results = {}

        scorer_functions = ["word_frequency_scorer_function", "document_location_scorer_function", "word_distance_scorer_function"]
        for scorer_function in scorer_functions:
            properties = {"search_scorer_function_identifier" : scorer_function}
            test_results[scorer_function] = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", "luis martinho", properties)

        combined_test_results = {}

        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 1.0,
                                                                                  "document_location_scorer_function" : 0.0,
                                                                                  "word_distance_scorer_function" : 0.0}}
        combined_test_results["word_frequency_scorer_function"] = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", "luis martinho", properties)

        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 0.0,
                                                                                  "document_location_scorer_function" : 1.0,
                                                                                  "word_distance_scorer_function" : 0.0}}
        combined_test_results["document_location_scorer_function"] = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", "luis martinho", properties)

        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 0.0,
                                                                                  "document_location_scorer_function" : 0.0,
                                                                                  "word_distance_scorer_function" : 1.0}}
        combined_test_results["word_distance_scorer_function"] = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", "luis martinho", properties)
        
        for scorer_function in test_results:
            for i in range(len(test_results[scorer_function])):
                self.assertEquals(test_results[scorer_function][i]["document_id"], combined_test_results[scorer_function][i]["document_id"])
                self.assertEquals(test_results[scorer_function][i]["score"], combined_test_results[scorer_function][i]["score"])

    def test_hive_source_code_indexing_combined_relevance(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to the Combined Scorer
        computing the metrics in index time.
        """

        test_index = None
        start_path = "/remote_home/search/scorer_functions_test"
        # gather index start time
        start_time = time.time()

        test_index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.new_index_identifier", 
                                                              {"start_path" : start_path,
                                                               "type" : INDEX_TYPE,
                                                               "file_extensions" : ["py", "PY", "txt", "TXT"]})
        # gather index end time
        end_time = time.time()

        # compute duration
        duration = end_time - start_time

        print "Index creation on '%s'" % start_path, " took ", duration, " s"
        index_statistics = test_index.get_statistics()
        print index_statistics

        test_results = {}

        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 1.0,
                                                                                  "document_location_scorer_function" : 1.0,
                                                                                  "word_distance_scorer_function" : 1.0}}
        query = "luis martinho"

        # gather index start time
        start_time = time.time()

        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.new_index_identifier", query, properties)

        # gather index end time
        end_time = time.time()

        # compute duration
        duration = end_time - start_time

        print "Search for '%s'" % query, " took ", duration, " s"

        print "frequency_location_distance_scorer_function", properties["frequency_location_distance_scorer_function_parameters"]
        for test_result in test_results[0:10]:
            print test_result["document_id"], "SCORE: ", test_result["score"]

    def test_no_hits_found(self):
        index = self.plugin.create_index_with_identifier("pt.hive.colony.plugins.search.test_index_identifier", {"start_path" : "/remote_home/search/scorer_functions_test", "type" : "file_system"})

        properties = {"query_evaluator_type" : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.test_index_identifier", "luis query", properties)
        self.assertEquals(len(test_results), 0)
        test_results = self.plugin.search_index_by_identifier("pt.hive.colony.plugins.search.test_index_identifier", "query", properties)
        self.assertEquals(len(test_results), 0)

    def test_no_documents_for_indexing(self):
        pass
    
    def test_non_regional_characters_find_regional_characters(self):
        pass

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
        return "Search Plugin test case covering the server side plugin's facade"
