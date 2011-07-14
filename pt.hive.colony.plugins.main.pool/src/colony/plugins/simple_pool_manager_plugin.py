#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class SimplePoolManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Simple Pool Manager plugin.
    """

    id = "pt.hive.colony.plugins.main.pool.simple_pool_manager"
    name = "Simple Pool Manager Plugin"
    short_name = "Simple Pool Manager"
    description = "Simple Pool Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_pool/simple_pool_manager/resources/baf.xml"
    }
    capabilities = [
        "simple_pool_manager",
        "build_automation_item"
    ]
    main_modules = [
        "main_pool.simple_pool_manager.simple_pool_manager_exceptions",
        "main_pool.simple_pool_manager.simple_pool_manager_system"
    ]

    simple_pool_manager = None
    """ The simple pool manager """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_pool.simple_pool_manager.simple_pool_manager_system
        self.simple_pool_manager = main_pool.simple_pool_manager.simple_pool_manager_system.SimplePoolManager(self)

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

    def create_new_simple_pool(self, name, description, pool_size, scheduling_algorithm, maximum_pool_size):
        return self.simple_pool_manager.create_new_simple_pool(name, description, pool_size, scheduling_algorithm, maximum_pool_size)
