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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1805 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-03-10 08:56:01 +0000 (Tue, 10 Mar 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class DataConverterIoAdapterXmlPlugin(colony.base.plugin_system.Plugin):
    """
    Provides a means to load and save intermediate structures to and from xml format.
    """

    id = "pt.hive.colony.plugins.data_converter.io_adapter.xml"
    name = "Data Converter Input Output Adapter Xml plugin"
    short_name = "Data Converter Input Output Adapter Xml"
    description = "Provides a means to load and save intermediate structures to and from xml format"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/data_converter_io_adapter_xml/io_adapter_xml/resources/baf.xml"
    }
    capabilities = [
        "data_converter_io_adapter.xml",
        "build_automation_item"
    ]
    main_modules = [
        "data_converter_io_adapter_xml.io_adapter_xml.data_converter_io_adapter_xml_exceptions",
        "data_converter_io_adapter_xml.io_adapter_xml.data_converter_io_adapter_xml_system"
    ]

    io_adapter_xml = None
    """ The intermediate structure xml input output adapter """

    def __init__(self, manager):
        colony.base.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import data_converter_io_adapter_xml.io_adapter_xml.data_converter_io_adapter_xml_system
        self.io_adapter_xml = data_converter_io_adapter_xml.io_adapter_xml.data_converter_io_adapter_xml_system.IoAdapterXml(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the
        xml source specified in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        return self.io_adapter_xml.load_intermediate_structure(configuration, intermediate_structure, options)

    def save_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in xml format at the location
        and with characteristics defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate
        structure into xml format.
        """

        return self.io_adapter_xml.save_intermediate_structure(configuration, intermediate_structure, options)
