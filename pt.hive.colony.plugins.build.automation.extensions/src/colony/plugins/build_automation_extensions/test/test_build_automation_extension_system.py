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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

class TestBuildAutomationExtension:
    """
    The test build automation extension class.
    """

    test_build_automation_extension_plugin = None
    """ The test build automation extension plugin """

    def __init__(self, test_build_automation_extension_plugin):
        """
        Constructor of the class.
        
        @type test_build_automation_extension_plugin: TestBuildAutomationExtensionPlugin
        @param test_build_automation_extension_plugin: The test build automation extension plugin.
        """

        self.test_build_automation_extension_plugin = test_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure):
        # retrieves the main test plugin
        main_test_plugin = self.test_build_automation_extension_plugin.main_test_plugin

        # retrieves all the test cases for the given plugin
        plugin_test_cases = main_test_plugin.get_all_test_cases_plugin(plugin.id, plugin.version)

        # starts the test cases
        main_test_plugin.start_test(plugin_test_cases)
