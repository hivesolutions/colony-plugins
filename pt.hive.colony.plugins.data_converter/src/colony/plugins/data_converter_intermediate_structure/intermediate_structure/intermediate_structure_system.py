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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import intermediate_structure_exceptions

class IntermediateStructure:
    """
    Intermediate structure used to hold the results of each conversion step.
    """

    def __init__(self, intermediate_structure_plugin):
        """
        Class constructor.

        @type intermediate_structure_plugin: IntermediateStructurePlugin
        @param intermediate_structure: Intermediate structure plugin.
        """

        self.intermediate_structure_plugin = intermediate_structure_plugin

    def load(self, intermediate_structure, io_adapter_plugin_id, options):
        """
        Populates the intermediate structure with data retrieved from the csv source specified in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type io_adapter_plugin_id: str
        @param io_adapter_plugin_id: Unique identifier for the input output adapter plugin one wants to use to save intermediate structure.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided intermediate structure.
        """

        # retrieves the specified input output adapter plugin
        input_adapter_plugin = None
        for io_adapter_plugin in self.intermediate_structure_plugin.io_adapter_plugins:
            if io_adapter_plugin_id == io_adapter_plugin.id:
                input_adapter_plugin = io_adapter_plugin

        # raises an exception in case the specified io adapter plugin was not found
        if not input_adapter_plugin:
            raise intermediate_structure_exceptions.IntermediateStructurePluginMissing("IntermediateStructure.load - Specified input output adapter plugin was not found (io_adapter_plugin = %s)" % io_adapter_plugin_id)

        # resets the intermediate structure's state
        intermediate_structure.reset()

        # redirects the load request to the specified input output adapter
        input_adapter_plugin.load(intermediate_structure, options)

    def save(self, intermediate_structure, io_adapter_plugin_id, options):
        """
        Saves the intermediate structure to a file in csv format at the location and with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type io_adapter_plugin_id: str
        @param io_adapter_plugin_id: Unique identifier for the input output adapter plugin one wants to use to save intermediate structure.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure into csv format.
        """

        # retrieves the specified input output adapter plugin
        output_adapter_plugin = None
        for io_adapter_plugin in self.intermediate_structure_plugin.io_adapter_plugins:
            if io_adapter_plugin_id == io_adapter_plugin.id:
                output_adapter_plugin = io_adapter_plugin

        # raises an exception in case the specified io adapter plugin was not found
        if not output_adapter_plugin:
            raise intermediate_structure_exceptions.IntermediateStructurePluginMissing("IntermediateStructure.save - Specified input output adapter plugin was not found (io_adapter_plugin = %s)" % io_adapter_plugin_id)

        # redirects the save request to the specified input output adapter
        output_adapter_plugin.save(intermediate_structure, options)
