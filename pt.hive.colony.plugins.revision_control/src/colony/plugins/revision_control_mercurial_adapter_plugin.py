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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2300 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:10:15 +0100 (Wed, 01 Apr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class RevisionControlMercurialAdapterPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Revision Control Mercurial adapter plugin
    """

    id = "pt.hive.colony.plugins.revision_control.mercurial_adapter"
    name = "Revision Control Mercurial Adapter Plugin"
    short_name = "Revision Control Mercurial Adapter"
    description = "Revision Control Mercurial Adapter Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["revision_control.adapter"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "Mercurial", "mercurial", "1.4.x", "http://mercurial.selenic.com")]
    events_handled = []
    events_registrable = []
    main_modules = ["revision_control.mercurial_adapter.revision_control_mercurial_adapter_system"]

    revision_control_mercurial_adapter = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global revision_control
        import revision_control.mercurial_adapter.revision_control_mercurial_adapter_system
        self.revision_control_mercurial_adapter = revision_control.mercurial_adapter.revision_control_mercurial_adapter_system.RevisionControlMercurialAdapter(self)

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

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def update(self, resource_identifiers, revision_identifier):
        return self.revision_control_mercurial_adapter.update(resource_identifiers, revision_identifier)

    def get_adapter_name(self):
        return self.revision_control_mercurial_adapter.get_adapter_name()
