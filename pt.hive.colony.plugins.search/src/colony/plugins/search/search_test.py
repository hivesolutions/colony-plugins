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

import unittest

TEST_FILES_PATH = "resources/test"
""" The path to the test resources """

DEFAULT_INDEX_TYPE = "file_system"
""" The default type to use when creating an index """

DEFAULT_PERSISTENCE_TYPE = "file_system"
""" The default persistence type to use when persisting an index """

DEFAULT_SERIALIZER_TYPE = "cpickle"
""" The default serializer type to use when serializing an index """

TEST_QUERY = "lorem ipsum"
""" The test query for index querying """

QUERY_EVALUATOR_TYPE_VALUE = "query_evaluator_type"
""" The key for the properties map, to access the query evaluator type """

TEST_INDEX_IDENTIFIER = "test_index_identifier"
""" The index identifier to be used throughout the tests """

SCORER_FUNCTIONS_INDEX_IDENTIFIER = "scorer_functions_index_identifier"
""" The identifier for the index over the scorer function path """

TEST_WORD_VALUE = "lorem"
""" The word to test for frequency """

TEST_WORD_HITS = 3
""" The number of hits for the test word """

FILE_1_NUMBER_HITS = 157
""" The number of hits in file 1 """

FILE_2_NUMBER_HITS = 110
""" The number of hits in file 2 """

FILE_3_NUMBER_HITS = 126
""" The number of hits in file 3 """

TEST_WORD_FILE_1_HITS = 1
""" The number of hits of the test word in file 1 """

TEST_WORD_FILE_2_HITS = 2
""" The number of hits of the test word in file 2 """

TEST_WORD_FILE_1_HIT_DISTANCE_TO_TOP = 0
""" The distance to top for the test word in file 1 """

TEST_WORD_FILE_2_HIT_DISTANCE_TO_TOP = 62
""" The distance to top for the test word in file 2 """

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

    test_resources_path = None
    """ The path to the test resources """

    crawl_target_path = None
    """ The path to the crawl target directory """

    test_index = None
    """ The common test index """

    test_index_identifier = "none"
    """ The test index identifier """

    def setUp(self):
        self.plugin.info("Setting up Search Test Case...")

        # initialize the file paths for the test resources
        self.generate_test_file_paths()

        # generates the common indexes for re-use
        self.generate_test_indexes()

    def tearDown(self):
        properties = {}

        # if an index has been added to the repository remove it
        try:
            self.plugin.remove_index_with_identifier(TEST_INDEX_IDENTIFIER, properties)
        except Exception:
            pass

        # if the index persistence file has been created, remove it
        try:
            os.unlink(self.index_persistence_target_file_path)
        except OSError:
            pass

    def generate_test_file_paths(self):
        # in case the crawl target path has not been initialized
        if not self.test_resources_path:
            # determines the base path for the test resources
            self.test_resources_path = os.path.join(os.path.dirname(__file__), TEST_FILES_PATH)

            # determines the basic crawl target
            self.crawl_target_path = self.test_resources_path + "/crawler"

            # determines the crawler target path for the empty directory
            self.empty_crawler_target_path = self.test_resources_path + "/empty"

            # determines the file path for the index persistence
            self.index_persistence_target_file_path = self.test_resources_path + "/index.idx"

    def generate_test_indexes(self):
        if not self.test_index:
            # initializes the test index identifier
            self.test_index_identifier = TEST_INDEX_IDENTIFIER

            # creates the test index
            self.test_index = self.plugin.create_index_with_identifier(self.test_index_identifier, {"search_crawler_type" : DEFAULT_INDEX_TYPE,
                                                                                                    "search_crawler_options" : {"start_path" : self.crawl_target_path}})

    def test_create_index(self):
        """
        This method targets the index creation using an available test path.
        """

        # creates an index using the base crawl directory
        test_index = self.plugin.create_index({"search_crawler_type" : DEFAULT_INDEX_TYPE,
                                               "search_crawler_options" : {"start_path" : self.crawl_target_path}})

        # asserts that the index was successfully created
        self.assertTrue(test_index)

        # asserts that the index contains a forward index
        self.assertTrue(test_index.forward_index_map)

        # asserts that the index contains a inverted index
        self.assertTrue(test_index.inverted_index_map)

    def test_create_index_using_repository(self):
        """
        This method targets the index creation using an available test path and uses the repository in the process.
        """

        # creates an index using the base crawl directory and stores it in the repository
        create_index_result = self.plugin.create_index_with_identifier(TEST_INDEX_IDENTIFIER, {"search_crawler_type" : DEFAULT_INDEX_TYPE,
                                                                                               "search_crawler_options" : {"start_path" : self.crawl_target_path}})

        # asserts that the index was successfully created
        self.assertTrue(create_index_result)

        # retrieves the created index from the repository
        test_index = self.plugin.get_index_by_identifier(TEST_INDEX_IDENTIFIER)

        # asserts that the index was successfully retrieved
        self.assertTrue(test_index)

        # asserts that the retrieved index contains a forward index
        self.assertTrue(test_index.forward_index_map)

        # asserts that the retrieved index contains a inverted index
        self.assertTrue(test_index.inverted_index_map)

    def test_persist_index(self):
        """
        This method targets the index persistence façade method of the search plugin.
        """

        # retrieves a test index
        test_index = self.test_index

        # creates the properties map for the operation
        properties = {"file_path" : self.index_persistence_target_file_path, "search_persistence_type" : DEFAULT_PERSISTENCE_TYPE, "serializer_type" : DEFAULT_SERIALIZER_TYPE}

        # persists the index to defined storage
        persistence_sucess = self.plugin.persist_index(test_index, properties)

        # asserts that the persistence operation was successful
        self.assertTrue(persistence_sucess)

    def test_persist_index_with_identifier(self):
        """
        This method targets the index persistence façade method of the search plugin, using an index already in the repository
        """

        # retrieves a test index identifier
        test_index_identifier = self.test_index_identifier

        # creates a properties map specified the target persistence file and the persistence options
        properties = {"file_path" : self.index_persistence_target_file_path, "search_persistence_type" : DEFAULT_PERSISTENCE_TYPE, "serializer_type" : DEFAULT_SERIALIZER_TYPE}

        # persists the index to defined storage from the specified identifier
        persistence_sucess = self.plugin.persist_index_with_identifier(test_index_identifier, properties)

        # asserts if the persistence operation was successful
        self.assertTrue(persistence_sucess)

    def test_query_index(self):
        """
        This test exercises the query index of the search plugin's façade.
        The test begins by indexing small document repository containing only '.txt' files, and then query the resulting index.
        """

        # retrieves an in-memory index
        test_index = self.test_index

        # creates the test query
        test_query = "lorem and ipsum and amet and consectetur"

        # retrieves file 1
        file_1_path = self.crawl_target_path + "/1.txt"

        # queries the index
        search_results = self.plugin.query_index(test_index, test_query, {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"})

        # retrieves the first result
        first_result = search_results[0]

        # retrieves the document id for the first result
        first_result_document_id = first_result["document_id"]

        # checks the retrieves document id against the expected first result
        self.assertEqual(first_result_document_id, file_1_path)

    def test_search_index_by_identifier(self):
        """
        This method targets the index creation using an available test path
        and saving to the search index repository with a specified identifier.
        """

        # retrieves the appropriate test index identifier
        test_index_identifier = self.test_index_identifier

        # retrieves file 1
        file_1_path = self.crawl_target_path + "/1.txt"

        # creates the properties for the searhc operation
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}

        # searches the test index
        test_results_map = self.plugin.search_index_by_identifier(test_index_identifier, "lorem and ipsum and amet", properties)

        # retrieves the search results from the search results map
        test_results = test_results_map["search_results"]

        # asserts that the index was successfully created
        first_result = test_results[0]

        # retrieves the document id from the first hit
        first_result_document_id = first_result["document_id"]

        # checks the retrieves document against the expect test result
        self.assertEqual(first_result_document_id, file_1_path)

    def test_search_index_term_frequency_formula(self):
        """
        This test exercises querying the index, scoring the results and
        sorting according to the term frequency score.
        """

        # initializes the query for the term frequency formula
        query = TEST_WORD_VALUE

        # initializes the expected result for the term frequency query test
        term_frequency_scorer_first_result = self.crawl_target_path + "/2.txt"

        # retrieves the appropriate test index
        test_index = self.test_index

        # creates the properties map for the search query using the term frequency scorer function
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}

        # queries the index and retrieves scored and sorted results
        search_results_map = self.plugin.search_index(test_index, query, properties)

        # retrieves the search results list from the search results map
        search_results = search_results_map["search_results"]

        # retrieves the best result
        first_result = search_results[0]

        # gets the document id from the best result map
        first_result_document_id = first_result["document_id"]

        # asserts that the top result was the expected one
        self.assertEqual(first_result_document_id, term_frequency_scorer_first_result)

    def test_term_frequency_metrics(self):
        """
        This method targets the index time computation.
        """

        # creates the properties map for creating the index with term frequency metric
        properties = {"search_crawler_type" : DEFAULT_INDEX_TYPE,
                      "search_crawler_options" : {"start_path" : self.crawl_target_path},
                      "metrics_identifiers" : ["term_frequency_scorer_metric"]}

        # creates the test index
        test_index = self.plugin.create_index(properties)

        # assert that the term frequency scorer metric was correctly calculated for the word test word
        self.assertEquals(test_index.inverted_index_map[TEST_WORD_VALUE]["metrics"]["term_frequency_scorer_metric"], TEST_WORD_HITS)

    def test_document_level_metrics(self):
        """
        This method targets the index time computation of document level metrics.
        """

        # creates the properties for creating the index with the documents hits scorer metric
        properties = {"search_crawler_type" : DEFAULT_INDEX_TYPE,
                      "search_crawler_options" : {"start_path" : self.crawl_target_path},
                      "metrics_identifiers" : ["document_hits_scorer_metric"]}

        # creates the index
        test_index = self.plugin.create_index(properties)

        # retrieves file 1
        file_1_path = self.crawl_target_path + "/1.txt"

        # retrieves file 2
        file_2_path = self.crawl_target_path + "/2.txt"

        # retrieves file 3
        file_3_path = self.crawl_target_path + "/3.txt"

        # checks the number of words in each file against the expected values
        self.assertEquals(test_index.forward_index_map[file_1_path]["metrics"]["document_hits_scorer_metric"], FILE_1_NUMBER_HITS)
        self.assertEquals(test_index.forward_index_map[file_2_path]["metrics"]["document_hits_scorer_metric"], FILE_2_NUMBER_HITS)
        self.assertEquals(test_index.forward_index_map[file_3_path]["metrics"]["document_hits_scorer_metric"], FILE_3_NUMBER_HITS)

    def test_word_document_level_metrics(self):
        """
        This method targets the index time computation of word-document combination level metrics.
        """

        # creates the properties for the index creation
        properties = {"search_crawler_type" : DEFAULT_INDEX_TYPE,
                      "search_crawler_options" : {"start_path" : self.crawl_target_path},
                      "metrics_identifiers" : ["word_document_frequency_scorer_metric"]}

        # creates the index
        test_index = self.plugin.create_index(properties)

        # retrieves file 1
        file_1_path = self.crawl_target_path + "/1.txt"

        # retrieves file 2
        file_2_path = self.crawl_target_path + "/2.txt"

        # retrieves file 3
        file_3_path = self.crawl_target_path + "/3.txt"

        # retrieves the hits map for the test word
        test_word_hits_map = test_index.inverted_index_map[TEST_WORD_VALUE]["hits"]

        # asserts that the word document frequency was correctly calculated for the test word in file 1
        self.assertEquals(test_word_hits_map[file_1_path]["metrics"]["word_document_frequency_scorer_metric"], TEST_WORD_FILE_1_HITS)

        # asserts that the word document frequency was correctly calculated for the test word in file 2
        self.assertEquals(test_word_hits_map[file_2_path]["metrics"]["word_document_frequency_scorer_metric"], TEST_WORD_FILE_2_HITS)

        # asserts that file 3 does not contain the test word
        try:
            # tries to retrieve the entry for file 3
            test_word_hits_map[file_3_path]

            # fails in case no exception is throw
            self.assertTrue(False);
        except KeyError:
            # success implies a KeyError exception
            self.assertTrue(True);
        except Exception, exception:
            # fails in case a different exception is thrown
            raise exception

    def test_hit_level_metrics(self):
        """
        This method targets the index time computation of hit level metrics.
        """

        # creates the properties for index creation
        properties = {"search_crawler_type" : DEFAULT_INDEX_TYPE,
                      "search_crawler_options" : {"start_path" : self.crawl_target_path},
                      "metrics_identifiers" : ["hit_distance_to_top_scorer_metric"]}

        # creates the index
        test_index = self.plugin.create_index(properties)

        # retrieves file 1
        file_1_path = self.crawl_target_path + "/1.txt"

        # retrieves file 2
        file_2_path = self.crawl_target_path + "/2.txt"

        # retrieves file 3
        file_3_path = self.crawl_target_path + "/3.txt"

        # retrieves the hits map for the test word
        test_word_hits_map = test_index.inverted_index_map[TEST_WORD_VALUE]["hits"]

        # asserts that the test word hit distance to top is the expected in file 1
        self.assertEquals(test_word_hits_map[file_1_path]["hits"][0]["metrics"]["hit_distance_to_top_scorer_metric"], TEST_WORD_FILE_1_HIT_DISTANCE_TO_TOP)

        # asserts that the test word hit distance to top is the expected in file 2
        self.assertEquals(test_word_hits_map[file_2_path]["hits"][0]["metrics"]["hit_distance_to_top_scorer_metric"], TEST_WORD_FILE_2_HIT_DISTANCE_TO_TOP)

        # asserts that file 3 does not contain the test word
        try:
            # tries to retrieve the entry for file 3
            test_word_hits_map[file_3_path]

            # fails in case no exception is throw
            self.assertTrue(False);
        except KeyError:
            # success implies a KeyError exception
            self.assertTrue(True);
        except Exception, exception:
            # fails in case a different exception is thrown
            raise exception

    def test_term_frequency_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        """

        # retrieves a test index
        test_index = self.test_index

        # initializes the query
        query = TEST_WORD_VALUE

        # determines the file path for the best result, by term frequency
        term_frequency_best_file_path = self.crawl_target_path + "/2.txt"

        # creates the properties for the search operation
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}

        # runs the search
        test_results_map = self.plugin.search_index(test_index, query, properties)

        # retrieves the search results list from the search results map
        test_results = test_results_map["search_results"]

        # retrieves the top search result
        first_result = test_results[0]

        # retrieves the document id for the top search result
        first_result_document_id = first_result["document_id"]

        # asserts that the best result is the expected one
        self.assertEqual(first_result_document_id, term_frequency_best_file_path)

    def test_word_frequency_scoring_with_search_time_metrics(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        computing the metrics in search time.
        """

        # retrieves the test index identifier
        test_index_identifier = self.test_index_identifier

        # initializes the test query to use in the test
        query = TEST_WORD_VALUE

        # initializes the expected search result for the test
        word_frequency_best_file = self.crawl_target_path + "/2.txt"

        # creates the properties map for the word frequency scorer function query
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_frequency_scorer_function"}

        # searches the index index the specified properties
        test_results_map = self.plugin.search_index_by_identifier(test_index_identifier, query, properties)

        # retrieves the search results from the search results map
        test_results = test_results_map["search_results"]

        # retrieves the top search result
        first_result = test_results[0]

        # retrieves the document id from the result
        first_result_document_id = first_result["document_id"]

        # checks the retrieved document against the expected result for the test
        self.assertEqual(first_result_document_id, word_frequency_best_file)

    def test_word_frequency_scoring_with_index_time_metrics(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to WF
        computing the metrics in index time.
        """

        # initializes the test query to use in the test
        query = TEST_WORD_VALUE

        # initializes the expected search result for the test
        word_frequency_best_file = self.crawl_target_path + "/2.txt"

        # creates the index to support the test
        self.plugin.create_index_with_identifier(TEST_INDEX_IDENTIFIER, {"search_crawler_type" : DEFAULT_INDEX_TYPE,
                                                                         "search_crawler_options" : {"start_path" : self.crawl_target_path},
                                                                         "metrics_identifiers" : ["word_document_frequency_scorer_metric"]})

        # creates the properties map for the search operation
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_frequency_scorer_function"}

        # searches the index with the specified options
        test_results_map = self.plugin.search_index_by_identifier(TEST_INDEX_IDENTIFIER, query, properties)

        # retrieves the results from the results map
        test_results = test_results_map["search_results"]

        # retrieves the top result
        first_result = test_results[0]

        # retrieves the top result's document id
        first_result_document_id = first_result["document_id"]

        # checks the retrieved result id against the expect result for the test
        self.assertEqual(first_result_document_id, word_frequency_best_file)

    def test_document_location_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to Document Location.
        """

        # retrieves a test index identifier
        test_index_identifier = self.test_index_identifier

        # retrieves a test query
        test_query = TEST_QUERY

        # creates the properties for the search operation
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "document_location_scorer_function"}

        # searches the index
        test_results_map = self.plugin.search_index_by_identifier(test_index_identifier, test_query, properties)

        # retrieves the search results list from the search results map
        test_results = test_results_map["search_results"]

        # retrieves the top result
        first_result = test_results[0]

        # retrieves the document id for the top result
        first_result_document_id = first_result["document_id"]

        # retrieves the best file
        document_location_best_file = self.crawl_target_path + "/1.txt"

        # asserts that the retrieved document was the expected one
        self.assertEqual(first_result_document_id, document_location_best_file)

    def test_word_distance_scoring(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to Word Distance
        computing the metrics in index time.
        """

        # retrieves a test index identifier
        test_index_identifier = self.test_index_identifier

        # retrieves a test query
        test_query = "consectetur adipiscing vivamus"

        # creates a properties map for the search operation
        properties = {QUERY_EVALUATOR_TYPE_VALUE : "query_parser", "search_scorer_function_identifier" : "word_distance_scorer_function"}

        # searches the index
        test_results_map = self.plugin.search_index_by_identifier(test_index_identifier, test_query, properties)

        # retrieves the search results list from the search results map
        test_results = test_results_map["search_results"]

        # retrieves the top result
        first_result = test_results[0]

        # retrieves the top result document id
        first_result_document_id = first_result["document_id"]

        # retrieves the expected best file
        word_distance_best = self.crawl_target_path + "/1.txt"

        # checks if the retrieved result is the expected one
        self.assertEqual(first_result_document_id, word_distance_best)

    def test_combined_scorer(self):
        """
        This method targets the scoring infrastructure, and asserts if the results were properly scored and sorted according to the combined scorer
        computing the metrics in index time.
        """

        # retrieves a test index identifier
        test_index_identifier = self.test_index_identifier

        # retrieves a test query
        test_query = TEST_QUERY

        # initializes the test results map
        test_results = {}

        # initializes the scorer functions list
        scorer_functions = ["word_frequency_scorer_function", "document_location_scorer_function", "word_distance_scorer_function"]

        # for each scorer function
        for scorer_function in scorer_functions:
            # creates the search properties
            properties = {"search_scorer_function_identifier" : scorer_function}

            # performs the search
            search_results_map = self.plugin.search_index_by_identifier(test_index_identifier, test_query, properties)

            # retrieves the search results
            search_results = search_results_map["search_results"]

            # sets the results for the current scorer function in the test results map
            test_results[scorer_function] = search_results

        # initializes the combined test results
        combined_test_results = {}

        # creates the properties for the first search combination
        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 1.0,
                                                                                  "document_location_scorer_function" : 0.0,
                                                                                  "word_distance_scorer_function" : 0.0}}

        # performs the search sorting by word frequency
        search_results_map = self.plugin.search_index_by_identifier(TEST_INDEX_IDENTIFIER, test_query, properties)
        search_results = search_results_map["search_results"]
        combined_test_results["word_frequency_scorer_function"] = search_results

        # creates the properties for the second search combination
        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 0.0,
                                                                                  "document_location_scorer_function" : 1.0,
                                                                                  "word_distance_scorer_function" : 0.0}}

        # performs the search sorting by document location
        search_results_map = self.plugin.search_index_by_identifier(TEST_INDEX_IDENTIFIER, test_query, properties)
        search_results = search_results_map["search_results"]
        combined_test_results["document_location_scorer_function"] = search_results

        # creates the properties for the third search combination
        properties = {"search_scorer_function_identifier" : "frequency_location_distance_scorer_function",
                      "frequency_location_distance_scorer_function_parameters" : {"word_frequency_scorer_function" : 0.0,
                                                                                  "document_location_scorer_function" : 0.0,
                                                                                  "word_distance_scorer_function" : 1.0}}

        # performs the search sorting by word distance
        search_results_map = self.plugin.search_index_by_identifier(TEST_INDEX_IDENTIFIER, test_query, properties)
        combined_test_results["word_distance_scorer_function"] = search_results_map["search_results"]

        # asserts that the results from the individual functions are the same as the combined equivalents
        for scorer_function in test_results:
            for index in range(len(test_results[scorer_function])):
                self.assertEquals(test_results[scorer_function][index]["document_id"], combined_test_results[scorer_function][index]["document_id"])
                self.assertEquals(test_results[scorer_function][index]["score"], combined_test_results[scorer_function][index]["score"])

    def test_no_hits_found(self):
        # retrieves a test query
        test_query = TEST_QUERY

        # creates the index for the test and stores it in the repository
        self.plugin.create_index_with_identifier(TEST_INDEX_IDENTIFIER, {"search_crawler_type" : "file_system",
                                                                         "search_crawler_options" : {"start_path" : self.empty_crawler_target_path}})

        # creates the properties for the search operation
        properties = {"query_evaluator_type" : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}

        # searches the index
        test_results_map = self.plugin.search_index_by_identifier(TEST_INDEX_IDENTIFIER, test_query, properties)

        # retrieves the results list
        test_results = test_results_map["search_results"]

        # checks that the list is empty
        self.assertEquals(len(test_results), 0)

    def test_no_documents_for_indexing(self):
        # creats the test query
        test_query = TEST_QUERY

        # creates the index for the test and stores it in the repository
        self.plugin.create_index_with_identifier(TEST_INDEX_IDENTIFIER, {"search_crawler_type" : "file_system",
                                                                         "search_crawler_options" : {"start_path" : self.empty_crawler_target_path}})

        # creates the properties map for the empty search
        properties = {"query_evaluator_type" : "query_parser", "search_scorer_function_identifier" : "term_frequency_scorer_function"}

        # search indexes
        self.plugin.search_index_by_identifier(TEST_INDEX_IDENTIFIER, test_query, properties)

        # checks if no exception ocurred
        self.assertTrue(True)

    def test_search_index_start_record_number_records(self):
        """
        This method targets the sliding window feature of the search infrastructure. The search method
        provides optional start_record and number_records specification, allowing for variable size result set.
        """

        # creates the index for the test and stores it in the repository
        self.plugin.create_index_with_identifier(TEST_INDEX_IDENTIFIER, {"search_crawler_type" : DEFAULT_INDEX_TYPE,
                                                                         "search_crawler_options" : {"start_path" : self.crawl_target_path}})

        # creates the properties for the search
        properties = {"start_record" : 0, "number_records" : 2}

        # performs the search
        test_results = self.plugin.search_index_by_identifier(TEST_INDEX_IDENTIFIER, "luis", properties)

        # determines the number of search results
        test_results_size = len(test_results)

        # checks if the only two results where returned
        self.assertTrue(test_results_size == 2)

class SearchPluginTestCase:

    @staticmethod
    def get_test_case():
        return SearchTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Search Plugin test case covering the server side plugin's facade"
