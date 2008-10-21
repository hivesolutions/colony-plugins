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

__revision__ = "$LastChangedRevision: 1615 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-08-07 18:45:11 +0100 (Qui, 07 Ago 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class CustomersDocxPlugin(colony.plugins.plugin_system.Plugin):

    id = "pt.hive.colony.plugins.hivefs.customers_docx"
    name = "Hive Filesystem Customers DOCX plugin"
    short_name = "HiveFS Customers DOCX plugin"
    description = "Hive file system Customers DOCX plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["document_generator.docx"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.io.openxml", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.prototype.business.services", "1.0.0")]
    events_handled = []
    events_registrable = []

    codebase = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""

    openxml_plugin = None
    business_services_plugin = None
    
    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global hivefs
        import hivefs.customers.customers_docx_system
        
    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.codebase = None
        self.openxml_plugin = None
        self.business_services_plugin = None

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.codebase = hivefs.customers.customers_docx_system.HiveFSCustomersDocx(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.hivefs.customers_docx", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.io.openxml")
    def set_openxml_plugin(self, openxml_plugin):
        self.openxml_plugin = openxml_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.prototype.business.services")    
    def set_business_services_plugin(self, business_services_plugin):
        self.business_services_plugin = business_services_plugin

    def get_supported_entity(self):
        return "clientes"

    def get_supported_format(self):
        return "docx"

    def get_files(self):
        return self.codebase.get_files()

    def get_template(self):
        return self.codebase.get_template()

    def update_file(self, uid, new_content):
        self.codebase.update_file(uid, new_content)

    def create_file(self, content):
        self.codebase.create_file(content)
