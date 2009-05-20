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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import dbi
import odbc
import stat
import string
import datetime
import os.path

import io_adapter_dbase_exceptions

DBASE_EXTENSION = "dbf"
ODBC_CONNECTION_STRING = 'Driver={Microsoft Visual FoxPro Driver};SourceType=DBF;SourceDB=%s;Exclusive=No;Collate=Machine;NULL=NO;DELETED=NO;BACKGROUNDFETCH=NO;'

class IoAdapterDbase:
    """
    Input output adapter used to serialize data converter intermediate structures to dbase format.
    """

    def __init__(self, io_adapter_dbase_plugin):
        """
        Class constructor.

        @type io_adapter_dbase_plugin: IoAdapterDbasePlugin
        @param io_adapter_dbase_plugin: Input output adapter dbase plugin.
        """

        self.io_adapter_dbase_plugin = io_adapter_dbase_plugin

    def load(self, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the dbase source specified in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided intermediate structure.
        """

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["directory_paths"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_dbase_exceptions.IoAdapterDbaseOptionMissing("IoAdapterDbase.load - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        directory_paths = options["directory_paths"]

        # raises an exception in case the specified directory does not exist
        for directory_path in directory_paths:
            if not os.path.exists(directory_path):
                raise io_adapter_dbase_exceptions.IoAdapterDbaseOptionValid("IoAdapterDbase.load - Specified directory to load intermediate structure from does not exist (directory_path = %s)" % directory_path)

    def save(self, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in dbase format at the location and with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure into dbase format.
        """

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["directory_paths"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_dbase_exceptions.IoAdapterDbaseOptionMissing("IoAdapterDbase.save - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        directory_paths = options["directory_paths"]

        # raises an exception in case the specified directory does not exist
        for directory_path in directory_paths:
            if not os.path.exists(directory_path):
                raise io_adapter_dbase_exceptions.IoAdapterDbaseOptionValid("IoAdapterDbase.save - Specified directory to load intermediate structure from does not exist (directory_path = %s)" % directory_path)
