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

import re
import os

import data_converter_io_adapter_csv_exceptions

INPUT_DIRECTORY_PATH_VALUE = "input_directory_path"
""" The input directory path value """

INPUT_ENTITY_HANDLERS_VALUE = "input_entity_handlers"
""" The input entity handlers value """

INPUT_ATTRIBUTE_HANDLERS_VALUE = "input_attribute_handlers"
""" The input attribute handlers value """

TOKEN_SEPARATOR_VALUE = "token_separator"
""" The token separator value """

TEXT_DELIMITER_VALUE = "text_delimiter"
""" The text delimiter value """

FILE_READ_MODE = "r"
""" The read access mode for files in python """

CSV_FILE_EXTENSION = ".csv"
""" Extension of csv files """

DEFAULT_TOKEN_SEPARATOR = ","
""" The default csv token separator """

DEFAULT_TEXT_DELIMITER = "\""
""" The default csv text delimiter """

NUMBER_REGEX = "[0-9]+((\.|,)[0-9]*)?"
""" Regular expression used to detect if a string contains a number """

class IoAdapterCsv:
    """
    Input output adapter used to load and save data converter intermediate
    structures to and from csv format.
    """

    io_adapter_csv_plugin = None
    """ Io adapter csv plugin """

    def __init__(self, io_adapter_csv_plugin):
        """
        Constructor of the class.

        @type io_adapter_csv_plugin: IoAdapterCsvPlugin
        @param io_adapter_csv_plugin: Input output adapter csv plugin.
        """

        self.io_adapter_csv_plugin = io_adapter_csv_plugin

    def load_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the
        csv source specified in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to
        load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        # extracts the mandatory options
        directory_path = configuration.get_option(INPUT_DIRECTORY_PATH_VALUE)

        # sets the directory paths
        directory_paths = [
            directory_path
        ]

        # extracts the non-mandatory options
        input_entity_handlers = options.get(INPUT_ENTITY_HANDLERS_VALUE, [])
        input_attribute_handlers = options.get(INPUT_ATTRIBUTE_HANDLERS_VALUE, [])
        token_separator = options.get(TOKEN_SEPARATOR_VALUE, DEFAULT_TOKEN_SEPARATOR)
        text_delimiter = options.get(TEXT_DELIMITER_VALUE, DEFAULT_TEXT_DELIMITER)

        # indexes the csv files in the specified directories
        entity_name_file_path_map = self.index_csv_files(directory_paths)

        # loads the csv files into the intermediate structure
        for entity_name, file_path in entity_name_file_path_map.iteritems():

            # raises an exception in case the specified file does not exist
            if not os.path.exists(file_path):
                raise data_converter_io_adapter_csv_exceptions.IoAdapterCsvFileNotFound(file_path)

            # opens the csv file
            csv_file = open(file_path, FILE_READ_MODE)

            # retrieves the csv header tokens removing whitespaces, newline characters and text delimiters
            csv_header = csv_file.readline()[:-1]
            csv_header_tokens = csv_header.split(token_separator)
            csv_header_tokens = [csv_header_token.strip() for csv_header_token in csv_header_tokens]
            csv_header_tokens = [csv_header_token[1:-1].strip() for csv_header_token in csv_header_tokens]

            # reads the csv file
            csv_file_data = csv_file.read()

            # decodes the file data in case the input encoding was specified
            if configuration.has_option("input_encoding"):
                input_encoding = configuration.get_option("input_encoding")
                csv_file_data = csv_file_data.decode(input_encoding)

            # tokenizes the csv data
            csv_data_tokens = self.tokenize_csv_data(csv_file_data, token_separator, text_delimiter)

            # closes the csv file
            csv_file.close()

            # iterates through the csv file tokens populating the specified entities
            first_pass = False
            for csv_data_token_index in range(len(csv_data_tokens)):

                # retrieves the csv header token - csv data token pair
                csv_header_token_index = csv_data_token_index % len(csv_header_tokens)
                csv_header_token = csv_header_tokens[csv_header_token_index]
                csv_data_token = csv_data_tokens[csv_data_token_index]

                # creates a new entity in case the cursor is aligned with the
                # first header token
                if csv_header_token_index == 0:
                    entity = intermediate_structure.create_entity(entity_name)

                    # passes the previous entity through the specified input entity handlers
                    if not first_pass:
                        for input_entity_handler in input_entity_handlers:
                            entity = input_entity_handler(intermediate_structure, entity)

                    first_pass = False

                # sets the pair as an entity attribute in case the csv header token is not empty
                if csv_header_token:
                    attribute_name = csv_header_token
                    attribute_value = csv_data_token

                    # passes the attribute through the specified input attribute handlers
                    for input_attribute_handler in input_attribute_handlers:
                        attribute_value = input_attribute_handler(intermediate_structure, entity, attribute_value)

                    entity.set_attribute(attribute_name, attribute_value)

    def save_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in csv format at the location
        and with characteristics defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate
        structure into csv format.
        """

        raise data_converter_io_adapter_csv_exceptions.IoAdapterCsvMethodNotImplemented()

    # @todo: comment this
    def tokenize_csv_data(self, csv_data, token_separator, text_delimiter):
        separators = (
            token_separator,
            "\n"
        )

        tokens = []
        token = str()
        inside_text = False

        # parses the csv data into tokens
        for character in csv_data:

            # marks the parser as being inside or outside a text
            # in case it finds a text delimiter, and ignores the character
            if character == text_delimiter:
                inside_text = not inside_text
            elif not inside_text and character in separators:
                # inserts the token into the list of tokens in
                # case the parser is not inside a text and the
                # character is a separator
                token = self.extract_value(token, text_delimiter)
                tokens.append(token)
                token = ""
            else:
                # otherwise adds the character to the current token
                token += character

        return tokens

    # @todo: comment this
    def extract_value(self, csv_value, text_delimiter):
        value = None

        # removes white spaces and newlines around the string
        csv_value = csv_value.strip()

        # converts the value in case it is not an empty string
        if csv_value:

            # converts the value to a float in case it is a number
            number_regex = re.compile(NUMBER_REGEX)
            regex_match = number_regex.match(csv_value)
            if regex_match and regex_match.group() == csv_value:
                value = csv_value.replace(",", ".")
                value = float(value)

                # converts the float to an integer in case it has
                # no decimal values
                if value - int(value) == 0.0:
                    value = int(value)
            else:
                # otherwise keeps the value as a string
                value = csv_value

        return value

    def index_csv_files(self, directory_paths):
        """
        Crawls the provided directories searching for csv files and indexing
        their names to their directory path.

        @type directory_paths: List
        @param directory_paths: List with directory paths where to search for csv files.
        @rtype: Dictionary
        @return: Map associating the names of the discovered csv files with the
        paths of the directories they are contained in.
        """

        entity_name_path_map = {}

        for directory_path in directory_paths:
            for root_path, _directories, files in os.walk(directory_path, topdown = True):
                for file_name in files:
                    extension_name = file_name[len(file_name) - 4:]
                    if extension_name == CSV_FILE_EXTENSION:
                        entity_name = file_name[:-4]
                        file_path = os.path.join(root_path, file_name)
                        entity_name_path_map[entity_name] = file_path

        return entity_name_path_map
