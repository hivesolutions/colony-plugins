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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 12670 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-01-13 13:08:29 +0000 (qui, 13 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class HttpLogParserCommonPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Http Log Parser Common plugin.
    """

    id = "pt.hive.colony.plugins.http_log_parser.common"
    name = "Http Log Parser Common Plugin"
    short_name = "Http Log Parser Common"
    description = "The http log parser common plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/http_log_parser_common/log_parser_common/resources/baf.xml"
    }
    capabilities = [
        "http_log_parser",
        "build_automation_item"
    ]
    main_modules = [
        "http_log_parser_common.log_parser_common.http_log_parser_common_exceptions",
        "http_log_parser_common.log_parser_common.http_log_parser_common_system"
    ]

    http_log_parser_common = None
    """ The http log parser common """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import http_log_parser_common.log_parser_common.http_log_parser_common_system
        self.http_log_parser_common = http_log_parser_common.log_parser_common.http_log_parser_common_system.HttpLogParserCommon(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_log_type(self):
        # returns the log type
        return self.http_log_parser_common.get_log_type()

    def create_log_parser(self):
        # returns the created log parser
        return self.http_log_parser_common.create_log_parser()
