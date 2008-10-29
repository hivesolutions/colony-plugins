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

class DocumentManager:
    """
    This class keeps reference to open documents.
    """

    def __init__(self, document_manager_plugin):
        """
        Class constructor.
        
        @type document_manager_plugin: DocumentManagerPlugin
        @param document_manager_plugin: Reference to the document manager
        plugin.
        """
        self.document_manager_plugin = document_manager_plugin
        self.document_id_document_map = {}
        self.current_document_id = 1
    
    def get_next_id(self):
        """
        Generates a new unique file identification number.
        
        @rtype: Integer
        @return: Unique identification number.
        """
        self.current_document_id += 1
        return self.current_document_id
    
    def get_open_documents(self):
        """
        Returns a list with references to the currently open documents.
        
        @rtype: Array
        @return: List of references to open documents.
        """
        documents = self.document_id_document_map.values()
        return documents
    
    def open(self, document_plugin, url):
        """
        Opens a document from the specified location and returns an object
        that allows performing operations on it.
        
        @type document_plugin: DocumentPlugin
        @param document_plugin: Plugin that allows performing operations 
        over a document. 
        @type url: String
        @param url: Location of the desired document.
        
        @rtype: Document
        @return: Document object that allows performing operations over
        the specified document.
        """
        document_id = self.get_next_id()
        document = document_plugin.open(self.document_manager_plugin, url, document_id)
        self.document_id_document_map[document_id] = document
        return document

    def close(self, document):
        """
        Closes a document.
        
        @type document: Document
        @param document: Reference to the open document object.
        """
        document_id = document.get_id()
        del self.document_id_document_map[document_id]
