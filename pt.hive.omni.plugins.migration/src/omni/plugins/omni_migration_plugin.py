#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Omni ERP
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1805 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-03-10 08:56:01 +0000 (Tue, 10 Mar 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class OmniMigrationPlugin(colony.plugins.plugin_system.Plugin):
    """
    Configuration used to migrate data to omni.
    """

    id = "pt.hive.omni.plugins.migration"
    name = "Omni Migration Plugin"
    short_name = "Omni Migration"
    description = "Configuration used to migrate data to omni"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = []
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    omni_migration_configuration = None
    """ The omni migration configuration """

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global omni_migration
        import omni_migration.omni_migration_system
        self.omni_migration_configuration = omni_migration.omni_migration_system.OmniMigration(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.omni_migration_configuration.load_data_converter_configuration()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.omni_migration_configuration = None

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.omni.plugins.migration", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.omni.plugins.migration", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.omni.plugins.migration", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_intermediate_entity_schemas(self):
        """
        Returns the intermediate structure schemas
        provided by this configuration.

        @rtype: List
        @return: The intermediate structure schema
        configurations provided by this configuration.
        """

        return self.omni_migration_configuration.get_intermediate_entity_schemas()

    def get_attribute_mapping_output_entities(self):
        """
        Returns the attribute mapping output entity configurations
        provided by this configuration.

        @rtype: List
        @return: The attribute mapping output entity
        configurations provided by this configuration.
        """

        return self.omni_migration_configuration.get_attribute_mapping_output_entities()

    def get_relation_mapping_entities(self):
        """
        Returns the relation mapping entity configurations
        provided by this configuration.

        @rtype: List
        @return: Relation mapping entity configurations
        provided by this configuration.
        """

        return self.omni_migration_configuration.get_relation_mapping_entities()

    def get_post_attribute_mapping_handlers(self):
        """
        Returns the post attribute mapping handlers
        provided by this configuration.

        @rtype: List
        @return: List of post attribute mapping handlers
        provided by this configuration.
        """

        return self.omni_migration_configuration.get_post_attribute_mapping_handlers()

    def get_post_relation_mapping_handlers(self):
        """
        Returns the post relation mapping handlers
        provided by this configuration.

        @rtype: List
        @return: List of post relation mapping handlers
        provided by this configuration.
        """

        return self.omni_migration_configuration.get_post_relation_mapping_handlers()

    def get_post_conversion_handlers(self):
        """
        Returns the post processing handlers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        return self.omni_migration_configuration.get_post_conversion_handlers()

    def get_input_entity_indexers(self):
        """
        Returns the input entity indexers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        return self.omni_migration_configuration.get_input_entity_indexers()

    def get_output_entity_indexers(self):
        """
        Returns the output entity indexers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        return self.omni_migration_configuration.get_output_entity_indexers()

    def get_input_io_adapters_options(self):
        """
        Returns the input output adapter configuration
        to load data into the intermediate structure with.

        @rtype: List
        @return: List with maps with the input output adapter configuration.
        """

        return self.omni_migration_configuration.get_input_io_adapters_options()

    def get_output_io_adapters_options(self):
        """
        Returns the input output adapter configuration
        to save the intermediate structure with.

        @rtype: List
        @return: List with maps with the output output adapter configuration.
        """

        return self.omni_migration_configuration.get_output_io_adapters_options()
