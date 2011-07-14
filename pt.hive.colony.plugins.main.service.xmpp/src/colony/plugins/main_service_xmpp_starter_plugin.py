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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainServiceXmppStarterPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Xmpp Service Main Starter plugin.
    """

    id = "pt.hive.colony.plugins.main.service.xmpp.starter"
    name = "Xmpp Service Main Starter Plugin"
    short_name = "Xmpp Service Main Starter"
    description = "The plugin that starts the xmpp service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_service_xmpp_starter/starter/resources/baf.xml"
    }
    capabilities = [
        "main",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.service.xmpp", "1.0.0")
    ]
    main_modules = [
        "main_service_xmpp_starter.starter.main_service_xmpp_starter_system"
    ]

    main_service_xmpp_plugin = None
    """ The main service xmpp plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

        # defines the parameters
        parameters = {
            "socket_provider" : "normal",
            "port" : 5222
        }

        self.main_service_xmpp_plugin.start_service(parameters)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

        self.main_service_xmpp_plugin.stop_service({})

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_main_service_xmpp_plugin(self):
        return self.main_service_xmpp_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.service.xmpp")
    def set_main_service_xmpp_plugin(self, main_service_xmpp_plugin):
        self.main_service_xmpp_plugin = main_service_xmpp_plugin
