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

import installation_zip_exceptions

ADAPTER_NAME = "zip"
""" The adapter name """

FILE_EXTENSION_VALUE = ".zip"
""" The file extension value """

PACKAGE_VALUE = "package"
""" The package value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

PACKAGE_VERSION_VALUE = "package_version"
""" The package name value """

PACKAGE_ARCHITECTURE_VALUE = "package_architecture"
""" The package architecture value """

NAME_SEPARATION_TOKEN = "_"
""" The name separation token """

class InstallationZip:
    """
    The installation zip class.
    """

    installation_zip_plugin = None
    """ The installation zip plugin """

    def __init__(self, installation_zip_plugin):
        """
        Constructor of the class.

        @type installation_zip_plugin: InstallationZipPlugin
        @param installation_zip_plugin: The installation zip plugin.
        """

        self.installation_zip_plugin = installation_zip_plugin

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return ADAPTER_NAME

    def generate_installation_file(self, parameters):
        """
        Generates the installation file for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the installation file generation.
        """

        # in case the file path is not in the parameters map
        if not FILE_PATH_VALUE in parameters:
            # raises the missing parameter exception
            raise installation_zip_exceptions.MissingParameter(FILE_PATH_VALUE)

        # retrieves the package from the parameters
        package = parameters[PACKAGE_VALUE]

        # retrieves the file path from the parameters
        file_path = parameters[FILE_PATH_VALUE] + NAME_SEPARATION_TOKEN + package[PACKAGE_VERSION_VALUE] + NAME_SEPARATION_TOKEN + package[PACKAGE_ARCHITECTURE_VALUE] + FILE_EXTENSION_VALUE

        print file_path
