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

import colony.base.plugin_system

class RevisionControlMercurialAdapterPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Revision Control Mercurial adapter plugin
    """

    id = "pt.hive.colony.plugins.revision_control.mercurial_adapter"
    name = "Revision Control Mercurial Adapter Plugin"
    short_name = "Revision Control Mercurial Adapter"
    description = "Revision Control Mercurial Adapter Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/revision_control/mercurial_adapter/resources/baf.xml"
    }
    capabilities = [
        "revision_control.adapter",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PackageDependency("Mercurial", "mercurial", "1.4.x", "http://mercurial.selenic.com")
    ]
    main_modules = [
        "revision_control.mercurial_adapter.revision_control_mercurial_adapter_system"
    ]

    revision_control_mercurial_adapter = None
    """ The revision control mercurial adapter """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import revision_control.mercurial_adapter.revision_control_mercurial_adapter_system
        self.revision_control_mercurial_adapter = revision_control.mercurial_adapter.revision_control_mercurial_adapter_system.RevisionControlMercurialAdapter(self)

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

    def create_revision_control_reference(self, revision_control_parameters):
        return self.revision_control_mercurial_adapter.create_revision_control_reference(revision_control_parameters)

    def add(self, revision_control_reference, resource_identifiers, recurse):
        return self.revision_control_mercurial_adapter.add(revision_control_reference, resource_identifiers, recurse)

    def update(self, revision_control_reference, resource_identifiers, revision):
        return self.revision_control_mercurial_adapter.update(revision_control_reference, resource_identifiers, revision)

    def commit(self, revision_control_reference, resource_identifiers, commit_message):
        return self.revision_control_mercurial_adapter.commit(revision_control_reference, resource_identifiers, commit_message)

    def log(self, revision_control_reference, resource_identifiers, start_revision, end_revision):
        return self.revision_control_mercurial_adapter.log(revision_control_reference, resource_identifiers, start_revision, end_revision)

    def log_time(self, revision_control_reference, resource_identifiers, start_time, end_time):
        return self.revision_control_mercurial_adapter.log_time(revision_control_reference, resource_identifiers, start_time, end_time)

    def status(self, revision_control_reference, resource_identifiers):
        return self.revision_control_mercurial_adapter.status(revision_control_reference, resource_identifiers)

    def diff(self, revision_control_reference, resource_identifiers, revision_1, revision_2):
        return self.revision_control_mercurial_adapter.diff(revision_control_reference, resource_identifiers, revision_1, revision_2)

    def remove(self, revision_control_reference, resource_identifiers):
        return self.revision_control_mercurial_adapter.remove(revision_control_reference, resource_identifiers)

    def get_resources_revision(self, revision_control_reference, resource_identifier, revision):
        return self.revision_control_mercurial_adapter.get_resources_revision(revision_control_reference, resource_identifier, revision)

    def get_adapter_name(self):
        return self.revision_control_mercurial_adapter.get_adapter_name()
