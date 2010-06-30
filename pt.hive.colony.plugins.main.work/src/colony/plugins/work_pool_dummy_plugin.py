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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 9011 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-06-22 09:36:13 +0100 (ter, 22 Jun 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class WorkPoolDummyPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Work Pool Dummy plugin
    """

    id = "pt.hive.colony.plugins.main.work.work_pool_dummy"
    name = "Work Pool Dummy Plugin"
    short_name = "Work Pool Dummy"
    description = "Work Pool Dummy Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.JYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {}
    capabilities = ["startup"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.work.work_pool_manager", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = []

    work_pool_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

        self.work_pool = self.work_pool_manager_plugin.create_new_work_pool("dummy work pool", "dummy work pool", ProcessingClass, [], 3, 1, 5, 10, 1)
        self.work_pool.start_pool()

        for _index in range(100):
            self.work_pool.insert_work(_index)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.work_pool.stop_pool_tasks()
        self.work_pool.stop_pool()

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.main.work.work_pool_dummy", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_work_pool_manager_plugin(self):
        return self.work_pool_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.work.work_pool_manager")
    def set_work_pool_manager_plugin(self, work_pool_manager_plugin):
        self.work_pool_manager_plugin = work_pool_manager_plugin

class ProcessingClass:

    def __init__(self):
        self.work_list = []

    def start(self):
        pass

    def stop(self):
        pass

    def process(self):
        for work in self.work_list:
            import thread

            thread_id = thread.get_ident()

            print str(work) + " " + str(thread_id)

            # removes the work
            self.remove_work(work)

    def wake(self):
        pass

    def work_added(self, work_reference):
        self.work_list.append(work_reference)

    def work_removed(self, work_reference):
        self.work_list.remove(work_reference)
