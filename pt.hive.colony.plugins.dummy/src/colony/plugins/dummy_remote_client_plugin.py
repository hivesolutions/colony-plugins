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

__revision__ = "$LastChangedRevision: 136 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-24 11:42:26 +0100 (Fri, 24 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class DummyRemoteClientPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Dummy Remote Client Plugin.
    """

    id = "pt.hive.colony.plugins.dummy.remote_client"
    name = "Dummy Remote Client Plugin"
    short_name = "Dummy Remote Client"
    description = "Just another dummy remote client plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/dummy/remote_client/resources/baf.xml"
    }
    capabilities = [
        "dummy_remote_client",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.remote.client.manager", "1.0.0")
    ]
    main_modules = [
        "dummy.remote_client.dummy_remote_client_system"
    ]

    dummy_remote_client = None
    """ The dummy remote client """

    remote_client_manager_plugin = None
    """ The remote client manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import dummy.remote_client.dummy_remote_client_system
        self.dummy_remote_client = dummy.remote_client.dummy_remote_client_system.DummyRemoteClient(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.create_remote_call()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_remote_call(self):
        return self.dummy_remote_client.create_remote_call()

    def get_remote_client_manager_plugin(self):
        return self.remote_client_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.remote.client.manager")
    def set_remote_client_manager_plugin(self, remote_client_manager_plugin):
        self.remote_client_manager_plugin = remote_client_manager_plugin
