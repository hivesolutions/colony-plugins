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

import dummy_plugin
import colony.plugins.plugin_system
import colony.plugins.decorators

class DummyPluginRpcService(dummy_plugin.DummyPlugin):
    """
    The main class for the Dummy Rpc Service plugin.
    """

    id = "pt.hive.colony.plugins.dummy.rpc_service"
    name = "Dummy Plugin Rpc Service"
    short_name = "Dummy Rpc Service"
    description = "Dummy Rpc Service Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.LAZY_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["rpc_service"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    valid = True

    def load_plugin(self):
        dummy_plugin.DummyPlugin.load_plugin(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        dummy_plugin.DummyPlugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        dummy_plugin.DummyPlugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        dummy_plugin.DummyPlugin.unload_allowed(self, plugin, capability)
        print "unloading dummy windows forms label 1 allowed..."

    def dependency_injected(self, plugin):
        dummy_plugin.DummyPlugin.dependency_injected(self, plugin)

    @colony.plugins.decorators.plugin_call(True)
    def get_service_id(self):
        return "dummy_service"

    @colony.plugins.decorators.plugin_call(True)
    def get_service_alias(self):
        return []

    @colony.plugins.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return [self.echo]

    @colony.plugins.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return {self.echo : []}

    def echo(self, value):
        return "ola signor: " + value
