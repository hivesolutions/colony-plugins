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

__revision__ = "$LastChangedRevision: 2688 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-16 12:24:34 +0100 (qui, 16 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class CommunicationPushPersistenceDatabasePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Communication Push Persistence Database plugin.
    """

    id = "pt.hive.colony.plugins.communication.push_persistence"
    name = "Communication Push Persistence Database Plugin"
    short_name = "Communication Push Persistence Database"
    description = "A plugin to manager the push notifications communication persistence using a database"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/communication_push_persistence_database/database/resources/baf.xml"
    }
    capabilities = [
        "communication.push_persistence",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.data.entity_manager_helper", "1.0.0")
    ]
    main_modules = [
        "communication_push_persistence_database.database.communication_push_persistence_database_system"
    ]

    communication_push_persistence_database = None
    """ The communication push persistence database """

    entity_manager_helper_plugin = None
    """ The entity manager helper plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global communication_push_persistence_database
        import communication_push_persistence_database.database.communication_push_persistence_database_system
        self.communication_push_persistence_database = communication_push_persistence_database.database.communication_push_persistence_database_system.CommunicationPushPersistenceDatabase(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.communication.push_persistence", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_persistence_name(self):
        """
        Retrieves the persistence name.

        @rtype: String
        @return: The persistence name.
        """

        return self.communication_push_persistence_database.get_persistence_name()

    def create_client(self, parameters):
        """
        Creates a client object for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to be used in creating
        the client object.
        @rtype: CommunicationPushPersistenceDatabaseClient
        @return: The created client object.
        """

        return self.communication_push_persistence_database.create_client(parameters)

    def get_entity_manager_helper_plugin(self):
        return self.entity_manager_helper_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.data.entity_manager_helper")
    def set_entity_manager_helper_plugin(self, entity_manager_helper_plugin):
        self.entity_manager_helper_plugin = entity_manager_helper_plugin
