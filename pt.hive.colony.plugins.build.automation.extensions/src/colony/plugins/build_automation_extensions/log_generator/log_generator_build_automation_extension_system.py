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

import os

LOG_DIRECTORY_VALUE = "log_directory"
""" The log directory value """

FULL_LOG_NAME = "build_automation.log"
""" The full log name """

class LogGeneratorBuildAutomationExtension:
    """
    The log generator build automation extension class.
    """

    log_generator_build_automation_extension_plugin = None
    """ The log generator build automation extension plugin """

    def __init__(self, log_generator_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type log_generator_build_automation_extension_plugin: LogGeneratorBuildAutomationExtensionPlugin
        @param log_generator_build_automation_extension_plugin: The log generator build automation extension plugin.
        """

        self.log_generator_build_automation_extension_plugin = log_generator_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # retrieves the logging buffer
        logging_buffer = build_automation_structure_runtime.logging_buffer

        # retrieves the logging contents from the logging buffer
        logging_contents = logging_buffer.get_value()

        # retrieves the log directory
        log_directory = build_properties[LOG_DIRECTORY_VALUE]

        # creates the full log file path
        full_log_file_path = os.path.join(log_directory, FULL_LOG_NAME)

        # writes the logging contents to the log file
        self._write_file(full_log_file_path, logging_contents)

        # returns true (success)
        return True

    def _write_file(self, file_path, file_contents):
        # opens the file
        file = open(file_path, "wb")

        try:
            # writes the file contents
            file.write(file_contents)
        except:
            # closes the file
            file.close()
