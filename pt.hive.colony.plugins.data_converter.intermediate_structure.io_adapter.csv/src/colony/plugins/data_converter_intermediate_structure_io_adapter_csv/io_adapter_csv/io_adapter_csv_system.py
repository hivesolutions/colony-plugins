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

import os.path

import io_adapter_csv_exceptions

DEFAULT_CSV_TOKEN_SEPARATOR = ","
""" The default csv token separator """

class IoAdapterCsv:
    """
    Input output adapter used to serialize data converter intermediate structures to csv format.
    """

    def __init__(self, io_adapter_csv_plugin):
        """
        Class constructor.

        @type io_adapter_csv_plugin: IoAdapterCsvPlugin
        @param io_adapter_csv_plugin: Input output adapter csv plugin.
        """

        self.io_adapter_csv_plugin = io_adapter_csv_plugin

    def load(self, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the csv source specified in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided intermediate structure.
        """

        self.io_adapter_csv_plugin.logger.info("[%s] Loading intermediate structure with csv io adapter" % self.io_adapter_csv_plugin.id)

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["file_path", "entity_names", "entity_name_attribute_names"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_csv_exceptions.IoAdapterCsvOptionNotFound("IoAdapterCsv.load - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        file_path = options["file_path"]
        entity_names = options["entity_names"]
        entity_name_attribute_names_map = options["entity_name_attribute_names"]

        # raises an exception if there is a specified entity whose schema was not provided
        for entity_name in entity_names:
            if not entity_name in entity_name_attribute_names_map:
                raise io_adapter_csv_exceptions.IoAdapterCsvOptionNotFound("IoAdapterCsv.load - Schema missing for specified entity (entity_name = %s)" % entity_name)

        # extracts the non-mandatory options
        csv_token_separator = DEFAULT_CSV_TOKEN_SEPARATOR
        if "csv_token_separator" in options:
            csv_token_separator = options["csv_token_separator"]

        # raises an exception in case the specified file does not exist
        if not os.path.exists(file_path):
            raise io_adapter_csv_exceptions.IoAdapterCsvOptionValid("IoAdapterCsv.load - Specified file to load intermediate structure from does not exist (file_path = %s)" % file_path)

        # opens the csv file and retrieves the raw data
        csv_file = open(file_path, "r")
        csv_file_data = csv_file.read()
        csv_file.close()

        # tokenizes the raw data and extracts the entities from it
        csv_file_token_index = 0
        csv_file_tokens = []
        if csv_file_data:
            csv_file_tokens = csv_file_data.split(csv_token_separator)

        # iterates through the csv file tokens populating the specified entities
        while csv_file_token_index < len(csv_file_tokens):

            # extracts entities in the specified order
            for entity_name in entity_names:
                attribute_names = entity_name_attribute_names_map[entity_name]
                entity = intermediate_structure.create_entity(entity_name)

                # extracts attributes in the specified order
                for attribute_name in attribute_names:
                    attribute_value = csv_file_tokens[csv_file_token_index]
                    entity.set_attribute(attribute_name, attribute_value)
                    csv_file_token_index += 1

    def save(self, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in csv format at the location and with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure into csv format.
        """

        self.io_adapter_csv_plugin.logger.info("[%s] Saving intermediate structure with csv io adapter" % self.io_adapter_csv_plugin.id)

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["file_path", "entity_names", "entity_name_attribute_names"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_csv_exceptions.IoAdapterCsvOptionNotFound("IoAdapterCsv.save - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        file_path = options["file_path"]
        entity_names = options["entity_names"]
        entity_name_attribute_names_map = options["entity_name_attribute_names"]

        # raises an exception if there is a specified entity whose schema was not provided
        for entity_name in entity_names:
            if not entity_name in entity_name_attribute_names_map:
                raise io_adapter_csv_exceptions.IoAdapterCsvOptionNotFound("IoAdapterCsv.save - Schema missing for specified entity (entity_name = %s)" % entity_name)

        # extracts the non-mandatory options
        csv_token_separator = DEFAULT_CSV_TOKEN_SEPARATOR
        if "csv_token_separator" in options:
            csv_token_separator = options["csv_token_separator"]

        # opens the csv file and retrieves the raw data
        csv_file = open(file_path, "w")
        csv_file_data = ""

        # saves the entities in the specified order
        entities = intermediate_structure.get_entities()
        for entity in entities:
            entity_name = entity.get_name()
            attribute_names = entity_name_attribute_names_map[entity_name]

            # saves the attributes in the specified order
            for attribute_name in attribute_names:
                attribute_value = entity.get_attribute(attribute_name)
                csv_file_data += attribute_value + csv_token_separator

        # removes the extra token separator left at the end of the file data
        csv_file_data = csv_file_data[:-1 * len(csv_token_separator)]

        # writes the csv data to the file
        csv_file.write(csv_file_data)

        # closes the csv file
        csv_file.close()
