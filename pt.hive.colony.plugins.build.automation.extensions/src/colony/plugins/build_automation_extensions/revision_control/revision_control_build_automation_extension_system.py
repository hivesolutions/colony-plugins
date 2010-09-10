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

import os

ADAPTER_VALUE = "adapter"
""" The adapter value """

PATH_VALUE = "path"
""" The path value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

REPOSITORY_PATH_VALUE = "repository_path_value"
""" The repository path value """

VERSION_FILE_PATH_VALUE = "version_file_path"
""" The version file path value """

class RevisionControlBuildAutomationExtension:
    """
    The revision control build automation extension class.
    """

    revision_control_build_automation_extension_plugin = None
    """ The revision control build automation extension plugin """

    def __init__(self, revision_control_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type revision_control_build_automation_extension_plugin: RevisionControlBuildAutomationExtensionPlugin
        @param revision_control_build_automation_extension_plugin: The revision control build automation extension plugin.
        """

        self.revision_control_build_automation_extension_plugin = revision_control_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure):
        # retrieves the revision control manager plugin
        revision_control_manager_plugin = self.revision_control_build_automation_extension_plugin.revision_control_manager_plugin

        # retrieves the required parameters
        adapter = parameters[ADAPTER_VALUE]
        path = parameters[PATH_VALUE]
        target_path = parameters[TARGET_PATH_VALUE]
        version_file_path = parameters.get(VERSION_FILE_PATH_VALUE, None)

        # creates the revision control parameters
        revision_control_parameters = {REPOSITORY_PATH_VALUE : target_path}

        # loads a new revision control manager for the specified adapter name
        revision_control_manager = revision_control_manager_plugin.load_revision_control_manager(adapter, revision_control_parameters)

        # in case the target path already exists
        if os.path.exists(target_path):
            # updates the repository to the current head revision
            revision = revision_control_manager.update([target_path], None)
        else:
            # checks out the repository to the target path
            revision = revision_control_manager.checkout(path, target_path)

        # writes the version number in case it is defined
        version_file_path and self._write_version_number(version_file_path, revision)

    def _write_version_number(self, version_file_path, revision):
        # retrieves the revision number
        revision_number = revision.get_number()

        # converts the revision number to a string
        revision_number_string = str(revision_number)

        # opens the version file
        version_file = open(version_file_path, "wb")

        try:
            # writes the revision number string value
            version_file.write(revision_number_string)
        finally:
            # closes the version file
            version_file.close()
