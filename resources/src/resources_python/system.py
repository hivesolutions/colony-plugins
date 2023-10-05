#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import sys

import colony

RESOURCES_PARSER_NAME = "python"
""" The resources parser name """

CONFIGURATION_VALUE = "configuration"
""" The configuration value """

class ResourcesPython(colony.System):
    """
    The resources python (parser) class.
    """

    def get_resources_parser_name(self):
        return RESOURCES_PARSER_NAME

    def parse_resource(self, resource):
        # retrieves the python file path
        python_file_path = resource.data

        # retrieves the full resources path
        full_resources_path = resource.full_resources_path

        # creates the full python file path
        # from the full resources path and the python file path
        full_python_file_path = full_resources_path + "/" + python_file_path

        # retrieves the file system encoding
        file_system_encoding = sys.getfilesystemencoding()

        # encodes the full python file path using the file system encoding
        full_python_file_path = full_python_file_path.encode(file_system_encoding)

        # creates the symbols map to be used in the interpretation
        # of the file as the locals and globals map
        symbols_map = {}

        # interprets the python file path with the symbols map
        colony.legacy.execfile(full_python_file_path, symbols_map, symbols_map)

        # tries to retrieve the configuration
        configuration = symbols_map.get(CONFIGURATION_VALUE, {})

        # parses the configuration contents from the python module
        resource.data = configuration
