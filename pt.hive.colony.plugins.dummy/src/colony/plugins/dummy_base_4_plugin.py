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

import colony.base.plugin_system
import colony.base.decorators

class DummyBase4Plugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Dummy Base 4 plugin.
    """

    id = "pt.hive.colony.plugins.dummy.base_4"
    name = "Dummy Base 4 Plugin"
    short_name = "Dummy Base 4"
    description = "Dummy Base 4 Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/dummy/base_4/resources/baf.xml"
    }
    capabilities = [
        "dummy_base_4_capability",
        "task_information",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.tasks.task_manager", "1.0.0")
    ]
    events_handled = [
        "task_information_changed"
    ]
    main_modules = [
        "dummy.base_4.dummy_base_4_system"
    ]

    dummy_base_4 = None
    """ The dummy base 4 """

    task_manager_plugin = None
    """ The task manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import dummy.base_4.dummy_base_4_system
        self.dummy_base_4 = dummy.base_4.dummy_base_4_system.DummyBase4(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.dummy.base_4", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_test_task(self):
        return self.dummy_base_4.create_test_task()

    def pause_test_task(self):
        return self.dummy_base_4.pause_test_task()

    def resume_test_task(self):
        return self.dummy_base_4.resume_test_task()

    def stop_test_task(self):
        return self.dummy_base_4.stop_test_task()

    def generate_test_event(self):
        return self.dummy_base_4.generate_test_event()

    def get_task_manager_plugin(self):
        return self.task_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.tasks.task_manager")
    def set_task_manager_plugin(self, task_manager_plugin):
        self.task_manager_plugin = task_manager_plugin
