#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class PrintingManagerPlugin(colony.Plugin):
    """
    The main class for the Printing Manager plugin.
    """

    id = "pt.hive.colony.plugins.printing.manager"
    name = "Printing Manager"
    description = "Printing Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "printing_manager",
        "console_command_extension"
    ]
    capabilities_allowed = [
        "printing"
    ]
    main_modules = [
        "printing_manager"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import printing_manager
        self.system = printing_manager.PrintingManager(self)
        self.console = printing_manager.ConsolePrintingManager(self)

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    def get_console_extension_name(self):
        return self.console.get_console_extension_name()

    def get_commands_map(self):
        return self.console.get_commands_map()

    def print_test(self, printing_options):
        return self.system.print_test(printing_options)

    def print_test_no_options(self):
        return self.system.print_test()

    def print_test_image(self, printing_options):
        return self.system.print_test_image(printing_options)

    def print_test_image_no_options(self):
        return self.system.print_test_image()

    def print_printing_language(self, printing_language_string, printing_options):
        return self.system.print_printing_language(printing_language_string, printing_options)

    def print_printing_language_no_options(self, printing_language_string):
        return self.system.print_printing_language(printing_language_string)

    @colony.load_allowed_capability("printing")
    def printing_load_allowed(self, plugin, capability):
        self.system.load_printing_plugin(plugin)

    @colony.unload_allowed_capability("printing")
    def printing_unload_allowed(self, plugin, capability):
        self.system.unload_printing_plugin(plugin)
