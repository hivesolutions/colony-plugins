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

__revision__ = "$LastChangedRevision: 2112 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:23:46 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class TextInputOutputPlugin(colony.plugins.plugin_system.Plugin):

    id = "pt.hive.colony.plugins.io.text"
    name = "Text input/output plugin"
    short_name = "Text I/O"
    description = "description here"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["io.text"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    codebase = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self) 
        global io
        import io.text.text_io
        self.codebase = io.text.text_io.TextInputOutput()
        self.codebase.open_file("c:/dump.txt")     

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.codebase.close_file()
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

    def query(self, object):
        """
        @see: colony.plugins.io_text.text.text_io.query()
        """
        return self.codebase.query(object)

    def bind(self, entity_class_map):
        """
        @see: colony.plugins.io_text.text.text_io.bind()
        """
        self.codebase.bind(entity_class_map)
