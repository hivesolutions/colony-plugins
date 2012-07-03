#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class FormatMimePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Mime Format plugin.
    """

    id = "pt.hive.colony.plugins.format.mime"
    name = "Mime Format Plugin"
    short_name = "Mime Format"
    description = "The plugin that offers the mime format support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/format/mime/resources/baf.xml"
    }
    capabilities = [
        "format.mime",
        "build_automation_item"
    ]
    main_modules = [
        "format.mime.format_mime_exceptions",
        "format.mime.format_mime_system"
    ]

    format_mime = None
    """ The format mime """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import format.mime.format_mime_system
        self.format_mime = format.mime.format_mime_system.FormatMime(self)

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

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.plugin_system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.plugin_system.Plugin.unset_configuration_property(self, property_name)

    def create_message(self, parameters):
        return self.format_mime.create_message(parameters)

    def create_message_part(self, parameters):
        return self.format_mime.create_message_part(parameters)

    def get_mime_type_file_name(self, file_name):
        return self.format_mime.get_mime_type_file_name(file_name)

    @colony.base.decorators.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.format_mime.set_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.format_mime.unset_configuration_property()
