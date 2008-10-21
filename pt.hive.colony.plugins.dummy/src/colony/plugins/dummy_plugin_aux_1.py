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

__revision__ = "$LastChangedRevision: 2105 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 14:55:42 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

import colony.plugins.plugin_system
import colony.plugins.decorators

TIMEOUT = 0.5

class DummyPluginAux1(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Dummy Aux 1 plugin
    """

    id = "pt.hive.colony.plugins.dummy.aux1"
    name = "Dummy Plugin Aux 1"
    short_name = "Dummy Aux 1"
    description = "Dummy Aux 1 Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.JYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.IRON_PYTHON_ENVIRONMENT]
    capabilities = ["dummy_aux1_capability"]
    capabilities_allowed = ["dummy_aux2_capability", "dummy_aux3_capability"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.threads.thread_pool_manager", "1.0.0")]
    events_handled = ["dummy_aux1_event"]
    events_registrable = ["plugin_manager.loaded_plugin"]

    thread_pool_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        print "loading dummy aux 1..."

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.test_pool = self.thread_pool_manager_plugin.create_new_thread_pool("test pool", "test pool description", 5, 1, 5)
        self.test_pool.start_pool()

        # the control flags
        self.valid = True
        self.paused = False

        # retrieves the task descriptor class
        task_descriptor_class = self.thread_pool_manager_plugin.get_thread_task_descriptor_class()

        for i in range(1):
            self.task_descriptor = task_descriptor_class(start_method = self.start_print_running_thread_pool,
                                                         stop_method = self.stop_print_running_thread_pool,
                                                         pause_method = self.pause_print_running_thread_pool,
                                                         resume_method = self.resume_print_running_thread_pool)
            self.test_pool.insert_task(self.task_descriptor)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        print "unloading dummy aux 1..."
        self.test_pool.remove_task(self.task_descriptor)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.dummy.aux1", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)
        print "loading dummy aux 1 allowed..."

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.dummy.aux1", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)
        print "unloading dummy aux 1 allowed..."

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.dummy.aux1", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.plugins.decorators.event_handler("pt.hive.colony.plugins.dummy.aux1", "1.0.0")
    def event_handler(self, event_name, *event_args):
        try:
            colony.plugins.plugin_system.Plugin.event_handler(self, event_name, *event_args)
        except Exception, exception:
            colony.plugins.plugin_system.Plugin.treat_exception(self, exception)

    @colony.plugins.decorators.load_allowed_capability("dummy_aux2_capability")
    def dummy_aux2_capability_load_allowed(self, plugin, capability):
        print "dummy aux 1 loaded allowed dummy_aux2_capability plugin " + plugin.id + " with version " + plugin.version

    @colony.plugins.decorators.load_allowed_capability("dummy_aux3_capability")
    def dummy_aux3_capability_load_allowed(self, plugin, capability):
        print "dummy aux 1 loaded allowed dummy_aux3_capability plugin " + plugin.id + " with version " + plugin.version

    @colony.plugins.decorators.unload_allowed_capability("dummy_aux2_capability")
    def dummy_aux2_capability_unload_allowed(self, plugin, capability):
        print "dummy aux 1 unloaded allowed dummy_aux2_capability plugin " + plugin.id + " with version " + plugin.version

    @colony.plugins.decorators.unload_allowed_capability("dummy_aux3_capability")
    def dummy_aux3_capability_unload_allowed(self, plugin, capability):
        print "dummy aux 1 unloaded allowed dummy_aux3_capability plugin " + plugin.id + " with version " + plugin.version

    def get_thread_pool_manager_plugin(self):
        return self.thread_pool_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.threads.thread_pool_manager")
    def set_thread_pool_manager_plugin(self, thread_pool_manager_plugin):
        self.thread_pool_manager_plugin = thread_pool_manager_plugin

    @colony.plugins.decorators.event_handler_method("plugin_manager.loaded_plugin")
    def loaded_plugin_handler(self, event_name, plugin_id, plugin_version, plugin, *event_args):
        print "dummy aux 1 detected the loading of " + plugin_id + " with version " + plugin_version

    def start_print_running_thread_pool(self):
        while self.valid:
            if not self.paused:
                print "running in thread pool"
            time.sleep(TIMEOUT)

    def stop_print_running_thread_pool(self):
        self.valid = False

    def pause_print_running_thread_pool(self):
        self.paused = True

    def resume_print_running_thread_pool(self):
        self.paused = False
