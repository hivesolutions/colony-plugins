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

class ServiceYadisPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Yadis Service plugin.
    """

    id = "pt.hive.colony.plugins.service.yadis"
    name = "Yadis Service Plugin"
    short_name = "Yadis Service Main"
    description = "The plugin that offers the yadis service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/service_yadis/yadis/resources/baf.xml"
    }
    capabilities = [
        "service.yadis",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.client.http", "1.0.0")
    ]
    main_modules = [
        "service_yadis.yadis.service_yadis_exceptions",
        "service_yadis.yadis.service_yadis_parser",
        "service_yadis.yadis.service_yadis_system"
    ]

    service_yadis = None
    """ The service yadis """

    main_client_http_plugin = None
    """ The main client http plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import service_yadis.yadis.service_yadis_system
        self.service_yadis = service_yadis.yadis.service_yadis_system.ServiceYadis(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.service.yadis", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: YadisClient
        @return: The created remote client.
        """

        return self.service_yadis.create_remote_client(service_attributes)

    def get_main_client_http_plugin(self):
        return self.main_client_http_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.client.http")
    def set_main_client_http_plugin(self, main_client_http_plugin):
        self.main_client_http_plugin = main_client_http_plugin
