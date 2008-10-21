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
import colony.plugins.decorators

class HiveFSPlugin(colony.plugins.plugin_system.Plugin):

    id = "pt.hive.colony.plugins.hivefs"
    name = "Hive Filesystem plugin"
    short_name = "HiveFS plugin"
    description = "Hive file system plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["rpc_service"]
    capabilities_allowed = ["document_generator"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.io.openxml", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.resource_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    hivefs = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""

    openxml_plugin = None
    resource_manager_plugin = None
    document_generator_plugins = []

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global hivefs
        global base64
        global random
        global shutil
        global tempfile
        import base64
        import random
        import shutil
        import tempfile

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.codebase = None
        self.openxml_plugin = None
        self.resource_manager_plugin = None
        self.document_generator_plugins = None

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.hivefs", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.hivefs", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.hivefs", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.plugins.decorators.plugin_call(True)
    def get_service_id(self):
        return "hivefs"

    @colony.plugins.decorators.plugin_call(True)
    def get_service_alias(self):
        return []

    @colony.plugins.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return [self.get_files, self.get_template]

    @colony.plugins.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return {self.get_files : [], self.get_template : []}

    def get_files(self, entity_name, file_format):
        for document_generator_plugin in self.document_generator_plugins:
            if document_generator_plugin.get_supported_entity() == entity_name and document_generator_plugin.get_supported_format() == file_format:
                files_list = document_generator_plugin.get_files()
                return files_list
        
    def get_template(self, entity_name, file_format):
        for document_generator_plugin in self.document_generator_plugins:
            if document_generator_plugin.get_supported_entity() == entity_name and document_generator_plugin.get_supported_format() == file_format:
                template_content = document_generator_plugin.get_template()
                return template_content

    def update_file(self, entity_name, file_format, uid, new_content_b64):
        new_content = base64.b64decode(new_content_b64)
        temp_docx_file_path = os.path.join(tempfile.gettempdir(), "tempdoc.docx")
        file = open(temp_docx_file_path, "w")
        file.write(new_content)
        file.close()
        document = openxml_plugin.open(temp_docx_file_path)
        document_path = document.get_full_path("word/document.xml")
        file = open(document_path, "r")
        new_content = file.read()
        file.close()
        document.close()
        for document_generator_plugin in self.document_generator_plugins:
            if document_generator_plugin.get_supported_entity() == entity_name and document_generator_plugin.get_supported_format() == file_format:
                document_generator_plugin.update_file(entity_name, file_format, uid, new_content)   

    def create_file(self, entity_name, file_format, content_b64):
        content = base64.b64decode(content_b64)
        temp_docx_file_path = os.path.join(tempfile.gettempdir(), "tempdoc.docx")
        file = open(temp_docx_file_path, "w")
        file.write(content)
        file.close()
        document = openxml_plugin.open(temp_docx_file_path)
        document_path = document.get_full_path("word/document.xml")
        file = open(document_path, "r")
        content = file.read()
        file.close()
        document.close()
        for document_generator_plugin in self.document_generator_plugins:
            if document_generator_plugin.get_supported_entity() == entity_name and document_generator_plugin.get_supported_format() == file_format:
                document_generator_plugin.create_file(entity_name, file_format, content)
                
    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.io.openxml")
    def set_openxml_plugin(self, openxml_plugin):
        self.openxml_plugin = openxml_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin

    @colony.plugins.decorators.load_allowed_capability("document_generator")
    def document_generator_capability_load_allowed(self, plugin, capability):
        self.document_generator_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("document_generator")
    def document_generator_capability_unload_allowed(self, plugin, capability):
        if plugin in self.document_generator_plugins:
            self.document_generator_plugins.remove(plugin)
            