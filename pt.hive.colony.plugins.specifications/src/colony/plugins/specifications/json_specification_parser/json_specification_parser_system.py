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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

import json_specification_parser_exceptions

SPECIFICATION_PARSER_NAME = "json"
""" The specification parser name """

JSON_FILE_ENCODING = "utf-8"
""" The json file encoding """

class JsonSpecificationParser:
    """
    The json specification parser class.
    """

    json_specification_parser_plugin = None
    """ The json specification parser plugin """

    def __init__(self, json_specification_parser_plugin):
        """
        Constructor of the class.

        @type json_specification_parser_plugin: JsonSpecificationParserPlugin
        @param json_specification_parser_plugin: The json specification parser plugin.
        """

        self.json_specification_parser_plugin = json_specification_parser_plugin

    def get_specification_parser_name(self):
        """
        Retrieves the specification parser name.

        @rtype: String
        @return: The specification parser name.
        """

        return SPECIFICATION_PARSER_NAME

    def parse_specification(self, specification):
        # retrieves the json plugin
        json_plugin = self.json_specification_parser_plugin.json_plugin

        # tries to retrieve the file buffer
        file_buffer = specification.get_file_buffer()

        # retrieves the specification file path
        file_path = specification.get_file_path()

        # in case the file buffer is defined
        if file_buffer:
            # parses the json contents retrieving the json data
            json_data = json_plugin.loads(file_buffer)
        # in case the file path is defined
        elif file_path:
            # verifies the file path
            self._verify_file_path(file_path)

            # opens the json file
            json_file = open(file_path, "rb")

            try:
                # parses the json contents retrieving the json data
                json_data = json_plugin.load_file_encoding(json_file, JSON_FILE_ENCODING)
            finally:
                # closes the json file
                json_file.close()
        else:
            # raises the invalid specification file exception
            raise json_specification_parser_exceptions.InvalidSpecificationFile("not enough information about file")

        # iterates over all the json keys and values
        # to copy the information to the specification structure
        # properties map
        for json_key, json_value in json_data.items():
            # sets the json key and value as a property in
            # the specification structure
            specification.set_property(json_key, json_value)

    def _verify_file_path(self, file_path):
        """
        Verifies the given file path, testing if the file exits.

        @type file_path: String
        @param file_path: The file path to be verified.
        """

        # in case the file path does not exist
        if not os.path.exists(file_path):
            # raises the invalid specification file exception
            raise json_specification_parser_exceptions.InvalidSpecificationFile("file not found: " + file_path)
