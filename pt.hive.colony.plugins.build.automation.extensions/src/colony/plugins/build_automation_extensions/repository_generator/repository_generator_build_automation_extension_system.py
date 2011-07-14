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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

RESOURCES_DIRECTORY_VALUE = "resources_directory"
""" The resources directory value """

REPOSITORY_DIRECTORY_VALUE = "repository_directory"
""" The repository directory value """

FORMATS_VALUE = "formats"
""" The formats value """

SOURCE_VALUE = "source"
""" The source value """

TARGET_VALUE = "target"
""" The target value """

CONTENTS_VALUE = "contents"
""" The contents value """

class RepositoryGeneratorBuildAutomationExtension:
    """
    The repository generator build automation extension class.
    """

    repository_generator_build_automation_extension_plugin = None
    """ The repository generator build automation extension plugin """

    def __init__(self, repository_generator_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type repository_generator_build_automation_extension_plugin: RepositoryGeneratorBuildAutomationExtensionPlugin
        @param repository_generator_build_automation_extension_plugin: The repository generator build automation extension plugin.
        """

        self.repository_generator_build_automation_extension_plugin = repository_generator_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # retrieves the repository generator manager plugin
        repository_generator_manager_plugin = self.repository_generator_build_automation_extension_plugin.repository_generator_manager_plugin

        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the resources directory
        resources_directory = build_properties[RESOURCES_DIRECTORY_VALUE]

        # retrieves the repository directory
        repository_directory = build_properties[REPOSITORY_DIRECTORY_VALUE]

        # retrieves the formats list
        formats = parameters[FORMATS_VALUE].split(",")

        # retrieves the source
        source = parameters.get(SOURCE_VALUE, resources_directory)

        # retrieves the target
        target = parameters.get(TARGET_VALUE, repository_directory)

        # retrieves the contents
        contents = parameters[CONTENTS_VALUE]

        # iterates over all the formats to generate the installation files
        for format in formats:
            # creates the repository generation parameters map
            repository_generation_parameters = {
                "repository_generator_adapter" : format,
                "source" : source,
                "target" : target,
                "contents" : contents
            }

            # generates the repository
            repository_generator_manager_plugin.generate_repository(repository_generation_parameters)

        # returns true (success)
        return True
