#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony


class APIYadisPlugin(colony.Plugin):
    """
    The main class for the Yadis API plugin.
    """

    id = "pt.hive.colony.plugins.api.yadis"
    name = "Yadis API"
    description = "The plugin that offers the Yadis API"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["api.yadis"]
    dependencies = [colony.PluginDependency("pt.hive.colony.plugins.client.http")]
    main_modules = ["api_yadis"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import api_yadis

        self.system = api_yadis.APIYadis(self)

    def create_client(self, api_attributes):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :rtype: YadisClient
        :return: The created client.
        """

        return self.system.create_client(api_attributes)
