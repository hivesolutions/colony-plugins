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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import datetime

import colony.libs.map_util

DEFAULT_ENCODING = "Cp1252"
""" The default encoding """

DATE_FORMAT = "%b %d %Y %H:%M:%S"
""" The format used to convert dates to strings """

VERSION_VALUE = "version"
""" The version value """

RELEASE_VERSION_VALUE = "release_version"
""" the release version value """

DATE_VALUE = "date"
""" the date value """

class TemplateEngineBuildAutomationExtension:
    """
    The template engine build automation extension class.
    """

    template_engine_build_automation_extension_plugin = None
    """ The template engine build automation extension plugin """

    def __init__(self, template_engine_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type template_engine_build_automation_extension_plugin: TemplateEngineBuildAutomationExtensionPlugin
        @param template_engine_build_automation_extension_plugin: The template engine build automation extension plugin.
        """

        self.template_engine_build_automation_extension_plugin = template_engine_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.template_engine_build_automation_extension_plugin.template_engine_manager_plugin

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # retrieves the contents from the parameters
        contents = parameters.get("contents", {})

        # retrieves the files from the parameters
        files = colony.libs.map_util.map_get_values(contents, "file")

        # iterates over all the files
        for file in files:
            # retrieves the file path from the file
            file_path = file["path"]

            # retrieves the file encoding from the file
            file_encoding = file.get("encoding", DEFAULT_ENCODING)

            # parses the template file path using the file encoding
            template_file = template_engine_manager_plugin.parse_file_path_encoding(file_path, file_encoding)

            # assigns the values to the template file using the build
            # automation structure runtime
            self._assign_template_file(template_file, build_automation_structure_runtime)

            # processes the template file
            processed_template_file = template_file.process()

            # encodes the processed template using the file encoding
            processed_template_file_encoded = processed_template_file.encode(file_encoding)

            # open the file
            _file = open(file_path, "wb")

            try:
                # writes the processed template file encoded to the
                # file (as the final result)
                _file.write(processed_template_file_encoded)
            finally:
                # closes the file
                _file.close()

        # returns true (success)
        return True

    def _assign_template_file(self, template_file, build_automation_structure_runtime):
        # retrieves the current datetime
        current_datetime = datetime.datetime.utcnow()

        # formats the current datetime to string
        current_date_string = current_datetime.strftime(DATE_FORMAT)

        # retrieves the current version value
        version_value = build_automation_structure_runtime.properties.get(VERSION_VALUE, -1)

        # assigns the release version to the template file
        template_file.assign(RELEASE_VERSION_VALUE, "b" + str(version_value))

        # assigns the date to the template file
        template_file.assign(DATE_VALUE, current_date_string)
