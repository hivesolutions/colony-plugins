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

import data_converter_exceptions

class DataConverter:
    """
    Converts data from one medium and schema to another.
    """

    data_converter_plugin = None
    """ Data converter plugin """

    def __init__(self, data_converter_plugin):
        """
        Class constructor.

        @type data_converter_plugin: DataConverterPlugin
        @param data_converter_plugin: Data converter plugin.
        """

        self.data_converter_plugin = data_converter_plugin

    def convert_data(self, input_options, output_options, conversion_options):
        """
        Converts data from one intermediate structure to another transforming its schema along the way.

        @type input_options: Dictionary
        @param input_options: Options used to determine how the input intermediate structure should retrieve its data.
        @type output_options: Dictionary
        @param output_options: Options used to determine how the output intermediate structure should save its data.
        @type conversion_options: Dictionary
        @param conversion_options: Options used to determine how to perform the conversion process.
        """

        self.data_converter_plugin.logger.info("Data conversion process started")

        # raises an exception in case one of the mandatory options is not provided
        mandatory_input_output_options = ["io_adapter_plugin_id"]
        for mandatory_input_output_option in mandatory_input_output_options:
            if not mandatory_input_output_option in input_options or not mandatory_input_output_option in output_options:
                raise data_converter_exceptions.DataConverterOptionMissing("DataConverter.convert_data - Mandatory option not supplied (option_name = %s)" % mandatory_input_output_option)

        # extracts the mandatory options
        input_adapter_plugin_id = input_options["io_adapter_plugin_id"]
        output_adapter_plugin_id = output_options["io_adapter_plugin_id"]

        # creates the input and output intermediate structures
        input_intermediate_structure = self.data_converter_plugin.intermediate_structure_plugin.create_intermediate_structure()
        output_intermediate_structure = self.data_converter_plugin.intermediate_structure_plugin.create_intermediate_structure()

        # loads the source data into the input intermediate structure
        self.data_converter_plugin.intermediate_structure_plugin.load(input_intermediate_structure, input_adapter_plugin_id, input_options)

        # saves the output intermediate structure with the results of the conversion
        self.data_converter_plugin.intermediate_structure_plugin.save(input_intermediate_structure, output_adapter_plugin_id, output_options)

        self.data_converter_plugin.logger.info("Data conversion process ended")
