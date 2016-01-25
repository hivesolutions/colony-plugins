#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class Crypton(colony.System):
    """
    The crypton class, responsible for the coordination of
    the main operation under the encryption infra-structure.
    """

    keys_map = {}
    """ The map of keys """

    security_map = {}
    """ The map of security """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.keys_map = {}
        self.security_map = {}

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the mvc utils plugin and uses it in the generation
        # of the proper entity manager arguments for the assign operation
        mvc_utils_plugin = self.plugin.mvc_utils_plugin
        self.arguments = mvc_utils_plugin.manager_arguments(
            self.plugin,
            parameters = dict(
                id = "pt.hive.colony.crypton.database",
                database_prefix = "crypton_"
            )
        )

        # creates the entity models classes by creating the entity manager
        # and updating the classes, this trigger the loading of the entity
        # manager (and creation of it if necessary) then creates the controllers
        mvc_utils_plugin.assign_models_controllers(self, self.plugin, self.arguments)

    def unload_components(self):
        """
        Unloads the main components models, controllers, etc.
        This load should occur the earliest possible in the unloading process.
        """

        # retrieves the mvc utils plugin and uses the reference to
        # destroy the entity models, unregistering them from the
        # entity manager instance and then destroy the controllers,
        # unregistering them from the internal structures
        mvc_utils_plugin = self.plugin.mvc_utils_plugin
        mvc_utils_plugin.unassign_models_controllers(self, self.arguments)

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
            (r"crypton/encrypt", self.main_controller.encrypt, "get"),
            (r"crypton/decrypt", self.main_controller.decrypt, "get"),
            (r"crypton/sign", self.main_controller.sign, "get"),
            (r"crypton/verify", self.main_controller.verify, "get"),
            (r"crypton/consumers", self.consumer_controller.create, "post")
        )

    def get_controller(self, name):
        controller = self.controllers[name]
        return controller

    def set_configuration_property(self, configuration_property):
        configuration = configuration_property.get_data()
        keys_map = configuration["keys"]
        security_map = configuration["security"]
        self.keys_map = keys_map
        self.security_map = security_map

    def unset_configuration_property(self):
        self.keys_map = {}
        self.security_map = {}
