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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

import colony.base.plugin_system
import colony.base.decorators

TIMEOUT = 0.5
""" The timeout value to be used """

class DummyBase1Plugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Dummy Aux 1 plugin.
    """

    id = "pt.hive.colony.plugins.dummy.base_1"
    name = "Dummy Aux 1 Plugin"
    short_name = "Dummy Aux 1"
    description = "Dummy Aux 1 Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/dummy/base_1/resources/baf.xml"}
    capabilities = ["dummy_base_1_capability", "build_automation_item"]
    capabilities_allowed = [("dummy_base_2_capability", colony.base.plugin_system.NEW_DIFFUSION_SCOPE), ("dummy_base_3_capability", colony.base.plugin_system.NEW_DIFFUSION_SCOPE)]
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.threads.thread_pool_manager", "1.0.0")]
    events_handled = ["dummy_base_1_event"]
    events_registrable = ["plugin_manager.end_load_plugin"]
    main_modules = ["dummy.base_1.dummy_base_1_system"]

    thread_pool_manager_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.test_pool = self.thread_pool_manager_plugin.create_new_thread_pool("test pool", "test pool description", 5, 1, 5)
        self.test_pool.start_pool()

        # the control flags
        self.valid = True
        self.paused = False

        # retrieves the task descriptor class
        task_descriptor_class = self.thread_pool_manager_plugin.get_thread_task_descriptor_class()

        for _index in range(1):
            self.task_descriptor = task_descriptor_class(start_method = self.start_print_running_thread_pool,
                                                         stop_method = self.stop_print_running_thread_pool,
                                                         pause_method = self.pause_print_running_thread_pool,
                                                         resume_method = self.resume_print_running_thread_pool)
            self.test_pool.insert_task(self.task_descriptor)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.test_pool.remove_task(self.task_descriptor)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.dummy.base_1", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.dummy.base_1", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.dummy.base_1", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.event_handler("pt.hive.colony.plugins.dummy.base_1", "1.0.0")
    def event_handler(self, event_name, *event_args):
        try:
            colony.base.plugin_system.Plugin.event_handler(self, event_name, *event_args)
        except Exception, exception:
            colony.base.plugin_system.Plugin.treat_exception(self, exception)

    @colony.base.decorators.load_allowed_capability("dummy_base_2_capability")
    def dummy_base_2_capability_load_allowed(self, plugin, capability):
        self.debug("dummy aux 1 loaded allowed dummy_base_2_capability plugin '%s' with version '%s'" % (plugin.id, plugin.version))

    @colony.base.decorators.load_allowed_capability("dummy_base_3_capability")
    def dummy_base_3_capability_load_allowed(self, plugin, capability):
        self.debug("dummy aux 1 loaded allowed dummy_base_3_capability plugin '%s' with version '%s'" % (plugin.id, plugin.version))

    @colony.base.decorators.unload_allowed_capability("dummy_base_2_capability")
    def dummy_base_2_capability_unload_allowed(self, plugin, capability):
        self.debug("dummy aux 1 unloaded allowed dummy_base_2_capability plugin '%s' with version '%s'" % (plugin.id, plugin.version))

    @colony.base.decorators.unload_allowed_capability("dummy_base_3_capability")
    def dummy_base_3_capability_unload_allowed(self, plugin, capability):
        self.debug("dummy aux 1 unloaded allowed dummy_base_3_capability plugin '%s' with version '%s'" % (plugin.id, plugin.version))

    def get_thread_pool_manager_plugin(self):
        return self.thread_pool_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.threads.thread_pool_manager")
    def set_thread_pool_manager_plugin(self, thread_pool_manager_plugin):
        self.thread_pool_manager_plugin = thread_pool_manager_plugin

    @colony.base.decorators.event_handler_method("plugin_manager.end_load_plugin")
    def end_load_plugin_handler(self, event_name, plugin_id, plugin_version, plugin, *event_args):
        self.debug("dummy aux 1 detected the end of loading of '%s with version '%s'" % (plugin_id, plugin_version))

    def start_print_running_thread_pool(self):
        # starts the index value
        index = 0

        # iterates while it's valid
        while self.valid:
            # in case the paused flag is not valid
            if not self.paused:
                # prints a debug message
                self.debug("Running in thread pool")

            # sleeps for the given time
            time.sleep(TIMEOUT)

            # increments the index value
            index += 1

    def stop_print_running_thread_pool(self):
        # unsets the valid flag
        self.valid = False

    def pause_print_running_thread_pool(self):
        # sets the paused flag
        self.paused = True

    def resume_print_running_thread_pool(self):
        # unsets the paused flag
        self.paused = False
