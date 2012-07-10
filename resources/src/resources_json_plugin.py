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

class ResourcesJsonlugin(colony.base.system.Plugin):
    """
    The main class for the Resources Json plugin.
    """

    id = "pt.hive.colony.plugins.resources.json"
    name = "Resources Json"
    description = "A plugin to parse json resources"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "resources_parser"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.x.x")
    ]
    main_modules = [
        "resources.json.system"
    ]

    resources_json = None
    """ The resources json (parser) """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import resources.json.system
        self.resources_json = resources.json.system.ResourcesJson(self)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def get_resources_parser_name(self):
        return self.resources_json.get_resources_parser_name()

    def parse_resource(self, resource):
        return self.resources_json.parse_resource(resource)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
