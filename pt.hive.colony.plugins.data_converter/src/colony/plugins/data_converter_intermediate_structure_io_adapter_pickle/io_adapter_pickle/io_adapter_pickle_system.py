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

        self.io_adapter_pickle_plugin.logger.info("Loading intermediate structure with pickle io adapter")

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
        unpickler = pickle.Unpickler(storage_file)
        unpickler.persistent_load = self.get_persistent_object
        intermediate_structure.entities, intermediate_structure.entity_name_entities_map, intermediate_structure.index_entity_map = unpickler.load()
        storage_file.close()

    def save(self, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in pickle format at the location and with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure into pickle format.
        """

        self.io_adapter_pickle_plugin.logger.info("Saving intermediate structure with pickle io adapter")

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["file_path"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_pickle_exceptions.IoAdapterPickleOptionMissing("IoAdapterPickle.save - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        file_path = options["file_path"]

        # serializes the intermediate structure
        storage_file = open(file_path, "w")
        pickler = pickle.Pickler(storage_file)
        pickler.persistent_id = self.get_persistent_object_id
        pickler.dump((intermediate_structure.entities, intermediate_structure.entity_name_entities_map, intermediate_structure.index_entity_map))
        storage_file.close()

    def get_persistent_object_id(self, object):
        """
        Retrieves an identifier to replace for the object in the serialization process.

        @param object: Object that is going to be serialized by pickle.
        @rtype: str
        @return: String that will be serialized instead of the object, None in case the object itself should be serialized.
        """

        if object.__class__.__name__.endswith("Plugin"):
            return object.id + ";" + object.version

    def get_persistent_object(self, persistent_object_id):
        """
        Retrieves the object that corresponds to the serialized persistent object id.

        @type: str
        @param persistent_object_id: Identifier that was serialized instead of the object.
        @return: The object that corresponds to the persistent object id.
        """

        plugin_id, plugin_version = persistent_object_id.split(";")
        plugin = self.io_adapter_pickle_plugin.manager.get_plugin_by_id_and_version(plugin_id, plugin_version)

        return plugin
