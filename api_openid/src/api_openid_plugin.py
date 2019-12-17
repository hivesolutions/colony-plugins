#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class APIOpenidPlugin(colony.Plugin):
    """
    The main class for the OpenID API plugin.
    """

    id = "pt.hive.colony.plugins.api.openid"
    name = "OpenID API"
    description = "The plugin that offers the OpenID API"
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
        self.system = api_openid.APIOpenid(self)

    def create_server(self, api_attributes):
        """
        Creates a server, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :rtype: OpenIDServer
        :return: The created server.
        """

        return self.system.create_server(api_attributes)

    def create_client(self, api_attributes):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :rtype: OpenIDClient
        :return: The created client.
        """

        return self.system.create_client(api_attributes)
