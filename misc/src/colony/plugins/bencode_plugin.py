#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 2688 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-16 12:24:34 +0100 (qui, 16 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class BencodePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Bencode plugin.
    """

    id = "pt.hive.colony.plugins.misc.bencode"
    name = "Bencode Plugin"
    short_name = "Bencode"
    description = "A plugin to serialize and unserialize bencode files"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/bencode/resources/baf.xml"
    }
    capabilities = [
        "serializer.bencode",
        "build_automation_item"
    ]
    main_modules = [
        "misc.bencode.bencode_exceptions",
        "misc.bencode.bencode_serializer",
        "misc.bencode.bencode_system"
    ]

    bencode = None
    """ The bencode """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import misc.bencode.bencode_system
        self.bencode = misc.bencode.bencode_system.Bencode(self)

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

    def dumps(self, object):
        return self.bencode.dumps(object)

    def loads(self, bencode_string):
        return self.bencode.loads(bencode_string)

    def load_file(self, bencode_file):
        return self.bencode.load_file(bencode_file)

    def load_file_encoding(self, bencode_file, encoding):
        return self.bencode.load_file(bencode_file, encoding)

    def get_mime_type(self):
        return self.bencode.get_mime_type()
