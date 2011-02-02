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

__revision__ = "$LastChangedRevision: 888 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-28 16:39:52 +0000 (Sun, 28 Dec 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "data_converter"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

INVALID_ADDRESS_MESSAGE = "invalid address"
""" The invalid address message """

HELP_TEXT = "### DATA CONVERTER HELP ###\n\
list_configurations                                                           - lists the data converter configurations\n\
list_loaded_configurations                                                    - lists the currently loaded configurations\n\
load_configuration <configuration_plugin_id>                                  - loads a conversion configuration from a plugin\n\
unload_configuration <configuration_id>                                       - unloads a conversion configuration\n\
set_configuration_option <configuration_id> <option_name> <option_value>      - sets an option in the conversion configuration\n\
list_configuration_items <configuration_id>                                   - lists all configuration items that are available in the current configuration\n\
list_dependent_configuration_items <configuration_id> <configuration_item_id> - lists all configuration items that depend on the specified one\n\
enable_configuration_item <configuration_id> <configuration_item_id>          - enables the conversion of a certain configuration item\n\
enable_all_configuration_items <configuration_id>                             - enables all data converter configuration items\n\
disable_configuration_item <configuration_id> <configuration_item_id>         - disables the conversion of a certain configuration item\n\
disable_all_configuration_items <configuration_id>                            - disables all data converter configuration items\n\
convert_data <configuration_id>                                               - migrates data from one medium and schema to another"
""" The help text """

COLUMN_SPACING = 4
""" The column spacing """

ACTIVE_VALUE = "ACTIVE"
""" The active value """

INACTIVE_VALUE = "INACTIVE"
""" The inactive value """

ID_COLUMN_HEADER = "ID"
""" The id column header """

ENABLED_COLUMN_HEADER = "ENABLED"
""" The enabled column header """

TYPE_COLUMN_HEADER = "TYPE"
""" The type column header """

DESCRIPTION_COLUMN_HEADER = "DESCRIPTION"
""" The description column header """

class ConsoleDataConverter:
    """
    The console data converter class.
    """

    data_converter_plugin = None
    """ The data converter plugin """

    commands = ["list_configurations",
                "list_loaded_configurations",
                "load_configuration",
                "unload_configuration",
                "set_configuration_option",
                "list_configuration_items",
                "list_dependent_configuration_items",
                "enable_configuration_item",
                "enable_all_configuration_items",
                "disable_configuration_item",
                "disable_all_configuration_items",
                "convert_data"]
    """ The commands list """

    def __init__(self, data_converter_plugin):
        """
        Constructor of the class.

        @type data_converter_plugin: DataConverterPlugin
        @param data_converter_plugin: The data converter plugin.
        """

        self.data_converter_plugin = data_converter_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def get_output_configuration_items_string(self, configuration_items):
        maximum_id_column_length = len(ID_COLUMN_HEADER)
        maximum_enabled_column_length = len(ENABLED_COLUMN_HEADER)
        maximum_type_column_length = len(TYPE_COLUMN_HEADER)
        maximum_description_column_length = len(DESCRIPTION_COLUMN_HEADER)

        # discovers the maximum column length for each column
        for configuration_item in configuration_items:
            # sets the new maximum id column length
            configuration_item_id = configuration_item.get_configuration_item_id()
            configuration_item_id_str = str(configuration_item_id)
            if len(configuration_item_id_str) > maximum_id_column_length:
                maximum_id_column_length = len(configuration_item_id_str)

            # sets the new maximum enabled column length
            enabled = configuration_item.is_enabled()
            enabled_str = INACTIVE_VALUE
            if enabled:
                enabled_str = ACTIVE_VALUE
            if len(enabled_str) > maximum_enabled_column_length:
                maximum_enabled_column_length = len(enabled_str)

            # sets the new maximum type column length
            configuration_item_type_str = configuration_item.__class__.__name__
            if len(configuration_item_type_str) > maximum_type_column_length:
                maximum_type_column_length = len(configuration_item_type_str)

            # sets the new maximum description column length
            configuration_description_str = str(configuration_item)
            if len(configuration_description_str) > maximum_description_column_length:
                maximum_description_column_length = len(configuration_description_str)

        # creates the table header
        id_column_gap_length = (maximum_id_column_length - len(ID_COLUMN_HEADER)) + COLUMN_SPACING
        output_configuration_items_str = ID_COLUMN_HEADER + " " * id_column_gap_length
        enabled_column_gap_length = (maximum_enabled_column_length - len(ENABLED_COLUMN_HEADER)) + COLUMN_SPACING
        output_configuration_items_str += ENABLED_COLUMN_HEADER + " " * enabled_column_gap_length
        type_column_gap_length = (maximum_type_column_length - len(TYPE_COLUMN_HEADER)) + COLUMN_SPACING
        output_configuration_items_str += TYPE_COLUMN_HEADER + " " * type_column_gap_length
        output_configuration_items_str += DESCRIPTION_COLUMN_HEADER + "\n"

        # creates the table rows
        for configuration_item in configuration_items:
            configuration_item_str = str()

            # creates the cell for the id column
            configuration_item_id_str = str(configuration_item.get_configuration_item_id())
            id_column_gap_length = (maximum_id_column_length - len(configuration_item_id_str)) + COLUMN_SPACING
            configuration_item_str += configuration_item_id_str + " " * id_column_gap_length

            # creates the cell for the enabled column
            enabled = configuration_item.is_enabled()
            enabled_str = INACTIVE_VALUE
            if enabled:
                enabled_str = ACTIVE_VALUE
            enabled_column_gap_length = (maximum_enabled_column_length - len(enabled_str)) + COLUMN_SPACING
            configuration_item_str += enabled_str + " " * enabled_column_gap_length

            # creates the cell for the type column
            configuration_item_type_str = configuration_item.__class__.__name__
            type_column_gap_length = (maximum_type_column_length - len(configuration_item_type_str)) + COLUMN_SPACING
            configuration_item_str += configuration_item_type_str + " " * type_column_gap_length

            # creates the description for the description column
            configuration_item_description_str = str(configuration_item)
            configuration_item_str += configuration_item_description_str

            output_configuration_items_str += configuration_item_str + "\n"

        return output_configuration_items_str

    def get_configurations_string(self, configurations):
        maximum_id_column_length = len(ID_COLUMN_HEADER)
        maximum_description_column_length = len(DESCRIPTION_COLUMN_HEADER)

        # discovers the maximum column length for each column
        for configuration in configurations:

            # sets the new maximum id column length
            configuration_id = configuration.get_configuration_id()
            configuration_id_str = str(configuration_id)
            if len(configuration_id_str) > maximum_id_column_length:
                maximum_id_column_length = len(configuration_id_str)

            # sets the new maximum description column length
            configuration_description_str = str(configuration)
            if len(configuration_description_str) > maximum_description_column_length:
                maximum_description_column_length = len(configuration_description_str)

        # creates the table header
        id_column_gap_length = (maximum_id_column_length - len(ID_COLUMN_HEADER)) + COLUMN_SPACING
        output_configurations_str = ID_COLUMN_HEADER + " " * id_column_gap_length
        output_configurations_str += DESCRIPTION_COLUMN_HEADER + "\n"

        # creates the table rows
        for configuration in configurations:
            configuration_str = str()

            # creates the cell for the id column
            configuration_id_str = str(configuration.get_configuration_id())
            id_column_gap_length = (maximum_id_column_length - len(configuration_id_str)) + COLUMN_SPACING
            configuration_str += configuration_id_str + " " * id_column_gap_length

            # creates the description for the description column
            configuration_description_str = str(configuration)
            configuration_str += configuration_description_str

            output_configurations_str += configuration_str + "\n"

        return output_configurations_str

    def process_list_configurations(self, args, output_method):
        # outputs a list of available data converter configurations
        output_string = "".join([configuration_plugin.id + "\n" for configuration_plugin in self.data_converter_plugin.configuration_plugins])[:-1]
        output_method(output_string)

    def process_list_loaded_configurations(self, args, output_method):
        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the loaded configurations
        loaded_configuration_ids = data_converter.get_loaded_configuration_ids()
        loaded_configurations = [data_converter.get_loaded_configuration(loaded_configuration_id) for loaded_configuration_id in loaded_configuration_ids]

        # outputs the retrieved configurations
        output_method(self.get_configurations_string(loaded_configurations))

    def process_load_configuration(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the data converter configuration id from the console command arguments
        data_converter_configuration_plugin_id = args[0]

        # loads a new configuration instance from the specified configuration plugin
        data_converter.load_configuration(data_converter_configuration_plugin_id, {})

    def process_unload_configuration(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the data converter configuration id from the console command arguments
        data_converter_configuration_id = int(args[0])

        # unloads a new configuration instance from the specified configuration plugin
        data_converter.unload_configuration(data_converter_configuration_id)

    def process_set_configuration_option(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the command parameters
        data_converter_configuration_id = int(args[0])
        option_name = args[1]
        option_value = args[2]

        # sets an option in the specified conversion configuration
        data_converter.set_configuration_option(data_converter_configuration_id, option_name, option_value)

    def process_list_configuration_items(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the data converter configuration id from the console command arguments
        data_converter_configuration_id = int(args[0])

        # retrieves the specified data converter configuration instance
        data_converter_configuration = data_converter.get_loaded_configuration(data_converter_configuration_id)

        # retrieves configuration item ids of the specified type in case two arguments were provided
        if len(args) >= 2:
            configuration_item_type = args[1]
            configuration_item_ids = data_converter_configuration.get_configuration_item_ids_by_type(configuration_item_type)
        else:
            # otherwise retrieves all configuration item ids
            configuration_item_ids = data_converter_configuration.get_configuration_item_ids()

        # retrieves the configuration items that correspond to the retrieved configuration item ids
        configuration_items = [data_converter_configuration.get_configuration_item(configuration_item_id) for configuration_item_id in configuration_item_ids]

        # outputs the retrieved configuration items
        output_method(self.get_output_configuration_items_string(configuration_items))

    def process_list_dependent_configuration_items(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the data converter configuration id and dependency configuration item id from the console command arguments
        data_converter_configuration_id = int(args[0])
        configuration_item_id = int(args[1])

        # retrieves the specified data converter configuration instance
        data_converter_configuration = data_converter.get_loaded_configuration(data_converter_configuration_id)

        # retrieves the dependent configuration item ids of the specified type in case three arguments were provided
        if len(args) >= 3:
            configuration_item_type = args[2]
            dependent_configuration_item_ids = data_converter_configuration.get_dependent_configuration_item_ids_by_type(configuration_item_id, configuration_item_type)
        else:
            # otherwise retrieves all dependent configuration item ids
            dependent_configuration_item_ids = data_converter_configuration.get_dependent_configuration_item_ids(configuration_item_id)

        # retrieves the configuration items that correspond to the retrieved configuration item ids
        dependent_configuration_items = [data_converter_configuration.get_configuration_item(dependent_configuration_item_id) for dependent_configuration_item_id in dependent_configuration_item_ids]

        # outputs the retrieved configuration items
        output_method(self.get_output_configuration_items_string(dependent_configuration_items))

    def process_enable_configuration_item(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the data converter configuration id and configuration item id from the console command arguments
        data_converter_configuration_id = int(args[0])
        configuration_item_id = int(args[1])

        # retrieves the specified data converter configuration instance
        data_converter_configuration = data_converter.get_loaded_configuration(data_converter_configuration_id)

        # enables the specified configuration item and all that depend on it
        data_converter_configuration.enable_configuration_item(configuration_item_id)

    def process_enable_all_configuration_items(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the data converter configuration id from the console command arguments
        data_converter_configuration_id = int(args[0])

        # retrieves the specified data converter configuration instance
        data_converter_configuration = data_converter.get_loaded_configuration(data_converter_configuration_id)

        # enables all disabled configuration items
        configuration_item_ids = data_converter_configuration.get_configuration_item_ids()
        for configuration_item_id in configuration_item_ids:

            # enables the configuration item only if its disabled
            if not data_converter_configuration.is_configuration_item_enabled(configuration_item_id):
                data_converter_configuration.enable_configuration_item(configuration_item_id)

    def process_disable_configuration_item(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the data converter configuration id and configuration item id from the console command arguments
        data_converter_configuration_id = int(args[0])
        configuration_item_id = int(args[1])

        # retrieves the specified data converter configuration instance
        data_converter_configuration = data_converter.get_loaded_configuration(data_converter_configuration_id)

        # disables the specified configuration item and all that depend on it
        data_converter_configuration.disable_configuration_item(configuration_item_id)

    def process_disable_all_configuration_items(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the data converter configuration id from the console command arguments
        data_converter_configuration_id = int(args[0])

        # retrieves the specified data converter configuration instance
        data_converter_configuration = data_converter.get_loaded_configuration(data_converter_configuration_id)

        # disables all enabled configuration items
        configuration_item_ids = data_converter_configuration.get_configuration_item_ids()
        for configuration_item_id in configuration_item_ids:

            # disables the configuration item only if its enabled
            if data_converter_configuration.is_configuration_item_enabled(configuration_item_id):
                data_converter_configuration.disable_configuration_item(configuration_item_id)

    def process_convert_data(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the data converter instance
        data_converter = self.data_converter_plugin.data_converter

        # retrieves the data converter configuration id from the console command arguments
        data_converter_configuration_id = int(args[0])

        # converts data using the specified data converter configuration
        data_converter.convert_data(data_converter_configuration_id)
