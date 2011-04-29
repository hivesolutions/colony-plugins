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

class HttpLogAnalyzerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Log Analyzer  plugin.
    """

    id = "pt.hive.colony.plugins.http_log_analyzer"
    name = "Http Log Analyzer Plugin"
    short_name = "Http Log Analyzer "
    description = "The http log analyzer plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/http_log_analyzer/log_analyzer/resources/baf.xml"
    }
    capabilities = [
        "_console_command_extension",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "http_log_parser"
    ]
    main_modules = [
        "http_log_analyzer.log_analyzer.console_http_log_analyzer",
        "http_log_analyzer.log_analyzer.http_log_analyzer_exceptions",
        "http_log_analyzer.log_analyzer.http_log_analyzer_system"
    ]

    http_log_analyzer = None
    """ The http log analyzer """

    http_log_parser_plugins = []
    """ The http log parser plugins list """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global http_log_analyzer
        import http_log_analyzer.log_analyzer.http_log_analyzer_system
        import http_log_analyzer.log_analyzer.console_http_log_analyzer
        self.http_log_analyzer = http_log_analyzer.log_analyzer.http_log_analyzer_system.HttpLogAnalyzer(self)
        self.console_http_log_analyzer = http_log_analyzer.log_analyzer.console_http_log_analyzer.ConsoleHttpLogAnalyzer(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.http_log_analyzer", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.http_log_analyzer", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.http_log_analyzer", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.load_allowed_capability("http_log_parser")
    def http_log_parser_load_allowed(self, plugin, capability):
        self.http_log_parser_plugins.append(plugin)
        self.http_log_analyzer.http_log_parser_plugin_load(plugin)

    @colony.base.decorators.unload_allowed_capability("http_log_parser")
    def http_log_parser_unload_allowed(self, plugin, capability):
        self.http_log_parser_plugins.remove(plugin)
        self.http_log_analyzer.http_log_parser_plugin_unload(plugin)

    def get_console_extension_name(self):
        return self.console_http_log_analyzer.get_console_extension_name()

    def get_commands_map(self):
        return self.console_http_log_analyzer.get_commands_map()

    def analyze_log(self, log_file_path, log_file_type):
        # analyzes the specified log file
        return self.http_log_analyzer.analyze_log(log_file_path, log_file_type)
