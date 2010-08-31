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

import installation_deb_exceptions

ADAPTER_NAME = "deb"
""" The adapter name """

FILE_PATH_VALUE = "file_path"
""" The file path value """

class InstallationDeb:
    """
    The installation deb class.
    """

    installation_deb_plugin = None
    """ The installation deb plugin """

    def __init__(self, installation_deb_plugin):
        """
        Constructor of the class.

        @type installation_deb_plugin: InstallationDebPlugin
        @param installation_deb_plugin: The installation deb plugin.
        """

        self.installation_deb_plugin = installation_deb_plugin

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
            raise installation_deb_exceptions.MissingParameter(FILE_PATH_VALUE)

        # in case the file path is not in the parameters map
        if not FILE_PATH_VALUE in parameters:
            # raises the missing parameter exception
            raise installation_deb_exceptions.MissingParameter(FILE_PATH_VALUE)

        # retrieves the file path from the parameters
        file_path = parameters[FILE_PATH_VALUE]

        # retrieves the file format from the parameters
        #file_format = parameters.get(FILE_FORMAT_VALUE, DEFAULT_FILE_FORMAT)

        # retrieves the file path references from the parameters
        #deb_file_arguments = parameters.get(DEB_FILE_ARGUMENTS_VALUE, DEFAULT_DEB_FILE_ARGUMENTS)

        # creates a new deb file
        #deb_file = DebFile(self, file_path, file_format, deb_file_arguments)

        # returns the deb file
        #return deb_file

class InstallationFile:
    pass
