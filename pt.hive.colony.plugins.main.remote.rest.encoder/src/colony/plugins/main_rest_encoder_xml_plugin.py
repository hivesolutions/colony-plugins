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

__revision__ = "$LastChangedRevision: 429 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-21 13:03:27 +0000 (Sex, 21 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class MainRestEncoderXmlPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Rest Encoder Xml Main plugin.
    """

    id = "pt.hive.colony.plugins.main.remote.rest.encoder.xml"
    name = "Rest Encoder Xml Main Plugin"
    short_name = "Rest Encoder Xml Main"
    description = "Rest Encoder Xml Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_remote_rest_encoder/xml/resources/baf.xml"
    }
    capabilities = [
        "rest_encoder",
        "build_automation_item"
    ]
    main_modules = [
        "main_remote_rest_encoder.xml.main_rest_encoder_xml_system"
    ]

    main_rest_encoder_xml = None
    """ The main rest encoder xml """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global rest_encoder_xml
        import main_remote_rest_encoder.xml.main_rest_encoder_xml_system
        self.main_rest_encoder_xml = main_remote_rest_encoder.xml.main_rest_encoder_xml_system.MainRestEncoderXml(self)

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

    def get_encoder_name(self):
        """
        Retrieves the encoder name.

        @rtype: String
        @return: The encoder name.
        """

        return self.main_rest_encoder_xml.get_encoder_name()

    def get_content_type(self):
        """
        Retrieves the content type.

        @rtype: String
        @return: The content type.
        """

        return self.main_rest_encoder_xml.get_content_type()

    def encode_value(self, value):
        """
        Encodes the given value.

        @type value: Object
        @param value: The value to be encoded.
        @rtype: String
        @return: The encoded value.
        """

        return self.main_rest_encoder_xml.encode_value(value)
