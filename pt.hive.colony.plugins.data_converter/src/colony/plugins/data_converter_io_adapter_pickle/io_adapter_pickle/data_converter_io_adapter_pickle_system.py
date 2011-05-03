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

import os
import cPickle

import data_converter_io_adapter_pickle_exceptions

FILE_PATH_VALUE = "file_path"

class IoAdapterPickle:
    """
    Input output adapter used to serialize data converter intermediate structures to pickle binary format.
    """

    io_adapter_pickle_plugin = None
    """ Io adapter pickle plugin """

    def __init__(self, io_adapter_pickle_plugin):
        """
        Constructor of the class.

        @type io_adapter_pickle_plugin: IoAdapterPickle
        @param io_adapter_pickle_plugin: Input output adapter pickle plugin.
        """

        self.io_adapter_pickle_plugin = io_adapter_pickle_plugin

    def load_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the pickle source specified in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided intermediate structure.
        """

        # extracts the mandatory options
        file_path = options[FILE_PATH_VALUE]

        # raises and exception in case the specified file does not exist
        if not os.path.exists(file_path):
            raise data_converter_io_adapter_pickle_exceptions.IoAdapterPickleFileNotFound(file_path)

        # loads intermediate structure from the specified file
        storage_file = open(file_path, "r")
        try:
            unpickler = cPickle.Unpickler(storage_file)
            unpickler.persistent_load = self.get_persistent_object
            intermediate_structure.entities, intermediate_structure.entity_name_entities_map, intermediate_structure.index_entity_map = unpickler.load()
        finally:
            storage_file.close()

    def save_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in pickle format at the location and with characteristics defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure into pickle format.
        """

        # extracts the mandatory options
        file_path = options[FILE_PATH_VALUE]

        # serializes the intermediate structure
        storage_file = open(file_path, "w")
        try:
            # creates the pickler instance
            pickler = cPickle.Pickler(storage_file)

            # sets the pickler persistent id
            pickler.persistent_id = self.get_persistent_object_id

            # defines the pickler dump tuple
            pickler_dump_tuple = (
                intermediate_structure.entities,
                intermediate_structure.entity_name_entities_map,
                intermediate_structure.index_entity_map
            )

            # dumps the pickler dump tuple
            pickler.dump(pickler_dump_tuple)
        finally:
            storage_file.close()

    def get_persistent_object_id(self, object):
        """
        Retrieves an identifier to replace for the object in the serialization process.

        @type object: Object
        @param object: Object that is going to be serialized by pickle.
        @rtype: String
        @return: String that will be serialized instead of the object, None in case the object itself should be serialized.
        """

        pass

    def get_persistent_object(self, persistent_object_id):
        """
        Retrieves the object that corresponds to the serialized persistent object id.

        @type persistent_object_id: String
        @param persistent_object_id: Identifier that was serialized instead of the object.
        @rtype: Object
        @return: The object that corresponds to the persistent object id.
        """

        pass
