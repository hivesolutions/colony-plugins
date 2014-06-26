#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class MvcUtilsPlugin(colony.Plugin):
    """
    The main class for the Mvc Utils plugin.
    """

    id = "pt.hive.colony.plugins.mvc.utils"
    name = "Mvc Utils"
    description = "The plugin that offers the top-level abstractions for mvc processing"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "mvc.utils"
    ]
    capabilities_allowed = [
        "template_engine"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.template_engine"),
        colony.PluginDependency("pt.hive.colony.plugins.data.entity.manager"),
        colony.PluginDependency("pt.hive.colony.plugins.data.file.manager"),
        colony.PluginDependency("pt.hive.colony.plugins.business.helper"),
        colony.PluginDependency("pt.hive.colony.plugins.resources.manager"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.json")
    ]
    main_modules = [
        "mvc_utils"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import mvc_utils
        self.system = mvc_utils.MvcUtils(self)

    def assign_models(
        self,
        system_instance,
        plugin_instance,
        entity_manager_arguments
    ):
        return self.system.create_models(
            system_instance,
            plugin_instance,
            entity_manager_arguments = entity_manager_arguments
        )

    def unassign_models(
        self,
        system_instance,
        entity_manager_arguments
    ):
        return self.system.destroy_models(
            system_instance,
            entity_manager_arguments = entity_manager_arguments
        )

    def assign_controllers(
        self,
        system_instance,
        plugin_instance,
        entity_manager_arguments = {}
    ):
        return self.system.create_controllers(
            system_instance,
            plugin_instance,
            entity_manager_arguments = entity_manager_arguments
        )

    def unassign_controllers(self, system_instance):
        return self.system.destroy_controllers(system_instance)

    def assign_models_controllers(
        self,
        system_instance,
        plugin_instance,
        entity_manager_arguments = {}
    ):
        self.system.create_models(
            system_instance,
            plugin_instance,
            entity_manager_arguments = entity_manager_arguments
        )
        self.system.create_controllers(
            system_instance,
            plugin_instance,
            entity_manager_arguments = entity_manager_arguments
        )
        return True

    def unassign_models_controllers(
        self,
        system_instance,
        entity_manager_arguments = {}
    ):
        self.system.destroy_models(
            system_instance,
            entity_manager_arguments = entity_manager_arguments
        )
        self.system.destroy_controllers(system_instance)
        return True

    def create_file_manager(self, engine_name, connection_parameters):
        """
        Creates a new file manager reference, to manage files
        in an indirect and adapted fashion.
        The created file manager respects the given engine name
        and connection parameters.

        @type engine_name: String
        @param engine_name: The name of the engine to be used in
        the file manager.
        @type connection_parameters: Dictionary
        @param connection_parameters: The parameters for the connection
        in the file manager.
        @rtype: FileManager
        @return: The created file manager.
        """

        return self.system.create_file_manager(engine_name, connection_parameters)

    def generate_patterns(self, patterns, controller, prefix_name):
        return self.system.generate_patterns(patterns, controller, prefix_name)

    def generate_entity_manager_arguments(self, plugin, base = None, parameters = {}):
        return self.system.generate_entity_manager_arguments(plugin, base, parameters)

    def manager_arguments(self, *args, **kwargs):
        return self.generate_entity_manager_arguments(*args, **kwargs)
