#!/usr/bin/python
# -*- coding: utf-8 -*-
# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import copy
import uuid
import time
import types
import zipfile
import tempfile
import mysql_system
import pgsql_system
import sqlite_system

import colony.base.system
import colony.libs.path_util
import colony.libs.structures_util
import colony.libs.string_buffer_util

import exceptions
import structures
import test_mocks

DEFAULT_ENCODING = "utf-8"
""" The default encoding to be used during the encoding
(serialization) of the data in the files """

ID_VALUE = "id"
""" The id value """

OPTIONS_VALUE = "options"
""" The options value """

ENTITIES_LIST_VALUE = "entities_list"
""" The entities list value """

GENERATOR_VALUE = "_generator"
""" The value that is going to be used to create (and refer)
the generator table (table name) """

FILE_ENTITY_COUNT = 8192
""" The default number of entities to be exported into a single
file using the entity manager exporting feature """

SAVED_STATE_VALUE = 1
""" The saved state value, set in the entity after the save
operation to indicate the result of the save operation """

UPDATED_STATE_VALUE = 2
""" The updated state value, set in the entity after the update
operation to indicate the result of the update operation """

REMOVED_STATE_VALUE = 3
""" The removed state value, set in the entity after the remove
operation to indicate the result of the remove operation """

RESERVED_NAMES = ("_class", "_mtime")
""" The tuple containing the names that are considered to be
reserved (special cases) for the queries """

SEQUENCE_TYPES = (types.ListType, types.TupleType)
""" The tuple containing the various sequence types """

OPTIONS_KEYS = (
    "filters",
    "names",
    "eager",
    "retrieve_eager",
    "start_record",
    "number_records",
    "order_by",
    "count",
    "fields",
    "range",
    "minimal",
    "map",
    "set",
    "entities",
    "scope",
    "sort",
    "order_names"
)
""" The list of keys that may appear in an options map """

SQL_TYPES_MAP = {
    "text" : "text",
    "string" : "varchar(255)",
    "integer" : "integer",
    "long" : "bigint",
    "float" : "double precision",
    "date" : "double precision",
    "data" : "text"
}
""" The map containing the association of the entity types with
the corresponding sql types """

class DataEntityManager(colony.base.system.System):
    """
    The data entity manager class.
    """

    entity_manager_engine_plugins_map = {}
    """ The map of entity manager engine plugins """

    loaded_entity_manager_map = {}
    """ The map associating the id with the (loaded) entity manager """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        
        self.entity_manager_engine_plugins_map = {
            "sqlite" : sqlite_system.SqliteSystem(),
            "mysql" : mysql_system.MysqlSystem(),
            "pgsql" : pgsql_system.PgsqlSystem()
        }
        self.loaded_entity_manager_map = {}

    def register_entity_manager_engine_plugin(self, entity_manager_engine_plugin):
        # retrieves the plugin engine name
        engine_name = entity_manager_engine_plugin.get_engine_name()

        # sets the entity manager engine plugin in the entity manager
        # engine plugins map
        self.entity_manager_engine_plugins_map[engine_name] = entity_manager_engine_plugin

    def unregister_entity_manager_engine_plugin(self, entity_manager_engine_plugin):
        # retrieves the plugin engine name
        engine_name = entity_manager_engine_plugin.get_engine_name()

        # removes the entity manager engine plugin from the entity manager
        # engine plugins map
        del self.entity_manager_engine_plugins_map[engine_name]

    def load_entity_manager(self, engine_name, properties = {}):
        """
        Loads an entity manager for the given engine name.
        The loading of an entity manager may return an existing
        instance in case an entity manager with the same id is
        already loaded.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @type properties: Dictionary
        @param properties: The properties to be used in the
        loading of the entity manager.
        @rtype: EntityManager
        @return: The loaded entity manager.
        """

        # tries to retrieve the id of the "target" entity manager, falling back to
        # an undefined value for the id
        id = properties.get(ID_VALUE, None)

        # retrieves the options to be used to configure the entity manager to be
        # created, these options are going to "guide" the entity manager runtime
        options = properties.get(OPTIONS_VALUE, {})

        # tries to retrieve the entities (classes) list, then generates the map
        # describing the various entities from the entities list
        entities_list = properties.get(ENTITIES_LIST_VALUE, [])
        entities_map = self._generate_class_map(entities_list)

        # in case the engine name does not exist in the entity manager
        # engine plugins map
        if not engine_name in self.entity_manager_engine_plugins_map:
            # raises the entity manager engine not found exception
            raise exceptions.EntityManagerEngineNotFound("engine " + engine_name + " not available")

        # in case the id is already defined in the loaded
        # entity manager map (no need to load the entity manager)
        if id in self.loaded_entity_manager_map:
            # prints a debug message
            self.plugin.debug("Re-loading existent entity manager with id: %s" % id)

            # retrieves the entity manager from the loaded entity
            # manager map and extends the it with the current entities
            # (classes) map, "upgrading" it to the new status
            entity_manager = self.loaded_entity_manager_map[id]
            entity_manager.extend(entities_map)

            # returns the entity manager (immediately)
            return entity_manager

        # prints a debug message
        self.plugin.debug("Loading new entity manager with engine: %s" % engine_name)

        # retrieves the entity mager engine plugin
        entity_manager_engine_plugin = self.entity_manager_engine_plugins_map[engine_name]

        # creates a new entity manager with the entity manager plugin, entity manager engine
        # plugin, (entity manager) id and the map containing the initial entities to set the
        # context for the entity manager, this action does not trigger any loading of entities
        # of any major internal structure change
        entity_manager = EntityManager(self.plugin, entity_manager_engine_plugin, id, entities_map, options)

        # in case the id of the entity manager is defined
        # (need to set the entity manager in the map)
        if id:
            # sets the entity manager in the loaded entity manager(s) map
            self.loaded_entity_manager_map[id] = entity_manager

        # returns the entity manager
        return entity_manager

    def get_entity_manager(self, id):
        """
        Retrieves the appropriate entity manager instance for the
        given (entity manager) identifier.
        In case no entity manager instance is found none is retrieved.

        @type id: String
        @param id: The identifier of the entity manager to be retrieved.
        @rtype: EntityManager
        @return: The retrieved entity manager.
        """

        # retrieves the entity manager for the given id from the
        # loaded entity manager map, sets as none if not found
        entity_manager = self.loaded_entity_manager_map.get(id, None)

        # returns the entity manager
        return entity_manager

    def get_entity_class(self):
        """
        Retrieves the top level entity class, responsible for the base
        methods to be used along all the entity classes.

        All the entities to be used in the context of the entity manager
        should inherit from this class in order to provide the appropriate
        interface for entity manager handling.

        @rtype: EntityClass
        @return: The top level entity class, responsible for the base
        methods to be used along all the entity classes.
        """

        return structures.EntityClass

    def _generate_class_map(self, class_list):
        # creates a list of tuples containing the class name
        # associated with the class itself and then uses these
        # series of tuples to construct a map with the same
        # indexing strategy (class name associated with class)
        class_tuples = [(value.__name__, value) for value in class_list]
        class_map = dict(class_tuples)

        # returns the map that associates the class name
        # with the class implementation reference
        return class_map

class EntityManager:
    """
    The entity manager class, responsible for
    the overall management of entities and
    coordination of the underlying engines.
    This class represents the overall front-end
    to the usage of the persistence layer.
    """

    entity_manager_plugin = None
    """ The entity manager plugin """

    engine = None
    """ The engine to be used in the underlying logic """

    id = None
    """ The identifier for the entity manager """

    entities_map = None
    """ The map associating the various entity class names
    with their respective entity classes """

    options = None
    """ The map containing the various options to configure
    the entity manager, these options are going to be used
    in runtime execution of the entity manager """

    connection = None
    """ The connection with the data source sub-system """

    connection_parameters = {}
    """ The map containing the set of parameters to be passed
    to the underlying engine upon the connection creation """

    _exists = {}
    """ Map for indexing of the classes that have already been persisted """

    def __init__(self, entity_manager_plugin, engine_plugin, id, entities_map, options = {}):
        """
        Constructor of the class.

        @type entity_manager_plugin: EntityManagerPlugin
        @param entity_manager_plugin: The entity manager plugin reference.
        @type engine_plugin: EntityManagerEnginePlugin
        @param engine_plugin: The engine entity manager plugin to be used.
        @type id: String
        @param id: The identifier to be used to reference the entity manager.
        @type entities_map: Dictionary
        @param entities_map: The map associating the various entity class names
        with their respective entity classes, this map is going to be used
        for resolution along the various operations.
        @type options: Dictionary
        @param options: The map containing the various options to configure
        the entity manager, these options are going to be used in runtime
        execution of the entity manager.
        """

        self.entity_manager_plugin = entity_manager_plugin
        self.engine = engine_plugin.create_engine(self)
        self.id = id
        self.entities_map = entities_map
        self.options = options

        self.connection_parameters = {}
        self._exists = {}

    def get_mock_entities(self):
        """
        Retrieves a module containing a series of test entities
        that may be used for testing of the entity manager.

        This method is very useful for fast testing of the
        entity manager in situations where defining a new model
        set is very difficult.

        @rtype: module
        @return: The module containing the set of mock entities
        that may be used for testing.
        """

        return test_mocks

    def get_entity(self, entity_name):
        """
        Retrieves the entity class reference from the given
        entity name, useful for reverse resolution.

        The method uses the current internal state of the
        entity manager (registered entities) to try to find
        the most appropriate entity class for the request.

        @type entity_name: String
        @param entity_name: The name of the entity class to
        be retrieved.
        @rtype: EntityClass
        @return: the entity class reference from the given
        entity name, reverse lookup.
        """

        return self.entities_map.get(entity_name, None)

    def get_entity_class(self):
        """
        Retrieves the top level entity class, responsible
        for the top level facade method for entities.

        All the entity classes must inherit from this class
        in order to provide the correct (and expected) facade
        of an entity class.

        @rtype: EntityClass
        @return: The top level entity class to be used in the
        inheritance of all the entity classes.
        """

        return structures.EntityClass

    def get_engine_name(self):
        """
        Retrieves the engine name for the current
        connection (using the internal engine).

        The name of the engine should be related to
        the underlying technology used.

        @rtype: String
        @return: The engine name for the current
        connection.
        """

        return self.engine.get_engine_name()

    def get_internal_version(self):
        """
        Retrieves the internal version for the current
        connection (using the internal engine).

        The internal version should represent a reference
        to the version of the underlying data source system.

        @rtype: String
        @return: The internal version for the current
        connection.
        """

        return self.engine.get_internal_version()

    def get_host(self):
        return self.engine.get_host()

    def get_database_size(self):
        """
        Retrieves an approximate measurement for the size of
        the underlying database (using the internal engine).

        This number should only represent an approximate measurement
        of the real size of the database in secondary storage.

        @rtype: int
        @return: The database size in bytes for the current
        connection (just reference number).
        """

        return self.engine.get_database_size()

    def get_connection(self):
        """
        Retrieves the current available connection.

        @rtype: Connection
        @return: The current available database connection.
        """

        # in case the current connection is not set or it's
        # closed one must be created and connected
        if self.connection == None or self.connection.is_closed():
            # creates a new connection with the specified parameters for the
            # appropriate connection handling
            self.connection = self.connection or structures.Connection({})

            # connects the connection using the engine, the connection parameters
            # are sent to provide configuration over the connection
            self.engine.connect(self.connection, self.connection_parameters)

        # returns the current connection
        return self.connection

    def close_connection(self):
        """
        Closes the current available connection.
        After the closing of the connection it becomes
        impossible to use the entity manager for persistence
        operation (connection is not available)
        """

        # in case no connection is defined or the connection
        # is closed, no need to disconnect an inexistent
        # connection (fail silently)
        if not self.connection or self.connection.is_closed():
            # returns immediately (nothing to be
            # disconnected)
            return

        # disconnects the connection using the engine
        # logic for the execution
        self.engine.disconnect(self.connection)

    def set_connection_parameters(self, connection_parameters):
        """
        Sets the connection parameters of the entity manager.
        The connection parameters are used to establish the connection
        with the data source endpoint.

        @type connection_parameters: Dictionary
        @param connection_parameters: The map containing the connection parameters,
        to be used to establish the connection with the data source endpoint.
        """

        self.connection_parameters = connection_parameters

    def import_f(self, serializer, file_path = "default.emd"):
        """
        Imports a file containing the data information in the
        "standard" entity data format (specification defined).

        The imported data will be loaded in the current data
        source "attached" in the entity manager.

        @type serializer: Serializer
        @param serializer: The serializer object to be used to
        unserialize the data (must comply with serializer interface).
        @type file_path: String
        @param file_path: the path to the file to be used for
        the importing of the data from the data file.
        """

        # creates a new temporary directory to hold the created data
        # files for the entity manager contents
        directory_path = tempfile.mkdtemp()

        try:
            # opens the container file in zip mode for
            # reading all of its contents
            zip_file = zipfile.ZipFile(file_path, "r")

            # extracts the containers file contents into the
            # temporary directory and then closes tht file
            try: zip_file.extractall(directory_path)
            finally: zip_file.close()

            # loads the information map from the meta information
            # file and then tries to retrieve the default options
            information = self._load_meta( directory_path + "/meta.json")
            full_mode = information.get("full_mode", False)
            encoding = information.get("encoding", DEFAULT_ENCODING)

            # imports the data generated from the containers file
            # that is now located in the temporary directory into
            # the currently loaded data source
            self.import_data(serializer, directory_path = directory_path + "/data", full_mode = full_mode, encoding = encoding)
            self.import_generator(serializer, directory_path = directory_path + "/data")
        finally:
            # removes the temporary directory files to avoid
            # the leaking of files (garbage collection)
            colony.libs.path_util.remove_directory(directory_path)

    def export_f(self, serializer, file_path = "default.emd", date_range = None):
        """
        Exports the current representation of the entity manager
        in the data source to a file in the "standard" entity data
        format (specification defined).

        The date range of the exported data may be "controlled"
        using the date range tuple attribute.

        The serializer attribute controls the kind of serializer
        that is going to be used in the data (json or bson are
        the recommended formats)

        @type serializer: Serializer
        @param serializer: The serializer object to be used to
        serialize the data (must comply with serializer interface).
        @type file_path: String
        @param file_path: The path to the file to be set with the
        exported data file.
        @type date_range: Tuple
        @param date_range: The range of dates as timestamp to the
        the exported data, this is going to be used to filter the
        data in the data source base on the modified time.
        """

        # retrieves the json plugin reference
        json_plugin = self.entity_manager_plugin.json_plugin

        # creates a new temporary directory to hold the generated data
        # files for the entity manager contents
        directory_path = tempfile.mkdtemp()

        try:
            # exports the current (complete) set of data in the entity
            # manager to the temporary directory and for the defined
            # data range, then list the directory to get the references
            # to all the data files contained there
            self.export_data(serializer, directory_path = directory_path, date_range = date_range)
            self.export_generator(serializer, directory_path = directory_path, date_range = date_range)
            file_names = os.listdir(directory_path)

            # opens the (target) file path in zip mode, this is going to
            # be the final container file containing the complete set
            # of entities (includes also the meta data information)
            zip_file = zipfile.ZipFile(file_path, "w", compression = zipfile.ZIP_DEFLATED)

            try:
                # iterates over all the file names in the directory to add
                # them to the container file
                for file_name in file_names:
                    # joins the directory path with the file name to get
                    # the complete file path then adds it to the container
                    # file under the data directory
                    file_path = os.path.join(directory_path, file_name)
                    zip_file.write(file_path, "data/" + file_name)

                # creates the meta information map containing some general
                # information about the contents present in the container file
                information = {
                    "type" : "json",
                    "entities" : [entity_name for entity_name in self.entities_map],
                    "time" : time.time(),
                    "range" : date_range,
                    "encoding" : DEFAULT_ENCODING
                }

                # dumps the information structure using the json serializer
                # to serialize its data
                information_data = json_plugin.dumps_pretty(information)

                # creates the zip info structure to hold the meta file entry
                # information for the meta information and then adds it to
                # the zip file
                zip_info = zipfile.ZipInfo("meta.json")
                zip_file.writestr(zip_info, information_data)
            finally:
                # closes the zip file so that no file information
                # is leaked by the system
                zip_file.close()
        finally:
            # removes the temporary directory files to avoid
            # the leaking of files (garbage collection)
            colony.libs.path_util.remove_directory(directory_path)

    def import_data(self, serializer, entity_classes = None, directory_path = None, full_mode = False, include_parents = False, encoding = DEFAULT_ENCODING):
        """
        Imports data encoded with the expected serializer input
        into the data source associated with the current entity
        manager.

        The set of entity classes to be used during the import
        may be controlled with the provided list, if not provided
        the complete set of entity registered in the entity
        manager is used.

        An optional full mode option may be set if the intended
        behavior is that of importing all the parent names of
        the entity class (no cls names usage).

        An optional include parents mode may be set if the parent
        classes of the entity classes should be included.

        @type serializer: Serializer
        @param serializer: The serializer object to be used for
        serialization of the data.
        @type entity_classes: List
        @param entity_classes: The list of entity classes to be
        imported (the file prefix to be searched).
        @type directory_path: String
        @param directory_path: The path to the directory to be used
        for searching for the entity data files.
        @type full_mode: bool
        @param full_mode: If the full mode (parent names mode)
        should be used in the importing process.
        @type include_parents: bool
        @param include_parents: If the parent classes should be
        automatically ensured in the entities list.
        @type encoding: String
        @param encoding: The encoding to be used for decoding
        the data files.
        """

        # retrieves the plugin manager reference
        plugin_manager = self.entity_manager_plugin.manager

        # sets the directory path as the temporary plugin manager path
        # in case none is specified (default behavior)
        directory_path = directory_path or plugin_manager.get_temporary_path()

        # retrieves the entity classes from the current entities map
        # (complete export) in case no entity classes are defined
        # for export, then ensures that the parents are in the list in
        # case the include parents flag is set (this allows the class
        # hierarchy to be exported avoiding data corruption problems)
        entity_classes = entity_classes or self.entities_map.values()
        entity_classes = include_parents and self._ensure_parents(entity_classes) or entity_classes

        # iterates over the complete set of entity classes to try to
        # import them into the current workspace
        for entity_class in entity_classes:
            # in case the current entity class is of type
            # abstract (no need to proceed with import)
            if entity_class.is_abstract(): continue

            # retrieves the name for the current entity
            # class, this should be the prefix to the
            # file with the entity exports
            entity_name = entity_class.get_name()

            # starts the file index counter, this value
            # is going to be used to iterate over the
            # various files of the entity
            file_index = 0

            # iterates continuously to import the complete set
            # of entity classes (all files imported)
            while True:
                # creates the file path for the current entity file
                # (using the current file index) then joins it with
                # the current directory path to retrieve the complete
                # file path
                file_path = entity_name + "_" + str(file_index) + ".dat"
                file_path = os.path.join(directory_path, file_path)

                # in case the file path does no exists, the
                # current entity class is completely imported
                # (no more files to be processed)
                if not os.path.exists(file_path): break

                # opens the file in the source file path
                # (this is the partial contents file)
                file = open(file_path, "rb")

                # reads the data from the source file, this
                # data is in the serialized form, then closes
                # the file avoiding any possible leaking
                try: data = file.read()
                finally: file.close()

                # decodes the data using the encoding defined
                # for the data files, in case one is defined
                data = encoding and data.decode(encoding) or data

                # imports the entities contained in the current data
                # buffer into the the data source associated with the
                # current entity manager instance
                self._import_class(entity_class, serializer, data, full_mode)

                # increments the file index value to "jump"
                # to the next entity file
                file_index += 1

    def export_data(self, serializer, entity_classes = None, directory_path = None, date_range = None, entity_count = FILE_ENTITY_COUNT, include_parents = False):
        """
        Exports entities from the current entity manager into
        a data file structure defined by the provided serializer
        object (must comply with the serializer interface).

        The set of entity classes to be used during the export
        may be controlled with the provided list, if not provided
        the complete set of entity registered in the entity
        manager is used.

        An optional entity count argument may be provided to
        control the amount of entities export by each file.

        An optional include parents mode may be set if the parent
        classes of the entity classes should be included.

        @type serializer: Serializer
        @param serializer: The serializer object to be used for
        serialization of the data.
        @type entity_classes: List
        @param entity_classes: The list of entity classes to be
        imported (the file prefix to be searched).
        @type directory_path: String
        @param directory_path: The path to the directory to be used
        for outputting for the entity data files.
        @type date_range: Tuple
        @param date_range: The range of dates (as timestamp) for the
        interval to be used for data retrieval, in case one of the
        limits is as none it's considered to be open.
        @type entity_count: int
        @param entity_count: The number of entities to be written
        in each of the files representing the entity class.
        @type include_parents: bool
        @param include_parents: If the parent classes should be
        automatically ensured in the entities list.
        """

        # retrieves the plugin manager reference
        plugin_manager = self.entity_manager_plugin.manager

        # sets the directory path as the temporary plugin manager path
        # in case none is specified (default behavior)
        directory_path = directory_path or plugin_manager.get_temporary_path()

        # retrieves the entity classes from the current entities map
        # (complete export) in case no entity classes are defined
        # for export, then ensures that the parents are in the list in
        # case the include parents flag is set (this allows the class
        # hierarchy to be exported avoiding data corruption problems)
        entity_classes = entity_classes or self.entities_map.values()
        entity_classes = include_parents and self._ensure_parents(entity_classes) or entity_classes

        # creates the set of filters that may be used to limit
        # the current find query to the given date range then
        # in case they are valid adds them to the options map
        filters = self._create_range_filters(date_range)
        options = filters and {"filters" : filters} or None

        # iterates over all the entity classes to serializes them and
        # store them in the appropriate data files in the target
        # directory (serialization is done in parts using the file
        # entity count parameter)
        for entity_class in entity_classes:
            # in case the current entity class is of type
            # abstract (no need to proceed with export)
            if entity_class.is_abstract(): continue

            # counts the number of entities present in the data source
            # for the current entity class being evaluated, this value
            # is going to be used in the calculates for the distribution
            # of the entities over the various data files
            count = self.count(entity_class, options)

            # calculates the integer file count value from
            # the integer division on the (entity) count and the
            # the file entity count parameter then used the modulus
            # of the operation to get the remaining values
            file_count = count / entity_count
            remain = count % entity_count

            # calculates the total file count, taking into account that
            # if the remain is zero no increment is done to the (original)
            # file count (integer division) value
            total_file_count = remain and file_count + 1 or file_count

            # retrieves the (table) name of the current entity, this
            # is going to be used to create the appropriate file name
            # for the entity exporting
            entity_name = entity_class.get_name()

            # iterates over the range of the partial files to be used
            # in the exporting of the complete class
            for _index in range(total_file_count):
                # creates the start record from the current index and the
                # current file entity count (per block) the calculates the
                # the number of records for the current range from the file
                # count (in case it's the last index) or from the file entity
                # count in case it's any other index, after that creates the
                # range tuple using both the start record and the number of
                # record (going to be used in to guide the exporting of the class)
                start_record = _index * FILE_ENTITY_COUNT
                number_records = _index == file_count and remain or FILE_ENTITY_COUNT
                _range = (start_record, number_records)

                # exports the current entity class in the current range, this
                # call should return a string containing the serialized data
                data = self._export_class(entity_class, serializer, range = _range, filters = filters)

                # creates the base file path using the entity name the
                # the current (file) index and the appropriate extension
                # and then creates the full file path "joining" the base
                # file path to the directory path
                file_path = entity_name + "_" + str(_index) + ".dat"
                file_path = os.path.join(directory_path, file_path)

                # opens the file in the target file path
                # (this is the partial contents file)
                file = open(file_path, "wb")

                # writes the data contents into the file
                # (flushes the current data), then closes
                # the file avoiding any possible leaking
                try: file.write(data)
                finally: file.close()

    def import_generator(self, serializer, directory_path = None):
        # retrieves the plugin manager reference
        plugin_manager = self.entity_manager_plugin.manager

        # sets the directory path as the temporary plugin manager path
        # in case none is specified (default behavior)
        directory_path = directory_path or plugin_manager.get_temporary_path()

        # creates the file path for the generator using the
        # default (and previously defined) file name then
        # joins it with the current directory path to retrieve
        # the complete file path for the generator
        file_path = os.path.join(directory_path, "_generator.dat")

        # in case the file containing the generator data does
        # not exists returns immediately (nothing to import)
        if not os.path.exists(file_path): return

        # opens the file in the source file path
        # (this is the complete contents file)
        file = open(file_path, "rb")

        # reads the data from the source file, this
        # data is in the serialized form, then closes
        # the file avoiding any possible leaking
        try: data = file.read()
        finally: file.close()

        # imports the (generator) entities contained in the
        # current data buffer into the the data source
        # associated with the current entity manager instance
        self._import_generator(serializer, data)

    def export_generator(self, serializer, directory_path = None, date_range = None):
        # retrieves the plugin manager reference
        plugin_manager = self.entity_manager_plugin.manager

        # sets the directory path as the temporary plugin manager path
        # in case none is specified (default behavior)
        directory_path = directory_path or plugin_manager.get_temporary_path()

        # exports the generator entities, this call should return a
        # string containing the serialized data
        data = self._export_generator(serializer, date_range = date_range)

        # creates the base file path using the default and previously
        # defined generator file name then creates the full file path
        # "joining" the base file path to the directory path
        file_path = os.path.join(directory_path, "_generator.dat")

        # opens the file in the target file path
        # (this is the complete contents file)
        file = open(file_path, "wb")

        # writes the data contents into the file
        # (flushes the current data), then closes
        # the file avoiding any possible leaking
        try: file.write(data)
        finally: file.close()

    def open(self, start = True):
        # retrieves the connection, ensuring that
        # at least one connection pool is available
        # for communication with the data source
        self.get_connection()

        # starts the current entity manager initializing
        # all the current internal and external data structure
        # this will imply data source access (slow operation)
        start and self.start()

    def close(self):
        self.stop()
        self.close_connection()

    def start(self):
        # begins the transaction that will start
        # all the internal and external structures
        # associated with the current entity manager
        self.begin()

        try:
            # creates the definition for all the currently
            # available classes this will ensure the definition
            # of the various entity classes on the data source,
            # after it creates the generator table
            self.create_definitions()
            self.create_generator()
        except:
            # "rollsback" the current transaction (something failed)
            # and re-raises the exception for upper except
            self.rollback()
            raise
        else:
            # commits the current transaction, flushing the data to
            # the current data source (data persistence)
            self.commit()

    def stop(self):
        pass

    def destroy(self):
        self.engine.destroy()
        self._reset_exists()

    def begin(self):
        self.engine.begin()

    def commit(self):
        self.engine.commit()

    def rollback(self):
        self.engine.rollback()

    def lock(self, entity_class, id_value = None, lock_parents = True):
        self.engine.lock(entity_class, id_value, lock_parents)

    def lock_table(self, table_name, parameters):
        self.engine.lock_table(table_name, parameters)

    def extend(self, entities_map):
        # iterates over all the entity classes to be registered to add
        # them to the current internal structures (taking into account
        # a possible garbage collection)
        for entity_name, entity_class in entities_map.items():
            # checks if the entity class already exists (registered) in the
            # entity manager (garbage collection required)
            entity_exists = entity_name in self.entities_map

            # in case the entity classes exists (reloading case),
            # runs garbage collection strategy
            if entity_exists:
                # prints a warning message (for the duplicate entity loading)
                self.entity_manager_plugin.warning("Duplicate entity class '%s' in '%s' possible overlapping" % (entity_name, self.id))

            # adds the entity class for the current entity
            # name to the entities map (entity registering)
            self.entities_map[entity_name] = entity_class

    def shrink(self, entities_map):
        # iterates over all the entity classes to be unregistered to remove
        # them from the current internal structures (taking into account
        # a possible garbage collection)
        for entity_name in entities_map:
            # removes the entity name reference from the
            # entities map (entity unregistering)
            del self.entities_map[entity_name]

    def extend_module(self, module):
        # retrieves all the entities (ordered in a map) for
        # the current module (loading all symbols inheriting
        # from the entity class)
        entities_map = self._get_entities_map(module)

        # extends the current entity manager with the
        # valid entity class symbols found in the the
        # current target module
        self.extend(entities_map)

    def shrink_module(self, module):
        # retrieves all the entities (ordered in a map) for
        # the current module (loading all symbols inheriting
        # from the entity class)
        entities_map = self._get_entities_map(module)

        # shrinks the current entity manager with the
        # valid entity class symbols found in the the
        # current target module
        self.shrink(entities_map)

    def create(self, entity_class):
        # in case the entity class to be created is abstract there is
        # no need to create it (no data source definition required)
        if entity_class.is_abstract(): self._exists[entity_class] = True; return

        # retrieves the parent classes of the entity class
        # to be able to check if they are already defined
        # in the data source
        parent_classes = entity_class.get_parents()

        # iterates over all the parent classes of the
        # entity class to check (and create if necessary)
        # the entity definition
        for parent_class in parent_classes:
            # in case the entity class definition
            # already exists (no need to create it
            # on the data source)
            if self.exists(parent_class):
                # continues the loop (no creation
                # required)
                continue

            # creates the parent (entity) class in
            # the data source
            self.create(parent_class)

        # ensures (makes sure) that the target class is defined
        # creates the entity definition in the data source in
        # case it's necessary
        self.ensure_definition(entity_class)

        # creates the (indirect) relations definitions for the
        # current entity class in the data source
        self.create_relations(entity_class)

        # updates the cache value of the entity
        # class to the exists value (fast access)
        self._exists[entity_class] = True

    def validate_relation(self, entity, relation_name):
        # retrieves the entity class associated with
        # the current entity to be used to access class
        # level methods
        entity_class = entity.__class__

        # retrieves the target entity from the entity using
        # the relation name and the normal value retriever
        target_entity = entity.get_value(relation_name)

        # in case the target entity is not defined must
        # return immediately, because it's not possible
        # to validate an unset relation
        if not target_entity: return False

        # retrieves the target id value and the is to many
        # flag validation to be used in the unpacking of the
        # result (in case it's to many a list must be considered)
        is_to_many = entity_class.is_to_many(relation_name)
        table_id_value = entity.get_id_value()

        # retrieves extracts the entity class from the target
        # entity to retrieve the id field name, finally retrieves
        # the value of the identifier from the entity instances
        # (in case it's a to many relations the target id value is
        # not a single value but a sequence of values)
        target_entity_class = is_to_many and target_entity[0].__class__ or target_entity.__class__
        target_id = target_entity_class.get_id()
        target_id_value = is_to_many and [value.get_id_value() for value in target_entity] or target_entity.get_id_value()

        # creates the option map for the retrieval of the target
        # value with the current relation loaded and filtering
        # it based on the target id name and the target id value
        # also sets the minimal flag for faster retrieval
        options = {
            "eager" : {
                relation_name : {
                    target_id : target_id_value
                }
            },
            "minimal" : True
        }

        # tries to retrieve the entity from the data source, making
        # sure that the relation is retrieved using the filter on
        # the identifier of the relation, in case no objects are
        # retrieved it's considered to be an invalid relation
        result_entity = self.get(entity_class, table_id_value, options)
        if not result_entity: return False

        # retrieves the result (relation) value to be checked for
        # coherence and presence
        result_value = result_entity.get_value(relation_name)

        # checks the the result value for coherence in case it's a
        # to many relation the resulting list must contain at least
        # the relation values to be checked
        if is_to_many:
            # creates the bitmap of identifier values for the retrieved
            # relation (result) values, it's going to be used in the
            # identifier validation step
            result_map = dict([(value.get_id_value(), None) for value in result_value])

            # sets the relation as valid by default in case an identifier
            # validation fails it will be set as not valid
            valid_relation = True

            # iterates over all the retrieved target entities and validates
            # if their identifier values match any of the values present
            # in the resulting map (in case the identifier is not set it's
            # "automatically" considered valid, no validation required/possible)
            for _target_entity in target_entity:
                # retrieves the current target entity identifier value to be used
                # for validation in the result map
                id_value =  _target_entity.get_id_value()

                # continues the loop, the entity does not contains
                # an identifier value (not persisted) or the entity
                # is present in results map (association valid)
                if id_value == None or id_value in result_map: continue

                # unsets the valid relation flag
                # and breaks the loop (validation failed)
                valid_relation = False
                break

        # otherwise a single a checking is required and the
        # a comparison of the target entity identifier and
        # the result value identifier is "enough"
        else: valid_relation = target_entity.get_id_value() == result_value.get_id_value()

        # returns the boolean (flag) result for the relation validation
        # (in case the relation is valid extra security is present)
        return valid_relation

    def create_definitions(self):
        """
        Creates the complete set of definitions for the
        various entities classes currently defined in the
        entity manager.

        This process should be able to verify the integrity
        of the current data source and update it accordingly.
        """

        # iterates over all the entities contained in the
        # entities map to create the references in the data
        # source (required for entity manager usage)
        for _entity_name, entity_class in self.entities_map.items():
            # creates the definition of the entity class
            # in the currently associated data source
            self.create(entity_class)

    def ensure_definition(self, entity_class):
        """
        Ensures the "correct" definition of the entity class
        schema in the data source.

        This process may evolve the creation of the entity mode
        in the data sources (slow).

        @type entity_class: EntityClass
        @param entity_class: The class to be ensured for definition
        in the data source.
        """

        # in case the exists flag is already "cached" in the current
        # exists indexing map
        if entity_class in self._exists:
            # returns immediately no need to
            # create the definition
            return

        # in case the entity class already has a definition
        # of it in the data source, no creation required
        if self.has_definition(entity_class):
            # returns immediately no need to
            # create the definition
            return

        # creates the entity class definition in the data source
        # this process may take some time (expensive operation)
        self.create_definition(entity_class)

        # indexes the various fields of the entity class to be
        # sets as indexed in the data source (for fast access)
        self.index_fields(entity_class)

    def create_relations(self, entity_class):
        """
        Creates the (indirect) relations associative tables, so that
        an indirect relation may be mapped in runtime.

        This operation should be avoided to duplicate, in that case
        and exception will be raised from the data source.

        @type entity_class: EntityClass
        @param entity_class: The entity class to be used in he creation
        of the indirect relations associative tables.
        """

        # retrieves the ensure integrity option that should "request"
        # if a data source level integrity must be done or if the data
        # should only be checked at the entity manger level
        ensure_integrity = self.options.get("ensure_integrity", False)

        # retrieves the table name and if associated with the entity
        # class and then retrieves the table id value (description)
        # for relation description analysis
        table_name = entity_class.get_name()
        table_id = entity_class.get_id()
        table_id_value = getattr(entity_class, table_id)

        # retrieves the current table type (table id type) for the
        # construction of the relation table (for indirect relations)
        table_type = SQL_TYPES_MAP[table_id_value.get("data_type", "integer")]

        # retrieves the complete set of indirect relations for the
        # current entity class, the list is going to be used during
        # the creation of the various association (relation) tables
        indirect_relations = entity_class.get_indirect_relations()

        # iterates over all the indirect relations to create the
        # association table for them, this is query construction
        for indirect_relation in indirect_relations:
            # retrieves the relation unique value that is going to
            # be used as the name for the association table representing
            # the current indirect relation
            relation_unique = entity_class.get_relation_unique(indirect_relation)

            # in case the exists flag is already "cached" in the current
            # exists indexing map
            if relation_unique in self._exists:
                # continues the loop no need to create an existent
                # relation table
                continue

            # in case the association (table) is already deifined in the
            # current context no need to recreate it
            if self.engine.has_table_definition(relation_unique):
                # updates the cache value of the relation
                # unique to the exists value (fast access)
                self._exists[relation_unique] = True

                # continues the loop no need to create an existent
                # relation table
                continue

            # retrieves the target class for the current indirect relation
            # from the class it will be possible to extract the information
            # to create the other side (foreign key) of the association table
            target_class = entity_class.get_target(indirect_relation)

            # ensures (makes sure) that the target class is defined
            # in the data source (avoids problems defining foreign keys)
            ensure_integrity and self.ensure_definition(target_class)

            # retrieves the target name id and value (definition) from the
            # target class to construct the "target" side of the relation
            target_name = target_class.get_name()
            target_id = target_class.get_id()
            target_id_value = getattr(target_class, target_id)

            # retrieves the associated sql (data) type for the type
            # of the (target) table id attribute (foreign key)
            target_type = SQL_TYPES_MAP[target_id_value.get("data_type", "integer")]

            # creates the buffer to hold the query and populates it with the
            # base values of the query (base creation of the table)
            query_buffer = colony.libs.string_buffer_util.StringBuffer()
            query_buffer.write("create table ")
            query_buffer.write(relation_unique)
            query_buffer.write("(")
            query_buffer.write(table_name)
            query_buffer.write(" ")
            query_buffer.write(table_type)
            query_buffer.write(", ")
            query_buffer.write(target_name)
            query_buffer.write(" ")
            query_buffer.write(target_type)
            query_buffer.write(", ")
            query_buffer.write("constraint %s_pk primary key(%s, %s)" % (relation_unique, table_name, target_name))

            # in case the ensure integrity flag is set the foreign keys for
            # the external referencing fields must be created, this requires
            # the data source definition for the references to be created
            if ensure_integrity:
                query_buffer.write(", ")
                query_buffer.write("constraint %s_%s_fk foreign key(%s) references %s(%s)" % (relation_unique, table_name, table_name, table_name, table_id))
                query_buffer.write(", ")
                query_buffer.write("constraint %s_%s_fk foreign key(%s) references %s(%s)" % (relation_unique, target_name, target_name, target_name, target_id))

            # writes the final separator into the query buffer, end of query
            query_buffer.write(")")

            # retrieves the "final" query value from
            # the query (string) buffer and executes
            # the query creating the associative table
            # definition
            query = query_buffer.get_value()
            self.execute_query(query)

            # creates the indexes for the two foreign key field and executes
            # them creating both indexes
            query = self.engine._table_index_query(relation_unique, table_name, "hash")
            self.execute_query(query)
            query = self.engine._table_index_query(relation_unique, target_name, "hash")
            self.execute_query(query)

            # updates the cache value of the relation
            # unique to the exists value (fast access)
            self._exists[relation_unique] = True

    def delete_relations(self, entity_class):
        """
        Deletes all the (indirect) relations definitions
        of an entity class.

        This method should end up by removing all the associative
        table definitions.

        @type entity_class: EntityClass
        @param entity_class: The entity class to have the indirect
        relations removed.
        """

        # retrieves all the indirect relation of an entity class
        # to used them to remove their (table) definition
        indirect_relations = entity_class.get_indirect_relations()

        # iterates over all the indirect relations to remove their
        # table definition
        for indirect_relation in indirect_relations:
            # retrieves the relation unique name, that must be
            # the association table name
            relation_unique = entity_class.get_relation_unique(indirect_relation)

            # checks if the association table is defined in the
            # data source, in case it's not no need to delete it
            if not self.engine.has_table_definition(relation_unique):
                # continues the loop, no need
                # to remove a inexistent table
                continue

            # creates the buffer to hold the query and populates it with the
            # base values of the query (base altering of the table)
            query_buffer = colony.libs.string_buffer_util.StringBuffer()
            query_buffer.write("drop table ")
            query_buffer.write(relation_unique)

            # retrieves the "final" query value from
            # the query (string) buffer and executed
            # the query deleting the associative table
            # definition
            query = query_buffer.get_value()
            self.execute_query(query)

    def delete_contraints(self, entity_class):
        """
        Deletes the various foreign key constraints created
        by the direct relation associated with the entity
        class.

        This method does not delete the foreign keys of
        invisible relations (relations no defined in the current
        side of the entity class).

        @type entity_class: EntityClass
        @param entity_class: The entity class to have it's constraints
        removed from the associated direct relations
        """

        # in case the underlying engine does not support
        # the dropping of values in the alter statement
        # it's not possible to execute the constraint delete
        if not self.engine._allow_alter_drop():
            # returns immediately, not possible
            # to delete the constraints
            return

        # retrieves the various direct relations from the entity
        # class to remove the foreign keys they "contain"
        direct_relations = entity_class.get_direct_relations()

        # iterates over all the direct relations to remove
        # the foreign keys definition
        for direct_relations in direct_relations:
            # retrieves the target class of the relation and
            # then retrieves the target (table) name
            target_class = entity_class.get_target(direct_relations)
            target_name = target_class.get_name()

            # checks if the direct relation is defined in the
            # data source, in case it's not no need to alter it
            if not self.has_definition(target_class):
                # continues the loop, no need
                # to alter an inexistent class
                continue

            # retrieves the reverse name of the relation to be
            # used in the construction of the foreign key name
            reverse = entity_class.get_reverse(direct_relations)

            # creates the complete name of the foreign key from the
            # target name the reverse value of the relation and
            # the (typical) foreign key suffix
            foreign_key_name = target_name + "_" + reverse + "_fk"

            # creates the buffer to hold the query and populates it with the
            # base values of the query (base altering of the table)
            query_buffer = colony.libs.string_buffer_util.StringBuffer()
            query_buffer.write("alter table ")
            query_buffer.write(target_name)
            query_buffer.write(" drop constraint ")
            query_buffer.write(foreign_key_name)

            # retrieves the "final" query value from
            # the query (string) buffer and executes
            # the query altering the contents of the
            # table, removing the foreign keys
            query = query_buffer.get_value()
            self.execute_query(query)

    def delete(self, entity_class):
        """
        Deletes the entity class references from the data
        source, this process include a (semi) cascading
        heuristics to disable foreign keys from pointing
        entities.

        There is one major problem with the delete approach
        in an engine with no support for cascading the delete
        may fail if an invisible or one sided direct relation
        exists, because the foreign key constraint was not
        removed.

        @type entity_class: EntityClass
        @param entity_class: The entity class to be removed from
        the data source, include (semi) cascading.
        """

        # in case the entity class definition does not (already)
        # exists in the data source no need to delete it
        if not self.has_definition(entity_class):
            # returns immediately
            return

        # deletes the various constraints present in
        # the direct relations to the entity manager
        self.delete_contraints(entity_class)

        # deletes the various indirect relations (association
        # table) "pointing" to the entity class
        self.delete_relations(entity_class)

        # deletes the definition of the entity class
        # in the data source
        self.delete_definition(entity_class)

        # updates the cache value of the entity
        # class to the not exists value (fast access)
        self._exists[entity_class] = False

        # retrieves all the direct relations of the entity
        # class to delete them from the data source
        direct_relations = entity_class.get_direct_relations()

        # iterates over all the direct relations, relations
        # that are mapped in the other side of the relation
        # to drop their entities (required for integrity)
        for direct_relation in direct_relations:
            # retrieves the target class of the direct relation
            # and deletes it from the data source
            target_class = entity_class.get_target(direct_relation)
            self.delete(target_class)

    def sync(self, entity_class):
        # retrieves the parent classes of the entity class
        # to be able to check if they are already "synced"
        # in the data source
        parent_classes = entity_class.get_parents()

        # iterates over all the parent classes of the
        # entity class to check (and "syncs" if necessary)
        # the entity definition
        for parent_class in parent_classes:
            # in case the entity class definition
            # is already "synced" (no need to sync it
            # on the data source)
            if self.synced(parent_class):
                # continues the loop (no creation
                # required)
                continue

            # "syncs" the parent (entity) class in
            # the data source
            self.sync(parent_class)

        # in case the entity class definition is (already)
        # "synced" in the data source no need to sync it
        if self.synced_definition(entity_class):
            # returns immediately
            return

        # "syncs" the definition of the entity class
        # in the data source
        self.sync_definition(entity_class)

    def exists(self, entity_class):
        """
        Checks if the given entity class, and all of its
        parent classes are already defined in the current
        data source being used.

        @type entity_class: EntityClass
        @param entity_class: The class to be checked for definition
        in the current data source.
        @rtype: bool
        @return: The result of the test for entity class definition.
        """

        # in case the exists flag is already "cached" in the current
        # exists indexing map
        if entity_class in self._exists:
            # returns the cached exists value from the
            # exists indexing map
            return self._exists[entity_class]

        # retrieves the parent classes of the entity class
        # to be able to check if they are already defined
        # in the data source
        parent_classes = entity_class.get_parents()

        # iterates over all the parent classes of the
        # entity class to check (and create if necessary)
        # the entity definition
        for parent_class in parent_classes:
            # in case the parent class (already)
            # exists (skips to the next test)
            if self.exists(parent_class):
                # continues the loop for more
                # entity existence testing
                continue

            # returns false, at least one
            # parent entity class is not defined
            return False

        # in case there is no definition of the entity
        # class in the data source
        if not self.has_definition(entity_class):
            # returns false the current entity class
            # is not defined in the data source
            return False

        # in case there is no definition of the (indirect)
        # entity relations in the data source
        if not self.has_relations_definition(entity_class):
            # returns false the entity class indirect
            # relations have not been defined in the data source
            return False

        # sets the exists flag for the entity class
        # this values is used as cache for fast
        # value retrieval in later accesses
        self._exists[entity_class] = True

        # returns valid (definition exists)
        return True

    def has_definition(self, entity_class):
        """
        Lower level function that verifies that the given
        entity class is defined in the underlying data
        source.

        @type entity_class: EntityClass
        @param entity_class: The entity class that's going
        to be verified to be defined in the data source.
        @rtype: bool
        @return: The result of the entity definition test.
        """

        return self.engine.has_definition(entity_class)

    def has_relations_definition(self, entity_class):
        # retrieves all the indirect relations (non mapped relations)
        # for the current entity class, to check for their
        # relations table
        indirect_relations = entity_class.get_indirect_relations()

        # iterates over all the indirect relation, to make
        # sure that the relation table is defined in the data source
        for indirect_relation in indirect_relations:
            # retrieves the relation unique value, this is the name
            # of the relation table for the current indirect relation
            relation_unique = entity_class.get_relation_unique(indirect_relation)

            # makes sure that the relation table is defined in the
            # data source, in case of failure continues with return
            if self.engine.has_table_definition(relation_unique):
                # continues the loop, validated
                continue

            # returns invalid (not all
            # relations are defined)
            return False

        # returns valid (all relations
        # are defined)
        return True

    def has_table_definition(self, table_name):
        return self.engine.has_table_definition(table_name)




    def synced_definition(self, entity_class):
        return self.engine.synced_definition(entity_class)


    def has_generator(self):
        return self.engine.has_table_definition(GENERATOR_VALUE)

    def create_generator(self):
        # in case the exists flag is already "cached" in the current
        # exists indexing map
        if GENERATOR_VALUE in self._exists:
            # returns immediately, no need to create
            # a duplicated table generator
            return

        # in case the current entity manager context
        # data source already contains a generator
        # the generation must be avoided
        if self.has_generator():
            # updates the cache value of the generator
            # to the exists value (fast access)
            self._exists[GENERATOR_VALUE] = True

            # returns immediately, no need to create
            # a duplicated table generator
            return

        query, index_queries = self._create_generator_query()
        self.execute_query(query)
        self.execute_query(index_queries)

        # updates the cache value of the generator
        # to the exists value (fast access)
        self._exists[GENERATOR_VALUE] = True

    def grab_id(self, name):
        next_id = self.increment_id(name)
        current_id = next_id - 1
        return current_id

    def next_id(self, name):
        query = self._next_id_query(name)
        cursor = self.execute_query(query, False)
        try: next_id = self._next_id_result(cursor)
        finally: cursor.close()
        return next_id

    def increment_id(self, name):
        query, next_id = self._increment_id_query(name)
        self.execute_query(query)
        return next_id

    def create_definition(self, entity_class):
        # generates the create definition query, general
        # sql query for the current context and then
        # executes it in the appropriate engine, the methods
        # also creates a series of index queries that are used
        # to create indexes in a series of field for fast access
        query, index_queries = self._create_definition_query(entity_class)
        self.execute_query(query)
        self.execute_query(index_queries)

    def delete_definition(self, entity_class):
        # generates the delete definition query, general
        # sql query for the current context and then
        # executes it in the appropriate engine
        query = self._delete_definition_query(entity_class)
        self.execute_query(query)

    def sync_entity_definition(self, entity_class):
        pass

    def enable(self, entity):
        # retrieves the entity class associated with the
        # current entity
        entity_class = entity.__class__

        # retrieves the id value of the current entity,
        # this value must be correctly set in this context
        id_value = entity.get_id_value()

        # sets the entity manager reference in the entity
        # (enabled data communication)
        entity._entity_manager = self

        # in case the entities map is not defined in the
        # the current entity context must return immediately
        # nothing more to be done
        if entity._entities == None: return

        # sets the entity in the entities map, first verifies
        # if the class is present and if is not creates a new
        # map to hold the various entities
        if not entity_class in entity._entities: entity._entities[entity_class] = {}
        entity._entities[entity_class][id_value] = entity

    def save(self, entity, generate = True):
        # generates all the generated attributes of the
        # entity (in case any is set to be generated)
        # this should include any generated identifier
        generate and self._generate_fields(entity)

        # generates the query for the saving operation and
        # executes it in the context for the data source
        query = self._save_query(entity)
        self.execute_query(query)

        # maps (saves) all relations for the entity that are considered
        # to be not mapped directly by the associated table
        self.map(entity)

        # enables the entity, providing the entity with the
        # mechanisms necessary for data source communication
        self.enable(entity)

        # updates the data state of the entity to saved, this
        # may be useful for consequent data usage
        entity.data_state = SAVED_STATE_VALUE

    def update(self, entity, lock = False):
        # retrieves the entity class for the entity
        # and the id value of the entity to be used
        # for the (possible) locking of the entity
        entity_class = entity.__class__
        id_value = entity.get_id_value()

        # in case the lock flag is set, locks the
        # data source for the current entity
        lock and self.lock(entity_class, id_value)

        # generates the query for the updating operation and
        # executes it in the context for the data source
        query = self._update_query(entity)
        self.execute_query(query)

        # maps (saves) all relations for the entity that are considered
        # to be not mapped directly by the associated table
        self.map(entity)

        # enables the entity, providing the entity with the
        # mechanisms necessary for data source communication
        self.enable(entity)

        # updates the data state of the entity to updated, this
        # may be useful for consequent data usage
        entity.data_state = UPDATED_STATE_VALUE

    def remove(self, entity, lock = False):
        # retrieves the entity class for the entity
        # and the id value of the entity to be used
        # for the (possible) locking of the entity
        entity_class = entity.__class__
        id_value = entity.get_id_value()

        # in case the lock flag is set, locks the
        # data source for the current entity
        lock and self.lock(entity_class, id_value)

        # generates the query for the removal operation and
        # executes it in the context for the data source
        query = self._remove_query(entity)
        self.execute_query(query)

        # enables the entity, providing the entity with the
        # mechanisms necessary for data source communication
        self.enable(entity)

        # updates the data state of the entity to removed, this
        # may be useful for consequent data usage
        entity.data_state = REMOVED_STATE_VALUE

    def save_update(self, entity, generate = True, lock = False):
        # retrieves the entity class associated with
        # the entity to be saved or updated then retrieved
        # its identifier value
        entity_class = entity.__class__
        id_value = entity.get_id_value()

        # verifies if an entity with the same identifier
        # is already persisted in the data source and then
        # saves or updates it accordingly (in case it exists
        # processes an update otherwise saves it)
        exists_entity = self.verify(entity_class, id_value)
        if exists_entity: self.update(entity, lock = lock)
        else: self.save(entity, generate = generate)

    def reload(self, entity, options = None):
        # normalizes the options, this is going to expand the
        # options map into a larger and easily accessible
        # map of values (this only happens in case the options
        # are already defined)
        options = options and self.normalize_options(options) or {}

        # retrieves the entity class associated with
        # the entity to be reloaded
        entity_class = entity.__class__

        # retrieves the map of names and the complete
        # set of relations for the entity, the first
        # is going to be used in the names population
        # of the entity and the second is going to be
        # used for the erasing of the relation values
        names_map = entity_class.get_names_map()
        all_relations = entity_class.get_all_relations()

        # retrieves the value of the identifier attribute
        # of the entity to be used for the retrieval of
        # the new entity data
        id_value = entity.get_id_value()

        # iterates over all the relations in the entity
        # to delete them (flushes relation values)
        for relation in all_relations: entity.delete_value(relation)

        # tries to retrieve the equivalent (new) entity from
        # the data source using the identifier value as the
        # "guide" for the retrieval process
        new_entity = self.get(entity_class, id_value, options)

        # iterates over all the names present in the complete
        # entity class hierarchy to update with the new values
        for name in names_map:
            # in case the current name in iteration is
            # not present in the new entity no need to
            # retrieve it and set it in the entity
            if not new_entity.has_value(name):
                # continues the loop the name is not present
                # in the new entity it's impossible to update
                # it in the entity
                continue

            # retrieves the value for the current
            # name in the new entity and sets it in
            # the entity to be reloaded (attribute update)
            value = new_entity.get_value(name)
            entity.set_value(name, value)

        # enables the entity, providing the entity with the
        # mechanisms necessary for data source communication
        self.enable(entity)

    def map(self, entity):
        """
        Maps the relations of the entity that are considered to
        be unmapped by the table associated with the entity.

        The unmapped relations include the indirect relations (association table)
        and also the relations mapped in the reverse side of the relation.

        @type entity: Entity
        @param entity: The entity to have the (unmapped) relation
        mapped in the data source.
        """

        query = self._map_query(entity)
        self.execute_query(query)

    def verify(self, entity_class, id_value):
        """
        Verifies if the entity with the given id is already present
        in the data source.

        The entity class to be used in the finding is the one provided
        to the method.

        The provided id value is flexible and may assume both a single
        representation or a tuple, in the second case the returned value
        is also a bit tuple in the same order as the provided id values.

        @type entity_class: EntityClass
        @param entity_class: The entity class to be used in the verification
        of the entity presence.
        @type id_value: Object/Tuple
        @param id_value: The if of the entity to be verified for persistence.
        @rtype: bool/Tuple
        @return: The result of the entity verification test.
        """

        query = self._verify_query(entity_class, id_value)
        cursor = self.execute_query(query, False)
        try: result = self._verify_result(entity_class, id_value, cursor)
        finally: cursor.close()
        return result

    def get(self, entity_class, id_value, options = None, lock = False):
        # normalizes the options, this is going to expand the
        # options map into a larger and easily accessible
        # map of values (this only happens in case the options
        # are already defined)
        options = options and self.normalize_options(options) or {}

        # retrieves the table id field, to be used
        # to create the appropriate equals filter
        table_id = entity_class.get_id()

        # retrieves the filters from the provided options
        # and converts it into a list to be "workable",
        # because this value should be an non manipulable tuple
        filters = list(options.get("filters", []))

        # adds the id value filtering part to the initial
        # options map provided, this is an extension to the
        # existing filters
        filters.append({
            "type" : "equals",
            "fields" : (
                {
                    "name" : table_id,
                    "value" : id_value
                },
            )
        })

        # sets the appropriate set of filters in the options
        # to be able to retrieve the exact match on the
        # identifier of the requested entity class
        options["filters"] = filters

        # in case the lock flag is set the entity class with
        # the requested id value is locked until the transaction
        # is "committed" or "rollbacked"
        lock and self.lock(entity_class, id_value)

        # "finds" the various entities that respect the created
        # options map, this should return either a list of size
        # one values or a none value and so the value must be
        # processes to the appropriate single value
        result = self.find(entity_class, options)
        result = result and result[0] or None

        # returns the processed result value
        return result

    def count(self, entity_class, options = None, lock = False):
        # normalizes the options, this is going to expand the
        # options map into a larger and easily accessible
        # map of values (this only happens in case the options
        # are already defined)
        options = options and self.normalize_options(options) or {}

        # sets the count flag in the options as true this
        # will provide access to the counting of the rows in
        # the current query
        options["count"] = True

        # "finds" the various entities that respect the created
        # options map, this should return an integer representing
        # the number of "rows" that fulfill the requirements defined
        # in the options map (simple queries with no filter and
        # no eager loading perform much faster)
        result = self.find(entity_class, options, lock)

        # returns the processed result value, number of rows
        # in the data source for the query
        return result

    def find(self, entity_class, options = {}, lock = False):
        # in case the lock flag is set the entity class with
        # is completely locked (this blocks the data source
        # information on the data for the entity class)
        lock and self.lock(entity_class)

        query, field_names = self._find_query(entity_class, options)
        cursor = self.execute_query(query, False)
        try: result = self._find_result(entity_class, field_names, options, cursor)
        finally: cursor.close()
        return result

    def execute(self, query):
        # executes the query in the current data source and
        # then retrieves the result set (all the) items
        # available for fetching and then closes the cursor
        cursor = self.execute_query(query, False)
        try: result_set = cursor.fetchall()
        finally: cursor.close()
        return result_set

    def index_fields(self, entity_class):
        """
        Indexes the various fields meant to be indexed in the
        for the provided entity class.
        These fields should be set with an appropriate decorated
        value in the model meta-information.

        The method is going to execute the queries for the creation
        of the indexed immediately during the execution.

        @type entity_class: EntityClass
        @param entity_class: The entity to be used for the indexing of
        the decorated fields.
        """

        # retrieves the name for the table associated with
        # the (current) entity class
        table_name = entity_class.get_name()

        # retrieves a list containing the field names of
        # the fields that are meant to be indexed in the
        # target data source
        indexed = entity_class.get_indexed()

        # iterates over all the indexed names to generate
        # their index queries (and generate them in the data
        # source), this should be able to create the index
        for _indexed in indexed:
            # uses the name (indexed) to retrieve the value (map)
            # containing the definition of the attribute
            indexed_value = getattr(entity_class, _indexed)

            # retrieves the set of index types to be used to create
            # the indexes on the current index field
            index_types = indexed_value.get("index_types", ("hash",))

            # iterates over all the type of indexed meant to be created
            # for the current entity class and uses them to create the
            # requested indexes
            for index_type in index_types:
                # creates the indexes for the indexed (name) fields
                # and executes the query immediately
                query = self.engine._table_index_query(table_name, _indexed, index_type)
                self.execute_query(query)

    def execute_query(self, query, close_cursor = True):
        # checks if the current engine requires the
        # the query to have its slash characters escaped
        # in such case they must be escaped
        escape_slash = self.engine._escape_slash()

        # unsets the cursor object value, the
        # original values is none to provide
        # query failure support
        cursor = None

        # retrieves the object type from the query
        query_type = type(query)

        # in case the query is a list (sequence)
        # a set of queries must be executed, in this
        # case only the last cursor is returned
        if query_type == types.ListType:
            # iterates over all the queries to be executed
            # to execute them in the underlying engine
            for _query in query:
                # in case the cursor is already defined
                # need to close it to avoid leaks
                cursor and cursor.close()

                # in case the current engine requires the slash characters
                # in the query to be escaped, escapes them accordingly
                _query = escape_slash and _query.replace("\\", "\\\\") or _query

                # executes (one more) query using the engine
                cursor = self.engine.execute_query(_query)
        # otherwise it's a "single" query
        # normal execution applies
        else:
            # in case the current engine requires the slash characters
            # in the query to be escaped, escapes them accordingly
            query = escape_slash and query.replace("\\", "\\\\") or query

            # executes the query in the engine and retrieves
            # the resulting cursor for execution
            cursor = self.engine.execute_query(query)

        # in case the close cursor flag is set
        # the cursor must be closed (avoiding leaks)
        close_cursor and cursor and cursor.close()

        # returns the cursor to be used in the query
        # execution, for data retrieval
        return cursor

    def _generate_fields(self, entity):
        """
        Generates an the various values for the given entity
        in case the entity's values must be generated using
        one of the possible strategies.

        The generated values are going to be set in the entity
        immediately after the generation of the value.

        @type entity: Entity
        @param entity: The entity to be used for values generation,
        will be changed during the value generation.
        """

        # retrieves the (entity) class associated with
        # the entity to generate the fields
        entity_class = entity.__class__

        # retrieves the map containing all the generated
        # fields associated with their respective parent
        # classes and ordered by priority
        generated_map = entity_class.get_generated_map()

        # iterates over all the generated names to generate
        # their respective values using the defined strategy
        # method (the data type of the value is dependent on
        # the associated method)
        for generated in generated_map:
            # in case the entity already has a value for the current
            # generated name no need to generate a new value, it's
            # considered to have a value if it contains a valid non
            # none value (none value is considered to be not set)
            value = entity.get_value(generated)
            if not value == None: continue

            # uses the name (generated) to retrieve the value (map)
            # containing the definition of the attribute
            generated_value = getattr(entity_class, generated)

            # retrieves the generator type from the information map
            # and then uses the generator type to retrieve the appropriate
            # generator method from the current entity instance
            generator_type = generated_value.get("generator_type", "table")
            generate_method = getattr(self, "_generate_" + generator_type)

            # generates the value using the just retrieve method for
            # the current entity context
            generate_method(entity, generated)

    def _generate_table(self, entity, name):
        # retrieves the (entity) class associated with
        # the entity to generate the value
        entity_class = entity.__class__

        # uses the name to retrieve the value (map)
        # containing the definition of the attribute
        value = getattr(entity_class, name)

        # retrieves the map containing the various entity names
        # associated with their respective classes and then
        # retrieves the entity class that "owns" the value
        names_map = entity_class.get_names_map()
        name_class = names_map[name]

        # retrieves the name of the table associated with the
        # current name and uses it to create the default field
        # name for the generation table (class name and field name)
        table_name = name_class.get_name()
        field_name = "%s_%s" % (table_name, name)

        # tries to retrieves the (generator) field name defaulting
        # to the name of the default field name, then "grabs" an id
        # value for the selected field name
        field_name = value.get("generator_field_name", field_name)
        value = self.grab_id(field_name)

        # sets the generated value in the entity, final setting
        # of the generated value
        entity.set_value(name, value)

    def _generate_uuid(self, entity, name):
        # generates a new global unique value and then sets the
        # string representation of it as the value
        uuid_value = uuid.uuid4()
        value = str(uuid_value)

        # sets the generated value in the entity, final setting
        # of the identifier value
        entity.set_value(name, value)

    def _generate_uuid_hex(self, entity, name):
        # generates a new global unique value and then sets the
        # hexadecimal string representation of it as the value
        uuid_value = uuid.uuid4()
        value = uuid_value.hex

        # sets the generated value in the entity, final setting
        # of the identifier value
        entity.set_value(name, value)

    def _create_generator_query(self):
        # creates the list to hold the various queries
        # to be used to create indexes
        index_queries = []

        # creates the create table query to be used to create
        # the generator table the table should be able to
        # associate a name with the next id value
        query = "create table %s (name char(255) primary key, next_id int, _mtime double precision)" % GENERATOR_VALUE

        # creates the indexes for the name field and adds
        # them to the list of index queries
        index_name_query = self.engine._table_index_query(GENERATOR_VALUE, "name", "hash")
        index_name_tree_query = self.engine._table_index_query(GENERATOR_VALUE, "name", "btree")
        index_queries.append(index_name_query)
        index_queries.append(index_name_tree_query)

        # creates the indexes for the modification time field and adds
        # them to the list of index queries
        index_mtime_query = self.engine._table_index_query(GENERATOR_VALUE, "_mtime", "hash")
        index_mtime_tree_query = self.engine._table_index_query(GENERATOR_VALUE, "_mtime", "btree")
        index_queries.append(index_mtime_query)
        index_queries.append(index_mtime_tree_query)

        # returns the generated (generator) definition query
        # and the list of index creation queries
        return query, index_queries

    def _next_id_query(self, name):
        # escapes the name value to avoid possible
        # security problems
        name = self._escape_text(name)

        # locks the generator table to avoid any possible
        # change in the generator during the retrieval
        # of the next id (this is a preemptive approach)
        self.lock_table(GENERATOR_VALUE, {"field_name" : "name", "field_value" : "'" + name + "'"})

        # creates the query to be used to select the next if
        # for the request name, this query should be executed
        # using a lock on the table (safe mode)
        query = "select name, next_id from " + GENERATOR_VALUE + " where name = '%s'" % name

        # returns the query generated for retrieval
        # of the next id for the requested name
        return query

    def _next_id_result(self, cursor):
        try:
            # selects all the id values for the table in the database
            # this values should be id values
            id_values = [value[1] for value in cursor]
        finally:
            # closes the cursor
            cursor.close()

        # retrieves the appropriate id value
        # according to the size of the results
        id_value = id_values and id_values[0] or None

        # returns the retrieved id value
        # (casted into a single value)
        return id_value

    def _increment_id_query(self, name):
        # retrieves the current next id value
        next_id = self.next_id(name)

        # escapes the name value to avoid possible
        # security problems
        name = self._escape_text(name)

        # retrieves the current modification time for
        # the generator as the current system time
        _mtime = time.time()

        # in case the next id value is not defined, it's
        # considered to be a new name in the data source
        # and so it must be created (insert query)
        if next_id == None:
            # sets the initial id value, the value should
            # be greater or equal to one plus one in order to avoid
            # enumeration validation collision, this value should
            # reflect the second value in the chain (because it's
            # the next value in chain)
            next_id = 2

            # creates the query to save a new entry in the generator
            # table setting the initial next id value and the initial
            # modification time values
            query = "insert into %s(name, next_id, _mtime) values('%s', %d, %f)" % (GENERATOR_VALUE, name, next_id, _mtime)
        # otherwise the name is already defined in the generator
        # table in the data source, and so an update is the
        # necessary operation (update query)
        else:
            # increments the next id value by one, this will
            # be the "new" next id value
            next_id += 1

            # creates the query to update the generator table set
            # the new next id and update the modification time
            query = "update %s set next_id = %d, _mtime = %f where name = '%s'" % (GENERATOR_VALUE, next_id, _mtime, name)

        # returns the query that will either update
        # or insert a value into the generator table
        # incrementing the next id value, the next id
        # is also returned to be able to be re-used in
        # different context
        return query, next_id

    def _create_definition_query(self, entity_class):
        # creates the list to hold the various queries
        # to be used to create indexes
        index_queries = []

        # creates the list that will hold the necessary
        # information for the creation of the foreign
        # key values
        foreign_keys = []

        # retrieves the ensure integrity option that should "request"
        # if a data source level integrity must be done or if the data
        # should only be checked at the entity manger level
        ensure_integrity = self.options.get("ensure_integrity", False)

        # retrieves the associated table name
        # as the "name" of the entity class and then
        # retrieves the items (map) for the entity class
        table_name = entity_class.get_name()
        table_items = entity_class.get_items()

        # creates the buffer to hold the query and populates it with the
        # base values of the query (base creation of the table)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("create table ")
        query_buffer.write(table_name)
        query_buffer.write("(")

        # unsets the flag that controls if the id
        # attribute was "already" set in the create
        # sql query string value
        id_set = False

        # sets the is first flag for the query
        # generation (provides way control comma)
        is_first = True

        # iterates over all the table items to be used
        # to create the table
        for item_name, item_value in table_items.items():
            # checks if the item name in the entity class
            # "refers" a relation value
            if entity_class.is_relation(item_name):
                # checks if the relation (attribute) is mapped
                # by the current class, in case it's not it should
                # not be created in the current table
                if not entity_class.is_mapped(item_name):
                    # continues the loop, no need to
                    # create the column for the relation
                    # attribute not mapped by the current
                    # class
                    continue

                # retrieves the target (class) of the relation with
                # the given name, this is going to use the relation attributes
                target_class = entity_class.get_target(item_name)

                # in case the target class is not itself, must ensure
                # the definition of the class in the data source and
                if not target_class == entity_class:
                    # ensures (makes sure) that the target class is defined
                    # in the data source (avoids problems defining foreign keys)
                    # this is only done when the integrity ensuring is a requirement
                    ensure_integrity and self.ensure_definition(target_class)

                # creates the foreign key tuple, containing both
                # the item name and the target class and adds it
                # to the list of foreign keys for latter generation
                # of the foreign key query section
                foreign_key = (item_name, target_class)
                ensure_integrity and foreign_keys.append(foreign_key)

                # retrieves the table id (name) and then uses
                # it to retrieve the value of it, this values
                # refer to the target class of the relation
                table_id = target_class.get_id()
                table_id_value = getattr(target_class, table_id)

                # retrieves the associated sql (data) type for the type
                # of the (target) table id attribute (foreign key)
                sql_type = SQL_TYPES_MAP[table_id_value.get("data_type", "integer")]

                # creates the index for the foreign key field and adds
                # it to the list of index queries
                index_query = self.engine._index_query(entity_class, item_name, "hash")
                index_queries.append(index_query)
            # otherwise it's a "normal" attribute
            else:
                # retrieves the associated sql (data) type for the type
                # of the current item value
                sql_type = SQL_TYPES_MAP[item_value.get("data_type", "integer")]

            # writes the comma to the query buffer only in case the
            # is first flag is not set
            is_first = not is_first and query_buffer.write(", ")

            # writes the item information into the current query
            # buffer, this information includes the field name,
            # sql data type and the primary reference (in case it's
            # necessary)
            query_buffer.write(item_name)
            query_buffer.write(" ")
            query_buffer.write(sql_type)
            item_value.get("id", False) and query_buffer.write(" primary key")

            # updates the id set flag to the correct value
            # in case the id attribute is found
            id_set = id_set or item_value.get("id", False)

        # in case the entity class does not have any
        # parents (it's the top level class) the "descriminator"
        # attribute must be written into it for latter
        # type discovery in retrieval of values
        if not entity_class.has_parents():
            # writes the comma to the query buffer only in case the
            # is first flag is not set
            is_first = not is_first and query_buffer.write(", ")

            # writes the class (descriminator) attribute definition
            # into the create table query
            query_buffer.write("_class text")

        # writes the comma to the query buffer only in case the
        # is first flag is not set, then writes the modified time
        # attribute into the create table query
        is_first = not is_first and query_buffer.write(", ")
        query_buffer.write("_mtime double precision")

        # in case the id attribute was not set (this is
        # a child class without id, so no direct id field
        # is available (need to create upper reference)
        if not id_set:
            # writes the comma to the query buffer only in case the
            # is first flag is not set
            is_first = not is_first and query_buffer.write(", ")

            # retrieves the table id (name) and then uses
            # it to retrieve the value of it
            table_id = entity_class.get_id()
            table_id_value = getattr(entity_class, table_id)

            # retrieves the associated sql (data) type for the type
            # of the table id (item) value
            table_id_type = SQL_TYPES_MAP[table_id_value.get("data_type", "integer")]

            # writes the upper table id information into the current query
            # buffer, this information includes the table id,
            # sql data type and the primary reference (key)
            query_buffer.write(table_id)
            query_buffer.write(" ")
            query_buffer.write(table_id_type)
            query_buffer.write(" primary key")

        # iterates over all the foreign keys to generate
        # the query code to create them, the iteration values
        # are the name and class of the foreign key
        for key_name, key_class in foreign_keys:
            # retrieves the table name and target
            # attribute for the foreign key
            key_table = key_class.get_name()
            key_target = key_class.get_id()

            # writes the comma to the query buffer only in case the
            # is first flag is not set
            is_first = not is_first and query_buffer.write(", ")

            # adds the necessary query code for the creation of
            # the foreign key, this uses the key name, table and target
            query_buffer.write("constraint %s_%s_fk foreign key(%s) references %s(%s)" % (table_name, key_name, key_name, key_table, key_target))

        # retrieves the table id to creates the appropriate
        # index "on top" of it
        table_id = entity_class.get_id()

        # creates the indexes for the primary key field and adds
        # them to the list of index queries
        index_query = self.engine._index_query(entity_class, table_id, "hash")
        index_tree_query = self.engine._index_query(entity_class, table_id, "btree")
        index_queries.append(index_query)
        index_queries.append(index_tree_query)

        # creates the indexes for the modified time field and adds
        # them to the list of index queries
        index_query = self.engine._index_query(entity_class, "_mtime", "hash")
        index_tree_query = self.engine._index_query(entity_class, "_mtime", "btree")
        index_queries.append(index_query)
        index_queries.append(index_tree_query)

        # writes the "final" create definition query character
        query_buffer.write(")")

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated definition query
        # and the list of index creation queries
        return query, index_queries

    def _delete_definition_query(self, entity_class):
        # retrieves the associated table name
        # as the "name" of the entity class
        table_name = entity_class.get_name()

        # creates the buffer to hold the query and populates it with the
        # base values of the query (base deletion of the table)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("drop table ")
        query_buffer.write(table_name)
        self.engine._allow_cascade() and query_buffer.write(" cascade")

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "dropping" query
        return query

    def _save_query(self, entity):
        # retrieves the entity class associated with
        # the entity
        entity_class = entity.__class__

        # retrieves the table (primary) id name
        # from the entity class (may use recursion)
        table_id = entity_class.get_id()

        # retrieves "all" the fields available
        # on the entity definition
        entity_fields = entity.get_fields()

        # retrieves the map that associates an entity
        # class with the map of items that are contained
        # inside it's scope
        items_map = entity_class.get_items_map()

        # creates the list to hold the set of queries
        # generated for saving a set of data
        queries = []

        # iterates over all the entity classes and table fields
        # in the items map to create the associated insert queries
        # (one query is created for each of the classes associated
        # with the entity)
        for _entity_class, table_fields in items_map.items():
            # retrieves the associated table name
            # as the "name" of the table
            table_name = _entity_class.get_name()

            # "filters" the entity fields that are associated with the current "class level"
            # in iteration, those attributes that are "contained" in other levels are not
            # going to be inserted in the query now
            _entity_fields = dict([(key, value) for key, value in entity_fields.items() if key in table_fields])

            # in case the entity class contains parents, no base id is set
            # and must be retrieved from the upper parents, in this case
            # an "upper reference" value must be inserted with the id
            if _entity_class.has_parents() and table_id in entity.__dict__:
                # sets the id attribute in the entity fields to create
                # the appropriate "upper reference"
                _entity_fields[table_id] = getattr(entity, table_id)

            # creates the buffer to hold the query and populates it with the
            # base values of the query (base insertion of the values)
            query_buffer = colony.libs.string_buffer_util.StringBuffer()
            query_buffer.write("insert into ")
            query_buffer.write(table_name)
            query_buffer.write("(")

            # sets the is first flag for the query
            # generation (provides way control comma)
            is_first = True

            # iterates over all the "filtered" entity fields
            # to be used in the inert query
            for field_name in _entity_fields:
                # in case the current field is a relation and is not mapped
                # by the current entity class, must create the mapping query
                # (query for updating external references)
                if entity_class.is_relation(field_name) and not entity_class.is_mapped(field_name):
                    # continues the loop the mapping of these relation
                    # will be done after the insert query is executed in
                    # the map part of the execution
                    continue

                # writes the comma to the query buffer only in case the
                # is first flag is not set
                is_first = not is_first and query_buffer.write(", ")

                # writes the current field name into the query buffer
                # insert field reference
                query_buffer.write(field_name)

            # in case the entity class has no parents (it's
            # the top level class) time to write the class
            # (descriminator) column reference
            if not _entity_class.has_parents():
                # writes the comma to the query buffer only in case the
                # is first flag is not set
                is_first = not is_first and query_buffer.write(", ")

                # writes the class column reference into the insert query
                query_buffer.write("_class")

            # writes the comma to the query buffer only in case the
            # is first flag is not set, then writes the modified time
            # into the insert query
            is_first = not is_first and query_buffer.write(", ")
            query_buffer.write("_mtime")

            # writes the values middle part of the insert query
            query_buffer.write(") values(")

            # sets the is first flag for the query
            # generation (provides way control comma)
            is_first = True

            # iterates over all the field values in the "filtered"
            # entity fields to populate the insert query
            for field_name, field_value in _entity_fields.items():
                # checks if the current field is a relation
                # (in that it is additional processing is required)
                if entity_class.is_relation(field_name):
                    # in case the field value is not mapped
                    # in the current entity class, cannot be
                    # used in current insert query (it's external)
                    if not entity_class.is_mapped(field_name):
                        # continues the attribute loop, nothing
                        # to be done for the current field
                        continue

                    # retrieves the target class for the relation currently
                    # in iteration, then uses it to retrieve the target id name
                    target_class = entity_class.get_target(field_name)
                    target_id = target_class.get_id()

                    # validates that the current field (relation) is valid according
                    # to the entity definition (must inherit from the target class)
                    entity.validate_relation_value(field_name, field_value, force = True)

                    # validates that the target id attribute contains the appropriate
                    # type for the field (relation) value class description (security
                    # validation), validates only if the field value is defined
                    field_value and field_value.validate_value(target_id)
                    field_value and field_value.validate_set(target_id)

                    # retrieves the id value of the relation entity
                    # as the field value to be written into the
                    # insert query (foreign key update) in case the
                    # field value is not set (invalid) the none value
                    # is set to dereference the value
                    field_value = field_value and field_value.get_id_value() or None

                # writes the comma to the query buffer only in case the
                # is first flag is not set
                is_first = not is_first and query_buffer.write(", ")

                # validates that the current field attribute
                # contains the appropriate type for the
                # entity class description (security
                # validation)
                entity.validate_value(field_name, field_value, force = True)

                # retrieves the sql value for the field and writes
                # it into the save query
                sql_value = entity.get_sql_value(field_name, field_value, force = True)
                query_buffer.write(sql_value)

            # in case the entity class has no parents (it's
            # the top level class) time to write the class
            # (descriminator) column value
            if not _entity_class.has_parents():
                # writes the comma to the query buffer only in case the
                # is first flag is not set
                is_first = not is_first and query_buffer.write(", ")

                # writes the class column value into the insert query
                query_buffer.write("'%s'" % entity_class.__name__)

            # retrieves the proper modification time either from
            # the entity or from the current system time
            _mtime = hasattr(entity, "_mtime") and entity._mtime or time.time()

            # writes the comma to the query buffer only in case the
            # is first flag is not set, then writes the modified time
            # into the insert query
            is_first = not is_first and query_buffer.write(", ")
            query_buffer.write("%f" % _mtime)

            # writes the "final" save query character
            query_buffer.write(")")

            # retrieves the "final" query value from
            # the query (string) buffer and adds it
            # to the list of queries
            query = query_buffer.get_value()
            queries.append(query)

        # returns the generated "insert" set of
        # queries (multiple inserts)
        return queries

    def _update_query(self, entity):
        # retrieves the entity class associated with
        # the entity
        entity_class = entity.__class__

        # retrieves "all" the fields available
        # on the entity definition
        entity_fields = entity.get_fields()

        # retrieves the table (primary) id name
        # from the entity class and then retrieves
        # the entity id attribute value from the entity
        table_id = entity_class.get_id()
        table_id_value = entity.get_id_value()

        # validates that the table id attribute
        # contains the appropriate type for the
        # entity class description (security
        # validation)
        entity.validate_value(table_id, table_id_value, force = True)

        # converts the table id value into the appropriate
        # sql representation for query usage (casting)
        table_id_sql_value = entity.get_sql_value(table_id, table_id_value, force = True)

        # retrieves the map that associates an entity
        # class with the map of items that are contained
        # inside it's scope
        items_map = entity_class.get_items_map()

        # creates the list to hold the set of queries
        # generated for updating a set of data
        queries = []

        # iterates over all the entity classes and table fields
        # in the items map to create the associated update queries
        # (one query is created for each of the classes associated
        # with the entity)
        for _entity_class, table_fields in items_map.items():
            # retrieves the associated table name
            # as the "name" of the table
            table_name = _entity_class.get_name()

            # "filters" the entity fields that are associated with the current "class level"
            # in iteration, those attributes that are "contained" in other levels are not
            # going to be inserted in the query now, note that the table identifier is
            # excluded because it's considered to be a immutable field (once set cannot be changed)
            # so there is no need to be include in the valid table field for update
            _entity_fields = dict([(key, value) for key, value in entity_fields.items() if key in table_fields and not key == table_id])

            # checks if the entity contains unmapped relations for the current
            # entity class parent level, in case it has the update query must
            # be ran even if there are no direct name field to be updated
            has_unmapped_relations = entity.has_unmapped_relations(_entity_class)

            # in case there are no entity fields to be used in the
            # update query (no need to update it), note that the
            # unmapped relations are taken into account because if
            # there are unmapped relations the modified time must be
            # updated for the current entity class level
            if not _entity_fields and not has_unmapped_relations:
                # continues the loop, not going to create
                # the query for update
                continue

            # creates the buffer to hold the query and populates it with the
            # base values of the query (base update of the values)
            query_buffer = colony.libs.string_buffer_util.StringBuffer()
            query_buffer.write("update ")
            query_buffer.write(table_name)
            query_buffer.write(" set ")

            # sets the is first flag for the query
            # generation (provides way control comma)
            is_first = True

            # iterates over all the entity fields to be updated
            # in the current query, these values are going to be
            # set one by one in the query in an equality
            for field_name, field_value in _entity_fields.items():
                # checks if the current field is a relation
                # (in that it is additional processing is required)
                if entity_class.is_relation(field_name):
                    # in case the field value is not mapped
                    # in the current entity class, cannot be
                    # used in current insert query (it's external)
                    if not entity_class.is_mapped(field_name):
                        # continues the attribute loop, nothing
                        # to be done for the current field
                        continue

                    # validates that the current field (relation) is valid according
                    # to the entity definition (must inherit from the target class)
                    entity.validate_relation_value(field_name, field_value, force = True)

                    # retrieves the id value of the relation entity
                    # as the field value to be written into the
                    # update query (foreign key update) in case the
                    # field value is not set (invalid) the none value
                    # is set to dereference the value
                    field_value = field_value and field_value.get_id_value() or None

                # writes the comma to the query buffer only in case the
                # is first flag is not set
                is_first = not is_first and query_buffer.write(", ")

                # validates that the current field attribute
                # contains the appropriate type for the
                # entity class description (security
                # validation)
                entity.validate_value(field_name, field_value, force = True)

                # converts the current field value into the appropriate
                # sql representation for query usage (casting)
                field_sql_value = entity.get_sql_value(field_name, field_value, force = True)

                # sets the field name associated with the new field
                # value for the current query
                query_buffer.write(field_name)
                query_buffer.write(" = ")
                query_buffer.write(field_sql_value)

            # retrieves the proper modification time either from
            # the entity or from the current system time
            _mtime = hasattr(entity, "_mtime") and entity._mtime or time.time()

            # writes the comma to the query buffer only in case the
            # is first flag is not set, then writes the modified time
            # into the update query
            is_first = not is_first and query_buffer.write(", ")
            query_buffer.write("_mtime = %f" % _mtime)

            # writes the table identifying (filtering part
            # of the query)
            query_buffer.write(" where ")
            query_buffer.write(table_id)
            query_buffer.write(" = ")
            query_buffer.write(table_id_sql_value)

            # retrieves the "final" query value from
            # the query (string) buffer and adds it
            # to the list of queries
            query = query_buffer.get_value()
            queries.append(query)

        # returns the generated "update" set of
        # queries (multiple updates)
        return queries

    def _remove_query(self, entity):
        # retrieves the entity class associated with
        # the entity
        entity_class = entity.__class__

        # retrieves the associated table name
        # as the "name" of the entity class
        table_name = entity_class.get_name()

        # retrieves the table (primary) id name
        # from the entity class
        table_id = entity_class.get_id()

        # validates that the table id attribute
        # contains the appropriate type for the
        # entity class description (security
        # validation)
        entity.validate_value(table_id)

        # retrieves the sql value for the table id from
        # the entity (this is the id value converted into
        # the proper sql representation)
        id_sql_value = entity.get_sql_value(table_id)

        # creates the list to hold the set of queries
        # generated for removing a set of data
        queries = []

        # retrieves "all" the parents from the entity
        # class, to be able to remove all the references
        # of the entity in the data source then creates
        # list of entity classes to be used in the removal
        # from the parents and the current entity
        all_parents = entity_class.get_all_parents()
        entity_classes = all_parents + [entity_class]

        # iterates over all the entity classes from
        # which the data should be removed in the
        # associated data source
        for _entity_class in entity_classes:
            # retrieves the associated table name
            # as the "name" of the table
            table_name = _entity_class.get_name()

            # creates the buffer to hold the query and populates it with the
            # base values of the query (base delete of the values)
            query_buffer = colony.libs.string_buffer_util.StringBuffer()
            query_buffer.write("delete from ")
            query_buffer.write(table_name)
            query_buffer.write(" where ")
            query_buffer.write(table_id)
            query_buffer.write(" = ")
            query_buffer.write(id_sql_value)

            # retrieves the "final" query value from
            # the query (string) buffer and adds it
            # to the list of queries
            query = query_buffer.get_value()
            queries.append(query)

        # returns the generated "remove" set of
        # queries (multiple deletes)
        return queries

    def _map_query(self, entity):
        # retrieves the entity class associated with
        # the entity
        entity_class = entity.__class__

        # creates the list to hold the set of queries
        # generated for inserting a set of data
        queries = []

        # retrieves both the indirect and direct relations
        # to be used to create the various mapping of the queries
        indirect_relations_map = entity_class.get_indirect_relations_map()
        direct_relations_map = entity_class.get_direct_relations_map()

        # iterates over all the entity classes and indirect relations
        # in the indirect relations map to create the map queries for all
        # of the present indirect relation in all parenting levels
        for entity_class, indirect_relations in indirect_relations_map.items():
            # retrieves both the entity class name as the
            # table name and the id name of the entity
            # to have the relations mapped
            table_name = entity_class.get_name()
            table_id = entity_class.get_id()

            # validates that the table id attribute
            # contains the appropriate type for the
            # entity class description (security
            # validation)
            entity.validate_value(table_id)

            # retrieves the sql value for the table id from
            # the entity (this is the id value converted into
            # the proper sql representation)
            id_sql_value = entity.get_sql_value(table_id)

            # iterates over all the indirect relations to create the insert
            # queries that will associate both parts of the relation
            for indirect_relation in indirect_relations:
                # in case the entity has no value for the given relation
                # (no need to continue)
                if not entity.has_value(indirect_relation):
                    # continues the loop, not going
                    # to persist inexistent relation
                    continue

                # retrieves the target class and the is to many flag
                # for the current (indirect) relation
                target_class = entity.get_target(indirect_relation)
                is_to_many = entity.is_to_many(indirect_relation)

                # checks if the target class is a "data reference" and
                # in case it is, tries to resolve it into the appropriate
                # concrete (real) class in case the resolution fails it's
                # impossible to map the indirect relation (skips mapping)
                target_is_reference = target_class.is_reference()
                if target_is_reference: target_class = self.get_entity(target_class.__name__)
                if not target_class: continue

                # in case the relation is of type to many it must be validated
                # so that the value is assured to be a sequence
                is_to_many and entity.validate_sequence(indirect_relation)

                # retrieves the target (table) name from the target
                # class value then retrieves the target id attribute
                # name to used it later in the insert query
                target_name = target_class.get_name()
                target_id = target_class.get_id()

                # retrieves the relation value and the (complete) unique
                # name of the relation (going to be use as relation table
                # name)
                relation_value = entity.get_value(indirect_relation)
                relation_unique = entity.get_relation_unique(indirect_relation)

                # in case the indirect relation is not of type to many
                # the relation value is converted into a list to allow
                # the map query implementation to work
                if not is_to_many: relation_value = [relation_value]

                # creates the query to delete the rows that are currently
                # associated with the entity, then adds the query to the
                # list of queries to be executed
                query = "delete from %s where %s = %s" % (relation_unique, table_name, id_sql_value)
                queries.append(query)

                # iterates over all the relation values to update the
                # appropriate relation table
                for _relation_value in relation_value:
                    # validates that the indirect relation is valid according
                    # to the entity definition (must inherit from the target class)
                    entity.validate_relation_value(indirect_relation, _relation_value, force = True)

                    # validates that the target id attribute contains the appropriate
                    # type for the relation value class description (security
                    # validation), validates only if the relation is defined
                    _relation_value and _relation_value.validate_value(target_id)
                    _relation_value and _relation_value.validate_set(target_id)

                    # retrieves the sql value for the target id from the relation value
                    # (entity) sets the value as null in case the relation value is not defined
                    relation_id_sql_value = _relation_value and _relation_value.get_sql_value(target_id) or "null"

                    # creates the query to be used to insert the various values
                    # into the relation table with the appropriates casts and
                    # then appends it to the list of queries to be executed
                    query = "insert into %s (%s, %s) values(%s, %s)" % (relation_unique, table_name, target_name, id_sql_value, relation_id_sql_value)
                    queries.append(query)

        # iterates over all the entity classes and direct relations
        # in the direct relations map to create the map queries for all
        # of the present indirect relation in all parenting levels
        for entity_class, direct_relations in direct_relations_map.items():
            # retrieves both the entity class name as the
            # table name and the id name of the entity
            # to have the relations mapped
            table_name = entity_class.get_name()
            table_id = entity_class.get_id()

            # validates that the table id attribute
            # contains the appropriate type for the
            # entity class description (security
            # validation)
            entity.validate_value(table_id)

            # retrieves the sql value for the table id from
            # the entity (this is the id value converted into
            # the proper sql representation)
            id_sql_value = entity.get_sql_value(table_id)

            # iterates over all the direct relations to create the update
            # queries that will associate both parts of the relation, the
            # update will be done on the other side of the relation
            for direct_relation in direct_relations:
                # in case the entity has no value for the given relation
                # (no need to continue)
                if not entity.has_value(direct_relation):
                    # continues the loop, not going
                    # to persist inexistent relation
                    continue

                # retrieves the target class, the reverse value and
                # then the is to many flag for the current (direct)
                # relation
                target_class = entity.get_target(direct_relation)
                reverse = entity.get_reverse(direct_relation)
                is_to_many = entity.is_to_many(direct_relation)

                # checks if the target class is a "data reference" and
                # in case it is, tries to resolve it into the appropriate
                # concrete (real) class in case the resolution fails it's
                # impossible to map the direct relation (skips mapping)
                target_is_reference = target_class.is_reference()
                if target_is_reference: target_class = self.get_entity(target_class.__name__)
                if not target_class: continue

                # in case the relation is of type to many it must be validated
                # so that the value is assured to be a sequence
                is_to_many and entity.validate_sequence(direct_relation)

                # retrieves the target (table) name from the target
                # class value then retrieves the target id attribute
                # name to used it later in the insert query
                target_name = target_class.get_name()
                target_id = target_class.get_id()

                # retrieves the relation value to be used to be stored
                # in the relation table, for indirect relation mapping
                relation_value = entity.get_value(direct_relation)

                # in case the direct relation is not of type to many
                # the relation value is converted into a list to allow
                # the map query implementation to work
                if not is_to_many: relation_value = [relation_value]

                # creates the query to update the foreign key values in
                # the target relation table to null values, it will unset
                # the relations for the current values, then adds the query
                # to the list of queries to be executed
                query = "update %s set %s = null where %s = %s" % (target_name, reverse, reverse, id_sql_value)
                queries.append(query)

                # iterates over all the relation values to update the
                # appropriate target table
                for _relation_value in relation_value:
                    # validates that the direct relation is valid according
                    # to the entity definition (must inherit from the target class)
                    entity.validate_relation_value(direct_relation, _relation_value, force = True)

                    # validates that the target id attribute contains the appropriate
                    # type for the relation value class description (security
                    # validation), validates only if the relation is defined
                    _relation_value and _relation_value.validate_value(target_id)
                    _relation_value and _relation_value.validate_set(target_id)

                    # retrieves the sql value for the target id from the relation value
                    # (entity) sets the value as null in case the relation value is not defined
                    relation_id_sql_value = _relation_value and _relation_value.get_sql_value(target_id) or "null"

                    # creates the query to be used to update the foreign key in
                    # the target relation table with the appropriates casts and
                    # then appends it to the list of queries to be executed
                    query = "update %s set %s = %s where %s = %s" % (target_name, reverse, id_sql_value, target_id, relation_id_sql_value)
                    queries.append(query)

        # returns the generated "insert" set of
        # queries (multiple inserts and updates)
        return queries

    def _verify_query(self, entity_class, id_value):
        # retrieves the type of provided id value
        # this value may be a tuple or a single value
        # the verify query will reflect this type
        id_value_type = type(id_value)

        # retrieves the associated table name
        # as the "name" of the entity class
        table_name = entity_class.get_name()

        # retrieves the table (primary) id name
        # from the entity class
        table_id = entity_class.get_id()

        # creates the buffer to hold the query and populates it with the
        # base values of the query (base verify of the table)
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("select ")
        query_buffer.write(table_id)
        query_buffer.write(" from ")
        query_buffer.write(table_name)
        query_buffer.write(" where ")
        query_buffer.write(table_id)

        # in case the id value is a tuple (sequence)
        # an "in" operator must be used in the query
        if id_value_type == types.TupleType:
            # adds the appropriate "in" operator to
            # the verify query
            query_buffer.write(" in (")

            # sets the is first flag for the query
            # generation (provides way control comma)
            is_first = True

            # iterates over all the id values in the id
            # value tuple (sequence)
            for _id_value in id_value:
                # writes the comma to the query buffer only in case the
                # is first flag is not set
                is_first = not is_first and query_buffer.write(", ")

                # converts the current id value into the appropriate
                # sql representation and write it into the select query
                _id_sql_value = entity_class._get_sql_value(table_id, _id_value)
                query_buffer.write(_id_sql_value)

            # writes the end of "in" sequence in the
            # verify query
            query_buffer.write(")")
        # otherwise it's a "precise" element and the "equals"
        # operator must be used
        else:
            # adds the appropriate "equals" operator to
            # the verify query
            query_buffer.write(" = ")

            # converts the id value into the appropriate sql
            # representation and write it into the select query
            id_sql_value = entity_class._get_sql_value(table_id, id_value)
            query_buffer.write(id_sql_value)

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated verification query
        return query

    def _verify_result(self, entity_class, id_value, cursor):
        try:
            # selects all the id values for the table in the database
            # this values should be entity model identifiers
            id_values = [value[0] for value in cursor]
        finally:
            # closes the cursor
            cursor.close()

        # retrieves the type of the provided id value in case it's a tuple
        # the length is calculated otherwise a tuple must created from the
        # single value
        id_value_type = type(id_value)
        id_length = id_value_type == types.TupleType and len(id_value) or 1
        id_value = id_value_type == types.TupleType and id_value or (id_value,)

        # creates the initial verifications bit list as a list of
        # false bits for all elements (by default they're not found)
        verifications = [False] * id_length

        # starts the index counter value, to be used
        # in the setting of the verification bit list
        index = -1

        # iterates over all the id values present in
        # the id value sequence
        for _id_value in id_value:
            # increments the index value (iteration)
            index += 1

            # in case the current id value is not present
            # in the "found" id values, not going to
            # update the verifications bit list
            if not _id_value in id_values:
                # continues the loop
                continue

            # updates the verifications bit list to set
            # the element as found
            verifications[index] = True

        # creates the final verified structure, in case the provided
        # id value is a tuple a tuple should be creates from the verifications
        # list otherwise the first result should be used (single value)
        verified = id_value_type == types.TupleType and tuple(verifications) or verifications[0]

        # returns the final verified value according
        # to the provided id value
        return verified

    def _find_query(self, entity_class, options):
        # normalizes the options, this is going to expand the
        # options map into a larger and easily accessible
        # map of values
        options = self.normalize_options(options)

        # creates the string buffer to hold the select query
        # and write the initial select token
        query_buffer = colony.libs.string_buffer_util.StringBuffer()
        query_buffer.write("select ")

        # writes the part of find query dedicated to the selecting
        # of the appropriate names from the result set, the string
        # will be updated based on the top level entity class names
        # an on the eager loading class names on it
        field_names = self._names_query_f(entity_class, options, query_buffer)

        # writes the part of the find query dedicated to the joining
        # of the various tables comprehending the parent hierarchy
        # of the entity class to be found and the various relation
        # hierarchies in a recursive approach
        self._join_query_f(entity_class, options, query_buffer)

        # writes the part of find query dedicated to the filtering
        # of the result set, the string will be updated based on the
        # the top level filter and on the eager loading relations
        # filters of the options map
        self._filter_query_f(entity_class, options, query_buffer)

        # writes the part of find query dedicated to the ordering
        # of the result set, the string will be updated based on the
        # the top level filter, the name of the ordering steps may
        # be a fully qualified name in dot notation
        self._order_query_f(entity_class, options, query_buffer)

        # writes the part of find query dedicated to the limiting
        # of the result set, the string will be updated based on the
        # start record and number records values of the options map
        self._limit_query_f(entity_class, options, query_buffer)

        # retrieves the "final" query value from
        # the query (string) buffer
        query = query_buffer.get_value()

        # returns the generated "finding" query
        # and list containing the field names in
        # the order used in the select statement
        return query, field_names

    def _names_query_f(self, entity_class, options, query_buffer):
        # retrieves the associated table as the id
        # of the entity class (table)
        table_id = entity_class.get_id()

        # retrieves the entity class name as the name
        # of the table representing it
        table_name = entity_class.get_name()

        # allocates the list to hold the various field names
        # to be inserted into the query, this list will be used
        # latter to know in advance the sequence of values
        # retrieved from the data source
        field_names = []

        # retrieves the map containing the various
        # (upper) parent classes associated with the
        # items contained in them
        items_map = entity_class.get_items_map()

        # retrieves the count flag from the options, if
        # the count flag is set the objective of the query
        # is to only count the values that respect the provided
        # filter, no names should be used in the query and no
        # entities should be returns (only a number)
        count = options.get("count", False)

        # retrieves the is minimal flag from the options,
        # a minimal query is a query that is meant to retrieve
        # only the basic information (id attribute) of the base
        # entity and it's eager relations, this is useful for
        # lazy loading relations retrieval
        is_minimal = options.get("minimal", False)

        # retrieves the order names flag from the options,
        # this flag defined if the order of the names to be
        # retrieved from the data source is critical and as
        # such should be maintained across various requests,
        # this flag has serious implications on the performance
        # of the query generation, typical applications for this
        # flag would be reports using the data set flag
        order_names = options.get("order_names", False)

        # retrieves the (attribute) names to be retrieved from
        # the current entity, in case this value is not set the
        # complete list of names is retrieve from the data source
        names = options.get("names", None)

        # creates the list to hold the already visited names, this
        # is a holder for the various name string values, only in
        # case the order names flag is set
        if order_names: _names = []

        # sets the is first flag for the query
        # generation (provides way control comma)
        is_first = True

        # in case the count flag is set, no need to
        # write all the name references in the query,
        # only need to write the count statement
        if count:
            # writes the count statement in the query
            # buffer and returns the field names
            query_buffer.write("count(*)")

            # returns the field names immediately, avoid
            # writing all the names for the select
            return field_names

        # retrieves the items map items and then in case the
        # the order names flag is set sorts them according to
        # the default sorting order
        items_items = items_map.items()
        if items_items: items_items.sort()

        # iterates over all the entity classes and table fields
        # in the items map to create the associated update queries
        # (one query is created for each of the classes associated
        # with the entity)
        for _entity_class, table_fields in items_items:
            # retrieves the current associated table name
            # as the "name" of the current entity class
            _table_name = _entity_class.get_name()

            # in case the names should be ordered retrieves the
            # table fields keys and then sorts them according to
            # the default order (expensive operation)
            if order_names: table_fields = table_fields.keys(); table_fields.sort()

            # iterates over all the table fields of the current
            # entity to put them into the select query
            for field_name in table_fields:
                # in case the (required) field names are defined and the
                # current field name is not contained in the set no need
                # to continue (unwanted field name)
                if names and not field_name in names: continue

                # in case the names list is defined and the field
                # name is not present in it continues the iteration
                # otherwise in case the names list is defined adds
                # the field name to the already visited names
                if names and field_name in _names: continue
                elif names: _names.append(field_name)

                # in case the is minimal flag is set and the current
                # field is not the id field (must avoid retrieval)
                # also in case the current field name refers a relation
                # it must also avoid retrieval
                if is_minimal and not field_name == table_id: continue
                if _entity_class.is_relation(field_name): continue

                # writes the comma to the query buffer only in case the
                # is first flag is not set
                is_first = not is_first and query_buffer.write(", ")

                # write the fully qualified field name (include table name)
                # in the select query
                query_buffer.write(_table_name + "." + field_name)

                # adds the field name to the list of field names
                # to maintain the correct order in the retrieval
                # of the values (provides easy interface for it)
                field_names.append(field_name)

        def join_names(entity_class, options, order_names = False, is_first = True, prefix = "", base_class = None):
            # retrieves the complete map of relations (ordered
            # by parent class) for the current entity class
            # to be processed, this is going to be used for
            # the retrieving all the appropriate names to be
            # retrieved by the select statement
            relations_map = entity_class.get_relations_map()

            # retrieves the eager (loading) option from the map
            # of options, the eager values are the maps describing
            # the various relations of the entity to be eagerly
            # loaded from the data source, this map may contains a
            # series of values describing the way the relations
            # should be loaded
            eager = options.get("eager", {})

            # retrieves the relations map items and then in case the
            # the order names flag is set sorts them according to
            # the default sorting order
            relations_items = relations_map.items()
            if relations_items: relations_items.sort()

            # iterates over each of the various parent classes relations
            # to create the names for the various relation fields in
            # select query
            for _entity_class, table_relations in relations_items:
                # retrieves the current associated table name
                # as the "name" of the current entity class
                _table_name = _entity_class.get_name()

                # in case the names should be ordered retrieves the
                # table relations keys and then sorts them according to
                # the default order (expensive operation)
                if order_names: table_relations = table_relations.keys(); table_relations.sort()

                # iterates over all the table fields of the current
                # entity to put them into the select query
                for table_relation in table_relations:
                    # checks if the table relation is of type lazy (or minimal
                    # flag is set), in case it is and it's not present in the
                    # eager map of the options, processing is avoided (in minimal
                    # processing the default eager loading relations are avoided)
                    is_lazy = _entity_class.is_lazy(table_relation) or is_minimal
                    if is_lazy and not table_relation in eager: continue

                    # retrieves the target class of the relation and uses
                    # it to retrieve both the name (table name)
                    target_class = _entity_class.get_target(table_relation)
                    target_name = target_class.get_name()

                    # checks if the target class is a "data reference" and
                    # in case it is, tries to resolve it into the appropriate
                    # concrete (real) class in case the resolution fails it's
                    # impossible to join the relation names (skips name joining)
                    target_is_reference = target_class.is_reference()
                    if target_is_reference: target_class = self.get_entity(target_class.__name__)
                    if not target_class: continue

                    # retrieves and normalizes the options, this is going
                    # to expand the options map into a larger and easily
                    # accessible map of values (this only happens in case
                    # the options are defined)
                    _options = eager.get(table_relation, {})
                    _options = _options and self.normalize_options(_options) or _options

                    # retrieves the (attribute) names to be retrieved from
                    # the current entity, in case this value is not set the
                    # complete list of names is retrieve from the data source
                    names = _options.get("names", None)

                    # creates the list to hold the already visited names, this
                    # is a holder for the various name string values, only in
                    # case the order names flag is set
                    if order_names: _names = []

                    # retrieves the map of items of the target class to use them
                    # as the base structure for population of the names in the query
                    target_items_map = target_class.get_items_map()

                    # normalizes the prefix by replacing the query "oriented"
                    # separator with the "normal" path separator, this prefix
                    # is going to be used for field name creation
                    _prefix = prefix and prefix[2:].replace("__", ".") + "." or ""

                    # creates the fully qualified name (fqn) from the prefix
                    # value and the current table relation name
                    fqn = prefix + "__" + table_relation

                    # iterates over all the table fields of the current
                    # entity to put them into the select query
                    for __entity_class, table_fields in target_items_map.items():
                        # retrieves the current associated table name
                        # as the "name" of the current entity class
                        __table_name = __entity_class.get_name()

                        # in case the names should be ordered retrieves the
                        # table fields keys and then sorts them according to
                        # the default order (expensive operation)
                        if order_names: table_fields = table_fields.keys(); table_fields.sort()

                        # iterates over all the table fields of the current
                        # entity to put them into the select query
                        for field_name in table_fields:
                            # in case the (required) field names are defined and the
                            # current field name is not contained in the set no need
                            # to continue (unwanted field name)
                            if names and not field_name in names: continue

                            # in case the names list is defined and the field
                            # name is not present in it continues the iteration
                            # otherwise in case the names list is defined adds
                            # the field name to the already visited names
                            if names and field_name in _names: continue
                            elif names: _names.append(field_name)

                            # in case the current field name refers a relation
                            # it cannot be included in the query collision of
                            # names in the joins may occurs an an invalid result
                            # set would be returned (problem in final unpacking)
                            if __entity_class.is_relation(field_name): continue

                            # writes the comma to the query buffer only in case the
                            # is first flag is not set
                            is_first = not is_first and query_buffer.write(", ")

                            # in case the table name is the target name, there is
                            # a relation to be resolved, need to include the (target)
                            # table name in the attribute name
                            if not __table_name == target_name:
                                # write the fully qualified field name (include table name)
                                # in the select query
                                query_buffer.write(fqn + "___" + __table_name + "." + field_name)
                            # otherwise it's a simple attribute in the current context and
                            # only the fully qualified field name (fqn) must be included
                            else:
                                # writes the fully qualified name and the the field name
                                # (field in the current context)
                                query_buffer.write(fqn + "." + field_name)

                            # adds the field name to the list of field names
                            # to maintain the correct order in the retrieval
                            # of the values (provides easy interface for it)
                            field_names.append(_prefix + table_relation + "." + field_name)

                    # in case the names list is not defined or in case the class
                    # name reference is contained in the names list, must write
                    # the appropriate query values so that it's selected
                    if not names or "_class" in names:
                        # retrieves the top parent class for the target class (relation)
                        # and then retrieves the name of it for comparison
                        _top_parent = target_class.get_top_parent()
                        _top_parent_name = _top_parent.get_name()

                        # writes the comma to the query buffer only in case the
                        # is first flag is not set
                        is_first = not is_first and query_buffer.write(", ")

                        # in case the top parent class name is exactly the same as the target
                        # name (the target is the top parent) there is no need to add any extra
                        # prefix to the reference, otherwise the top parent name must be written
                        # as to the full reference to the class attribute
                        if _top_parent_name == target_name: query_buffer.write(fqn + "._class")
                        else: query_buffer.write(fqn + "___" + _top_parent_name + "._class")

                        # adds the class attribute reference for the table relation
                        # to the list of field names (may be used for name resolution
                        # latter in data set retrieval)
                        field_names.append(_prefix + table_relation + "._class")

                    # in case the names list is not defined or in case the modified time
                    # name reference is contained in the names list, must write
                    # the appropriate query values so that it's selected
                    if not names or "_mtime" in names:
                        # writes the comma to the query buffer only in case the
                        # is first flag is not set
                        is_first = not is_first and query_buffer.write(", ")

                        # writes the fully qualified modified time attribute reference
                        # to the query buffer and the adds the reference to it to the
                        # fields names list (may be used for name resolution latter
                        # in data set retrieval)
                        query_buffer.write(fqn + "._mtime")
                        field_names.append(_prefix + table_relation + "._mtime")

                    # joins the various names for the relation table, this is the recursion
                    # step, returns the value of the is first control flag
                    is_first = join_names(target_class, _options, order_names, is_first, prefix + "__" + table_relation)

            # returns the value of the is first control flag it's
            # used to control the comma access in the string value
            return is_first

        # joins the various names for the relations of the current entity
        # class (recursion step)
        is_first = join_names(entity_class, options, order_names, is_first)

        # in case the names list is not defined or in case the class
        # name reference is contained in the names list, must write
        # the appropriate query values so that it's selected
        if not names or "_class" in names:
            # retrieves the top parent to be able to use it for the
            # construction of the fully qualified attribute name
            # of the class (descriminator) field
            top_parent = entity_class.get_top_parent()
            top_parent_name = top_parent.get_name()

            # writes the comma to the query buffer only in case the
            # is first flag is not set
            is_first = not is_first and query_buffer.write(", ")

            # writes the class (descriminator) reference to the select
            # query and adds the field to the list of fields, it's going
            # to be used latter for correct class matching
            query_buffer.write(top_parent_name + "._class")
            field_names.append("_class")

        # in case the names list is not defined or in case the modified time
        # name reference is contained in the names list, must write
        # the appropriate query values so that it's selected
        if not names or "_mtime" in names:
            # writes the comma to the query buffer only in case the
            # is first flag is not set
            is_first = not is_first and query_buffer.write(", ")

            # writes the modified time attribute reference to the select
            # query and adds the field to the list of fields, it may
            # be used latter to constrain the range of entries retrieved
            query_buffer.write(table_name + "._mtime")
            field_names.append("_mtime")

        # returns the list of select fields, this list is normalized
        # and so it's easy to understand for a parser perspective
        return field_names

    def _join_query_f(self, entity_class, options, query_buffer):
        # retrieves the associated table name and id
        # as the "name" and id of the entity class (table)
        table_name = entity_class.get_name()
        table_id = entity_class.get_id()

        # retrieves all the parent classes from the entity
        # classes, to provide a way of joining the values in
        # a bottom up strategy
        all_parents = entity_class.get_all_parents()

        # retrieves the is minimal flag from the options,
        # a minimal query is a query that is meant to retrieve
        # only the basic information (id attribute) of the base
        # entity and it's eager relations, this is useful for
        # lazy loading relations retrieval
        is_minimal = options.get("minimal", False)

        # retrieves the count flag from the options, if
        # the count flag is set the objective of the query
        # is to only count the values that respect the provided
        # filter, no names should be used in the query and no
        # entities should be returns (only a number)
        count = options.get("count", False)

        # retrieves the if the current options map contains
        # filters and also if it contains eager loading relations
        # in case the options map contains any of them the
        # simplified query for the count cannot be accomplished
        # and complete joining of parent or relation tables must
        # occur (much slower count query execution)
        has_filters = "filters" in options
        has_eager = "eager" in options

        # writes the "from" table reference part
        # of the select query
        query_buffer.write(" from ")
        query_buffer.write(table_name)

        # in case this is a count type query and the options
        # map does not contain any filters an does not contain
        # any eager loading relations, a simplified query may
        # be created (query without any joining on parent tables
        # and on relation tables)
        if count and not has_filters and not has_eager:
            # returns immediately, no need to join
            # on parent tables and on relation tables
            return

        # iterates over all the parents to provide
        # the necessary (inner) join of them into
        # the current query context, this is a main step
        # in achieving inheritance compliance in the query
        for parent in all_parents:
            # in case the parent class is abstract no need to join
            # it into the current query
            if parent.is_abstract(): continue

            # retrieves the parent name, assumes the
            # associated table has the same value
            parent_name = parent.get_name()

            # writes the table inheritance inner join
            # part of the query, ensuring data coherence
            # in the complete inheritance chain
            query_buffer.write(" inner join ")
            query_buffer.write(parent_name)
            query_buffer.write(" on ")
            query_buffer.write(table_name + "." + table_id)
            query_buffer.write(" = ")
            query_buffer.write(parent_name + "." + table_id)

        def join_tables(entity_class, options, prefix = ""):
            # retrieves the complete map of relations (ordered
            # by parent class) for the current entity class
            # to be processed, this is going to be used for
            # the joining the of the complete set of relations
            relations_map = entity_class.get_relations_map()

            # retrieves the eager (loading) option from the map
            # of options, the eager values are the maps describing
            # the various relations of the entity to be eagerly
            # loaded from the data source, this map may contains a
            # series of values describing the way the relations
            # should be loaded
            eager = options.get("eager", {})

            # iterates over all the relations in the relations map
            # to join their tables (ant their parent tables) into
            # the current query
            for _entity_class, table_relations in relations_map.items():
                # retrieves the current associated table name
                # as the "name" of the current entity class
                _table_name = _entity_class.get_name()

                # iterates over all the table fields of the current
                # entity to put them into the select query
                for table_relation in table_relations:
                    # checks if the table relation is of type lazy, (or minimal
                    # flag is set), in case it is and it's not present in the
                    # eager map of the options, processing is avoided (in minimal
                    # processing the default eager loading relations are avoided)
                    is_lazy = _entity_class.is_lazy(table_relation) or is_minimal
                    if is_lazy and not table_relation in eager: continue

                    # retrieves the target class for the relation and
                    # uses it to retrieve the target table name and
                    # the id (name) of the target table
                    target_class = _entity_class.get_target(table_relation)
                    target_table_name = target_class.get_name()
                    target_table_id = target_class.get_id()

                    # checks if the target class is a "data reference" and
                    # in case it is, tries to resolve it into the appropriate
                    # concrete (real) class in case the resolution fails it's
                    # impossible to join the tables (skips table joining)
                    target_is_reference = target_class.is_reference()
                    if target_is_reference: target_class = self.get_entity(target_class.__name__)
                    if not target_class: continue

                    # retrieves the "mapper" for the relation to check if
                    # the relation is of type indirect and also retrieves
                    # the is mapped attribute to check if the relation is
                    # of type direct or mapped (relation is mapped in the
                    # current entity model)
                    mapper = _entity_class.get_mapper(table_relation)
                    is_mapped = _entity_class.is_mapped(table_relation)

                    # retrieves the relation unique name, in case an indirect
                    # relation is present (no "mapper") it's going to be used to
                    # access the correct table
                    relation_unique = _entity_class.get_relation_unique(table_relation)

                    # creates the fqn (fully qualified name) of the relation from the
                    # current prefix and the name of the relation, this prefix
                    # going to be used to refer the attributes in the select part
                    # of the query, it's also going to be used to construct the composite
                    # (fqn) names for the parent tables of the current relation
                    fqn = prefix + "__" + table_relation

                    # creates the auxiliary prefix, to be used to create an unique
                    # virtual table name for joining the tables, note that if the
                    # current relation is from a parent class the table name must
                    # be appended to the prefix
                    if entity_class == _entity_class: _prefix = prefix or _table_name
                    else: _prefix = prefix and prefix + "___" + _table_name or _table_name

                    # in case the "mapper" is not defined, this relation
                    # is considered to be an indirect relation (uses
                    # relation table), the appropriate select query code
                    # must be created
                    if not mapper:
                        query_buffer.write(" left join ")
                        query_buffer.write(relation_unique)
                        query_buffer.write(" ")
                        query_buffer.write(fqn + relation_unique)
                        query_buffer.write(" on ")
                        query_buffer.write(_prefix + "." + table_id)
                        query_buffer.write(" = ")
                        query_buffer.write(fqn + relation_unique + "." + _table_name)
                        query_buffer.write(" left join ")
                        query_buffer.write(target_table_name)
                        query_buffer.write(" ")
                        query_buffer.write(fqn)
                        query_buffer.write(" on ")
                        query_buffer.write(fqn + relation_unique + "." + target_table_name)
                        query_buffer.write(" = ")
                        query_buffer.write(fqn + "." + target_table_id)

                    # in case this relation is mapped this means the relation
                    # is mapped in the table associated with the current entity model
                    # and the query code should reflect the join on this foreign
                    # key field element
                    elif is_mapped:
                        query_buffer.write(" left join ")
                        query_buffer.write(target_table_name)
                        query_buffer.write(" ")
                        query_buffer.write(fqn)
                        query_buffer.write(" on ")
                        query_buffer.write(_prefix + "." + table_relation)
                        query_buffer.write(" = ")
                        query_buffer.write(fqn + "." + target_table_id)

                    # in case the relation is not mapped in the current entity model
                    # the reverse foreign key must be used in the query code
                    else:
                        # retrieves the name of the reverse relation (attribute)
                        # for the current table relation, this attribute
                        # is the name of the relation in the target entity
                        reverse = _entity_class.get_reverse(table_relation)

                        query_buffer.write(" left join ")
                        query_buffer.write(target_table_name)
                        query_buffer.write(" ")
                        query_buffer.write(fqn)
                        query_buffer.write(" on ")
                        query_buffer.write(_prefix + "." + table_id)
                        query_buffer.write(" = ")
                        query_buffer.write(fqn + "." + reverse)

                    # retrieves all the parent class for the target
                    # relation class, these are going to be used for
                    # joining the relation with it's parents (parent
                    # joining process)
                    target_all_parents = target_class.get_all_parents()

                    # iterates over all the (target) parents to create the
                    # proper joins to retrieve it's values
                    for parent in target_all_parents:
                        # in case the parent class is abstract no need to join
                        # it into the current query
                        if parent.is_abstract(): continue

                        # retrieves the name of the parent table
                        # and uses it to construct the (fqn) name of
                        # the parent target table
                        parent_name = parent.get_name()
                        fqn_parent = fqn + "___" + parent_name

                        query_buffer.write(" left join ")
                        query_buffer.write(parent_name)
                        query_buffer.write(" ")
                        query_buffer.write(fqn_parent)
                        query_buffer.write(" on ")
                        query_buffer.write(fqn + "." + target_table_id)
                        query_buffer.write(" = ")
                        query_buffer.write(fqn_parent + "." + target_table_id)

                    # retrieves and normalizes "new" options for the current
                    # relation and uses them in conjunction with the new prefix
                    # value to join the tables for the relation
                    _options = eager.get(table_relation, {})
                    _options = _options and self.normalize_options(_options) or _options
                    join_tables(target_class, _options, prefix + "__" + table_relation)

        join_tables(entity_class, options)

    def _filter_query_f(self, entity_class, options, query_buffer):
        # starts the is first flag, this flag is going to
        # controls the where clause, setting it (in the query buffer)
        # when the first filter is processed
        is_first = True

        def _filter_eager(entity_class, options, prefix = "", is_first = True):
            # retrieves all the eager loading relations, to be able to
            # filter possible values in them
            eager = options.get("eager", {})

            # iterates over all the eager items to run their
            # filters and call the recursion step on their
            # options (possible sub-eager values)
            for relation, _eager in eager.items():
                # normalizes the eager loading options, to
                # be able to process them correctly
                _eager = self.normalize_options(_eager)

                # retrieves the various filters to be set
                # for the relation
                _filters = _eager.get("filters", [])

                # retrieves the target class for the relations to
                # filtered and processed, then uses the current prefix
                # to construct the complete table name of the relation
                target_class = entity_class.get_target(relation)
                table_name = prefix + "__" + relation

                # iterates over all the filters in the relation
                # to be able to process them correctly, creating
                # the appropriate filter code in the query
                for _filter in _filters:
                    is_first = self._process_filter(target_class, table_name, _filter, query_buffer, is_first)

                is_first = _filter_eager(target_class, _eager, table_name, is_first)

            return is_first

        is_first = _filter_eager(entity_class, options, "", is_first)

        # retrieves the various top level filters in the top level
        # queries
        filters = options.get("filters", [])

        # iterates over all the filters to process
        # them, generating the proper query code,
        # these are the top level filters associated
        # with the root entity
        for filter in filters:
            is_first = self._process_filter(entity_class, None, filter, query_buffer, is_first)

    def _order_query_f(self, entity_class, options, query_buffer):
        # retrieves the order by values, these values represent
        # the various field to be used to order the result and
        # the way of the order to be used
        order_by = options.get("order_by", ())

        # in case the order by option is not set no need to
        # write any information to the query buffer, returns
        # immediately with no change
        if not order_by: return

        # writes the initial order by reference into the
        # query string buffer to indicate the order by request
        query_buffer.write(" order by ")

        # sets the is first flag for the initial order
        # by iteration value
        is_first = True

        # iterates over all the order by values to write their
        # orders into the query buffer
        for order_by_value in order_by:
            # unpacks the order by value into the name of
            # the item to be used in the order and the order
            # "direction" to be used for the item
            name, order = order_by_value

            # in case the operator separator is present in the
            # name, must retrieve it otherwise operator is invalidated
            if ":" in name: operator, name = name.split(":", 1)
            else: operator = None

            # tries to resolve the operator into the appropriate one
            # (uses the engine internals) only does this in case the
            # operator is correclty set and retrieved
            operator = operator and self.engine._resolve_operator(operator) or operator

            # writes the comma to the query buffer only in case the
            # is first flag is not set
            is_first = not is_first and query_buffer.write(", ")

            # resolves the fully qualified name into the query escaped
            # version of it for query ordering and then writes it into
            # the query buffer
            name = self._resolve_name(entity_class, name)
            operator and query_buffer.write(operator + "(")
            query_buffer.write(name)
            operator and query_buffer.write(")")

            # writes the order of the order by into the query buffer
            # the value of the writing is the query oriented simplified
            # order string values
            if order == "ascending": query_buffer.write(" asc")
            elif order == "descending": query_buffer.write(" desc")

    def _limit_query_f(self, entity_class, options, query_buffer):
        # retrieves the range values, these values represent
        # both the start records (index value) and the number
        # of records the length of the query set retrieval
        start_record = options.get("start_record", -1)
        number_records = options.get("number_records", -1)

        # writes the limit part of the query to limit it
        # to the options defined limit, in case no limit is
        # defined no limit is written
        if number_records > -1:
            # writes the offset part of the filter query
            # according to the defined number of records
            query_buffer.write(" limit ")
            query_buffer.write(str(number_records))

        # writes the offset part of the query to set the offset
        # according to the options defined offset, in case no
        # offset is defined no offset is written
        if number_records > -1:
            # writes the offset part of the filter query
            # according to the defined start record
            query_buffer.write(" offset ")
            query_buffer.write(str(start_record))

    def _process_filter(self, entity_class, table_name, filter, query_buffer, is_first = True):
        # in case the is first flag
        # is set, need to write the initial
        # where clause to the query buffer
        if is_first:
            # adds the where operator in the query buffer
            query_buffer.write(" where (")

            # unsets the is first flag
            is_first = False
        # otherwise the and operator
        # must be added to the query buffer
        else:
            # adds the and operator in the query buffer
            query_buffer.write(" and (")

        # retrieves the filter type and then uses
        # it to retrieve the appropriate filter method
        filter_type = filter["type"]
        filter_method = getattr(self, "_process_filter_" + filter_type)

        # calls the filter method, updating the contents of the query
        # buffer accordingly
        filter_method(entity_class, table_name, filter, query_buffer)

        # writes the end of the filter
        query_buffer.write(")")

        # returns the is first flag value, useful
        # for latter avoid calls
        return is_first

    def _process_table_name(self, entity_class, table_name, name):
        """
        "Processes" the table name for the current entity class, table
        name and (attribute) name context.

        This processing includes the complete resolution of the table
        name according to the join naming convention.
        The created table name should be a reference in accordance with
        the joining of the various tables.

        The retrieved table name should respect one of the following
        conventions:
        1. table_name.[attribute_name]
        2. __relation___top_table_name.[attribute_name]

        @type entity_class: EntityClass
        @param entity_class: The entity class that is the current context
        of the select
        @type table_name: String
        @param table_name: The name of the current table context, that
        may be used as the prefix value for the composed table name.
        @type name: String
        @param name: The name of the attribute to be used to resolve
        the complete (composed) table name of the current context.
        @rtype: String
        @return: The resolved complete table name for the current context.
        """

        # retrieves the names map for the entity class to resolve
        # the proper entity class (responsible) for the current name
        # and then retrieves the table name as the resolved entity
        # class name
        names_map = entity_class.get_names_map()
        _entity_class = names_map.get(name, entity_class)
        _table_name = _entity_class.get_name()

        # in case the current name is a reserved name (special case)
        # the table name is nor completely resolved and instead is
        # returned immediately as the current  table name
        if name in RESERVED_NAMES: return table_name or _table_name

        # in case the table name is not defined, this is the top level
        # filtering entity and must be considered an exceptional case
        # (only the entity parent class is considered)
        if not table_name:
            # sets the table name as the single entitie's
            # table name
            table_name = _table_name
        # otherwise in case the entity class is not the current entity
        # class the table name must be created as a composed table name
        elif not _entity_class == entity_class:
            # composes the table name with the previous table name
            # (prefix) and the current entitie's table name
            table_name = table_name + "___" + _table_name

        # returns the "processed" table name to be used
        # in the context of the name execution
        return table_name

    def _process_filter_equals(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # checks if the current filter is of type post
        # in such case an patch may have to be applied
        # to force post processing
        is_post = filter.get("post", False)

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the equals filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name and value
            # this are the values that are going to be
            # used for filtering
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # validates that the filter field name exists in the
            # context of the entity class and validates that the
            # value of filter field value is also valid as a type
            # (this is a security validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)
            entity_class._validate_value(filter_field_name, filter_field_value)

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name + (is_post and " + 0" or "")

            # converts the filter field value into an appropriate sql representation
            # and writes the filter into the sql query value
            filter_field_sql_value = entity_class._get_sql_value(filter_field_name, filter_field_value)
            query_buffer.write(field_name + " = " + filter_field_sql_value)

    def _process_filter_not_equals(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the not equals filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name and value
            # this are the values that are going to be
            # used for filtering
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # validates that the filter field name exists in the
            # context of the entity class and validates that the
            # value of filter field value is also valid as a type
            # (this is a security validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)
            entity_class._validate_value(filter_field_name, filter_field_value)

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name

            # converts the filter field value into an appropriate sql representation
            # and writes the filter into the sql query value
            filter_field_sql_value = entity_class._get_sql_value(filter_field_name, filter_field_value)
            query_buffer.write("not " + field_name + " = " + filter_field_sql_value)

    def _process_filter_in(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the in filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query buffer
                query_buffer.write(" or ")

            # retrieves the filter field name and value
            # this are the values that are going to be
            # used for filtering
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # validates that the filter field name exists in the
            # context of the entity class and validates that the
            # value of filter field value is also valid as a type
            # (this is a security validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)
            [entity_class._validate_value(filter_field_name, value) for value in filter_field_value]

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name

            # creates the sql value for the filter field to be used in the in filter
            # this value is a list of values casted with the proper sql value
            filter_field_sql_value_list = [entity_class._get_sql_value(filter_field_name, value) for value in filter_field_value]
            filter_field_sql_value = "(" + ", ".join(filter_field_sql_value_list) + ")"

            # writes the in clause in the query buffer
            query_buffer.write(field_name + " in " + filter_field_sql_value)

    def _process_filter_not_in(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the not in filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name and value
            # this are the values that are going to be
            # used for filtering
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # validates that the filter field name exists in the
            # context of the entity class and validates that the
            # value of filter field value is also valid as a type
            # (this is a security validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)
            [entity_class._validate_value(filter_field_name, value) for value in filter_field_value]

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name

            # creates the sql value for the filter field to be used in the in filter
            # this value is a list of values casted with the proper sql value
            filter_field_sql_value_list = [entity_class._get_sql_value(filter_field_name, value) for value in filter_field_value]
            filter_field_sql_value = "(" + ", ".join(filter_field_sql_value_list) + ")"

            # writes the in clause not in the query buffer
            query_buffer.write("not " + field_name + " in " + filter_field_sql_value)

    def _process_filter_like(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields and
        # like filter type
        filter_fields = filter["fields"]
        like_type = filter.get("like_type", "both")

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the like filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name and value
            # this are the values that are going to be
            # used for filtering
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # validates that the filter field name exists in the
            # context of the entity class and validates that the
            # value of filter field value is also valid as a type
            # (this is a security validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)
            entity_class._validate_value(filter_field_name, filter_field_value)

            # escapes the filter field value, to remove any
            # possible problem (or injection) in the value field
            filter_field_value = self._escape_text(filter_field_value)

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name

            # creates a new buffer for the filter field value
            filter_field_value_buffer = colony.libs.string_buffer_util.StringBuffer()

            # sets the is first filter field
            # value flag
            is_first_filter_field_value = True

            # iterates over all the splitted filter
            # field values (separates the words for the like)
            for splitted_filter_value in filter_field_value.split():
                # in case the is first filter field
                # value is set
                if is_first_filter_field_value:
                    # unsets the is first filter field
                    # value
                    is_first_filter_field_value = False
                # otherwise the wildcard operator must
                # be added to the filter field value
                else:
                    # writes the wildcard operator
                    # in the filter field value buffer
                    filter_field_value_buffer.write("%")

                # writes the splitted filter value into
                # the filter field value buffer
                filter_field_value_buffer.write(splitted_filter_value)

            # writes the initial part of the like operand
            # in the query buffer
            query_buffer.write(field_name + " like ")

            # in case the like type is left
            # or both, the initial part must be wildcard
            if like_type in ("left", "both"):
                # writes the wildcard to the query
                # buffer
                query_buffer.write("'%")
            # otherwise no wildcard is set at the
            # initial (left) part of the string
            else:
                # writes the initial string to the
                # query buffer
                query_buffer.write("'")

            # retrieves the filter field value string (from buffer) and
            # writes it into the query buffer
            filter_field_value_string = filter_field_value_buffer.get_value()
            query_buffer.write(filter_field_value_string)

            # in case the like type is right
            # or both, the final part must be wildcard
            if like_type in ("right", "both"):
                # writes the wildcard to the query
                # buffer
                query_buffer.write("%'")
            # otherwise no wildcard is set at the
            # final (right) part of the string
            else:
                # writes the final string to the
                # query buffer
                query_buffer.write("'")

    def _process_filter_greater(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the greater filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name and value
            # this are the values that are going to be
            # used for filtering
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # validates that the filter field name exists in the
            # context of the entity class and validates that the
            # value of filter field value is also valid as a type
            # (this is a security validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)
            entity_class._validate_value(filter_field_name, filter_field_value)

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name

            # converts the filter field value into an appropriate sql representation
            # and writes the filter into the sql query value
            filter_field_sql_value = entity_class._get_sql_value(filter_field_name, filter_field_value)
            query_buffer.write(field_name + " > " + filter_field_sql_value)

    def _process_filter_greater_equal(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the greater or equal filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name and value
            # this are the values that are going to be
            # used for filtering
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # validates that the filter field name exists in the
            # context of the entity class and validates that the
            # value of filter field value is also valid as a type
            # (this is a security validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)
            entity_class._validate_value(filter_field_name, filter_field_value)

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name

            # converts the filter field value into an appropriate sql representation
            # and writes the filter into the sql query value
            filter_field_sql_value = entity_class._get_sql_value(filter_field_name, filter_field_value)
            query_buffer.write(field_name + " >= " + filter_field_sql_value)

    def _process_filter_lesser(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the lesser filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name and value
            # this are the values that are going to be
            # used for filtering
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # validates that the filter field name exists in the
            # context of the entity class and validates that the
            # value of filter field value is also valid as a type
            # (this is a security validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)
            entity_class._validate_value(filter_field_name, filter_field_value)

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name

            # converts the filter field value into an appropriate sql representation
            # and writes the filter into the sql query value
            filter_field_sql_value = entity_class._get_sql_value(filter_field_name, filter_field_value)
            query_buffer.write(field_name + " < " + filter_field_sql_value)

    def _process_filter_lesser_equal(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the lesser or equal filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name and value
            # this are the values that are going to be
            # used for filtering
            filter_field_name = filter_field["name"]
            filter_field_value = filter_field["value"]

            # validates that the filter field name exists in the
            # context of the entity class and validates that the
            # value of filter field value is also valid as a type
            # (this is a security validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)
            entity_class._validate_value(filter_field_name, filter_field_value)

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name

            # converts the filter field value into an appropriate sql representation
            # and writes the filter into the sql query value
            filter_field_sql_value = entity_class._get_sql_value(filter_field_name, filter_field_value)
            query_buffer.write(field_name + " <= " + filter_field_sql_value)

    def _process_filter_is_null(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # checks if the current filter is of type post
        # in such case an patch may have to be applied
        # to force post processing
        is_post = filter.get("post", False)

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the is null filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name that is
            # going to be used for filtering
            filter_field_name = filter_field["name"]

            # validates that the filter field name exists in the
            # context of the entity class (this is a security
            # validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name + (is_post and " + 0" or "")

            # writes the filter into the sql query value (the field name
            # is validated as null)
            query_buffer.write(field_name + " is null")

    def _process_filter_is_not_null(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filter fields
        filter_fields = filter["fields"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter fields
        # to set the is not null filter
        for filter_field in filter_fields:
            # in case the is first flag
            # is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or ")

            # retrieves the filter field name that is
            # going to be used for filtering
            filter_field_name = filter_field["name"]

            # validates that the filter field name exists in the
            # context of the entity class (this is a security
            # validation to avoid possible injection)
            entity_class._validate_name(filter_field_name)

            # process the "complete" table name (includes back relation references)
            # and then uses it to construct the complete field name
            _table_name = self._process_table_name(entity_class, table_name, filter_field_name)
            field_name = _table_name + "." + filter_field_name

            # writes the filter into the sql query value (the field name
            # is validated as null)
            query_buffer.write(field_name + " is not null")

    def _process_filter_or(self, entity_class, table_name, filter, query_buffer):
        # retrieves the filters
        filters = filter["filters"]

        # sets the is first flag
        is_first = True

        # iterates over all the filter
        # to set the or filter
        for _filter in filters:
            # in case the is first flag
            # is set
            if is_first:
                # writes the start of the filter
                query_buffer.write("(")

                # unsets the is first flag
                is_first = False
            # otherwise the or operand must
            # be added to the query string buffer
            else:
                # adds the or operator in the query
                # buffer
                query_buffer.write(" or (")

            # retrieves the filter type and then uses
            # it to retrieve the appropriate filter method
            filter_type = _filter["type"]
            filter_method = getattr(self, "_process_filter_" + filter_type)

            # calls the filter method, updating the contents of the query
            # string buffer accordingly
            filter_method(entity_class, table_name, _filter, query_buffer)

            # writes the end of the filter
            query_buffer.write(")")

    def _find_result(self, entity_class, field_names, options, cursor):
        # retrieves the map option from the options map
        # this option should provide information of how the
        # returns result set should be converted, in case the
        # option is set a set of maps must be returned instead
        # of the usual entity instances
        map = options.get("map", False)

        # retrieves the set options from the options map
        # this options "decides" if the result set should
        # be processed or not, in case the result is not
        # processed the processing time is greatly reduced
        set = options.get("set", False)

        # retrieves the count option, in case this option
        # is set the return values must be a single integer
        # value indicating the number of results (rows) for
        # the query (non complete parsing)
        count = options.get("count", False)

        try:
            # retrieves the result set (all the) items
            # available for fetching
            result_set = cursor.fetchall()
        finally:
            # closes the cursor
            cursor.close()

        # in case the count option is set the return
        # value is the number of results (rows) for
        # the query and so this value is returned
        # immediately (no complete parsing)
        if count: return result_set[0][0]

        # in case the set flag is set no need to unpack the
        # results and the proper result set is returned,
        # together with the names of the various fields
        if set: return self._apply_names_set(result_set, field_names)

        # unpacks the result set using the appropriate method
        # in case the map option is set the map method must be
        # used, otherwise the entity (instances) based method
        # should be used instead
        if map: result = self._unpack_result_m(entity_class, field_names, options, result_set)
        else: result = self._unpack_result_e(entity_class, field_names, options, result_set)

        # returns the unpacked result set that must contain either
        # a set of maps or a set of instances
        return result

    def _unpack_result_e(self, entity_class, field_names, options, result_set):
        # retrieves the map of entities, per class for fast
        # cache access in case one is provided in the options
        # then retrieves the (diffusion) scope for query execution
        # the final option is controls if the to many relations
        # must be sorted according to their identifier (this strategy
        # is aimed at guaranteeing some sort of order to their values)
        entities = options.get("entities", None)
        scope = options.get("scope", None)
        sort = options.get("sort", True)

        # creates the map that will hold the various
        # retrieved entities, organized by entity class,
        # an existent map is used in case one is passed
        # (this map will hold the entities cache)
        if entities == None: entities = {}

        # creates the map that will hold the scope parameters,
        # this map is going to be used to share state along
        # the various elements of the diffusion scope
        if scope == None: scope = {}

        # creates the map that will hold the various entities
        # indexed by their primary identifier for easy validation
        # (allows fast item presence checking) also creates a list
        # to hold the ordered version of the entities
        _entities_map = {}
        _entities_list = []

        # retrieves the table id attribute of the
        # current entity class, provides way to get
        # the unique id value for indexing
        table_id = entity_class.get_id()

        total_time_map = 0
        total_time_set = 0
        total_time_populate = 0
        total_time_relation_loading = 0
        total_time_proper_setting = 0

        # retrieves the database encoding, this is going to
        # be used in the value conversion from sql
        database_encoding = self.engine.get_database_encoding()

        # iterates over all the results present in the
        # result set to populate the various entity
        # classes
        for result in result_set:
            intial = time.clock()

            # creates the "result map" containing a map
            # associating the various field names with
            # the values of them, this map is useful
            # for key based access to the result
            result_map = dict(zip(field_names, result))

            total_time_map += time.clock() - intial

            # retrieves the id (value) from the result
            # to check if it has been already indexed
            # the current entity
            id = result_map[table_id]

            # retrieves the current class using the "descriminator"
            # for the retrieval of the entity definition
            current_class_name = result_map["_class"]
            current_class = self.entities_map.get(current_class_name, structures.EntityClass)

            # in case the current class does not exists in the
            # map of entities the map reference must be created
            # and set on the entities map
            if not current_class in entities:
                # creates a new map reference to hold all the entities
                # of the entity class index by the identifier value
                entities[current_class] = {}

            # in case the identifier value is not found for the current
            # class in the entities map a new entity instance must be
            # creates and set in the proper place "inside" the entities
            # map (for latter possible re-usage)
            if not id in entities[current_class]:
                # creates a new entity instance and associates it
                # with the entities "cache" map
                entities[current_class][id] = current_class.build(self, entities, scope)

            # retrieves the entity reference from the map
            # of entities cache (cache retrieval)
            entity = entities[current_class][id]

            intial = time.clock()

            # checks if the current entity is not yet present
            # in the map containing the entities in case it's
            # not the internal entities structures must be
            # updated accordingly
            if not id in _entities_map:
                # updates both the map containing the various
                # entity reference and the list that holds the
                # entities in an ordered fashion
                _entities_map[id] = entity
                _entities_list.append(entity)

            total_time_set += time.clock() - intial

            intial = time.clock()

            # iterates over all the results in the results map
            # to "populate" the current entity (and relations)
            for item_name, item_value in result_map.items():

                #@TODO: this kind of parsing must be removed because
                # it is too expensive

                # splits the item name around the dot separation
                # token to create the item path
                item_path = item_name.split(".")

                # retrieves the attribute path and name
                # from the (complete) item path
                attribute_path = item_path[:-1]
                attribute_name = item_path[-1]



                # unsets the error flag, by default no
                # error should occur, during the path traversing
                error_flag = False

                # sets the "initial" entity and class in
                # the attribute path traversing, this values
                # are the current references in the iteration
                _entity = entity
                _class = current_class


                #@TODO: remove this create it's not always
                # necessary
                current_path = str()


                intial_relation_loading = time.clock()

                # "traverses" the complete attribute path to
                # progressively retrieve or create the relation
                # objects
                for attribute_partial in attribute_path:
                    # in case the class reference does not contains
                    # reference to the current partial attribute name
                    # there is no reference is definition (error situation)
                    if not hasattr(_class, attribute_partial):
                        # sets the error flag, no definition
                        # and breaks the traversing loop
                        error_flag = True
                        break


                    current_path += attribute_partial + "."


                    # retrieves the relation attributes for the current
                    # relation, then retrieves the target relation class
                    # and the id (key) for the relation
                    relation = _class.get_relation(attribute_partial)
                    target_class = _class.get_target(attribute_partial)
                    target_id = target_class.get_id()

                    # retrieves the value of the id attribute of the target relation
                    # class, this value is going to be used to check for existing
                    # entity
                    target_id_value = result_map.get(current_path + target_id, None)

                    # in case the identifier value is not found in the result
                    # map it's not possible to process the relation
                    if target_id_value == None:
                        # sets the "new" entity as invalid, because it cannot
                        # be correctly parsed
                        _new_entity = None

                    # otherwise the target identifier value was found and so
                    # it may be used to retrieve a possible existing entity
                    # so it may be re-used
                    else:
                        # retrieves the target class using the "descriminator"
                        # for the retrieval of the entity definition, the name
                        # of the class must be resolved into the proper class instance
                        target_class_name = result_map[current_path + "_class"]
                        target_class = self.entities_map.get(target_class_name, structures.EntityClass)

                        # in case the target class does not exists in the
                        # map of entities the map reference must be created
                        # and set on the entities map
                        if not target_class in entities:
                            # creates a new map reference to hold all the entities
                            # of the entity class index by the identifier value
                            entities[target_class] = {}

                        # in case the identifier value is not found for the current
                        # class in the entities map a new entity instance must be
                        # creates and set in the proper place "inside" the entities
                        # map (for latter possible re-usage)
                        if not target_id_value in entities[target_class]:
                            # creates a new entity class and associates it
                            # with the entities "cache" map
                            entities[target_class][target_id_value] = target_class.build(self, entities, scope)

                        # retrieves the "new" entity from the entities map, taking
                        # into account the proper target class and the current
                        # identifier value (the new entity is the entity for the
                        # current iteration cycle)
                        _new_entity = entities[target_class][target_id_value]

                    # retrieves the type of the current relation, this will
                    # provide information about how to handle the "new" entity
                    relation_type = relation["type"]

                    # in case the relation is of type to many must
                    # check for current values in the sequence and
                    # add new values in case they do not exist
                    if relation_type == "to-many":
                        # in case the current attribute is not yet present
                        # in the entity, must create a new list to hold the
                        # the various values (it's going to be a "journaled"
                        # list to map the updated)
                        if not attribute_partial in _entity.__dict__:
                            # creates and sets the new list to hold the various
                            # to many relation values in the attribute
                            setattr(_entity, attribute_partial, colony.libs.structures_util.JournaledList())

                        # retrieves the list containing the relation values
                        # this is going to be used to set the entity on it
                        relation_list = getattr(_entity, attribute_partial)

                        # checks if the "new" entity is present in the relation
                        # list and in case it's not sets it in the relations list
                        #@todo: this is slow as hell (must check presence in list)
                        if not _new_entity in relation_list: _new_entity and relation_list._append(_new_entity)

                    # otherwise it must be a to one relation and sets the setting
                    # of the "new" entity is just a trivial set on the entity
                    else:
                        # sets the "new" entity in the entity as just a trivial
                        # setting, (normal case)
                        setattr(_entity, attribute_partial, _new_entity)

                    # updates the current entity and classes references
                    # with the new entity and class references, this should
                    # ensure integrity in the relation percolation
                    _entity = _new_entity
                    _class = _entity and target_class

                total_time_relation_loading += time.clock() - intial_relation_loading

                intial_proper = time.clock()

                # in case the error flag is set,
                # this attribute must be skipped
                if error_flag == True:
                    # continues the loop, skips
                    # the current attribute
                    continue

                # in case the class (for the entity) does not contain
                # a reference to the current attribute (not valid)
                if not hasattr(_class, attribute_name):
                    # continues the loop, ignoring
                    # the current item
                    continue

                # in case the entity already contains a value
                # for the current attribute (no overlap)
                if _entity.has_value(attribute_name):
                    # continues the loop, ignoring the
                    # attribute (avoid overlap)
                    continue

                # sets the item value (sql value) in the entity, converting
                # it into the correct representation before setting
                # it into the entity, sql conversion
                _entity.set_sql_value(attribute_name, item_value, encoding = database_encoding)

                total_time_proper_setting += time.clock() - intial_proper

            total_time_populate += time.clock() - intial

        #print "map: " + str(total_time_map)
        #print "set: " + str(total_time_set)
        #print "populate: " + str(total_time_populate)
        #print "relation_loading: " + str(total_time_relation_loading)
        #print "proper_setting: " + str(total_time_proper_setting)

        # in case the sort flag is not set no need to
        # continue (only sorting is missing) returns
        # the list of retrieved entities immediately
        if not sort: return _entities_list

        # iterate over all the entities in the entities list to run the
        # method that ensures order in the to many relation values, this
        # is very important to ensure a minimal and primary order in their
        # values (the running of this sorting is recursive)
        for entity in _entities_list: self._sort_to_many_e(entity, entity_class)

        # returns the list of retrieved entities,
        # the final result set (ordered list)
        return _entities_list

    def _unpack_result_m(self, entity_class, field_names, options, result_set):
        # retrieves the map of entities, per class for fast
        # cache access in case one is provided in the options
        # then retrieves the (diffusion) scope for query execution
        # the final option is controls if the to many relations
        # must be sorted according to their identifier (this strategy
        # is aimed at guaranteeing some sort of order to their values)
        entities = options.get("entities", None)
        scope = options.get("scope", None)
        sort = options.get("sort", True)

        # retrieves the table id attribute of the
        # current entity class, provides way to get
        # the unique id value for indexing
        table_id = entity_class.get_id()

        # creates the map that will hold the various
        # retrieved entities, organized by entity class,
        # an existent map is used in case one is passed
        # (this map will hold the entities cache)
        if entities == None: entities = {}

        # creates the map that will hold the scope parameters,
        # this map is going to be used to share state along
        # the various elements of the diffusion scope
        if scope == None: scope = {}

        # creates the map that will hold the various entities
        # indexed by their primary identifier for easy validation
        # (allows fast item presence checking) also creates a list
        # to hold the ordered version of the entities
        _entities_map = {}
        _entities_list = []

        # retrieves the database encoding, this is going to
        # be used in the value conversion from sql
        database_encoding = self.engine.get_database_encoding()

        total_time_map = 0
        total_time_set = 0
        total_time_populate = 0
        total_time_relation_loading = 0
        total_time_proper_setting = 0

        # iterates over all the results present in the
        # result set to populate the various maps
        for result in result_set:
            intial = time.clock()

            # creates the "result map" containing a map
            # associating the various field names with
            # the values of them, this map is useful
            # for key based access to the result
            result_map = dict(zip(field_names, result))

            total_time_map += time.clock() - intial

            # retrieves the id (value) from the result
            # to check if it has been already indexed
            # the current entity
            id = result_map[table_id]

            # retrieves the current class using the "descriminator"
            # for the retrieval of the entity definition
            current_class_name = result_map["_class"]
            current_class = self.entities_map.get(current_class_name, structures.EntityClass)

            # retrieves the current modified time value for the
            # current entity class level
            current_modified_time = result_map["_mtime"]

            # in case the current class does not exists in the
            # map of entities the map reference must be created
            # and set on the entities map
            if not current_class in entities:
                # creates a new map reference to hold all the entities
                # of the entity class index by the identifier value
                entities[current_class] = {}

            # in case the identifier value is not found for the current
            # class in the entities map a new entity instance must be
            # creates and set in the proper place "inside" the entities
            # map (for latter possible re-usage)
            if not id in entities[current_class]:
                # creates a new entity instance and associates it
                # with the entities "cache" map, note that the class
                # attribute is set in the new map
                entities[current_class][id] = {
                    "_class" : current_class_name,
                    "_mtime" : current_modified_time
                }

            # retrieves the entity reference from the map
            # of entities cache (cache retrieval)
            entity = entities[current_class][id]

            intial = time.clock()

            # checks if the current entity is not yet present
            # in the map containing the entities in case it's
            # not the internal entities structures must be
            # updated accordingly
            if not id in _entities_map:
                # updates both the map containing the various
                # entity reference and the list that holds the
                # entities in an ordered fashion
                _entities_map[id] = entity
                _entities_list.append(entity)


            total_time_set += time.clock() - intial

            intial = time.clock()

            # iterates over all the results in the results map
            # to "populate" the current entity (and relations)
            for item_name, item_value in result_map.items():

                #@TODO: this kind of parsing must be removed because
                # it is too expensive

                # splits the item name around the dot separation
                # token to create the item path
                item_path = item_name.split(".")

                # retrieves the attribute path and name
                # from the (complete) item path
                attribute_path = item_path[:-1]
                attribute_name = item_path[-1]



                # unsets the error flag, by default no
                # error should occur, during the path traversing
                error_flag = False

                # sets the "initial" entity and class in
                # the attribute path traversing, this values
                # are the current references in the iteration
                _entity = entity
                _class = current_class


                #@TODO: remove this create it's not always
                # necessary
                current_path = str()


                intial_relation_loading = time.clock()

                # "traverses" the complete attribute path to
                # progressively retrieve or create the relation
                # objects
                for attribute_partial in attribute_path:
                    # in case the class reference does not contains
                    # reference to the current partial attribute name
                    # there is no reference is definition (error situation)
                    if not hasattr(_class, attribute_partial):
                        # sets the error flag, no definition
                        # and breaks the traversing loop
                        error_flag = True
                        break


                    current_path += attribute_partial + "."


                    # retrieves the relation attributes for the current
                    # relation, then retrieves the target relation class
                    # and the id (key) for the relation
                    relation = _class.get_relation(attribute_partial)
                    target_class = _class.get_target(attribute_partial)
                    target_id = target_class.get_id()

                    # retrieves the value of the id attribute of the target relation
                    # class, this value is going to be used to check for existing
                    # entity
                    target_id_value = result_map.get(current_path + target_id, None)

                    # in case the identifier value is not found in the result
                    # map it's not possible to process the relation
                    if target_id_value == None:
                        # sets the "new" entity as invalid, because it cannot
                        # be correctly parsed
                        _new_entity = None

                    # otherwise the target identifier value was found and so
                    # it may be used to retrieve a possible existing entity
                    # so it may be re-used
                    else:
                        # retrieves the target class using the "descriminator"
                        # for the retrieval of the entity definition, the name
                        # of the class must be resolved into the proper class instance
                        target_class_name = result_map[current_path + "_class"]
                        target_class = self.entities_map.get(target_class_name, structures.EntityClass)

                        # retrieves the target modified time, to be set in the create
                        # map representing the entity, this may be used to check the
                        # last time the entity was modified
                        target_modified_time = result_map[current_path + "_mtime"]

                        # in case the target class does not exists in the
                        # map of entities the map reference must be created
                        # and set on the entities map
                        if not target_class in entities:
                            # creates a new map reference to hold all the entities
                            # of the entity class index by the identifier value
                            entities[target_class] = {}

                        # in case the identifier value is not found for the current
                        # class in the entities map a new entity instance must be
                        # creates and set in the proper place "inside" the entities
                        # map (for latter possible re-usage)
                        if not target_id_value in entities[target_class]:
                            # creates a new entity class and associates it
                            # with the entities "cache" map, note that the
                            # class attribute is set in the new map
                            entities[target_class][target_id_value] = {
                                "_class" : target_class_name,
                                "_mtime" : target_modified_time
                            }

                        # retrieves the "new" entity from the entities map, taking
                        # into account the proper target class and the current
                        # identifier value (the new entity is the entity for the
                        # current iteration cycle)
                        _new_entity = entities[target_class][target_id_value]

                    # retrieves the type of the current relation, this will
                    # provide information about how to handle the "new" entity
                    relation_type = relation["type"]

                    # in case the relation is of type to many must
                    # check for current values in the sequence and
                    # add new values in case they do not exist
                    if relation_type == "to-many":
                        # in case the current attribute is not yet present
                        # in the entity, must create a new list to hold the
                        # the various values
                        if not attribute_partial in _entity:
                            # creates and sets the new list to hold the various
                            # to many relation values in the attribute
                            _entity[attribute_partial] = []

                        # retrieves the list containing the relation values
                        # this is going to be used to set the entity on it
                        relation_list = _entity[attribute_partial]

                        # checks if the "new" entity is present in the relation
                        # list and in case it's not sets it in the relations list
                        #@todo: this is slow as hell (must check presence in list)
                        if not _new_entity in relation_list: _new_entity and relation_list.append(_new_entity)

                    # otherwise it must be a to one relation and sets the setting
                    # of the "new" entity is just a trivial set on the entity
                    else:
                        # sets the "new" entity in the entity as just a trivial
                        # setting, (normal case)
                        _entity[attribute_partial] = _new_entity

                    # updates the current entity and classes references
                    # with the new entity and class references, this should
                    # ensure integrity in the relation percolation
                    _entity = _new_entity
                    _class = not _entity == None and target_class

                total_time_relation_loading += time.clock() - intial_relation_loading

                intial_proper = time.clock()

                # in case the error flag is set,
                # this attribute must be skipped
                if error_flag == True:
                    # continues the loop, skips
                    # the current attribute
                    continue

                # in case the class (for the entity) does not contain
                # a reference to the current attribute (not valid)
                if not hasattr(_class, attribute_name):
                    # continues the loop, ignoring
                    # the current item
                    continue

                # converts the item value into the appropriate value
                # representation and sets it into the entity (map) in
                # the correct attribute name
                _entity[attribute_name] = _class._from_sql_value(attribute_name, item_value, encoding = database_encoding)

                total_time_proper_setting += time.clock() - intial_proper

            total_time_populate += time.clock() - intial

        #print "map: " + str(total_time_map)
        #print "set: " + str(total_time_set)
        #print "populate: " + str(total_time_populate)
        #print "relation_loading: " + str(total_time_relation_loading)
        #print "proper_setting: " + str(total_time_proper_setting)

        # in case the sort flag is not set no need to
        # continue (only sorting is missing) returns
        # the list of retrieved entities immediately
        if not sort: return _entities_list

        # iterate over all the entities in the entities list to run the
        # method that ensures order in the to many relation values, this
        # is very important to ensure a minimal and primary order in their
        # values (the running of this sorting is recursive)
        for entity in _entities_list: self._sort_to_many_m(entity, entity_class)

        # returns the list of retrieved entities,
        # the final result set (ordered list)
        return _entities_list

    def _sort_to_many_e(self, entity, entity_class, visited = None):
        # creates the visited map in case it's not already defined
        # (first iteration) then checks if the entity is already
        # present in the visited map in case it is return immediately
        # there's no need to sort an entity that's is already going
        # to be sorted (avoids cycle)
        if visited == None: visited = {}
        if entity in visited: return

        # sets the current entity being visited as visited in the
        # visited map (preemptive visiting)
        visited[entity] = True

        # retrieves the complete set of relation from the
        # current entity class to allow recursive sorting
        # on the relation values (if present)
        all_relations = entity_class.get_all_relations()

        # retrieves the map of to many relations so that is
        # possible to percolate over them to sort their values
        # according to their identifier
        to_many_map = entity_class.get_to_many_map()

        # iterates over all the relations to allow recursive
        # sorting in their values
        for relation in all_relations:
            # retrieves the relation and in case it's not valid
            # (not set or empty sequence) continues the loops
            # no action is performed
            value = entity.get_value(relation)
            if not value: continue

            # retrieves the target class for the current relation
            # this class is going to be used in the next step of
            # the sorting process
            target_class = entity_class.get_target(relation)

            # in case the entity class is of type to one encapsulates
            # the value around a list (sequence) then iterates over
            # all the values to sort their to many relation (this is
            # considered to be the recursion step)
            if not entity_class.is_to_many(relation): value = [value]
            for _value in value: self._sort_to_many_e(_value, target_class, visited)

        # iterates over all the levels in the to many relations map
        # (all the class levels and relations)
        for _class, relations in to_many_map.items():
            # iterates over all the relations in the current to many
            # relations class to sort the relation values
            for relation in relations:
                # retrieves the relation and in case it's not valid
                # (not set or empty sequence) continues the loops
                # no action is performed
                value = entity.get_value(relation)
                if not value: continue

                # retrieves the target class for the current relation
                # then uses it to retrieve the name of the attribute
                # considered to be the identifier
                target_class = entity_class.get_target(relation)
                target_id = target_class.get_id()

                # creates the comparator lambda function used to sort
                # the various sequence values to the relation, this is
                # a simple comparator on the relation class identifier
                comparator = lambda x, y: cmp(x.get_value(target_id), y.get_value(target_id))

                # sorts the various to many relation values using the
                # the comparator, this ensures that the relation values
                # are at least ordered by their identifier value (some order)
                value.sort(comparator)

    def _sort_to_many_m(self, entity, entity_class, visited = None):
        # creates the visited map in case it's not already defined
        # (first iteration) then checks if the entity is already
        # present in the visited map in case it is return immediately
        # there's no need to sort an entity that's is already going
        # to be sorted (avoids cycle)
        if visited == None: visited = {}
        if id(entity) in visited: return

        # sets the current entity being visited as visited in the
        # visited map (preemptive visiting)
        visited[id(entity)] = True

        # retrieves the complete set of relation from the
        # current entity class to allow recursive sorting
        # on the relation values (if present)
        all_relations = entity_class.get_all_relations()

        # retrieves the map of to many relations so that is
        # possible to percolate over them to sort their values
        # according to their identifier
        to_many_map = entity_class.get_to_many_map()

        # iterates over all the relations to allow recursive
        # sorting in their values
        for relation in all_relations:
            # retrieves the relation and in case it's not valid
            # (not set or empty sequence) continues the loops
            # no action is performed
            value = entity.get(relation, None)
            if not value: continue

            # retrieves the target class for the current relation
            # this class is going to be used in the next step of
            # the sorting process
            target_class = entity_class.get_target(relation)

            # in case the entity class is of type to one encapsulates
            # the value around a list (sequence) then iterates over
            # all the values to sort their to many relation (this is
            # considered to be the recursion step)
            if not entity_class.is_to_many(relation): value = [value]
            for _value in value: self._sort_to_many_m(_value, target_class, visited)

        # iterates over all the levels in the to many relations map
        # (all the class levels and relations)
        for _class, relations in to_many_map.items():
            # iterates over all the relations in the current to many
            # relations class to sort the relation values
            for relation in relations:
                # retrieves the relation and in case it's not valid
                # (not set or empty sequence) continues the loops
                # no action is performed
                value = entity.get(relation, None)
                if not value: continue

                # retrieves the target class for the current relation
                # then uses it to retrieve the name of the attribute
                # considered to be the identifier
                target_class = entity_class.get_target(relation)
                target_id = target_class.get_id()

                # creates the comparator lambda function used to sort
                # the various sequence values to the relation, this is
                # a simple comparator on the relation class identifier
                comparator = lambda x, y: cmp(x.get(target_id, None), y.get(target_id, None))

                # sorts the various to many relation values using the
                # the comparator, this ensures that the relation values
                # are at least ordered by their identifier value (some order)
                value.sort(comparator)

    def _import_class(self, entity_class, serializer, data, full_mode, depth = 1):
        # loads the various entity maps from the data
        # using the currently "selected" serializer, this
        # may be very expensive operation depending on
        # the size of the serialized data
        entity_maps = serializer.loads(data)

        # creates the list that will hold the complete set
        # of converted entities from the various entity maps
        entities = []

        # iterates over all the loaded entity maps, to parse
        # them and convert them into the proper entities to
        # be added to the entities list
        for entity_map in entity_maps:
            # retrieves the name of the class to be used in the
            # conversion of the entity map into an entity
            class_name = entity_map.get("_class", None)
            target_class = class_name and self.get_entity(class_name) or entity_class

            # in case the full mode is not set the class to be
            # used to select the attribute names for iteration
            # is set as the current entity class, otherwise the
            # class for names is unset (all names retrieved)
            cls_names = not full_mode and entity_class or None

            # converts the current entity map into an entity
            # object and then adds it to the entities list
            entity = target_class.from_map(entity_map, self, set_empty_relations = False, cls_names = cls_names)
            entities.append(entity)

        # starts a new transaction for the importing of the
        # various entities for the class
        self.begin()

        try:
            # iterates over all the entity reference to persist
            # them correctly into the data source
            for entity in entities:
                # retrieves the complete set of relation names
                # for the entity class so that is possible to
                # iterate over them to set them
                relations = entity_class.get_all_relations()

                # iterates over all the relations in the entity
                # to process them and persist them in case it's
                # necessary for relation
                for relation in relations:
                    # retrieves the value for the relation and
                    # in case it's not valid or empty skips iteration
                    value = entity.get_value(relation)
                    if not value: continue

                    # in case the relation is not of type to many it
                    # must be encapsulated into a sequence (list)
                    if not entity_class.is_to_many(relation): value = [value]

                    # iterates over all the relation values (entities)
                    # to process them (verify if they exist and save
                    # if they don't)
                    for _value in value:
                        # retrieves the entity class and the id value
                        # for the current iteration value
                        _entity_class = _value.__class__
                        id_value = _value.get_id_value()

                        # verifies if the current entity value already
                        # exists in the data source and if does not saves it
                        if self.verify(_entity_class, id_value): continue
                        self.save(_value, generate = False)

                # saves or updates the current entity values
                # into the data source
                self.save_update(entity, generate = False)
        except:
            # "rollsback" the transaction and re-raises the exception
            # to be caught at the upper levels
            self.rollback()
            raise
        else:
            # commits the current transaction into the data source
            # because everything succeed as expected
            self.commit()

    def _export_class(self, entity_class, serializer, depth = 1, range = None, filters = None):
        # creates the map to hold the various options to be sent
        # to the find operation and then creates the list to hold
        # the various relations to be eager loaded
        options = {}
        eager = []

        # sets the map option in the options map, so that the result
        # set of the find operation is a set of maps instead of instances
        # this option will provide a better structure for serialization and
        # better performance in query unpacking
        options["map"] = True

        # sets the list holding eager loading relations in the
        # options map to use them in the find operation
        options["eager"] = eager

        # in case the range is set, sets the range in the
        # map of options to limit the query range of results
        # this will result in a boost of performance per exporting
        # (minimal ram usage)
        if range: options["range"] = range

        # in case there is a filtering (set of filters) to be
        # used for the exporting (eg: setting the range of modified
        # times for the exporting) applies it to the options
        if filters: options["filters"] = filters

        # retrieves all the to one relations of the entity class
        # (only for the current parent level)
        to_one_relations = entity_class.get_to_one()

        # iterates over all the relations (names) of the entity to
        # add them to the eager (loading) list only is case it's
        # a to one relation (otherwise multiplicity would "destroy"
        # the range values in the query)
        for relation in to_one_relations: eager.append(relation)

        # finds the appropriate entities loading all the relations
        # associated with it
        entities = self.find(entity_class, options)

        # sets the to many relations in the various entities, this
        # method loads the various to many relations in a manner that
        # no range values are armed
        self._set_to_many(entities, entity_class)

        # minimizes the entities, so that only the required values
        # for the exporting are set in the entity and in its direct
        # relations (minimization process)
        for entity in entities: self._minimize(entity, entity_class)

        # serializes the list of map entities into a final text
        # oriented representation
        _entities_serialized = serializer.dumps(entities)

        # returns the serialized view of the entities
        return _entities_serialized

    def _import_generator(self, serializer, data):
        # loads the various entity maps from the data
        # using the currently "selected" serializer, this
        # may be very expensive operation depending on
        # the size of the serialized data
        entity_maps = serializer.loads(data)

        # starts a new transaction for the importing of the
        # various generator entities
        self.begin()

        try:
            # iterates over all the loaded entity maps, to parse
            # them and execute the proper update query
            for entity_map in entity_maps:
                # retrieves the various attributes from the
                # generator entity
                name = entity_map.get("name", None)
                next_id = entity_map.get("next_id", None)
                _mtime = entity_map.get("_mtime", time.time())

                # in case no name is defined it's impossible to
                # update the generator entity (no identifier found)
                if not name: continue

                # retrieves the current next id value, to check
                # if the name is already defined in the generator
                _next_id = self.next_id(name)

                # escapes the name value to avoid possible
                # security problems
                name = self._escape_text(name)

                # in case the next id value is not defined, it's
                # considered to be a new name in the data source
                # and so it must be created (insert query)
                if _next_id == None:
                    # creates the query to save a new entry in the generator
                    # table setting the initial next id value and the initial
                    # modification time values
                    query = "insert into %s(name, next_id, _mtime) values('%s', %d, %f)" % (GENERATOR_VALUE, name, next_id, _mtime)
                # otherwise the name is already defined in the generator
                # table in the data source, and so an update is the
                # necessary operation (update query)
                else:
                    # creates the query to update the generator table set
                    # the new next id and update the modification time
                    query = "update %s set next_id = %d, _mtime = %f where name = '%s'" % (GENERATOR_VALUE, next_id, _mtime, name)

                # executes the query in the data source to update
                # the generator table
                self.execute_query(query)
        except:
            # "rollsback" the transaction and re-raises the exception
            # to be caught at the upper levels
            self.rollback()
            raise
        else:
            # commits the current transaction into the data source
            # because everything succeed as expected
            self.commit()

    def _export_generator(self, serializer, date_range = None):
        # creates a string buffer to hold the information of
        # the query to retrieve the generator items
        query_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the initial select query string part to the
        # query buffer (this is the general part)
        query_buffer.write("select name, next_id, _mtime from ")
        query_buffer.write(GENERATOR_VALUE)

        # in case the data range is defined extra filtering
        # must occur in order to limit the result set
        if date_range:
            # in case the date range tuple is of size one
            # (only the start date is defined) must create
            # a new tuple with the end date as undefined
            if len(date_range) == 1: date_range = (date_range[0], None)

            # unpacks the date range into the start and the
            # end values to be used for the processing of filters
            range_start, range_end = date_range

            # writes the where clause to the query buffer to signal
            # the start of the filtering
            query_buffer.write(" where ")

            # writes the filters into the query buffer in case the
            # limit range (start or end) are defined
            if not range_start == None: query_buffer.write("_mtime >= %f" % range_start)
            if not range_end == None: query_buffer.write("_mtime < %f" % range_end)

        # retrieves the query value as the value currently
        # present in the query buffer and then executes it
        # (avoiding the closing of the cursor)
        query = query_buffer.get_value()
        cursor = self.execute_query(query, False)

        # retrieves the result set (all the) items
        # available for fetching, then closes the cursor
        try: result_set = cursor.fetchall()
        finally: cursor.close()

        # creates the tuple containing the various field names for
        # the generator in the order present in the select query and
        # then uses the tuple to create the entity definition maps
        # from the results present in the result set
        field_names = ("name", "next_id", "_mtime")
        entities = [dict(zip(field_names, result)) for result in result_set]

        # serializes the list of map entities into a final text
        # oriented representation, and returns them
        _entities_serialized = serializer.dumps(entities)
        return _entities_serialized

    def _set_to_many(self, entities, entity_class):
        # creates the list that will hold the various
        # relations to be loaded in an eager fashion
        # as the complete set of to many relations in
        # in the entity class
        eager = entity_class.get_to_many().keys()

        # retrieves the name of the id attribute for the entity class
        # and then retrieves the value of it from the various entity
        # maps contained in the received list of entities, this list
        # of id values is going to be used for filtering the retrieved
        # entities (so that only the required entities are retrieved)
        id = entity_class.get_id()
        id_values = [value[id] for value in entities]

        # creates the map of options, ensuring that
        # the retrieval is of type minimal and that
        # the eager loaded relation are loaded, the
        # retrieval is made in map mode
        options = {
            "map" : True,
            "minimal" : True,
            "eager" : eager,
            "filters" : (
                {
                    "type" : "in",
                    "fields" : {
                        id : id_values
                    }
                },
            )
        }

        # retrieves the new entities from the entity manager, according to
        # the provided options map (these entities are going to be used
        # with the only purpose of to many relation retrieval)
        _entities = self.find(entity_class, options)

        # creates the dictionaries indexing the entity maps by their
        # primary identifier so that an association between both of
        # them is possible (and fast enough for processing)
        entities_map = dict([(entity[id], entity) for entity in entities])
        _entities_map = dict([(_entity[id], _entity) for _entity in _entities])

        # iterates over the (retrieved) entities items to set their
        # to many relation values in the original entities
        for _id_value, _entity in _entities_map.items():
            # retrieves the entity associated with the currently
            # retrieved entity map to set the various retrieved relations
            entity = entities_map[_id_value]

            # sets the proper values in the entity, taking into account the
            # the "just" retrieved entity
            for _eager in eager: entity[_eager] = _entity[_eager]

    def _minimize(self, entity, entity_class):
        # retrieves the name of the identifier attribute
        # the list of names for the entity class and the
        # list of relations for the entity class this values
        # are going to be used for the value filtering process
        id = entity_class.get_id()
        names = entity_class.get_names()
        relations = entity_class.get_relations()
        reserved = (id, "_class", "_mtime")

        # creates the list to hold the various names to be
        # removed from the entity (must be used to avoid
        # dictionary corruption)
        removal_list = []

        # iterates over all the names in the entity map
        # to filter the ones that are not necessary
        for name in entity:
            # in case the name is present in the list of
            # names in the current parent level or in case
            # it's a reserved name (id or class) no need
            # to remove it from the entity map
            if name in names or name in reserved: continue

            # adds the name to the list of names to be removed
            # from the entity
            removal_list.append(name)

        # removes the complete set of names present in the
        # list of names to be removed from the entity map
        for name in removal_list: del entity[name]

        # iterates over all the relations to remove all of
        # their attributes, except the identifier and the
        # class identifier
        for relation_name in relations:
            # retrieves the relation for the current
            # relation name, in case it's not valid no
            # need to continue, skips iteration
            relation = entity.get(relation_name, None)
            if not relation: continue

            # checks if the current relation is of type to one
            # in case it's encapsulates the relation around a
            # sequence to provide a simple "interface" for iteration
            if not entity_class.is_to_many(relation_name): relation = [relation]

            # creates the list that will hold the final set of maps
            # for the relations, this method avoids the typical reference
            # problems provided by the entity manager
            relation_f = []

            # iterates over all the relation in the current relation
            # name to remove the unnecessary attributes
            for _relation in relation:
                # creates a copy of the relation, this helps avoiding the
                # possible overriding of the base entity attributes, because
                # they may share the same map
                _relation = copy.copy(_relation)

                # retrieves the relation class name from the class
                # attributes and uses it to retrieve the proper class
                # from the entity manager
                relation_class_name = _relation["_class"]
                relation_class = self.get_entity(relation_class_name)

                # retrieves the relation class identifier name and adds
                # it to the class attribute and modified time to create
                # the reserved name tuple (to be used for non exclusion)
                relation_id = relation_class.get_id()
                reserved = (relation_id, "_class", "_mtime")

                # creates the list to hold the various names to be
                # removed from the relation (must be used to avoid
                # dictionary corruption)
                removal_list = []

                # iterates over all the names in the relation map
                # to filter the ones that are not necessary
                for _name in _relation:
                    # in case the name is present in the reserved
                    # names tuple no need to remove it from the
                    # relations map
                    if _name in reserved: continue

                    # adds the name to the list of names to be removed
                    # from the relation
                    removal_list.append(_name)

                # removes the complete set of names present in the
                # list of names to be removed from the relation map
                for _name in removal_list: del _relation[_name]

                # adds the relation to the list of final values,
                # this should be the newly created copy amp
                relation_f.append(_relation)

            # ensures that is the relations is of type to one only the
            # first value of the list is set in the final relation value
            # then uses the final value to set it in the entity map for
            # the proper relation name (proper setting)
            if not entity_class.is_to_many(relation_name): relation_f = relation_f[0]
            entity[relation_name] = relation_f

    def _ensure_parents(self, entity_classes):
        # creates a list with the initial set of entity classes
        # so that it's possible to iterate over them to retrieve
        # their parent classes to add them to the set
        _entity_classes = list(entity_classes)

        # iterates over all the entity classes to add their parents
        # to the  list of entity classes to be exported
        for entity_class in entity_classes:
            # retrieves the complete set of parent classes
            # for the current entity and adds them to the list
            parents = entity_class.get_all_parents()
            _entity_classes.extend(parents)

        # creates a set with the list of entity classes, avoids duplicated
        # from the parents inclusion and returns it
        entity_classes = set(_entity_classes)
        return entity_classes

    def normalize_options(self, options):
        """
        Normalizes the given map of filter options, this
        normalization process targets the simplification of
        the query structure.

        @type options: Dictionary/Object
        @param options: The map of options to be normalized.
        This value may be a filters value and in that case it
        can assume a different type.
        @rtype: Dictionary
        @return: The normalized options map, this map is not
        verified to be the changed version of the input options
        map, due to filters wrapping.
        """

        # tries to retrieve the normalized flag from
        # the options map (for lazy loading) only in case the
        # options is a dictionary
        is_normalized = type(options) == types.DictionaryType and options.get("_normalized", False) or False

        # in case the options are already normalized
        # no need to normalize again (performance issues)
        if is_normalized:
            # returns immediately, the already
            # normalized options map
            return options

        # in case the options value is invalid or is an
        # empty map no need to normalize it return the
        # control immediately (avoids static map problems)
        if not options: return options

        # checks if the options map is not a filter, via
        # type and map key checking (if it is a new options
        # map must be constructed from it)
        if self._is_filter(options):
            # creates a new options map with the filters
            # defined in it
            options = {
                "filters" : options
            }

        # in case the eager option is present
        # must be processed
        if "eager"in options:
            # retrieves the eager (loading) relation value and the
            # the filters type
            eager_relations = options["eager"]
            eager_loading_relations_type = type(eager_relations)

            # in case the eager (loading) relations is a sequence
            # must create a map with all the name in it associated
            # with empty (options) maps
            if eager_loading_relations_type in SEQUENCE_TYPES:
                # creates a list of values for the various relation
                # associating (all with an empty options map)
                eager_loading_relations_length = len(eager_relations)
                relation_values = [{} for _value in range(eager_loading_relations_length)]

                # creates a dictionary of values from the tuple created by "zipping"
                # the eager (loading) relations list (keys) and the relations value list (value)
                # (the created map contains all the name with an empty map as value)
                eager_relations = dict(zip(eager_relations, relation_values))

            # sets the eager (loading) relations in the options map
            options["eager"] = eager_relations

        # in case the range is defined in the options
        # (composed start records and number of records)
        if "range" in options:
            # retrieves the range value and the
            # range type
            _range = options["range"]
            range_type = type(_range)

            # in case the range is a sequence it must be unpacked
            # into start record and number of records
            if range_type in SEQUENCE_TYPES:
                # determined the length of the range in order
                # to assume if it contains both the start record
                # and the number of records or just the start record
                range_length = len(_range)

                # in case the range contains two values
                if range_length == 2:
                    # unpacks the range into start record
                    # and number of records
                    start_record, number_records = _range
                # otherwise only one value is present, assumes
                # it's the start record
                else:
                    # retrieves the start record in from the
                    # range and sets the default value in the
                    # number of records
                    start_record = _range[0]
                    number_records = -1
            # otherwise it's a simple value and only the
            # start record may be used
            else:
                # sets the range as the start record and the
                # number of records as the default value
                start_record = _range
                number_records = -1

            # sets the start record and the number of records
            # in the options map
            options["start_record"] = start_record
            options["number_records"] = number_records

        # in case the order by option is present
        # must be processed
        if "order_by" in options:
            # retrieves the order by value and the
            # the order by type
            order_by = options["order_by"]
            order_by_type = type(order_by)

            # in case the order by is not of type sequence (only
            # one element)
            if not order_by_type in SEQUENCE_TYPES:
                # encapsulates the order by value into a tuple value
                order_by = (order_by,)

            # creates the list to hold the normalized order by
            # values (processed values)
            _order_by = []

            # iterates over all the order by element to normalize
            # them into expanded order by values
            for order_by_element in order_by:
                # retrieves the order by element type
                order_by_element_type = type(order_by_element)

                # in case the order by is not a sequence, single
                # item with default values
                if not order_by_element_type in SEQUENCE_TYPES:
                    # creates the order by element as a tuple with the
                    # default order value
                    order_by_element = (order_by_element, "descending")

                # retrieves the order by element length in order
                # to assume if the element contains the order
                # or not
                order_by_element_length = len(order_by_element)

                # in case the order by element is of size two
                # it's complete and may be added to the order
                # by list
                if order_by_element_length == 2:
                    # adds the order by element to the list
                    _order_by.append(order_by_element)
                # otherwise it's not complete and a default value
                # must be added
                else:
                    # adds the composite order by element with the default
                    # order value
                    _order_by.append((order_by_element[0], "descending"))

            # sets the order by tuple in the options map
            options["order_by"] = tuple(_order_by)

        # in case the filter option is present
        # must be processed
        if "filters" in options:
            # retrieves the filters value and the
            # the filters type
            filters = options["filters"]
            filters_type = type(filters)

            # in case the filter is not of type sequence (only
            # one element)
            if not filters_type in SEQUENCE_TYPES:
                # encapsulates the filters into a tuple value
                filters = (filters,)

            # creates the list to hold the normalized filters
            # values (processed values)
            _filters = []

            # iterates over all the set of filters
            # to normalize them
            for filter in filters:
                # in case the (filter) type is not present
                # in the filter (it must be the default equals
                # filter)
                if not "type" in filter:
                    # retrieves the type of the filter value
                    # to be able to check if it's an in filter
                    # or an equals filter
                    filter_value = filter.values()[0]
                    filter_value_type = type(filter_value)

                    # in case the "first" filter value is of type
                    # sequence, must assume this is meant to be
                    # a complete in filter, must create it
                    if filter_value_type in SEQUENCE_TYPES:
                        # creates an in filter and sets
                        # the filter fields as the filter elements
                        filter = {
                            "type" : "in",
                            "fields" : filter
                        }

                    # otherwise the "normal" equals filter should
                    # be applied assuming it's a normal set of filters
                    else:
                        # creates an equals filter and sets
                        # the filter fields as the filter elements
                        filter = {
                            "type" : "equals",
                            "fields" : filter
                        }

                # in case the (filter) fields are defined in the
                # filter map
                if "fields" in filter:
                    # retrieves the filter fields and the
                    # type in the filter fields
                    filter_fields = filter["fields"]
                    filter_fields_type = type(filter_fields)

                    # in case the filter field is of type dictionary
                    # (key value association) it must be converted to a list
                    # of map of name and value association (field normalization)
                    if filter_fields_type == types.DictionaryType:
                        # converts the map of name value association to a list of
                        # maps for each attribute (normalized value)
                        filter["fields"] = [{"name" : key, "value" : value} for key, value in filter_fields.items()]
                    # otherwise in case the filter fields is of type sequence
                    # it still needs to be constructed respecting the simple
                    # form of declaration
                    elif filter_fields_type in SEQUENCE_TYPES:
                        # creates a list to hold the normalized filter
                        # fields
                        _filter_fields = []

                        # iterates over all the filter fields to check
                        # for simple (single) values
                        for filter_field in filter_fields:
                            # retrieves the filter field type
                            filter_field_type = type(filter_field)

                            # in case the filter field is not of type dictionary
                            # assumes it's a simple field and creates the complete
                            # filter field value
                            if not filter_field_type == types.DictionaryType:
                                # creates the complete filter field using the
                                # invalid value as the value and the filter field
                                # as the name of the filter field
                                filter_field = {
                                    "name" : filter_field,
                                    "value" : None
                                }

                            # adds the filter field to the filter fields
                            _filter_fields.append(filter_field)

                        # sets the (filter) fields tuple in the filter map
                        filter["fields"] = tuple(_filter_fields)
                    # otherwise it must be a single simple (none based) value
                    # and a new set of filter fields containing a single null
                    # value must be created
                    else:
                        # sets the (filter) fields with a single null based field
                        # as a sequence of values
                        filter["fields"] = ({"name" : filter_fields, "value" : None},)

                # adds the filter tot the list
                # of (normalized) filters
                _filters.append(filter)

            # sets the filters tuple in the options map
            options["filters"] = tuple(_filters)

        # sets the normalized option, avoids
        # extra normalization (performance issues)
        options["_normalized"] = True

        # returns the normalized options value
        return options

    def _is_filter(self, options):
        """
        Checks if the given options map represents a map
        (or set) of filters instead of the "normal" options map.

        @type options: Dictionary/Object
        @param options: The map containing the options or
        a set of filters in map or in tuple set.
        @rtype: bool
        @return: If the given dictionary or object is a
        set of filters.
        """

        # in case the options is empty or
        # not valid, it's not considered to
        # be a filter
        if not options:
            # returns immediately as false
            return False

        # retrieves the options type
        options_type = type(options)

        # in case the options map is not of
        # type dictionary it must be a filter
        if not options_type == types.DictionaryType:
            # returns true (it's a filter)
            return True

        # iterates over all the options keys
        # to check if they appear in the options
        # map
        for option_key in OPTIONS_KEYS:
            # in case the options key exists
            # in the options map (it's an options
            # map and not a filter)
            if option_key in options:
                # returns false (it's an options
                # map)
                return False

        # returns true (it's a filter)
        return True

    def _create_range_filters(self, date_range):
        """
        Creates a series of filters that may be used by the
        entity manager to limit the range of entries retrieved
        by the entity manager to a certain range.

        The data range can be provided as an undefined value no
        range is applied or as a tuple with the defined start\
        and end data range values.

        @type date_range: Tuple
        @param date_range: The range of dates for which the entries
        should be retrieved from the data source.
        @rtype: List
        @return: The list of filters that can be used to filter
        the entries in a certain query to the data source.
        """

        # creates the list that will hold the various maps
        # representing the filters in the query
        filters = []

        # in case no date range is defined returns immediately
        # with the currently available filters
        if not date_range: return filters

        # in case the date range tuple is of size one
        # (only the start date is defined) must create
        # a new tuple with the end date as undefined
        if len(date_range) == 1: date_range = (date_range[0], None)

        # unpacks the date range into the start and the
        # end values to be used for the processing of filters
        range_start, range_end = date_range

        # in case the start date range is defined creates the
        # proper filter
        if not range_start == None:
            # creates the start date filter with the
            # range start value
            start_filter = {
                "type" : "greater_equal",
                "fields" : {
                    "_mtime" : str(range_start)
                }
            }

            # adds the start date filter to the list of filters
            filters.append(start_filter)

        # in case the end date range is defined creates the
        # proper filter
        if not range_end == None:
            # creates the end date filter with the
            # range end value
            end_filter = {
                "type" : "lesser",
                "fields" : {
                    "_mtime" : str(range_end)
                }
            }

            # adds the end date filter to the list of filters
            filters.append(end_filter)

        # returns the list of filters that may be used to limit
        # the range of dates of the entries in the data source
        return filters

    def _reset_exists(self):
        """
        Resets the current (definition) exists cache and
        any further access to the cache will be a miss.

        This method restores the exists cache to the original
        (empty) state.
        """

        self._exists.clear()

    def _get_entities_map(self, module):
        """
        Converts the set of entity classes present in the
        provided module into a map indexed by the entity class
        name (useful for extension and shrinking).

        @type module: module
        @param module: The module to find the set of entity classes
        that will constitute the create entities map.
        @rtype: Dictionary
        @return: The map containing the various found entity
        classes index by their class names.
        """

        # creates the map that will hold the various entity
        # classes to load from the module
        entities_map = {}

        # retrieves all the module names for the current
        # module, this names are going to be used to search
        # for the valid items (inheriting from entity class)
        module_names = dir(module)

        # iterates over all the module names to retrieve
        # the respective items and to set them as entities
        # in the entities map (if that's the case)
        for module_name in module_names:
            # retrieves the module item for the current
            # module name (current module item) and then
            # retrieves it's type for checking
            module_item = getattr(module, module_name)
            module_item_type = type(module_item)

            # in case the module item type is not the correct
            # or the module item is not a sub class of the top level
            # entity class, this is not a proper entity class item,
            # must continue the loop
            if not module_item_type == types.TypeType or not issubclass(module_item, structures.EntityClass):
                # continues the loop, trying to find valid
                # entity classes for registration
                continue

            # sets the module item (entity class) in the entities
            # map in order to use it for entity manager
            entities_map[module_item.__name__] = module_item

        # returns the map containing all the entities
        # in the current module indexed by their name
        return entities_map

    def _resolve_name(self, entity_class, name):
        """
        Resolves the name of the given attribute in the context of the
        provided entity class.

        This method should be able to converted a "normal" dot separated
        set of attribute path into the query oriented name.

        Eg: parent.status should be converted into __parent___root_entity.status
        as specified by the entity manager specification.

        The usage of this method must be carefully watched because this
        is a quite expensive operation.

        @type entity_class: EntityClass
        @param entity_class: The entity class to be used as reference during
        the resolution of the name. It should be the top level entry point for
        the resolution.
        @type name: String
        @param name: The name to be resolved (should be in dot notation) into
        the full query oriented value.
        @rtype: String
        @return: The resolved query oriented name value.
        """

        # splits the name list, allowing it to retrieve
        # the various partial names and the last and final
        # name from the complete (dot separated name)
        name_list = name.split(".")
        name_partials = name_list[:-1]
        final_name = name_list[-1]

        # creates a string buffer to hold the information of
        # the various partial names
        name_buffer = colony.libs.string_buffer_util.StringBuffer()

        # iterates over all the partial names to write their
        # relation information into the name buffer for latter
        # processing
        for name_partial in name_partials:
            # write the relation name and prefix into the name
            # buffer for relation indication
            name_buffer.write("__")
            name_buffer.write(name_partial)

            # updates the current entity class to the target
            # of the current relation (partial name)
            entity_class = entity_class.get_target(name_partial)

        # retrieves the name of the identifier attribute
        # for the current entity class
        id = entity_class.get_id()

        # retrieves the names map for the currently selected
        # entity class and determines the correct parent level
        # for the name (name associated class) note that if the
        # current final name is the identifier attribute the
        # current concrete entity class is used (performance tune)
        names_map = entity_class.get_names_map()
        name_class = final_name == id and entity_class or names_map.get(final_name, entity_class)
        name_class_name = name_class.get_name()

        # in case the list of partial names is not empty a final
        # test must be made to verify that the parent class reference
        # must appear in the name
        if name_partials:
            # in case the current name class is not the currently
            # selected entity class (must write parent class reference)
            if not name_class == entity_class:
                # writes the parent class reference into the name buffer
                # this should be able to reference the level for the name
                name_buffer.write("___")
                name_buffer.write(name_class_name)

        # otherwise it's a single name reference and the parent name class
        # must always be written to the name buffer (without prefix)
        else: name_buffer.write(name_class_name)

        # writes the final attribute indication to the name buffer
        # (this should be the final reference to the last name)
        name_buffer.write(".")
        name_buffer.write(final_name)

        # retrieves the final name from the name buffer and returns
        # it as the final (resolved) name for the base name
        name = name_buffer.get_value()
        return name

    def _escape_text(self, text_value, escape_slash = False, escape_double_quotes = False):
        """
        Escapes the text value in the sql context.
        This escaping process is important even for
        security reasons.

        This escaping process avoids many of the existing
        sql injection procedures.

        @type text_value: String
        @param text_value: The text value to be escaped.
        @type escape_slash: bool
        @param escape_slash: If the slash characters should be escaped.
        @type escape_double_quotes: bool
        @param escape_double_quotes: If the double quotes should be escaped.
        @rtype: String
        @return: The escaped text value, according to the sql
        standard specification.
        """

        return structures.EntityClass._escape_text(text_value, escape_slash, escape_double_quotes)

    def _load_meta(self, path):
        """
        Loads the meta information file according to the
        "standard" entity data format (specification defined).

        The returned value is a map representing the meta
        information contained in the file.

        @type path: String
        @param path: The path to the meta information file to
        be loaded into a map.
        @rtype: Dictionary
        @return: The map containing the meta information
        representation from the file.
        """

        # retrieves the json plugin reference, to be used
        # in the loading of the meta file
        json_plugin = self.entity_manager_plugin.json_plugin

        # in case the path to the meta file does not exits
        # an empty map is returned (default value)
        if not os.path.exists(path): return {}

        # opens the meta file for reading in the binary
        # form (json extraneous contents)
        file = open(path, "rb")

        try:
            # reads the contents (data) from the meta file
            # and then loads them as json
            contents = file.read()
            information_data = json_plugin.loads(contents)
        finally:
            # closes the file to avoids memory leaking
            file.close()

        # returns the map containing the information
        # contained in the meta file
        return information_data

    def _apply_names_set(self, result_set, names):
        """
        Adds the result set (header) names list as the first entry
        of the result set.
        This way it's possible to establish an inner relation between
        the result set and its contents.

        This is a very expensive operation as the result set tuple
        must be converted into a list and then the names added as the
        first item of it.

        @type result_set: Tuple
        @param result_set: The result set to have the names added to
        it (target result set).
        @type names: List
        @param names: The list of names for the sequence of values present
        in the various result set lines.
        @rtype: List
        @return: The result set with the first line as the names of the
        various values, this result set is represented as a list.
        """

        # converts the result into a list so that it may be changed
        # and then inserts the names list in it as the first element
        # this should be enough for one to associate the values with
        # the representing names
        result_set = list(result_set)
        result_set.insert(0, names)

        # returns the "transformed" result set, this values is now a list
        # instead of a tuple
        return result_set
