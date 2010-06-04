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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class DistributionPyroHelperPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Distribution Pyro Helper plugin.
    """

    id = "pt.hive.colony.plugins.distribution.helper.pyro"
    name = "Distribution Pyro Helper Plugin"
    short_name = "Distribution Pyro Helper"
    description = "Distribution Pyro Helper Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/distribution_helper/pyro/resources/baf.xml"}
    capabilities = ["distribution_helper", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.remote.client.pyro", "1.0.0")]
    events_handled = []
    events_registrable = []

    distribution_pyro_helper = None

    main_pyro_client_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global distribution_helper
        import distribution_helper.pyro.distribution_pyro_helper_system
        self.distribution_pyro_helper = distribution_helper.pyro.distribution_pyro_helper_system.DistributionPyroHelper(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.distribution.helper.pyro", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_helper_name(self):
        return self.distribution_pyro_helper.get_helper_name()

    def create_client(self, remote_reference):
        return self.distribution_pyro_helper.create_client(remote_reference)

    def get_main_pyro_client_plugin(self):
        return self.main_pyro_client_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.remote.client.pyro")
    def set_main_pyro_client_plugin(self, main_pyro_client_plugin):
        self.main_pyro_client_plugin = main_pyro_client_plugin
