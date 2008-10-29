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

class DocumentOdfPlugin(colony.plugins.plugin_system.Plugin):

    id = "pt.hive.colony.plugins.document.odt"
    name = "ODF Document plugin"
    short_name = "ODF Document"
    description = "description here"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["document.odt"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                   "pt.hive.colony.plugins.misc.zip", "1.0.0")]
    events_handled = []
    events_registrable = []

    zip_plugin = None
    
    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self) 
        global document
        import document.odt.document_odt

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.document.odt", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)
   
    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.zip")
    def set_zip_plugin(self, zip_plugin):
        self.zip_plugin = zip_plugin
        
    def open(self, document_manager_plugin, url, file_id):
        """
        Opens a document from the specified location and returns 
        document object that allows one to perform operations over it.
        
        @type document_manager_plugin: DocumentManagerPlugin
        @param document_manager_plugin: Reference to the document manager
        plugin (the document will need it to inform the manager when it closes).
        @type url: String
        @param url: Location of the desired document.
        @type file_id: Integer
        @param file_id: Identification number for this file as far as the document
        manager is concerned.
        
        @rtype: DocumentOdt
        @return: Document object encapsulating the specified document.
        """
        file = document.odt.document_odt.DocumentOdt(document_manager_plugin, self, url, file_id)
        file.open()
        return file
    
    def get_format(self):
        """
        Retrieves the document format supported by this plugins.
        
        @rtype: String
        @return: Returns a string indicating the document format supported by 
        this plugin.
        """
        return "odt"
