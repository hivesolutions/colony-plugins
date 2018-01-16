#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2018 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class ConsolePlugin(colony.Plugin):
    """
    The main class for the Console plugin.
    """

    id = "pt.hive.colony.plugins.console"
    name = "Console"
    description = "The console plugin that controls the console"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "console",
        "test_case"
    ]
    capabilities_allowed = [
        "console_command_extension",
        "console_authentication_handler"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.authentication")
    ]
    main_modules = [
        "console"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        self.system_command_plugins = []
        import console
        self.system = console.Console(self)
        self.test = console.ConsoleTestCase

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    @colony.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.Plugin.set_configuration_property(self, property_name, property)

    @colony.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.Plugin.unset_configuration_property(self, property_name)

    def create_console_context(self):
        """
        Creates a new console context for third party usage.

        :rtype: ConsoleContext
        :return: The creates console context.
        """

        return self.system.create_console_context()

    def create_console_interface_character(self, console_handler, console_context):
        """
        Creates a new console interface character based
        from the given console handler.

        :type console_handler: ConsoleHandler
        :param console_handler: The console handler to be used.
        :type console_context: ConsoleContext
        :param console_context: The console context to be used.
        :rtype: ConsoleInterfaceCharacter
        :return: The create console interface character.
        """

        return self.system.create_console_interface_character(console_handler, console_context)

    def execute_command_line(self, command_line):
        """
        Executes the given command line using the default
        output method.

        :type command_line: String
        :param command_line: The command line to be executed.
        :rtype: bool
        :return: If the execution of the command line was successful.
        """

        return self.system.process_command_line(command_line, None)

    def process_command_line(self, command_line, output_method):
        """
        Processes the given command line, with the given output method.

        :type command_line: String
        :param command_line: The command line to be processed.
        :type output_method: Method
        :param output_method: The output method to be used in the processing.
        :rtype: bool
        :return: If the processing of the command line was successful.
        """

        return self.system.process_command_line(command_line, output_method)

    def get_default_output_method(self):
        """
        Retrieves the default output method.

        :rtype: Method
        :return: The default output method for console.
        """

        return self.system.get_default_output_method()

    def get_test_case(self):
        """
        Retrieves the test case.

        :rtype: TestCase
        :return: The test case.
        """

        return self.test

    @colony.load_allowed_capability("console_command_extension")
    def console_command_extension_load_allowed(self, plugin, capability):
        self.system.console_command_extension_load(plugin)

    @colony.unload_allowed_capability("console_command_extension")
    def console_command_extension_unload_allowed(self, plugin, capability):
        self.system.console_command_extension_unload(plugin)

    @colony.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.system.set_configuration_property(property)

    @colony.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.system.unset_configuration_property()
