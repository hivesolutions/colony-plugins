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

STATUS_TASK_CREATED = 1
STATUS_TASK_RUNNING = 2
STATUS_TASK_PAUSED = 3
STATUS_TASK_STOPPED = 4

TIMEOUT = 0.5

class DummyPluginAux4(colony.base.plugin_system.Plugin):
    """
    The main class for the Dummy Aux 4 plugin.
    """

    id = "pt.hive.colony.plugins.dummy.aux4"
    name = "Dummy Plugin Aux 4"
    short_name = "Dummy Aux 4"
    description = "Dummy Aux 4 Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/dummy/aux_4/resources/baf.xml"}
    capabilities = ["dummy_aux4_capability", "task_information", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.tasks.task_manager", "1.0.0")]
    events_handled = ["task_information_changed"]
    events_registrable = []
    main_modules = []

    task_manager_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        print "loading dummy aux 4..."

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        print "unloading dummy aux 4..."

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)
        print "loading dummy aux 4 allowed..."

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)
        print "unloading dummy aux 4 allowed..."

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)
        if colony.base.plugin_system.is_capability_or_sub_capability_in_list("task_manager", plugin.capabilities):
            self.task_manager_plugin = plugin

    def test_create_task(self):
        self.task1 = self.task_manager_plugin.create_new_task("hello_task", "hello_description", self.task_handler)
        self.task1.set_task_pause_handler(self.pause_task_handler)
        self.task1.set_task_resume_handler(self.resume_task_handler)
        self.task1.set_task_stop_handler(self.stop_task_handler)
        self.task1.start([])

    def test_pause_task(self):
        self.task1.pause([])

    def test_resume_task(self):
        self.task1.resume([])

    def test_stop_task(self):
        self.task1.stop([])

    def task_handler(self, task, args):
        counter = 0
        while not task.status == STATUS_TASK_STOPPED and counter <= 100:
            print "hello world"
            if task.status == STATUS_TASK_PAUSED:
                # confirms the pause
                task.confirm_pause()
                while task.status == STATUS_TASK_PAUSED:
                    time.sleep(TIMEOUT)
                # confirms the resume
                task.confirm_resume()
            time.sleep(TIMEOUT)

            task.set_percentage_complete(counter)
            counter += 1

        # confirms the stop
        task.confirm_stop(True)

    def pause_task_handler(self, args):
        print "task paused"

    def resume_task_handler(self, args):
        print "task resumed"

    def stop_task_handler(self, args):
        print "task stopped"

    def test_generate_event(self):
        self.generate_event("task_information_changed.new_task", [])
