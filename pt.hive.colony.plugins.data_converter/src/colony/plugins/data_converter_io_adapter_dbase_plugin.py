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

class DataConverterIoAdapterDbasePlugin(colony.base.plugin_system.Plugin):
    """
    Provides a means to load and save intermediate structures to and from the dbase database format.
    """

    id = "pt.hive.colony.plugins.data_converter.io_adapter.dbase"
    name = "Data Converter Input Output Adapter Dbase plugin"
    short_name = "Data Converter Input Output Adapter Dbase"
    description = "Provides a means to load and save intermediate structures to and from the dbase database format"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/data_converter_io_adapter_dbase/io_adapter_dbase/resources/baf.xml"}
    capabilities = ["data_converter_io_adapter.dbase", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PackageDependency(
                    "Win32 Extensions for Python", "dbi", "b202", "http://starship.python.net/crew/mhammond/win32"),
                    colony.base.plugin_system.PackageDependency(
                    "Win32 Extensions for Python", "odbc", "b202", "http://starship.python.net/crew/mhammond/win32"),
                    colony.base.plugin_system.PackageDependency(
                    "DBFpy", "dbfpy", "2.2.3", "http://sourceforge.net/projects/dbfpy")]
    events_handled = []
    events_registrable = []
    main_modules = ["data_converter_io_adapter_dbase.io_adapter_dbase.data_converter_io_adapter_dbase_exceptions",
                    "data_converter_io_adapter_dbase.io_adapter_dbase.data_converter_io_adapter_dbase_system",
                    "data_converter_io_adapter_dbase.io_adapter_dbase.dbfpy_extensions"]

    io_adapter_dbase = None
    """ The intermediate structure dbase input output adapter """

    dbfpy_extensions = None
    """ Extensions to the datatypes supported by the dbfpy module """

    def __init__(self, manager):
        colony.base.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global data_converter_io_adapter_dbase
        import data_converter_io_adapter_dbase.io_adapter_dbase.data_converter_io_adapter_dbase_system
        import data_converter_io_adapter_dbase.io_adapter_dbase.dbfpy_extensions
        self.io_adapter_dbase = data_converter_io_adapter_dbase.io_adapter_dbase.data_converter_io_adapter_dbase_system.IoAdapterDbase(self)
        self.dbfpy_extensions = data_converter_io_adapter_dbase.io_adapter_dbase.dbfpy_extensions.DbfpyExtensions(self)
        self.dbfpy_extensions.register_extensions()

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.io_adapter_dbase = None
        self.dbfpy_extensions = None

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.data_converter.io_adapter.dbase", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.data_converter.io_adapter.dbase", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.data_converter.io_adapter.dbase", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the
        dbase source specified in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to
        load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into
        the provided intermediate structure.
        """

        return self.io_adapter_dbase.load_intermediate_structure(configuration, intermediate_structure, options)

    def save_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in dbase format at the
        location and with characteristics defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate
        structure into dbase format.
        """

        return self.io_adapter_dbase.save_intermediate_structure(configuration, intermediate_structure, options)
