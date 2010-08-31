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

__revision__ = "$LastChangedRevision: 8461 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-05-12 06:45:34 +0100 (qua, 12 Mai 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class InstallationDebPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Installation Deb plugin.
    """

    id = "pt.hive.colony.plugins.installation.deb"
    name = "Installation Deb Plugin"
    short_name = "Installation Deb"
    description = "A plugin to manage the installation generation of deb packages"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/installation/deb/resources/baf.xml"}
    capabilities = ["installation.adapter"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.packaging.deb", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["installation.deb.installation_deb_exceptions", "installation.deb.installation_deb_system"]

    installation_deb = None

    packaging_deb_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global installation
        import installation.deb.installation_deb_system
        self.installation_deb = installation.deb.installation_deb_system.InstallationDeb(self)

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

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.installation.deb", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return self.installation_deb.get_adapter_name()

    def generate_installation_file(self, parameters):
        """
        Generates the installation file for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the installation file generation.
        """

        return self.installation_deb.generate_installation_file(parameters)

    def get_packaging_deb_plugin(self):
        return self.packaging_deb_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.packaging.deb")
    def set_packaging_deb_plugin(self, packaging_deb_plugin):
        self.packaging_deb_plugin = packaging_deb_plugin
