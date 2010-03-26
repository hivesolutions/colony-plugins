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

CONSOLE_EXTENSION_NAME = "repository_descriptor"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### REPOSITORY DESCRIPTOR GENERATOR HELP ###\n\
generate_repository_descriptor <file-path> [repository-name] [repository-description] - generates a repository descriptor with the available plugins"
""" The help text """

class ConsoleRepositoryDescriptorGenerator:
    """
    The console repository descriptor generator class.
    """

    repository_descriptor_generator_plugin = None
    """ The repository descriptor generator plugin """

    commands = ["generate_repository_descriptor"]
    """ The commands list """

    def __init__(self, repository_descriptor_generator_plugin):
        """
        Constructor of the class.

        @type repository_descriptor_generator_plugin: RepositoryDescriptorGeneratorPlugin
        @param repository_descriptor_generator_plugin: The repository descriptor generator plugin.
        """

        self.repository_descriptor_generator_plugin = repository_descriptor_generator_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_generate_repository_descriptor(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        file_path = args[0]

        if len(args) > 1:
            repository_name = args[1]
        else:
            repository_name = "none"

        if len(args) > 2:
            repository_description = args[2]
        else:
            repository_description = "none"

        output_method("creating repository descriptor in " + file_path)

        self.repository_descriptor_generator_plugin.repository_descriptor_generator.generate_repository_descriptor_file(file_path, repository_name, repository_description)
