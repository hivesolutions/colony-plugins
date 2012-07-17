#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system

ENTITY_MANAGER_ARGUMENTS = {
    "id" : "pt.hive.colony.web.mvc.encryption.database",
    "engine" : "sqlite",
    "connection_parameters" : {
        "autocommit" : False
    }
}
""" The entity manager arguments """

ENTITY_MANAGER_PARAMETERS = {
    "default_database_prefix" : "crypton_"
}
""" The entity manager parameters """

class Crypton(colony.base.system.System):
    """
    The crypton class.
    """

    keys_map = {}
    """ The map of keys """

    security_map = {}
    """ The map of security """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        self.keys_map = {}
        self.security_map = {}

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the mvc utils plugin
        mvc_utils_plugin = self.plugin.mvc_utils_plugin

        # retrieves the entity manager arguments
        entity_manager_arguments = self.get_entity_manager_arguments()

        # creates the entity models classes by creating the entity manager
        # and updating the classes, this trigger the loading of the entity
        # manager (and creation of it if necessary) then creates the controllers
        mvc_utils_plugin.assign_models_controllers(self, self.plugin, entity_manager_arguments)

    def unload_components(self):
        """
        Unloads the main components models, controllers, etc.
        This load should occur the earliest possible in the unloading process.
        """

        # retrieves the mvc utils plugin
        mvc_utils_plugin = self.plugin.mvc_utils_plugin

        # retrieves the entity manager arguments
        entity_manager_arguments = self.get_entity_manager_arguments()

        # destroys the entity models, unregistering them from the
        # entity manager instance and then destroy the controllers,
        # unregistering them from the internal structures
        mvc_utils_plugin.unassign_models_controllers(self, entity_manager_arguments)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the mvc service.
        """

        return (
            (r"^crypton/sign$", self.main_controller.handle_sign, "get"),
            (r"^crypton/verify$", self.main_controller.handle_verify, "get"),
            (r"^crypton/consumers$", self.consumer_controller.handle_create, "post")
        )

    def get_communication_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as communication patterns,
        to the mvc service. The tuple should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as communication patterns,
        to the mvc service.
        """

        return ()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the mvc service.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)

        return (
            (r"^crypton/resources/.+$", (plugin_path + "/crypton/resources/extras", "crypton/resources")),
        )

    def get_controller(self, controller_name):
        """
        Retrieves the specified controller.

        @type controller_name: String
        @param controller_name: The controller's name.
        @rtype: Object
        @return The controller with the specified name.
        """

        # retrieves the controller
        controller = self.controllers[controller_name]

        # returns the controller
        return controller

    def set_configuration_property(self, configuration_property):
        # retrieves the configuration
        configuration = configuration_property.get_data()

        # retrieves the extension map
        keys_map = configuration["keys"]

        # retrieves the security map
        security_map = configuration["security"]

        # sets the keys map
        self.keys_map = keys_map

        # sets the security map
        self.security_map = security_map

    def unset_configuration_property(self):
        # sets the keys map
        self.keys_map = {}

        # sets the security map
        self.security_map = {}

    def get_entity_manager_arguments(self):
        """
        Retrieves the entity manager arguments.

        @rtype: Dictionary
        @return: The entity manager arguments.
        """

        # retrieves the mvc utils plugin
        mvc_utils_plugin = self.plugin.mvc_utils_plugin

        # generates the entity manager arguments
        entity_manager_arguments = mvc_utils_plugin.generate_entity_manager_arguments(self.plugin, ENTITY_MANAGER_ARGUMENTS, ENTITY_MANAGER_PARAMETERS)

        # returns the entity manager arguments
        return entity_manager_arguments
