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

__revision__ = "$LastChangedRevision: 8461 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-05-12 06:45:34 +0100 (qua, 12 Mai 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class RepositoryGeneratorManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Repository Generator Manager plugin.
    """

    id = "pt.hive.colony.plugins.repository.generator.manager"
    name = "Repository Generator Manager Plugin"
    short_name = "Repository Generator Manager"
    description = "A plugin to manager the generation of repositories"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/repository/generator_manager/resources/baf.xml"
    }
    capabilities = [
        "repository.generator.manager",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "repository.generator.adapter"
    ]
    main_modules = [
        "repository.generator_manager.repository_generator_manager_exceptions",
        "repository.generator_manager.repository_generator_manager_system"
    ]

    repository_generator_manager = None
    """ The repository generator manager """

    repository_generator_adapter_plugins = []
    """ The repository generator adapter plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import repository.generator_manager.repository_generator_manager_system
        self.repository_generator_manager = repository.generator_manager.repository_generator_manager_system.RepositoryGeneratorManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def generate_repository(self, parameters):
        """
        Generates a repository for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the repository generation.
        """

        return self.repository_generator_manager.generate_repository(parameters)

    @colony.base.decorators.load_allowed_capability("repository.generator.adapter")
    def repository_generator_adapter_load_allowed(self, plugin, capability):
        self.repository_generator_adapter_plugins.append(plugin)
        self.repository_generator_manager.repository_generator_adapter_load(plugin)

    @colony.base.decorators.unload_allowed_capability("repository.generator.adapter")
    def repository_generator_adapter_unload_allowed(self, plugin, capability):
        self.repository_generator_adapter_plugins.remove(plugin)
        self.repository_generator_manager.repository_generator_adapter_unload(plugin)
