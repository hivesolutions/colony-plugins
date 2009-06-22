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

import dummy_plugin
import colony.plugins.plugin_system

class DummyPluginWindowsForms(dummy_plugin.DummyPlugin):
    """
    The main class for the Dummy Windows Forms plugin.
    """

    id = "pt.hive.colony.plugins.dummy.windows_forms"
    name = "Dummy Plugin Windows Forms"
    short_name = "Dummy Windows Forms"
    description = "Dummy Windows Forms Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.IRON_PYTHON_ENVIRONMENT]
    capabilities = ["main", "dummy_windows_forms"]
    capabilities_allowed = ["dummy_windows_forms_label"]
    dependencies = []
    events_handled = []
    events_registrable = []
    valid = True

    dummy_windows_forms = None

    def load_plugin(self):
        dummy_plugin.DummyPlugin.load_plugin(self)
        print "loading dummy windows forms..."

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        global dummy
        import dummy.windows_forms.dummy_windows_forms_system
        self.dummy_windows_forms = dummy.windows_forms.dummy_windows_forms_system.DummyWindowsForms(self)
        self.dummy_windows_forms.start()

    def unload_plugin(self):
        dummy_plugin.DummyPlugin.unload_plugin(self)
        print "unloading dummy windows forms..."
        self.dummy_windows_forms.stop()

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.dummy.windows_forms", "1.0.0")
    def load_allowed(self, plugin, capability):
        dummy_plugin.DummyPlugin.load_allowed(self, plugin, capability)
        print "loading dummy windows forms allowed..."

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.dummy.windows_forms", "1.0.0")
    def unload_allowed(self, plugin, capability):
        dummy_plugin.DummyPlugin.unload_allowed(self, plugin, capability)
        print "unloading dummy windows forms allowed..."

    def dependency_injected(self, plugin):
        dummy_plugin.DummyPlugin.dependency_injected(self, plugin)

    @colony.plugins.decorators.load_allowed_capability("dummy_windows_forms_label")
    def dummy_windows_forms_label_load_allowed(self, plugin, capability):
        label = plugin.get_label()
        form = self.dummy_windows_forms.get_form()
        self.dummy_windows_forms.add_label(label)

    @colony.plugins.decorators.unload_allowed_capability("dummy_windows_forms_label")
    def dummy_windows_forms_label_unload_allowed(self, plugin, capability):
        label = plugin.get_label()
        form = self.dummy_windows_forms.get_form()
        self.dummy_windows_forms.remove_label(label)
