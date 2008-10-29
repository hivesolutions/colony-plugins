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
import re
import tempfile

class DocumentOdt:
    
    file = None
    """ Reference to the odt's content file. """
    
    url = None
    """ Location of the document. """
    
    document_id = None
    """ Unique number that identifies this file in the document manager. """
    
    temp_directory_path = None
    """ Path to the directory where files from the odt package are extracted to."""
    
    directory_paths_list = []
    """ List of temporary directories that need to be deleted when the document is closed. """
    
    file_paths_list = []
    """ List of temporary files that need to be deleted when the document is closed. """
    
    def __init__(self, document_manager_plugin, document_odt_plugin, url, document_id):
        """
        Class constructor.
        
        @type document_manager_plugin: DocumentManagerPlugin
        @param document_manager_plugin: Reference to the document manager plugin.
        @type document_odt_plugin: DocumentPlugin
        @param document_odt_plugin: Reference to the plugin that owns this class.
        @type url: String
        @param url: Location of the document.
        @type document_id: Integer
        @param document_id: Unique identification number for this file.
        """
        self.document_manager_plugin = document_manager_plugin
        self.document_odt_plugin = document_odt_plugin
        self.file = None
        self.document_id = document_id
        self.url = url
        self.temp_directory_path = None
        self.directory_paths_list = None
        self.file_paths_list = None
    
    def get_id(self):
        """
        Returns the unique number that identifies this file in the
        document manager.
        
        @rtype: Integer
        @return: Unique identification number for this file.
        """
        return self.document_id
    
    def open(self):
        """
        Opens the document.
        """
        zip_plugin = self.document_odt_plugin.zip_plugin
        document_path = os.path.abspath(self.url)
        if os.path.isfile(document_path):
            self.temp_directory_path = tempfile.gettempdir()
            self.directory_paths_list = zip_plugin.get_directory_paths(document_path)
            self.directory_paths_list.reverse()
            self.file_paths_list = zip_plugin.get_file_paths(document_path)
            zip_plugin.unzip(document_path, self.temp_directory_path)
            content_xml_path = os.path.join(self.temp_directory_path, "content.xml")
            self.file = open(content_xml_path, "r+")
    
    def close(self):
        """
        Closes the document and notifies the document manager.
        """
        self.file.close()
        document_path = os.path.abspath(self.url)
        self.document_odt_plugin.zip_plugin.zip(self.url, self.temp_directory_path, self.file_paths_list)
        for file_path in self.file_paths_list:
             file_path = os.path.join(self.temp_directory_path, file_path)
             os.remove(file_path)
        for directory_path in self.directory_paths_list:
             directory_path = os.path.join(self.temp_directory_path, directory_path[1:])
             os.rmdir(directory_path)
        self.document_manager_plugin.close(self)
        
    def read(self):
        """
        Extracts data from the file into a document template (each line
        in the text file is considered as a different template item).
        
        @rtype: DocumentTemplate
        @return: Template with data extracted from the document.
        """
        template = self.document_manager_plugin.get_new_template()
        content_xml = self.file.read()
        regex_id = re.compile('form:name="[^"]*"')
        regex_value = re.compile('form:current-value="[^"]*"')
        id_matches = regex_id.findall(content_xml)[1:]
        value_matches = regex_value.findall(content_xml)
        for chunk_offset in range(len(id_matches)):
             id_match = id_matches[chunk_offset]
             value_match = value_matches[chunk_offset]
             chunk_id = id_match[11:-1]
             chunk_value = value_match[20:-1]
             template.set_chunk(chunk_value, chunk_id)
        self.file.seek(0)
        return template

    def write(self, template):
        """
        Inserts data from the template into the document (each data item
        will be inserted into a different line in the file).
        
        @type template: DocumentTemplate
        @param template: Template with the data one wants to insert
        into the document. 
        """
        content_xml = self.file.read()
        content_xml_path = os.path.join(self.temp_directory_path, "content.xml")
        self.file.close()
        self.file = open(content_xml_path, "w")
        regex_id = re.compile('form:name="[^"]*"')
        regex_value = re.compile('form:current-value="[^"]*"')
        id_matches = regex_id.findall(content_xml)[1:]
        value_matches = regex_value.findall(content_xml)
        chunks = template.get_chunks()
        for chunk in chunks:
            chunk_id = chunk.get_id()
            chunk_value = chunk.get_value()
            for chunk_offset in range(len(id_matches)):
                 id_match = id_matches[chunk_offset]
                 old_chunk_id = id_match[11:-1]
                 if old_chunk_id == chunk_id:
                     value_match = value_matches[chunk_offset]
                     old_chunk_value = value_match[20:-1]
                     content_xml = content_xml.replace('form:current-value="' + old_chunk_value + '"', 'form:current-value="' + chunk_value + '"')
                     break
        self.file.seek(0)
        self.file.write(content_xml)
        self.file.seek(0)
  