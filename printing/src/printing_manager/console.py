#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

CONSOLE_EXTENSION_NAME = "printing"
""" The console extension name """


class ConsolePrintingManager(colony.System):
    """
    The console printing manager class, responsible
    for the handling of the printing commands.
    """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_print_test(
        self, arguments, arguments_map, output_method, console_context
    ):
        printing_manager = self.plugin.system
        printing_manager.print_test()

    def process_print_test_image(
        self, arguments, arguments_map, output_method, console_context
    ):
        printing_manager = self.plugin.system
        printing_manager.print_test_image()

    def process_print_printing_language(
        self, arguments, arguments_map, output_method, console_context, file_path
    ):
        # retrieves the provided file path value and reads it's contents
        # then closes the file, these contents are the ones that are going
        # to be used for the printing process of the file
        file_path = arguments_map.get("file_path", None)
        file = open(file_path, "r")
        try:
            contents = file.read()
        finally:
            file.close()

        # retrieves the reference to the printing manager instance
        # and runs the printing process for the provided contents
        printing_manager = self.plugin.system
        printing_manager.print_printing_language(contents)

    def __generate_commands_map(self):
        return {
            "print_test": {
                "handler": self.process_print_test,
                "description": "prints a test page",
            },
            "print_image": {
                "handler": self.process_print_test_image,
                "description": "prints a test page with an image",
            },
            "print_language": {
                "handler": self.process_print_test_image,
                "description": "prints the page described in the file of the given file path",
                "arguments": [
                    {
                        "name": "file_path",
                        "description": "path to the file name to be printed",
                        "values": str,
                        "mandatory": False,
                    }
                ],
            },
        }
