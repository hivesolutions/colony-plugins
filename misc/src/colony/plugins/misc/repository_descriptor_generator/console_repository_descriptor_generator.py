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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 15336 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-07-14 21:44:26 +0100 (qui, 14 Jul 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

NONE_VALUE = "none"
""" The none value """

SIMPLE_LAYOUT_VALUE = "simple"
""" The simple layout value """

CONSOLE_EXTENSION_NAME = "repository_descriptor_generator"
""" The console extension name """

class ConsoleRepositoryDescriptorGenerator:
    """
    The console repository descriptor generator class.
    """

    repository_descriptor_generator_plugin = None
    """ The repository descriptor generator plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, repository_descriptor_generator_plugin):
        """
        Constructor of the class.

        @type repository_descriptor_generator_plugin: RepositoryDescriptorGeneratorPlugin
        @param repository_descriptor_generator_plugin: The repository descriptor generator plugin.
        """

        self.repository_descriptor_generator_plugin = repository_descriptor_generator_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_generate_repository_descriptor(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the download command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the repository descriptor generator instance
        repository_descriptor_generator = self.repository_descriptor_generator_plugin.repository_descriptor_generator

        # retrieves the mandatory arguments
        file_path = arguments_map["file_path"]

        # retrieves the option arguments
        repository_name = arguments_map.get("repository_name", NONE_VALUE)
        repository_description = arguments_map.get("repository_description", NONE_VALUE)
        repository_layout = arguments_map.get("repository_layout", SIMPLE_LAYOUT_VALUE)

        # outputs a message stating that the repository descriptor is being created
        output_method("creating repository descriptor in " + file_path)

        # generates the repository descriptor file
        repository_descriptor_generator.generate_repository_descriptor_file(file_path, repository_name, repository_description, repository_layout)

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "generate_repository_descriptor" : {
                "handler" : self.process_generate_repository_descriptor,
                "description" : "generates a repository descriptor with the available plugins",
                "arguments" : [
                    {
                        "name" : "file_path",
                        "description" : "the path of the repository descriptor file",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "repository_name",
                        "description" : "the name of the repository",
                        "values" : str,
                        "mandatory" : False
                    },
                    {
                        "name" : "repository_description",
                        "description" : "the description of the repository",
                        "values" : str,
                        "mandatory" : False
                    },
                    {
                        "name" : "repository_layout",
                        "description" : "the layout of the repository",
                        "values" : str,
                        "mandatory" : False
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
