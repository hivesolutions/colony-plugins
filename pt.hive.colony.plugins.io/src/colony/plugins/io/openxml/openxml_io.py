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

import tempfile
import os.path

class OpenXMLFile:
    """
    Stores information about a currently open OpenXML file.
    """
    
    file_path = None
    extracted_file_path = None
    directory_paths_list = None
    file_paths_list = None
    
    def __init__(self, file_path, extracted_file_path, directory_paths_list, file_paths_list):
        """
        Class constructor.
        
        @type file_path: String
        @param file_path: Full path to the OpenXML document.
        @type extracted_file_path: String
        @param extracted_file_path: Full path to the directory where the OpenXML file is extracted.
        @type directory_paths_list: List
        @param directory_paths_list: List of relative paths to the directories extracted from the OpenXML document.
        @type file_paths_list: List
        @param file_paths_list: List of relative paths to the files extracted from the OpenXML document.
        """
        
        self.file_path = file_path
        self.extracted_file_path = extracted_file_path
        self.directory_paths_list = directory_paths_list
        self.file_paths_list = file_paths_list
        
    def get_file_paths(self):
        """
        Returns a list of relative paths to the files contained in the document.
        
        @rtype: List
        @return: List of relative file paths.
        """
        
        return self.file_paths_list
    
    def get_directory_paths(self):
        """
        Returns a list of relative paths to the directories contained in the document.
        
        @rtype: List
        @return: List of directory file paths.
        """
        
        return self.directory_paths_list
    
    def get_file_path(self):
        """
        Returns the full path to the original file from which the OpenXML document was extracted.
        
        @rtype: String
        @return: Absolute path to a file.
        """
        
        return self.file_path
    
    def get_extracted_file_path(self):
        """
        Returns the full path to the directory to which the OpenXML document was extracted.
        
        @rtype: String
        @return: Absolute path to a directory.
        """
        
        return self.extracted_file_path
    
    def get_full_path(self, relative_path):
        """
        Converts a relative path of an OpenXML component document to a full path.
        
        @type relative_path: String
        @param relative_path: Relative path to an OpenXML component.
        @return: Full path to a file or directory.
        """ 
        
        if relative_path[0] == "/" or relative_path[0] == "\\":
            relative_path = relative_path[1:]
            
        return os.path.join(self.get_extracted_file_path(), relative_path)
    
class OpenXMLInputOutput:
    """
    Provides functions to interact with OpenXML files.
    """
    
    parent_plugin = None
    """ Reference to the plugin that owns this object instance. """
    
    filepath_file_map = {}
    """ File associating file path with file information descriptor. """
    
    def __init__(self, parent_plugin):
        """
        Class constructor.
        
        @type parent_plugin: Plugin
        @param parent_plugin: Reference to the plugin that owns this object instance.
        """

        self.parent_plugin = parent_plugin
        self.filepath_file_map = {}
    
    def open(self, document_path):
        """
        Opens an OpenXML file.
        
        @type document_path: String
        @param document_path: Full path to the OpenXML document.
        """
        
        zip_plugin = self.parent_plugin.zip_plugin
        document_path = os.path.abspath(document_path)
        if os.path.isfile(document_path):
            temp_dir = tempfile.gettempdir()
            directory_paths_list = zip_plugin.get_directory_paths(document_path)
            file_paths_list = zip_plugin.get_file_paths(document_path)
            openxml_file = OpenXMLFile(document_path, temp_dir, directory_paths_list, file_paths_list)
            zip_plugin.unzip(document_path, temp_dir)
            self.filepath_file_map[document_path] = openxml_file
            return openxml_file    
            
    def close(self, document_path):
        """
        Closes a currently open OpenXML file.
        
        @type document_path: String
        @param document_path: Full path to the OpenXML document.
        """
        
        document_path = os.path.abspath(document_path)
        if document_path in self.filepath_file_map:
            file = self.filepath_file_map[document_path]
            file_path = file.get_file_path()
            extracted_file_path = file.get_extracted_file_path()
            directory_paths_list = file.get_directory_paths()
            directory_paths_list.reverse()
            file_paths_list = file.get_file_paths()
            self.parent_plugin.zip_plugin.zip(file_path, extracted_file_path, file_paths_list)
            for file_path in file_paths_list:
                os.remove(os.path.join(extracted_file_path, file_path))
            for directory_path in directory_paths_list:
                os.rmdir(os.path.join(extracted_file_path, directory_path[1:]))
            del self.filepath_file_map[document_path]
