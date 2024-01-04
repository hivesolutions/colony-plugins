#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony


class ResourcesJSONPlugin(colony.Plugin):
    """
    The main class for the Resources JSON plugin.
    """

    id = "pt.hive.colony.plugins.resources.json"
    name = "Resources JSON"
    description = "A plugin to parse JSON resources"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["resources_parser"]
    dependencies = [colony.PluginDependency("pt.hive.colony.plugins.misc.json")]
    main_modules = ["resources_json"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import resources_json

        self.system = resources_json.ResourcesJSON(self)

    def get_resources_parser_name(self):
        return self.system.get_resources_parser_name()

    def parse_resource(self, resource):
        return self.system.parse_resource(resource)
