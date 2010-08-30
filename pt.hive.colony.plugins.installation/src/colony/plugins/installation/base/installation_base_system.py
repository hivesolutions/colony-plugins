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

import installation_base_exceptions

FILE_PATH_VALUE = "file_path"
""" The file path value """

class InstallationBase:
    """
    The installation base class.
    """

    installation_base_plugin = None
    """ The installation base plugin """

    def __init__(self, installation_base_plugin):
        """
        Constructor of the class.

        @type installation_base_plugin: InstallationBasePlugin
        @param installation_base_plugin: The installation base plugin.
        """

        self.installation_base_plugin = installation_base_plugin

    def create_file(self, parameters):
        """
        Creates the file for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the file creation.
        @rtype: InstallationFile
        @return: The created file.
        """

        # in case the file path is not in the parameters map
        if not FILE_PATH_VALUE in parameters:
            # raises the missing parameter exception
            raise installation_base_exceptions.MissingParameter(FILE_PATH_VALUE)

        # in case the file path is not in the parameters map
        if not FILE_PATH_VALUE in parameters:
            # raises the missing parameter exception
            raise installation_base_exceptions.MissingParameter(FILE_PATH_VALUE)

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
