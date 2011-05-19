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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class DistributionXmlrpcHelperPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Distribution Xmlrpc Helper plugin.
    """

    id = "pt.hive.colony.plugins.distribution.helper.xmlrpc"
    name = "Distribution Xmlrpc Helper Plugin"
    short_name = "Distribution Xmlrpc Helper"
    description = "Distribution Xmlrpc Helper Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/distribution_helper/xmlrpc/resources/baf.xml"
    }
    capabilities = [
        "distribution_helper",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.remote.client.xmlrpc", "1.0.0")
    ]
    main_modules = [
        "distribution_helper.xmlrpc.distribution_xmlrpc_helper_system"
    ]

    distribution_xmlrpc_helper = None
    """ The distribution xmlrpc helper """

    main_xmlrpc_client_plugin = None
    """ The main xmlrpc client plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import distribution_helper.xmlrpc.distribution_xmlrpc_helper_system
        self.distribution_xmlrpc_helper = distribution_helper.xmlrpc.distribution_xmlrpc_helper_system.DistributionXmlrpcHelper(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.distribution.helper.xmlrpc", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_helper_name(self):
        return self.distribution_xmlrpc_helper.get_helper_name()

    def create_client(self, remote_reference):
        return self.distribution_xmlrpc_helper.create_client(remote_reference)

    def create_client_host(self, hostname, port, properties):
        return self.distribution_xmlrpc_helper.create_client_host(hostname, port, properties)

    def get_main_xmlrpc_client_plugin(self):
        return self.main_xmlrpc_client_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.remote.client.xmlrpc")
    def set_main_xmlrpc_client_plugin(self, main_xmlrpc_client_plugin):
        self.main_xmlrpc_client_plugin = main_xmlrpc_client_plugin
