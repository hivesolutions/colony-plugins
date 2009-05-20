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

import os.path
import cPickle as pickle

import io_adapter_pickle_exceptions

class IoAdapterPickle:
    """
    Input output adapter used to serialize data converter intermediate structures to pickle binary format.
    """

    def __init__(self, io_adapter_pickle_plugin):
        """
        Class constructor.

        @type io_adapter_pickle_plugin: IoAdapterPickle
        @param io_adapter_pickle_plugin: Input output adapter pickle plugin.
        """

        self.io_adapter_pickle_plugin = io_adapter_pickle_plugin

    def load(self, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the pickle source specified in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided intermediate structure.
        """

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["file_path"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_pickle_exceptions.IoAdapterPickleOptionMissing("IoAdapterPickle.load - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        file_path = options["file_path"]

        # raises and exception in case the specified file does not exist
        if not os.path.exists(file_path):
            raise io_adapter_pickle_exceptions.IoAdapterPickleOptionInvalid("IoAdapterPickle.load - Specified file to load intermediate structure from does not exist (file_path = %s)" % file_path)

        # loads intermediate structure from the specified file
        storage_file = open(file_path, "r")
        intermediate_structure.entities, intermediate_structure.store_map, intermediate_structure.index_map = pickle.load(storage_file)
        storage_file.close()

    def save(self, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in pickle format at the location and with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure into pickle format.
        """

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["file_path"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_pickle_exceptions.IoAdapterPickleOptionMissing("IoAdapterPickle.save - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        file_path = options["file_path"]

        # serializes the intermediate structure
        storage_file = open(file_path, "w")
        pickle.dump((intermediate_structure.entities, intermediate_structure.store_map, intermediate_structure.index_map), storage_file)
        storage_file.close()
