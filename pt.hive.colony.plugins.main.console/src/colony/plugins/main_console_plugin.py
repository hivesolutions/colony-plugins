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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class MainConsolePlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Console Main plugin.
    """

    id = "pt.hive.colony.plugins.main.console"
    name = "Console Main Plugin"
    short_name = "Console Main"
    description = "The main console plugin that controls the console"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.JYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_dir}/main_console/console/resources/baf.xml"}
    capabilities = ["main", "main_console", "test_case", "build_automation_item"]
    capabilities_allowed = ["console_command_extension"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["main_console.console.main_console", "main_console.console.main_console_test"]

    console = None
    console_test_case_class = None

    console_command_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        self.console_command_plugins = []
        global main_console
        import main_console.console.main_console
        import main_console.console.main_console_test
        self.console = main_console.console.main_console.MainConsole(self)
        self.console_test_case_class = main_console.console.main_console_test.MainConsoleTestCase
        self.console.load_console()

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

        self.console.unload_console()

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.main.console", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.main.console", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def process_command_line(self, command_line, output_method):
        """
        Processes the given command line, with the given output method.

        @type command_line: String
        @param command_line: The command line to be processed.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @rtype: bool
        @return: If the processing of the command line was successful.
        """

        self.console.process_command_line(command_line, output_method)

    def get_default_output_method(self):
        """
        Retrieves the default output method.

        @rtype: Method
        @return: The default output method for console.
        """

        return self.console.get_default_output_method()

    def get_test_case(self):
        """
        Retrieves the test case.

        @rtype: TestCase
        @return: The test case.
        """

        return self.console_test_case_class

    @colony.plugins.decorators.load_allowed_capability("console_command_extension")
    def console_command_extension_load_allowed(self, plugin, capability):
        self.console_command_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("console_command_extension")
    def console_command_extension_unload_allowed(self, plugin, capability):
        self.console_command_plugins.remove(plugin)
