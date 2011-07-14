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

class ElementPoolManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Element Pool Manager plugin.
    """

    id = "pt.hive.colony.plugins.main.pool.element_pool_manager"
    name = "Element Pool Manager Plugin"
    short_name = "Element Pool Manager"
    description = "Element Pool Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_pool/element_pool_manager/resources/baf.xml"
    }
    capabilities = [
        "element_pool_manager",
        "build_automation_item"
    ]
    main_modules = [
        "main_pool.element_pool_manager.element_pool_manager_exceptions",
        "main_pool.element_pool_manager.element_pool_manager_system"
    ]

    element_pool_manager = None
    """ The element pool manager """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_pool.element_pool_manager.element_pool_manager_system
        self.element_pool_manager = main_pool.element_pool_manager.element_pool_manager_system.ElementPoolManager(self)

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

    def create_new_element_pool(self, create_method, destroy_method, pool_size):
        return self.element_pool_manager.create_new_element_pool(create_method, destroy_method, pool_size)
