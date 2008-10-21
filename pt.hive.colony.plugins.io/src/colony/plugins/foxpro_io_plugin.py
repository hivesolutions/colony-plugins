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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

import colony.plugins.plugin_system

class FoxProInputOuputPlugin(colony.plugins.plugin_system.Plugin):
    """
    Provides a simple API to interface with FoxPro databases
    """

    id = "pt.hive.colony.plugins.io.foxpro"
    name = "FoxPro adapter plugin"
    short_name = "FoxPro plugin"
    description = "Provides a simple API to manipulate FoxPro databases"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["io.foxpro"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "Win32 Extensions for Python", "dbi", "b202", "http://starship.python.net/crew/mhammond/win32"),
                    colony.plugins.plugin_system.PackageDependency(
                    "Win32 Extensions for Python", "odbc", "b202", "http://starship.python.net/crew/mhammond/win32")]
    events_handled = []
    events_registrable = []

    codebase = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global io
        import io.foxpro.foxpro_io
        self.codebase = io.foxpro.foxpro_io.FoxProInputOutput()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.codebase = None

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def flush(self):
        """
        @see: colony.plugins.io_text.text.text_io.flush()
        """
        return self.codebase.flush()

    def delete(self, object):
        """
        @see: colony.plugins.io_text.text.text_io.delete()
        """
        return self.codebase.delete(object)

    def save(self, object):
        """
        @see: colony.plugins.io_text.text.text_io.save()
        """
        return self.codebase.save(object)

    def query(self, table_name, column_list):
        """
        @see: colony.plugins.io_text.text.text_io.query()
        """
        return self.codebase.query(table_name, column_list)

    def initialize(self, database_path):
        """
        @see: colony.plugins.io_text.text.text_io.bind()
        """
        self.codebase.initialize(database_path)
