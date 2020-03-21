#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class Nanger(colony.System):
    """
    The nanger class.
    """

    def load_components(self):
        """
        Loads the main components models, controllers, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the MVC utils plugin and uses it to creates the
        # controllers and assigning them to the current instance
        mvc_utils_plugin = self.plugin.mvc_utils_plugin
        mvc_utils_plugin.assign_controllers(self, self.plugin)

    def unload_components(self):
        """
        Unloads the main components models, controllers, etc.
        This load should occur the earliest possible in the unloading process.
        """

        # retrieves the MVC utils plugin and uses it to destroy the
        # controllers, unregistering them from the internal structures
        mvc_utils_plugin = self.plugin.mvc_utils_plugin
        mvc_utils_plugin.unassign_controllers(self)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the MVC service. The tuple should relate the route with the handler
        method/function.

        :rtype: Tuple
        :return: The tuple of regular expressions to be used as patterns,
        to the MVC service.
        """

        return (
            (r"nanger/?", self.main_controller.index, "get"),
            (r"nanger/index", self.main_controller.index, "get"),
            (r"nanger/plugins", self.main_controller.plugins, "get"),
            (r"nanger/console", self.main_controller.console, "get"),
            (r"nanger/log", self.main_controller.log, "get"),
            (r"nanger/diagnostics", self.main_controller.diagnostics, "get"),
            (r"nanger/about", self.main_controller.about, "get"),
            (r"nanger/diagnostics/requests", self.diagnostics_controller.requests, "get"),
            (r"nanger/diagnostics/requests/list", self.diagnostics_controller.requests_list, "get"),
            (r"nanger/diagnostics/requests/<int:request_id>", self.diagnostics_controller.requests_show, "get"),
            (r"nanger/plugins/list", self.plugin_controller.list, "get"),
            (r"nanger/plugins/<str:plugin_id>", self.plugin_controller.show, "get"),
            (r"nanger/plugins/<str:plugin_id>/load", self.plugin_controller.load, "get"),
            (r"nanger/plugins/<str:plugin_id>/unload", self.plugin_controller.unload, "get"),
            (r"nanger/plugins/<str:plugin_id>/reload", self.plugin_controller.reload, "get"),
            (r"nanger/console/init", self.console_controller.init, ("get", "post")),
            (r"nanger/console/execute", self.console_controller.execute, ("get", "post")),
            (r"nanger/console/autocomplete", self.console_controller.autocomplete, ("get", "post"))
        )

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the MVC service. The tuple should relate the route with the base
        file system path to be used.

        :rtype: Tuple
        :return: The tuple of regular expressions to be used as resource patterns,
        to the MVC service.
        """

        # retrieves the plugin manager and uses it to retrieve
        # the colony site plugin path
        plugin_manager = self.plugin.manager
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)

        return (
            (r"nanger/resources/.+", (plugin_path + "/nanger/resources/extras", "nanger/resources")),
        )
