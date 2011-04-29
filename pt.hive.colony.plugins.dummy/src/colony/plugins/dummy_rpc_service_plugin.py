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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class DummyRpcServicePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Dummy Rpc Service plugin.
    """

    id = "pt.hive.colony.plugins.dummy.rpc_service"
    name = "Dummy Rpc Service Plugin"
    short_name = "Dummy Rpc Service"
    description = "Dummy Rpc Service Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.LAZY_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/dummy/rpc_service/resources/baf.xml"
    }
    capabilities = [
        "rpc_service",
        "build_automation_item"
    ]
    main_modules = [
        "dummy.rpc_service.dummy_rpc_service_system"
    ]

    dummy_rpc_service = None
    """ The dummy rpc service """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global dummy
        import dummy.rpc_service.dummy_rpc_service_system
        self.dummy_rpc_service = dummy.rpc_service.dummy_rpc_service_system.DummyRpcService(self)

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

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.plugin_call(True)
    def get_service_id(self):
        return self.dummy_rpc_service.get_service_id()

    @colony.base.decorators.plugin_call(True)
    def get_service_alias(self):
        return self.dummy_rpc_service.get_service_alias()

    @colony.base.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return self.dummy_rpc_service.get_available_rpc_methods()

    @colony.base.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return self.dummy_rpc_service.get_rpc_methods_alias()

    def echo(self, value):
        return self.dummy_rpc_service.echo(value)
