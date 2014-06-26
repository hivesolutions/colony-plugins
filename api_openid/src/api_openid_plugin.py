#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class ApiOpenidPlugin(colony.Plugin):
    """
    The main class for the Openid Api plugin.
    """

    id = "pt.hive.colony.plugins.api.openid"
    name = "Openid Api"
    description = "The plugin that offers the openid api"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "api.openid"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.client.http"),
        colony.PluginDependency("pt.hive.colony.plugins.api.yadis"),
        colony.PluginDependency("pt.hive.colony.plugins.encryption.diffie_hellman"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.random")
    ]
    main_modules = [
        "api_openid"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import api_openid
        self.api_openid = api_openid.ApiOpenid(self)

    def create_server(self, api_attributes):
        """
        Creates a server, with the given api attributes.

        @type api_attributes: Dictionary
        @param api_attributes: The api attributes to be used.
        @rtype: OpenidServer
        @return: The created remote server.
        """

        return self.system.create_server(api_attributes)

    def create_client(self, api_attributes):
        """
        Creates a client, with the given api attributes.

        @type api_attributes: Dictionary
        @param api_attributes: The api attributes to be used.
        @rtype: OpenidClient
        @return: The created client.
        """

        return self.system.create_client(api_attributes)
