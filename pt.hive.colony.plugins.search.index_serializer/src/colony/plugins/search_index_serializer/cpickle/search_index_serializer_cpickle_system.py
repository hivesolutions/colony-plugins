#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
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

import gc
import time
import cPickle

import search_index_serializer_cpickle_exceptions

SEARCH_INDEX_SERIALIZER_TYPE = "cpickle"
""" The search index serializer type """

FILE_PATH_VALUE = "file_path"
""" The file path value """

class SearchIndexSerializerCpickle:
    """
    The search index serializer cpickle class.
    """

    search_index_serializer_cpickle_plugin = None
    """ The search index serializer cpickle plugin """

    def __init__(self, search_index_serializer_cpickle_plugin):
        """
        Constructor of the class.

        @type search_index_serializer_cpickle_plugin: SearchIndexSerializerCpicklePlugin
        @param search_index_serializer_cpickle_plugin: The search index serializer cpickle plugin.
        """

        self.search_index_serializer_cpickle_plugin = search_index_serializer_cpickle_plugin

    def get_type(self):
        return SEARCH_INDEX_SERIALIZER_TYPE

    def persist_index(self, search_index, properties):
        if not FILE_PATH_VALUE in properties:
            raise search_index_serializer_cpickle_exceptions.MissingProperty(FILE_PATH_VALUE)

        # retrieves the file path
        file_path = properties[FILE_PATH_VALUE]

        # opens the file for writing in binary
        # and if the file does not exists, it creates a new one
        file = open(file_path, "wb")

        # gets the start time for the cPickle dump operation
        start_time = time.time()

        # disabling the garbage collector to improve cPickle.dump performance
        gc.disable()

        # wrapping the dump operation in a try-finally block to keep the garbage collector to staying disable after an exception
        try:
            # dumps the search index object into the file using the cpickle serializer
            cPickle.dump(search_index, file, cPickle.HIGHEST_PROTOCOL)
        finally:
            # re-enabling the garbage collector
            gc.enable()

        # gets the end time for the cPickle dump operation
        end_time = time.time()

        duration = end_time - start_time
        self.search_index_serializer_cpickle_plugin.debug("SearchIndexSerializerCpickle persist index cPickle.dump finished in %s" % duration)

        # closes the file
        file.close()

        return True

    def load_index(self, properties):
        if not FILE_PATH_VALUE in properties:
            raise search_index_serializer_cpickle_exceptions.MissingProperty(FILE_PATH_VALUE)

        # retrieves the file path
        file_path = properties[FILE_PATH_VALUE]

        # opens the file for reading in binary
        file = open(file_path, "rb")

        # gets the start time for the cPickle dump operation
        start_time = time.time()

        # disabling the garbage collector to improve cPickle.load performance
        gc.disable()

        # wrapping the load operation in a try-finally block to keep the garbage collector to staying disable after an exception
        try:
            # loads the search index object from the file using the cpickle serializer
            search_index = cPickle.load(file)
        finally:
            # re-enabling the garbage collector
            gc.enable()

        # gets the end time for the cPickle dump operation
        end_time = time.time()

        duration = end_time - start_time
        self.search_index_serializer_cpickle_plugin.debug("SearchIndexSerializerCpickle load index cPickle.load finished in %s" % duration)

        # closes the file
        file.close()

        # returns the search index
        return search_index
