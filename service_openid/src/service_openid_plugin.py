#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

class ServiceOpenidPlugin(colony.base.system.Plugin):
    """
    The main class for the Openid Service plugin.
    """

    id = "pt.hive.colony.plugins.service.openid"
    name = "Openid Service"
    description = "The plugin that offers the openid service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/service_openid/openid/resources/baf.xml"
    }
    capabilities = [
        "service.openid",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.main.client.http", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.service.yadis", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.encryption.diffie_hellman", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.random", "1.x.x")
    ]
    main_modules = [
        "service_openid.openid.service_openid_exceptions",
        "service_openid.openid.service_openid_parser",
        "service_openid.openid.service_openid_system"
    ]

    service_openid = None
    """ The service openid """

    main_client_http_plugin = None
    """ The main client http plugin """

    service_yadis_plugin = None
    """ The service yadis plugin """

    encryption_diffie_hellman_plugin = None
    """ The encryption diffie helman plugin """

    random_plugin = None
    """ The random plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import service_openid.openid.service_openid_system
        self.service_openid = service_openid.openid.service_openid_system.ServiceOpenid(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def create_remote_server(self, service_attributes):
        """
        Creates a remote server, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: OpenidServer
        @return: The created remote server.
        """

        return self.service_openid.create_remote_server(service_attributes)

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: OpenidClient
        @return: The created remote client.
        """

        return self.service_openid.create_remote_client(service_attributes)

    def get_main_client_http_plugin(self):
        return self.main_client_http_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.client.http")
    def set_main_client_http_plugin(self, main_client_http_plugin):
        self.main_client_http_plugin = main_client_http_plugin

    def get_service_yadis_plugin(self):
        return self.service_yadis_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.service.yadis")
    def set_service_yadis_plugin(self, service_yadis_plugin):
        self.service_yadis_plugin = service_yadis_plugin

    def get_encryption_diffie_hellman_plugin(self):
        return self.encryption_diffie_hellman_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.encryption.diffie_hellman")
    def set_encryption_diffie_hellman_plugin(self, encryption_diffie_hellman_plugin):
        self.encryption_diffie_hellman_plugin = encryption_diffie_hellman_plugin

    def get_random_plugin(self):
        return self.random_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.random")
    def set_random_plugin(self, random_plugin):
        self.random_plugin = random_plugin
