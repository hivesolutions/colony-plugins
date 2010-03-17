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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

TARGET_DIRECTORY_VALUE = "target_directory"
""" The target directory value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

COLONY_VALUE = "colony"
""" The colony value """

SPECIFICATION_FILE_VALUE = "specification_file"
""" The specification file value """

class PackingBuildAutomationExtension:
    """
    The packing build automation extension class.
    """

    packing_build_automation_extension_plugin = None
    """ The packing build automation extension plugin """

    def __init__(self, packing_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type packing_build_automation_extension_plugin: PackingBuildAutomationExtensionPlugin
        @param packing_build_automation_extension_plugin: The packing build automation extension plugin.
        """

        self.packing_build_automation_extension_plugin = packing_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure):
        # retrieves the main packing manager plugin
        main_packing_manager_plugin = self.packing_build_automation_extension_plugin.main_packing_manager_plugin

        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the plugin path
        plugin_path = build_automation_structure.get_plugin_path()

        # retrieves the target directory
        target_directory = build_properties[TARGET_DIRECTORY_VALUE]

        # retrieves the specification file
        specification_file = parameters[SPECIFICATION_FILE_VALUE]

        # creates the file paths list
        file_paths_list = [plugin_path + "/" + specification_file]

        # creates the properties map for the directory packing
        properties = {TARGET_PATH_VALUE : plugin_path + "/" + target_directory}

        # packs the directory
        main_packing_manager_plugin.pack_files(file_paths_list, properties, COLONY_VALUE)
