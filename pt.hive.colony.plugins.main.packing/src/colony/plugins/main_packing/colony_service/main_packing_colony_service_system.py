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

__revision__ = "$LastChangedRevision: 7147 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-12-21 16:50:46 +0000 (seg, 21 Dez 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

SERVICE_NAME = "colony"
""" The service name """

class MainPackingColonyService:
    """
    The main packing colony service class.
    """

    main_packing_colony_service_plugin = None
    """ The main packing colony service plugin """

    def __init__(self, main_packing_colony_service_plugin):
        """
        Constructor of the class.

        @type main_packing_colony_service_plugin: MainPackingColonyServicePlugin
        @param main_packing_colony_service_plugin: The main packing colony service plugin.
        """

        self.main_packing_colony_service_plugin = main_packing_colony_service_plugin

    def get_service_name(self):
        """
        Retrieves the service name.

        @rtype: String
        @return: The service name.
        """

        return SERVICE_NAME

    def pack_directory(self, directory_path, recursive):
        """
        Packs the directory using the service.

        @type directory_path: String
        @param directory_path: The path to the directory to be used
        in the packing.
        @type recursive: bool
        @param recursive: If the packing should be made recursive.
        """

        print("packing directory files")

    def pack_files(self, file_paths_list):
        """
        Packs the given files using the service.

        @type file_paths_list: List
        @param file_paths_list: The list of file paths to be used in the packing.
        """

        print("packing random files")
