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

import os
import gc

import time

import unittest

TEST_FILES_PATH = "resources/test"

INDEX_TYPE = "file_system"
PERSISTENCE_TYPE = "file_system"
SERIALIZER_TYPE = "cpickle"

CRAWL_TARGET_INDEX_CREATION_BENCHMARK = 0.050
""" The benchmark for performance regression testing for index creation using CRAWL TARGET in seconds"""

TEST_QUERY = "ford"
""" The test query for index querying """

QUERY_EVALUATOR_TYPE_VALUE = "query_evaluator_type"
""" The key for the properties map, to access the query evaluator type """

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
        self.plugin.info("Setting up Search Test Case...")

        self.generate_test_files()

    def generate_test_files(self):
        # @todo: generate the test input on the fly

        # determine the base path for the test files
        self.test_files_path = os.path.join(os.path.dirname(__file__), TEST_FILES_PATH)

        # determine the basic crawl target
        self.crawl_target = self.test_files_path + "/crawler"

        self.index_persistence_target_file_path = self.test_files_path + "/index_persistence/index.idx"

        self.scorer_test_crawler_target = self.test_files_path + "/scorer"

        self.scorer_functions_test_crawler_target = self.test_files_path + "/scorer_functions"

        self.empty_crawler_target = self.test_files_path + "/empty"

        self.test_query_first_result = self.crawl_target + "/cars.txt"

    def test_method_create_index(self):
        """
        This method targets the index creation using an available test path.
        """

        test_index = self.plugin.create_index({"start_path" : self.crawl_target, "type" : INDEX_TYPE})

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

    def test_method_create_index_using_repository(self):
        """
        This method targets the index creation using an available test path and uses the repository in the process.
        """

        create_index_result = self.plugin.create_index_with_identifier("test_index_identifier", {"start_path" : self.crawl_target, "type" : INDEX_TYPE})

        # asserts that the index was sucessfully created
        self.assertTrue(create_index_result)

        test_index = self.plugin.get_index_by_identifier("test_index_identifier")

        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

    def test_method_persist_index(self):
        """
        This method targets the index persistence façade method of the search plugin.
        """

        # creates the test index
        test_index = self.plugin.create_index({"start_path" : self.crawl_target, "type" : "file_system"})

        # persists the index to defined storage
        properties = {"file_path" : self.index_persistence_target_file_path, "persistence_type" : PERSISTENCE_TYPE, "serializer_type": SERIALIZER_TYPE}
        persistence_sucess = self.plugin.persist_index(test_index, properties)
        self.assertTrue(persistence_sucess)

    def test_method_persist_index_with_identifier(self):
        """
        This method targets the index persistence façade method of the search plugin, using an index already in the repository
        """

        # declares the index identifier
        test_index_identifier = "test_index_identifier"

        # creates the test index
        test_index = self.plugin.create_index_with_identifier(test_index_identifier, {"start_path" : self.crawl_target, "type" : INDEX_TYPE})

        # persists the index to defined storage from the specified identifier
        properties = {"file_path" : self.index_persistence_target_file_path, "persistence_type" : PERSISTENCE_TYPE, "serializer_type": SERIALIZER_TYPE}
        persistence_sucess = self.plugin.persist_index_with_identifier(test_index_identifier, properties)
        self.assertTrue(persistence_sucess)

    def test_method_query_index(self):
        """
        This test exercises the query index of the search plugin's façade.
        The test begins by indexing small document repository containing only '.txt' files, and then query the resulting index.
        """

        # creates in-memory index
        test_index = self.plugin.create_index({"start_path" : self.crawl_target, "type" : INDEX_TYPE})

        search_results = self.plugin.query_index(test_index, "ford and jaguar", {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"})
        # FIXME: getting a memory problem here, the second time a run the query some of the data is messed up
        search_results = self.plugin.query_index(test_index, "ford jaguar", {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"})

        first_result = search_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, self.test_query_first_result)

    def test_method_search_index_term_frequency_formula(self):
        """
        This test exercises querying the index, scoring the results and
        sorting according to the term frequency score.
        """

        query = "luis"
        """ The query for the tf query test """

        term_frequency_scorer_first_result = "/remote_home/lmartinho/search/scorer_test/ficheiro_10.txt"
        """ The expected result for the tf query test """

        # creates in-memory index
        test_index = self.plugin.create_index({"start_path" : self.scorer_test_crawler_target, "type" : INDEX_TYPE})

        # queries the index and retrieves scored and sorted results
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}
        search_results_map = self.plugin.search_index(test_index, query, properties)

        search_results = search_results_map["search_results"]

        self.assertTrue(search_results)

        # asserts that the top result was the expected one
        first_result = search_results[0]
        # gets the document id from the sortable search result
        first_result_document_id = first_result["document_id"]

        # @todo: create assertion for the first result

    def test_method_create_index_with_identifier(self):
        """
        This method targets the index creation using an available test path
        and saving to the search index repository with a specified identifier.
        """

        test_index = self.plugin.create_index_with_identifier("test_index_identifier", {"start_path" : self.crawl_target, "type" : INDEX_TYPE})
        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}
        test_results_map = self.plugin.search_index_by_identifier("test_index_identifier", "ford", properties)

        test_results = test_results_map["search_results"]

        # asserts that the index was sucessfully created
        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        self.assertEqual(first_result_document_id, self.test_query_first_result)

    def test_term_frequency_metrics(self):
        """
        This method targets the index time computation.
        """

        properties = {"start_path" : self.scorer_test_crawler_target,
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["term_frequency_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("test_index_identifier", properties)

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

        properties = {"start_path" : self.scorer_test_crawler_target,
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["word_document_frequency_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("test_index_identifier", properties)

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        # assert that the term frequency scorer metric was correctly calculated for the word "luis" and the document
        file1_path = self.scorer_test_crawler_target + "/ficheiro_1.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file1_path]["metrics"]["word_document_frequency_scorer_metric"], 1)
        file10_path = self.scorer_test_crawler_target + "/ficheiro_10.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file10_path]["metrics"]["word_document_frequency_scorer_metric"], 10)

    def test_document_level_metrics(self):
        """
        This method targets the index time computation of document level metrics.
        """

        properties = {"start_path" : self.scorer_test_crawler_target,
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["document_hits_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("test_index_identifier", properties)

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        file1_path = self.scorer_test_crawler_target + "/ficheiro_1.txt"
        self.assertEquals(test_index.forward_index_map[file1_path]["metrics"]["document_hits_scorer_metric"], 6)
        file10_path = self.scorer_test_crawler_target + "/ficheiro_10.txt"
        self.assertEquals(test_index.forward_index_map[file10_path]["metrics"]["document_hits_scorer_metric"], 15)

    def test_word_document_level_metrics(self):
        """
        This method targets the index time computation of word-document combination level metrics.
        """

        properties = {"start_path" : self.scorer_test_crawler_target,
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["word_document_frequency_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("test_index_identifier", properties)

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        # assert that the term frequency scorer metric was correctly calculated for the word "luis" and the document
        file1_path = self.scorer_test_crawler_target + "/ficheiro_1.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file1_path]["metrics"]["word_document_frequency_scorer_metric"], 1)
        file10_path = self.scorer_test_crawler_target + "/ficheiro_10.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file10_path]["metrics"]["word_document_frequency_scorer_metric"], 10)

    def test_hit_level_metrics(self):
        """
        This method targets the index time computation of hit level metrics.
        """

        properties = {"start_path" : self.scorer_test_crawler_target,
                      "type" : INDEX_TYPE,
                      "metrics_identifiers" : ["hit_distance_to_top_scorer_metric"]}
        test_index = self.plugin.create_index_with_identifier("test_index_identifier", properties)

        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        file1_path = self.scorer_test_crawler_target + "/ficheiro_1.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file1_path]["hits"][0]["metrics"]["hit_distance_to_top_scorer_metric"], 0)

        file10_path = self.scorer_test_crawler_target + "/ficheiro_10.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file10_path]["hits"][1]["metrics"]["hit_distance_to_top_scorer_metric"], 6)

        file10_path = self.scorer_test_crawler_target + "/ficheiro_10.txt"
        self.assertEquals(test_index.inverted_index_map["luis"]["hits"][file10_path]["hits"][2]["metrics"]["hit_distance_to_top_scorer_metric"], 7)

    def test_term_frequency_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        """

        test_index = self.plugin.create_index_with_identifier("test_index_identifier", {"start_path" : self.scorer_test_crawler_target, "type" : INDEX_TYPE})
        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}
        test_results_map = self.plugin.search_index_by_identifier("test_index_identifier", "luis pedro", properties)
        test_results = test_results_map["search_results"]

        # asserts that the index was sucessfully created
        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        file5_path = self.scorer_test_crawler_target + "/ficheiro_5.txt"
        self.assertEqual(first_result_document_id, file5_path)

    def test_word_frequency_scoring_with_index_time_metrics(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        """

        test_index = self.plugin.create_index_with_identifier("test_index_identifier",
                                                              {"start_path" : self.scorer_test_crawler_target,
                                                               "type" : INDEX_TYPE,
                                                               "metrics_identifiers" : ["word_document_frequency_scorer_metric"]})
        # asserts that the index was sucessfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_frequency_scorer_function"}

        test_results_map = self.plugin.search_index_by_identifier("test_index_identifier", "luis", properties)
        test_results = test_results_map["search_results"]

        # asserts that the index was sucessfully created
        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        file10_path = self.scorer_test_crawler_target + "/ficheiro_10.txt"
        self.assertEqual(first_result_document_id, file10_path)

    def test_word_frequency_scoring_with_search_time_metrics(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        computing the metrics in search time.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("new_index_identifier",
                                                              {"start_path" : self.scorer_test_crawler_target,
                                                               "type" : INDEX_TYPE})
        # asserts that the index was successfully created
        self.assertTrue(test_index)
        self.assertTrue(test_index.forward_index_map)
        self.assertTrue(test_index.inverted_index_map)

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_frequency_scorer_function"}
        test_results_map = self.plugin.search_index_by_identifier("new_index_identifier", "luis", properties)
        test_results = test_results_map["search_results"]

        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        file10_path = self.scorer_test_crawler_target + "/ficheiro_10.txt"
        self.assertEqual(first_result_document_id, file10_path)

    def test_word_frequency_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        computing the metrics in index time.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("new_index_identifier",
                                                              {"start_path" : self.scorer_functions_test_crawler_target,
                                                               "type" : INDEX_TYPE,
                                                               "metrics_identifiers" : ["word_document_frequency_scorer_metric"]})

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_frequency_scorer_function"}
        test_results_map = self.plugin.search_index_by_identifier("new_index_identifier", "luis martinho", properties)
        test_results = test_results_map["search_results"]

        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        word_frequency_best_file = self.scorer_functions_test_crawler_target + "/word_frequency_best/word_frequency_best.txt"
        self.assertEqual(first_result_document_id, word_frequency_best_file)

    def test_document_location_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to Document Location.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("new_index_identifier",
                                                              {"start_path" : self.scorer_functions_test_crawler_target,
                                                               "type" : INDEX_TYPE})

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "document_location_scorer_function"}
        test_results_map = self.plugin.search_index_by_identifier("new_index_identifier", "luis martinho", properties)
        test_results = test_results_map["search_results"]

        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        document_location_best_file = self.scorer_functions_test_crawler_target + "/document_location_best.txt"
        self.assertEqual(first_result_document_id, document_location_best_file)

    def test_word_distance_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to Word Distance
        computing the metrics in index time.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("new_index_identifier",
                                                              {"start_path" : self.scorer_functions_test_crawler_target,
                                                               "type" : INDEX_TYPE})

        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_distance_scorer_function"}
        test_results_map = self.plugin.search_index_by_identifier("new_index_identifier", "luis martinho", properties)
        test_results = test_results_map["search_results"]

        first_result = test_results[0]
        first_result_document_id = first_result["document_id"]

        word_distance_best = self.scorer_functions_test_crawler_target + "/word_distance_best.txt"
        self.assertEqual(first_result_document_id, word_distance_best)

    def test_hive_source_code_indexing_compare_scorer_functions(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to Word Distance
        computing the metrics in index time.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("new_index_identifier",
                                                              {"start_path" : self.scorer_functions_test_crawler_target,
                                                               "type" : INDEX_TYPE,
                                                               "file_extensions" : ["py", "PY", "txt", "TXT"]})

        scorer_functions = ["word_frequency_scorer_function", "document_location_scorer_function", "word_distance_scorer_function"]

        for scorer_function in scorer_functions:
            properties = {"search_scorer_function_identifier" : scorer_function}
            test_results_map = self.plugin.search_index_by_identifier("new_index_identifier", "luis martinho plugin", properties)
            test_results = test_results_map["search_results"]

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
        test_index = self.plugin.create_index_with_identifier("new_index_identifier",
                                                              {"start_path" : self.scorer_functions_test_crawler_target,
                                                               "type" : INDEX_TYPE,
                                                               "file_extensions" : ["py", "PY", "txt", "TXT"]})
        test_results = {}

        scorer_functions = ["word_frequency_scorer_function", "document_location_scorer_function", "word_distance_scorer_function"]
        for scorer_function in scorer_functions:
            properties = {"search_scorer_function_identifier" : scorer_function}
            search_results_map = self.plugin.search_index_by_identifier("new_index_identifier", "luis martinho", properties)
            search_results = search_results_map["search_results"]
            test_results[scorer_function] = search_results

        combined_test_results = {}

        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 1.0,
                                                                                  "document_location_scorer_function" : 0.0,
                                                                                  "word_distance_scorer_function" : 0.0}}
        search_results_map = self.plugin.search_index_by_identifier("new_index_identifier", "luis martinho", properties)
        search_results = search_results_map["search_results"]
        combined_test_results["word_frequency_scorer_function"] = search_results

        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 0.0,
                                                                                  "document_location_scorer_function" : 1.0,
                                                                                  "word_distance_scorer_function" : 0.0}}
        search_results_map = self.plugin.search_index_by_identifier("new_index_identifier", "luis martinho", properties)
        search_results = search_results_map["search_results"]
        combined_test_results["document_location_scorer_function"] = search_results

        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 0.0,
                                                                                  "document_location_scorer_function" : 0.0,
                                                                                  "word_distance_scorer_function" : 1.0}}
        search_results_map = self.plugin.search_index_by_identifier("new_index_identifier", "luis martinho", properties)
        combined_test_results["word_distance_scorer_function"] = search_results_map["search_results"]

        for scorer_function in test_results:
            for i in range(len(test_results[scorer_function])):
                self.assertEquals(test_results[scorer_function][i]["document_id"], combined_test_results[scorer_function][i]["document_id"])
                self.assertEquals(test_results[scorer_function][i]["score"], combined_test_results[scorer_function][i]["score"])

    def test_no_hits_found(self):
        index = self.plugin.create_index_with_identifier("test_index_identifier", {"start_path" : self.scorer_functions_test_crawler_target, "type" : "file_system"})

        properties = {"query_evaluator_type" : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}
        test_results_map = self.plugin.search_index_by_identifier("test_index_identifier", "luis query", properties)
        test_results = test_results_map["search_results"]
        self.assertEquals(len(test_results), 0)
        test_results_map = self.plugin.search_index_by_identifier("test_index_identifier", "query", properties)
        test_results = test_results_map["search_results"]
        self.assertEquals(len(test_results), 0)

    def test_no_documents_for_indexing(self):
        index = self.plugin.create_index_with_identifier("test_index_identifier_nodocs", {"start_path" : self.empty_crawler_target, "type" : "file_system"})
        properties = {"query_evaluator_type" : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}
        test_results = self.plugin.search_index_by_identifier("test_index_identifier_nodocs", "luis query", properties)
        print test_results

    def test_method_persist_index_performance(self):
        """
        This method targets the index persistence façade method of the search plugin.
        """

        serializer_types = ["cpickle"]

        # switch to larger directory for more visible timing differences
        start_path = self.test_files_path
        index_file_path = self.index_persistence_target_file_path
        query = "martinho"

        test_index = None

        for serializer_type in serializer_types:
            for i in range(2):
                del test_index
                start_time = time.time()
                # creates the test index
                test_index = self.plugin.create_index({"start_path" : start_path, "type" : "file_system", "file_extensions" : ["py", "PY", "txt", "TXT", "xml", "XML", "js", "JS"]})
                end_time = time.time()

                duration = end_time - start_time
                self.plugin.debug("Index creation on '%s' took %f s" % (start_path, duration))

                start_time = time.time()
                # persists the index to defined storage
                properties = {"file_path" : index_file_path, "persistence_type" : "file_system", "serializer_type": serializer_type}
                persistence_sucess = self.plugin.persist_index(test_index, properties)
                end_time = time.time()

                duration = end_time - start_time
                self.plugin.debug("Persisting index on '%s' to index file '%s' took %f s using %s" % (start_path, index_file_path, duration, serializer_type))

                self.assertTrue(persistence_sucess)

        for serializer_type in serializer_types:
            for i in range(2):
                del test_index
                start_time = time.time()
                # loads the test index from the file
                properties = {"file_path" : index_file_path, "persistence_type" : "file_system", "serializer_type": serializer_type}
                test_index = self.plugin.load_index(properties)
                end_time = time.time()

                duration = end_time - start_time
                self.plugin.debug("Index loading from '%s' took %f s" % (index_file_path, duration))

                properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                              "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 1.0,
                                                                                          "document_location_scorer_function" : 1.0,
                                                                                          "word_distance_scorer_function" : 1.0}}

                # gather query start time
                start_time = time.time()
                test_results = self.plugin.search_index(test_index, query, properties)
                # gather index end time
                end_time = time.time()

                duration = end_time - start_time
                self.plugin.debug("Query on index from file '%s' took %f" % (index_file_path, duration))

                self.assertTrue(test_results)

    def test_hive_source_code_indexing_searching_performance_index_metrics(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to the Combined Scorer
        computing the metrics in index time.
        """

        test_index = None
        test_results = None
        # index the hive source
        start_path = self.test_files_path
        index_identifier = "test_index_identifier"
        query = "tiago silva hive ext"
        index_file_path = self.index_persistence_target_file_path

        # run the index creation and search repeatedly
        # index time metrics

        # gather index start time
        start_time = time.time()

        # clearing references
        test_index = None
        test_results = None

        properties = {"file_path" : index_file_path, "persistence_type" : "file_system", "serializer_type" : "cpickle"}

        # try to load a previously created index
        try:
            test_index = self.plugin.load_index_with_identifier(index_identifier, properties)
        except IOError:
            start_time = time.time()
            # if unable to load, create and store
            test_index = self.plugin.create_index_with_identifier(index_identifier,
                                                                  {"start_path" : start_path,
                                                                   "type" : "file_system",
                                                                   "file_extensions" : ["py", "PY", "txt", "TXT", "xml", "XML", "js", "JS"],
                                                                   "metrics_identifiers" : ["word_document_frequency_scorer_metric"]})

            end_time = time.time()
            duration = end_time - start_time
            self.plugin.debug("Index creation on '%s' took %f s" % (start_path, duration))

            properties = {"file_path" : index_file_path, "persistence_type" : "file_system", "serializer_type" : "cpickle"}
            self.plugin.persist_index(test_index, properties)

        # setup the search properties
        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 1.0,
                                                                                  "document_location_scorer_function" : 1.0,
                                                                                  "word_distance_scorer_function" : 1.0}}

        durations = []
        self.plugin.debug("START PERFORMANCE WATCH SEARCH BLOCK")
        for i in range(10):
            # gather query start time
            start_time = time.time()

            test_results_map = self.plugin.search_index_by_identifier(index_identifier, query, properties)
            test_results = test_results_map["search_results"]

            # gather index end time
            end_time = time.time()

            # compute duration
            duration = end_time - start_time

            self.plugin.debug("Search for '%s' with pre-computed metrics took %f s" % (query, duration))
            durations.append(duration)

        # compute average run time
        average = sum(durations) / len(durations)
        self.plugin.debug(">>> Search for '%s' with pre-computed metrics took on AVERAGE %f s" % (query, average))
        self.plugin.debug("END PERFORMANCE WATCH SEARCH BLOCK")

        durations = []
        query = "tiago silva"
        self.plugin.debug("START PERFORMANCE WATCH SEARCH BLOCK")
        for i in range(10):
            # gather query start time
            start_time = time.time()

            test_results_map = self.plugin.search_index_by_identifier(index_identifier, query, properties)
            test_results = test_results_map["search_results"]

            # gather index end time
            end_time = time.time()

            # compute duration
            duration = end_time - start_time

            self.plugin.debug("Search for '%s' with pre-computed metrics took %f s" % (query, duration))
            durations.append(duration)

        # compute average run time
        average = sum(durations) / len(durations)
        self.plugin.debug(">>> Search for '%s' with pre-computed metrics took on AVERAGE %f s" % (query, average))
        self.plugin.debug("END PERFORMANCE WATCH SEARCH BLOCK")

        durations = []
        query = "tiago silva hive"
        self.plugin.debug("START PERFORMANCE WATCH SEARCH BLOCK")
        for i in range(10):
            # gather query start time
            start_time = time.time()

            test_results_map = self.plugin.search_index_by_identifier(index_identifier, query, properties)
            test_results = test_results_map["search_results"]

            # gather index end time
            end_time = time.time()

            # compute duration
            duration = end_time - start_time

            self.plugin.debug("Search for '%s' with pre-computed metrics took %f s" % (query, duration))
            durations.append(duration)

        # compute average run time
        average = sum(durations) / len(durations)
        self.plugin.debug(">>> Search for '%s' with pre-computed metrics took on AVERAGE %f s" % (query, average))
        self.plugin.debug("END PERFORMANCE WATCH SEARCH BLOCK")

    def test_hive_source_code_indexing_searching_performance_search_metrics(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to the Combined Scorer
        computing the metrics in index time.
        """

        test_index = None
        # index the hive source
        start_path = self.test_files_path
        query = "tiago silva hive ext"

        # run the index creation and search repeatedly
        for i in range(3):
            # index time metrics

            # gather index start time
            start_time = time.time()

            # clearing references
            test_index = None
            test_results = None

            self.plugin.debug("Performance Test garbage collection started")
            garbage_collection_return = gc.collect()
            self.plugin.debug("Performance Test garbage collection finished in %f s returning %s" % (time.time() - start_time, garbage_collection_return))

            start_time = time.time()
            test_index = self.plugin.create_index_with_identifier("test_index_identifier",
                                                                  {"start_path" : start_path,
                                                                   "type" : "file_system",
                                                                   "file_extensions" : ["py", "PY", "txt", "TXT", "xml", "XML", "js", "JS"]})

            # gather index end time
            end_time = time.time()

            # compute duration
            duration = end_time - start_time

            self.plugin.debug("Index creation WITHOUT metrics on '%s' took %f s" % (start_path, duration))
            index_statistics = test_index.calculate_statistics()

            properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                          "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 1.0,
                                                                                      "document_location_scorer_function" : 1.0,
                                                                                      "word_distance_scorer_function" : 1.0}}

            # gather query start time
            start_time = time.time()

            test_results_map = self.plugin.search_index_by_identifier("test_index_identifier", query, properties)
            test_results = test_results_map["search_results"]

            # gather index end time
            end_time = time.time()

            # compute duration
            duration = end_time - start_time

            self.plugin.debug("Search for '%s' with search time metrics took %f s" % (query, duration))

            self.plugin.debug("frequency_location_distance_scorer_function %s" % properties["frequency_location_distance_scorer_function_parameters"])
            for test_result in test_results[0:10]:
                self.plugin.debug(" %s SCORE: %f" % (test_result["document_id"], test_result["score"]))

    def test_search_index_start_record_number_records(self):
        """
        This method targets the sliding window feature of the search infrastructure. The search method
        provides optional start_record and number_records specification, allowing for variable size result set.
        """

        test_index = None
        test_index = self.plugin.create_index_with_identifier("new_index_identifier",
                                                              {"start_path" : self.scorer_functions_test_crawler_target,
                                                               "type" : INDEX_TYPE})

        properties = {"start_record" : 0, "number_records" : 2}
        test_results = self.plugin.search_index_by_identifier("new_index_identifier", "luis", properties)
        test_results_size = len(test_results)

        self.assertTrue(test_results_size == 2)

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
