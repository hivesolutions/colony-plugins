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

class FormatMimeUtilsPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Mime Format Utils plugin.
    """

    id = "pt.hive.colony.plugins.format.mime.utils"
    name = "Mime Format Utils Plugin"
    short_name = "Mime Format Utils"
    description = "The plugin that offers the mime format utils support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/format/mime_utils/resources/baf.xml"
    }
    capabilities = [
        "format.mime.utils",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.format.mime", "1.x.x")
    ]
    main_modules = [
        "format.mime_utils.format_mime_utils_system"
    ]

    format_mime_utils = None
    """ The format mime utils """

    format_mime_plugin = None
    """ The format mime plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import format.mime_utils.format_mime_utils_system
        self.format_mime_utils = format.mime_utils.format_mime_utils_system.FormatMimeUtils(self)

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

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def add_mime_message_attachment_contents(self, mime_message, contents, file_name):
        return self.format_mime_utils.add_mime_message_attachment_contents(mime_message, contents, file_name)

    def add_mime_message_attachment_contents_mime_type(self, mime_message, contents, file_name, mime_type):
        return self.format_mime_utils.add_mime_message_attachment_contents(mime_message, contents, file_name, mime_type)

    def add_mime_message_contents(self, mime_message, contents_path, content_extensions):
        return self.format_mime_utils.add_mime_message_contents(mime_message, contents_path, content_extensions)

    def add_mime_message_contents_non_recursive(self, mime_message, contents_path, content_extensions):
        return self.format_mime_utils.add_mime_message_contents(mime_message, contents_path, content_extensions, False)

    def get_format_mime_plugin(self):
        return self.format_mime_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.format.mime")
    def set_format_mime_plugin(self, format_mime_plugin):
        self.format_mime_plugin = format_mime_plugin
