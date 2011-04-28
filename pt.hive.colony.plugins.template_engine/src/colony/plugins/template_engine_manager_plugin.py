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

__revision__ = "$LastChangedRevision: 723 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-15 21:09:57 +0000 (Seg, 15 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class TemplateEngineManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Template Engine Manager plugin.
    """

    id = "pt.hive.colony.plugins.template_engine.manager"
    name = "Template Engine Manager Plugin"
    short_name = "Template Engine Manager"
    description = "Template Engine Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/template_engine/manager/resources/baf.xml"
    }
    capabilities = [
        "template_engine_manager",
        "build_automation_item"
    ]
    main_modules = [
        "template_engine.manager.template_engine_ast",
        "template_engine.manager.template_engine_exceptions",
        "template_engine.manager.template_engine_manager_system",
        "template_engine.manager.template_engine_visitor"
    ]

    template_engine_manager = None
    """" The template engine manager """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global template_engine
        import template_engine.manager.template_engine_manager_system
        self.template_engine_manager = template_engine.manager.template_engine_manager_system.TemplateEngineManager(self)

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

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def parse_file_path(self, file_path):
        return self.template_engine_manager.parse_file_path(file_path)

    def parse_file_path_encoding(self, file_path, encoding):
        return self.template_engine_manager.parse_file_path(file_path, encoding)

    def parse_file_path_variable_encoding(self, file_path, encoding, variable_encoding):
        return self.template_engine_manager.parse_file_path_variable_encoding(file_path, encoding, variable_encoding)

    def parse_file(self, file):
        return self.template_engine_manager.parse_file(file)
