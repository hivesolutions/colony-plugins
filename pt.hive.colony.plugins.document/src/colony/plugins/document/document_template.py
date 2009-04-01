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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class DocumentTemplateChunk:
    """
    Class storing a piece of data and associated meta-attributes.
    Each document format plugin is responsible to handle these document
    chunks and respective attributes in their own way (ex: an html plugin
    can support the interpretation of style attributes, but a plain text
    one will not).
    """

    def __init__(self, id, value):
        """
        Class constructor.

        @type id: Integer
        @param id: Unique chunk identification number.
        @type value: String
        @param value: Value one wants to store in this chunk.
        """
        self.id = id
        self.value = value
        self.property_name_value_map = {}

    def get_id(self):
        """
        Returns the unique identifier for this document chunk.

        @rtype: String
        @return: Unique identifier for this document chunk.
        """
        return self.id

    def get_value(self):
        """
        Returns the value contained in this document chunk.

        @rtype: String
        @return: Value contained in this document chunk.
        """
        return self.value

    def set_value(self, value):
        """
        Changes the value contained in this document chunk.

        @type value: String
        @param value: Vaue to store in this document chunk.
        """
        self.value = value

    def get_property(self, property_name):
        """
        Returns the value of one of the chunk's properties.

        @type property_name: String
        @param property_name: Name of the desired property.

        @rtype: Object
        @return: Value of the specified property, None if it doesn't exist.
        """
        if property_name in self.property_name_value_map:
            property_value = self.property_name_value_map[property_name]
            return property_value

    def set_property(self, property_name, property_value):
        """
        Changes the value of the specified property.

        @type property_name: String
        @param property_name: Name of the property whose value one wants
        to change.
        @type property_value: Object
        @param property_value: Value to store in the property.
        """
        self.property_name_value_map[property_name] = property_value

    def unset_property(self, property_name):
        """
        Removes a property from this document chunk.

        @type property_name: String
        @param property_name: Name of the property to remove from the
        chunk.
        """
        if property_name in self.property_name_value_map:
            del self.property_name_value_map[property_name]

class DocumentTemplate:
    """
    Class that holds that was extracted from a document and/or
    will be inserted into one.
    """

    chunks = []
    """ List of document chunks. """

    chunk_id_chunk_map = {}
    """ Map associating chunk id with the document chunk object. """

    chunk_id = 1;
    """ The next unique identifier for a document chunk. """

    def __init__(self):
        """
        Class constructor.
        """
        self.template = None
        self.chunks = []
        self.chunk_id_chunk_map = {}
        self.chunk_id = 1

    def get_next_id(self):
        """
        Generates a new unique chunk identification number.

        @rtype: Integer
        @return: Unique chunk identification number.
        """
        self.chunk_id += 1
        return self.chunk_id

    def get_chunks(self):
        """
        Returns a list of with the document chunks stored in this
        template.

        @rtype: List
        @return: List of document chunks.
        """
        return self.chunks

    def get_chunk(self, chunk_id):
        """
        Retrieves the document chunk that has the specified id.

        @type chunk_id: Integer
        @param chunk_id: Unique chunk identification number.

        @rtype: DocumentChunk
        @return: Returns the specified document chunk, or None if not found.
        """
        if chunk_id in self.chunk_id_chunk_map:
            chunk = self.chunk_id_chunk_map[chunk_id]
            return chunk

    def set_chunk(self, chunk_value, chunk_id = None):
        """
        Changes the value of an existing document chunk, or creates a new one
        if no chunk with the specified id exists.

        @type chunk_value: String
        @param chunk_value: Value one wants to store in the document chunk.
        @type chunk_id: Integer
        @param chunk_id: Optional unique chunk identification number.

        @rtype: DocumentChunk
        @return: Reference to the created or modified document chunk.
        """
        # if no document chunk id is specified generate one
        if chunk_id is None:
            chunk_id = self.get_next_id()
        chunk = self.get_chunk(chunk_id)
        # if there is no chunk with the specified id create one
        if chunk is None:
            chunk = DocumentTemplateChunk(chunk_id, chunk_value)
            self.chunks.append(chunk)
            self.chunk_id_chunk_map[chunk_id] = chunk
        else: # otherwise change the value of the existing one
            chunk.set_value(chunk_value)
        return chunk
