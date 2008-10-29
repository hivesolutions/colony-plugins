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

import colony.plugins.plugin_system

class DocumentManagerPlugin(colony.plugins.plugin_system.Plugin):

    id = "pt.hive.colony.plugins.document.manager"
    name = "Document Manager plugin"
    short_name = "Document manager"
    description = "Manages open document instances, acts as a middleman" \
    " to the plugins supporting each document format, and provides a generic" \
    " document template object that allows the interchange of data between document" \
    " plugins supporting different formats."
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["plugin_test_case_bundle"]
    capabilities_allowed = ["document"]
    dependencies = []
    events_handled = []
    events_registrable = []

    format_plugins_map = {}
    """ Map associating a file format with a list of the plugins that handle it. """
    
    document_manager = None
    """ Object that tracks open documents. """
    
    document_test = None
    """ Object with the test suite for this plugin. """
    
    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self) 
        global document
        import document.document_manager
        import document.document_template
        import document.document_test
        self.document_manager = document.document_manager.DocumentManager(self)
        self.document_test = document.document_test.DocumentTest(self)

    def unload_plugin(self):
        self.format_plugins_map = {}
        self.document_manager = None
        self.document_test = None
        
    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.document.manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)
        
    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.document.manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)
    
    @colony.plugins.decorators.load_allowed_capability("document")
    def document_load_allowed(self, plugin, capability):
        format = plugin.get_format()
        if not format in self.format_plugins_map:
            self.format_plugins_map[format] = []
        format_plugins = self.format_plugins_map[format]
        format_plugins.append(plugin)
    
    @colony.plugins.decorators.unload_allowed_capability("document")
    def document_unload_allowed(self, plugin, capability):
        format = plugin.get_format()
        format_plugins = self.format_plugins_map[format]
        format_plugins.remove(plugin)
        
    def get_plugin_test_case_bundle(self):
        return self.document_test.get_plugin_test_case_bundle()

    def get_supported_formats(self):
        """
        Returns a list with the formats supported by the document manager.
        
        @rtype: Array
        @return: List of supported document formats.
        """
        formats = self.format_plugins_map.keys()
        return formats
            
    def get_document_plugin(self, format):
        """
        Retrieves the plugin that is capable of handling the specified document format.
        
        @type format: String
        @param format: Desired document format.
        @rtype: Plugin
        @return: Plugin capable of handling the specified document format.
        """
        format_plugins = self.format_plugins_map[format]
        if len(format_plugins) > 0:
            format_plugin = format_plugins[0]
            return format_plugin

    def get_open_documents(self):
        """
        Retrieves with references to the currently open documents.
        
        @rtype: Array
        @return: List of open documents.
        """
        open_documents = self.document_manager.get_open_documents()
        return open_documents
        
    def get_new_template(self):
        """
        Retrieves an empty document template object.
        
        @rtype: DocumentTemplate
        @return: Empty document template.
        """
        template = document.document_template.DocumentTemplate()
        return template
    
    def open(self, url, format):
        """
        Opens a document of the specified format and location.
        
        @type url: String
        @param url: Location of the desired document.
        @type format: String
        @param format: Format of the desired document.
        @rtype: Document
        @return: Returns a document object, or None if there is no plugin 
        supporting this document format, or the document is not found.
        """
        document_plugin = self.get_document_plugin(format)
        if document_plugin is not None:
            document = self.document_manager.open(document_plugin, url)
            return document

    def close(self, document):
        """
        Removes the document from the document manager.
        
        @type document: Document
        @param document: Reference to a document object.
        """
        self.document_manager.close(document)
    