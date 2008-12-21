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

__author__ = "Lu�s Martinho <lmartinho@hive.pt>"
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

class SearchTest:
    """
    The Search plugin unit test class.
    The search plugin represents the centralized interface to the search infrastructure, an is used as entry point for the search features.
    This test suite exercises the plugin's fa�ade, exercising any attached plugins in the process.
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
        This method targets the index creation using an available test path
        """

        test_index = self.plugin.create_index({"start_path" : CRAWL_TARGET, "type" : INDEX_TYPE})
        # asserts that the index was sucessfully created
        assert test_index
        assert test_index.forward_index_map
        assert test_index.inverted_index_map

    def test_method_persist_index(self):
        """
        This method targets the index persistence fa�ade method of the search plugin
        """

        # creates the test index
        test_index = self.plugin.create_index({"start_path" : CRAWL_TARGET, "type" : INDEX_TYPE})
        
        # persists the index to defined storage
        persistence_sucess = self.plugin.persist_index(test_index, {"file_path" : INDEX_PERSISTENCE_TARGET_FILE_PATH, "persistence_type" : PERSISTENCE_TYPE, "serializer_type": SERIALIZER_TYPE})
        assert persistence_sucess

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
        assert duration <= CRAWL_TARGET_INDEX_CREATION_BENCHMARK

        # asserts that the index was successfully created
        assert test_index
        assert test_index.forward_index_map
        assert test_index.inverted_index_map
        
    def test_method_query_index(self):
        """
        This test exercises the query index of the search plugin's fa�ade. 
        The test begins by indexing small document repository containing only '.txt' files, and then query the resulting index.
        """

        # creates in-memory index
        test_index = self.plugin.create_index({"start_path" : CRAWL_TARGET, "type" : INDEX_TYPE})

        self.plugin.query_index(test_index, TEST_QUERY, {"search_scorer_formula_type": "term_frequency_formula_type"})
        

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
