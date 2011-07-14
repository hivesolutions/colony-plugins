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

__revision__ = "$LastChangedRevision: 8461 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-05-12 06:45:34 +0100 (qua, 12 Mai 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import repository_generator_manager_exceptions

REPOSITORY_GENERATOR_ADAPTER_VALUE = "repository_generator_adapter"
""" The repository generator adapter value """

class RepositoryGeneratorManager:
    """
    The repository generator manager class.
    """

    repository_generator_manager_plugin = None
    """ The repository generator manager plugin """

    repository_generator_adapter_plugins_map = {}
    """ The repository generator adapter plugins map """

    def __init__(self, repository_generator_manager_plugin):
        """
        Constructor of the class.

        @type repository_generator_manager_plugin: RepositoryGeneratorManagerPlugin
        @param repository_generator_manager_plugin: The repository generator manager plugin.
        """

        self.repository_generator_manager_plugin = repository_generator_manager_plugin

        self.repository_generator_adapter_plugins_map = {}

    def generate_repository(self, parameters):
        """
        Generates a repository for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the repository generation.
        """

        # in case the repository generator adapter is not in the parameters map
        if not REPOSITORY_GENERATOR_ADAPTER_VALUE in parameters:
            # raises the missing parameter exception
            raise repository_generator_manager_exceptions.MissingParameter(REPOSITORY_GENERATOR_ADAPTER_VALUE)

        # retrieves the repository generator adapter name from the parameters
        repository_generator_adapter_name = parameters[REPOSITORY_GENERATOR_ADAPTER_VALUE]

        # in case the adapter is not found in the adapter plugins map
        if not repository_generator_adapter_name in self.repository_generator_adapter_plugins_map:
            # raises an repository generator adapter not found exception
            raise repository_generator_manager_exceptions.RepositoryGeneratorHandlerNotFoundException("no adapter found for current request: " + repository_generator_adapter_name)

        # retrieves the repository generator adapter from the repository generator adapter plugins map
        repository_generator_adapter = self.repository_generator_adapter_plugins_map[repository_generator_adapter_name]

        # generates the repository using the repository generator adapter
        repository_generator_adapter.generate_repository(parameters)

    def repository_generator_adapter_load(self, repository_generator_adapter_plugin):
        # retrieves the plugin adapter name
        adapter_name = repository_generator_adapter_plugin.get_adapter_name()

        self.repository_generator_adapter_plugins_map[adapter_name] = repository_generator_adapter_plugin

    def repository_generator_adapter_unload(self, repository_generator_adapter_plugin):
        # retrieves the plugin adapter name
        adapter_name = repository_generator_adapter_plugin.get_adapter_name()

        del self.repository_generator_adapter_plugins_map[adapter_name]
