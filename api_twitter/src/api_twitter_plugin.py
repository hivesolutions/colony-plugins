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
import colony.base.decorators

class ApiTwitterPlugin(colony.base.system.Plugin):
    """
    The main class for the Twitter Api plugin.
    """

    id = "pt.hive.colony.plugins.api.twitter"
    name = "Twitter Api"
    description = "The plugin that offers the twitter api"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "api.twitter"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.client.http", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.x.x")
    ]
    main_modules = [
        "api_twitter.exceptions",
        "api_twitter.system"
    ]

    api_twitter = None
    """ The api twitter """

    client_http_plugin = None
    """ The client http plugin """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import api_twitter.system
        self.api_twitter = api_twitter.system.ApiTwitter(self)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def create_remote_client(self, api_attributes):
        """
        Creates a remote client, with the given api attributes.

        @type api_attributes: Dictionary
        @param api_attributes: The api attributes to be used.
        @rtype: TwitterClient
        @return: The created remote client.
        """

        return self.api_twitter.create_remote_client(api_attributes)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.client.http")
    def set_client_http_plugin(self, client_http_plugin):
        self.client_http_plugin = client_http_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
