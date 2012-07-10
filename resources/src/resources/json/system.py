#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system

RESOURCES_PARSER_NAME = "json"
""" The resources parser name """

JSON_FILE_ENCODING = "utf-8"
""" The json file encoding """

class ResourcesJson(colony.base.system.System):
    """
    The resources json (parser) class.
    """

    def get_resources_parser_name(self):
        return RESOURCES_PARSER_NAME

    def parse_resource(self, resource):
        # retrieves the json plugin
        json_plugin = self.plugin.json_plugin

        # retrieves the json file path
        json_file_path = resource.data

        # retrieves the full resources path
        full_resources_path = resource.full_resources_path

        # constructs the full json file path
        full_json_file_path = full_resources_path + "/" + json_file_path

        # opens the json file in read mode then reads
        # the complete set of contents from it and
        # closes the file to avoid any possible leaks
        json_file = open(full_json_file_path, "rb")
        try: resource.data = json_plugin.load_file_encoding(json_file, JSON_FILE_ENCODING)
        finally: json_file.close()
