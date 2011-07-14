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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import unittest

import colony.libs.logging_util

TEST_METHOD_PREFIX = "test_"
""" The test method prefix """

class MainTest:
    """
    The main test class.
    """

    main_test_plugin = None
    """ The main test plugin """

    current_id = 0
    """ The current id used for the test case """

    loaded_test_cases_list = []
    """ The list of loaded test cases """

    loaded_plugin_test_cases_list = []
    """ The list of loaded plugin test cases """

    test_case_test_case_plugin_map = {}
    """ The map associating the test cases with the test case plugins """

    test_case_plugin_test_case_map = {}
    """ The map associating the test case plugins with the test cases """

    test_case_test_case_name_map = {}
    """ The map associating the test case with the test case name """

    test_case_name_test_cases_map = {}
    """ The map associating a the test case name with the test cases """

    plugin_test_case_plugin_test_case_plugin_map = {}
    """ The map associating the plugin test cases with the plugin test case plugins """

    plugin_test_case_plugin_plugin_test_case_map = {}
    """ The map associating the plugin test case plugins with the plugin test cases """

    loaded_test_cases_id_map = {}
    """ The map with the loaded test cases associated with the test case id """

    id_loaded_test_cases_map = {}
    """ The map associating the test case id with the loaded test cases """

    def __init__(self, main_test_plugin):
        """
        Constructor of the class.

        @type main_test_plugin: MainTestPlugin
        @param main_test_plugin: The main test plugin.
        """

        self.main_test_plugin = main_test_plugin

        self.current_id = 0
        self.loaded_test_cases_list = []
        self.loaded_plugin_test_cases_list = []
        self.test_case_test_case_plugin_map = {}
        self.test_case_plugin_test_case_map = {}
        self.test_case_test_case_name_map = {}
        self.test_case_name_test_cases_map = {}
        self.plugin_test_case_plugin_test_case_plugin_map = {}
        self.plugin_test_case_plugin_plugin_test_case_map = {}
        self.loaded_test_cases_id_map = {}
        self.id_loaded_test_cases_map = {}

    def load_test_case(self, test_case, test_case_plugin, test_case_name = None):
        """
        Loads the given test case with the test case plugin referece an test
        case name.

        @type test_case: TestCase
        @param test_case: The test case to be loaded.
        @type test_case_plugin: Plugin
        @param test_case_plugin: The test case plugin to be used as reference in
        the test case load.
        @type test_case_name: String
        @param test_case_name: The test case name to be used in the test case
        loading.
        """

        # in case no test name is set
        if not test_case_name:
            # retrieves the test case name
            test_case_name = test_case.__name__

        # adds the test case to the list of test cases
        self.loaded_test_cases_list.append(test_case)

        # associates the test case with the test case plugin
        self.test_case_test_case_plugin_map[test_case] = test_case_plugin

        # associates the test case with the test case name
        self.test_case_test_case_name_map[test_case] = test_case_name

        # in case there is no test case name key in the map
        if not test_case_name in self.test_case_name_test_cases_map:
            self.test_case_name_test_cases_map[test_case_name] = []

        # associates the test case name with the test case
        self.test_case_name_test_cases_map[test_case_name].append(test_case)

        # in case there is no test plugin key in the map
        if not test_case_plugin in self.test_case_plugin_test_case_map:
            self.test_case_plugin_test_case_map[test_case_plugin] = []

        # associates the test case plugin with the test case
        self.test_case_plugin_test_case_map[test_case_plugin].append(test_case)

        # associates the test case with the test case id
        self.loaded_test_cases_id_map[test_case] = self.current_id

        # associates the test case id with the test case
        self.id_loaded_test_cases_map[self.current_id] = test_case

        # increments the current id
        self.current_id += 1

    def unload_test_case(self, test_case, test_case_plugin, test_case_name = None):
        """
        Unloads the given test case with the test case plugin referece an test
        case name.

        @type test_case: TestCase
        @param test_case: The test case to be unloaded.
        @type test_case_plugin: Plugin
        @param test_case_plugin: The test case plugin to be used as reference in
        the test case unload.
        @type test_case_name: String
        @param test_case_name: The test case name to be used in the test case
        unloading.
        """

        # in case no test name is set
        if not test_case_name:
            # retrieves the test case name
            test_case_name = test_case.__name__

        # retrieves the test case id
        test_case_id = self.loaded_test_cases_id_map[test_case]

        if test_case in self.loaded_test_cases_list:
            self.loaded_test_cases_list.remove(test_case)

        if test_case in self.test_case_test_case_plugin_map:
            del self.test_case_test_case_plugin_map[test_case]

        if test_case in self.test_case_test_case_name_map:
            del self.test_case_test_case_name_map[test_case]

        if test_case_name in self.test_case_name_test_cases_map:
            if test_case in self.test_case_name_test_cases_map[test_case_name]:
                self.test_case_name_test_cases_map[test_case_name].remove(test_case)

        if test_case_plugin in self.test_case_plugin_test_case_map:
            if test_case in self.test_case_plugin_test_case_map[test_case_plugin]:
                self.test_case_plugin_test_case_map[test_case_plugin].remove(test_case)

        if test_case in self.loaded_test_cases_id_map:
            del self.loaded_test_cases_id_map[test_case]

        if test_case_id in self.id_loaded_test_cases_map:
            del self.id_loaded_test_cases_map[test_case_id]

    def load_test_case_plugin(self, test_case_plugin):
        """
        Loads the test case for the given plugin.

        @type test_case_plugin: Plugin
        @param test_case_plugin: The plugin that contains the test case to be
        loaded.
        """

        # retrieves the test case
        test_case = test_case_plugin.get_test_case()

        # loads the test case
        self.load_test_case(test_case, test_case_plugin)

    def unload_test_case_plugin(self, test_case_plugin):
        """
        Unloads the test case for the given plugin.

        @type test_case_plugin: Plugin
        @param test_case_plugin: The plugin that contains the test case to be
        unloaded.
        """

        # retrieves the test case
        test_case = test_case_plugin.get_test_case()

        # unloads the test case
        self.unload_test_case(test_case, test_case_plugin)

    def load_test_case_bundle_plugin(self, test_case_bundle_plugin):
        """
        Loads the test case bundle for the given plugin.

        @type test_case_bundle_plugin: Plugin
        @param test_case_bundle_plugin: The plugin that contains the test case
        bundle to be loaded.
        """

        # retrieves the test case bundle
        test_case_bundle = test_case_bundle_plugin.get_test_case_bundle()

        # iterates over all the test cases in the test case bundle
        for test_case in test_case_bundle:
            self.load_test_case(test_case, test_case_bundle_plugin)

    def unload_test_case_bundle_plugin(self, test_case_bundle_plugin):
        """
        Unloads the test case bundle for the given plugin.

        @type test_case_bundle_plugin: Plugin
        @param test_case_bundle_plugin: The plugin that contains the test case
        bundle to be unloaded.
        """

        # retrieves the test case bundle
        test_case_bundle = test_case_bundle_plugin.get_test_case_bundle()

        # iterates over all the test cases in the test case bundle
        for test_case in test_case_bundle:
            self.unload_test_case(test_case, test_case_bundle_plugin)

    def load_plugin_test_case(self, plugin_test_case, plugin_test_case_plugin):
        """
        Loads the plugin test case for the given plugin test case plugin.

        @type plugin_test_case: PluginTestcase
        @param plugin_test_case: The plugin test case to be loaded.
        @type plugin_test_case_plugin: Plugin
        @param plugin_test_case_plugin: The plugin test case plugin to be used as
        reference in the plugin test case load.
        """

        # retrieves the test case from the plugin test case
        test_case = plugin_test_case.get_test_case()

        # adds the plugin test case to the list of plugin test cases
        self.loaded_plugin_test_cases_list.append(plugin_test_case)

        # associates the plugin test case with the plugin test case plugin
        self.plugin_test_case_plugin_test_case_plugin_map[plugin_test_case] = plugin_test_case_plugin

        # in case there is no test plugin key in the map
        if not plugin_test_case_plugin in self.plugin_test_case_plugin_plugin_test_case_map:
            self.plugin_test_case_plugin_plugin_test_case_map[plugin_test_case_plugin] = []

        # associates the plugin test case plugin with the plugin test case
        self.plugin_test_case_plugin_plugin_test_case_map[plugin_test_case_plugin].append(plugin_test_case)

        # loads the test case
        self.load_test_case(test_case, plugin_test_case_plugin)

    def unload_plugin_test_case(self, plugin_test_case, plugin_test_case_plugin):
        """
        Unloads the plugin test case for the given plugin test case plugin.

        @type plugin_test_case: PluginTestcase
        @param plugin_test_case: The plugin test case to be unloaded.
        @type plugin_test_case_plugin: Plugin
        @param plugin_test_case_plugin: The plugin test case plugin to be used as
        reference in the plugin test case unload.
        """

        # retrieves the test case from the plugin test case
        test_case = plugin_test_case.get_test_case()

        if plugin_test_case in self.loaded_plugin_test_cases_list:
            self.loaded_plugin_test_cases_list.remove(plugin_test_case)

        if plugin_test_case in self.plugin_test_case_plugin_test_case_plugin_map:
            del self.plugin_test_case_plugin_test_case_plugin_map[plugin_test_case]

        if plugin_test_case_plugin in self.plugin_test_case_plugin_plugin_test_case_map:
            if plugin_test_case in self.plugin_test_case_plugin_plugin_test_case_map[plugin_test_case_plugin]:
                self.plugin_test_case_plugin_plugin_test_case_map[plugin_test_case_plugin].remove(plugin_test_case)

        # unloads the test case
        self.unload_test_case(test_case, plugin_test_case_plugin)

    def load_plugin_test_case_plugin(self, plugin_test_case_plugin):
        """
        Loads the plugin test case for the given plugin.

        @type plugin_test_case_plugin: Plugin
        @param plugin_test_case_plugin: The plugin that contains the plugin test
        case to be loaded.
        """

        # retrieves the plugin test case
        plugin_test_case = plugin_test_case_plugin.get_plugin_test_case()

        # loads the plugin test case
        self.load_plugin_test_case(plugin_test_case, plugin_test_case_plugin)

    def unload_plugin_test_case_plugin(self, plugin_test_case_plugin):
        """
        Unloads the plugin test case for the given plugin.

        @type plugin_test_case_plugin: Plugin
        @param plugin_test_case_plugin: The plugin that contains the plugin test
        case to be unloaded.
        """

        # retrieves the plugin test case
        plugin_test_case = plugin_test_case_plugin.get_plugin_test_case()

        # unloads the plugin test case
        self.unload_plugin_test_case(plugin_test_case, plugin_test_case_plugin)

    def load_plugin_test_case_bundle_plugin(self, plugin_test_case_bundle_plugin):
        """
        Loads the plugin test case bundle for the given plugin.

        @type plugin_test_case_bundle_plugin: Plugin
        @param plugin_test_case_bundle_plugin: The plugin that contains the plugin test
        case bundle to be loaded.
        """

        # retrieves the plugin test case bundle
        plugin_test_case_bundle = plugin_test_case_bundle_plugin.get_plugin_test_case_bundle()

        # iterates over all the plugin test cases in the plugin test case bundle
        for plugin_test_case in plugin_test_case_bundle:
            self.load_plugin_test_case(plugin_test_case, plugin_test_case_bundle_plugin)

    def unload_plugin_test_case_bundle_plugin(self, plugin_test_case_bundle_plugin):
        """
        Unloads the plugin test case bundle for the given plugin.

        @type plugin_test_case_bundle_plugin: Plugin
        @param plugin_test_case_bundle_plugin: The plugin that contains the plugin test
        case bundle to be unloaded.
        """

        # retrieves the plugin test case bundle
        plugin_test_case_bundle = plugin_test_case_bundle_plugin.get_plugin_test_case_bundle()

        # iterates over all the plugin test cases in the plugin test case bundle
        for plugin_test_case in plugin_test_case_bundle:
            self.unload_plugin_test_case(plugin_test_case, plugin_test_case_bundle_plugin)

    def get_test_cases_for_name(self, test_case_name):
        """
        Retrieves all the test cases for the given name.

        @type test_case_name: String
        @param test_case_name: The name of the test cases to be retrieved.
        @rtype: List
        @return: All the test cases for the given name.
        """

        pass

    def get_test_cases_for_names(self, test_case_names_list):
        """
        Retrieves all the test cases for the given list of names.

        @type test_case_names_list: List
        @param test_case_names_list: The list of names of the test cases to be retrieved.
        @rtype: List
        @return: All the test cases for the given list of names.
        """

        pass

    def get_all_test_cases(self):
        """
        Retrieves the list with all the test cases.

        @rtype: List
        @return: The list with all the test cases.
        """

        return self.loaded_test_cases_list

    def get_all_test_cases_plugin(self, plugin_id, plugin_version):
        """
        Retrieves a list with all the test cases for the given plugin id and
        version.

        @type plugin_id: String.
        @param plugin_id: The id of the plugin to retrieve the list of test cases.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve the list of test cases.
        @rtype: List
        @return: A list with all the test cases for the given plugin id and version.
        """

        # retrieves the plugin manager
        manager = self.main_test_plugin.manager

        # retrieves the plugin
        plugin = manager._get_plugin_by_id_and_version(plugin_id, plugin_version)

        # in case plugin exist in test case plugin test case map
        if plugin in self.test_case_plugin_test_case_map:
            # retrieves the test cases associated with the given plugin
            plugin_test_cases = self.test_case_plugin_test_case_map[plugin]
        else:
            plugin_test_cases = []

        return plugin_test_cases

    def start_all_test(self):
        """
        Starts all the available tests.
        """

        self.start_test(self.loaded_test_cases_list)

    def start_test(self, test_cases_list, logger = None):
        """
        Starts the given test cases.

        @type test_cases_list: List
        @param test_cases_list: The list with the test cases to be started.
        @type logger: Logger
        @param logger: The logger to be used.
        """

        # retrieves the unit test test loader
        test_loader = unittest.TestLoader()

        # sets the prefix for the test loader
        test_loader.testMethodPrefix = TEST_METHOD_PREFIX

        # creates the global test suite
        global_test_suite = unittest.TestSuite()

        # iterates over all the test cases
        for test_case in test_cases_list:
            # retrieves the test case plugin for the given test case
            test_case_plugin = self.test_case_test_case_plugin_map[test_case]

            # sets the test case plugin
            test_case.plugin = test_case_plugin

            # creates the test suite for the test case
            test_suite = test_loader.loadTestsFromTestCase(test_case)

            # adds the test suite to the global test suite
            global_test_suite.addTest(test_suite)

        # creates a new logger test runner
        runner = LoggerTestRunner(logger)

        # runs the text test runner, retrieving the result
        test_result = runner.run(global_test_suite)

        # returns the test result
        return test_result

class LoggerTestResult(unittest.TestResult):
    """
    Class representing a test result, that support
    the logging to a custom logger.
    """

    logger = None
    """ The logger to be used """

    def __init__(self, logger):
        unittest.TestResult.__init__(self)

        if logger:
            self.logger = logger
        else:
            self.logger = colony.libs.logging_util.DummyLogger("dummy")

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)

        # retrieves the test id
        test_id = test.id()

        # prints an info message
        self.logger.info("Starting test '%s'" % test_id)

    def stopTest(self, test):
        unittest.TestResult.stopTest(self, test)

        # retrieves the test id
        test_id = test.id()

        # prints an info message
        self.logger.info("Stopping test '%s'" % test_id)

class LoggerTestRunner:
    """
    Class that controls the execution of
    the test for a logger environment.
    """

    logger = None
    """ The logger to be used """

    def __init__(self, logger = None):
        """
        Constructor of the class.

        @type logger: Logger
        @param logger: The logger to be used during the
        test run.
        """

        self.logger = logger

    def run(self, test_suite):
        """
        Runs the given test suite in the current
        environment.

        @type test_suite: TestSuite
        @param test_suite: The test suite to run in the
        current environment.
        """

        # creates a new logger test result object
        result = LoggerTestResult(self.logger)

        # runs the test suite
        test_suite(result)

        # returns the result (object)
        return result
