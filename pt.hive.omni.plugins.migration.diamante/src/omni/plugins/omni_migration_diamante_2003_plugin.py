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

class OmniMigrationDiamante2003Plugin(colony.plugins.plugin_system.Plugin):
    """
    Configuration used to migrate data from diamante 2003 to omni.
    """

    id = "pt.hive.omni.plugins.migration.diamante.2003"
    name = "Diamante to Omni Migration Diamante 2003 Plugin"
    short_name = "Diamante to Omni Migration Diamante 2003"
    description = "Configuration used to migrate data from diamante 2003 to omni"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["data_converter_configuration"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.omni.plugins.migration", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.resources.resource_manager", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.image_treatment", "1.0.0")]
    events_handled = []
    events_registrable = []

    diamante_2003_configuration = None
    """ The diamante 2003 to omni migration configuration """

    omni_migration_plugin = None
    """ Omni migration plugin """

    resource_manager_plugin = None
    """ Resource manager plugin """

    image_treatment_plugin = None
    """ Image treatment plugin """

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global omni_migration_diamante_2003
        import omni_migration_diamante_2003.diamante_2003.omni_migration_diamante_2003_system
        self.diamante_2003_configuration = omni_migration_diamante_2003.diamante_2003.omni_migration_diamante_2003_system.OmniMigrationDiamante2003(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.diamante_2003_configuration.load_data_converter_configuration()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.diamante_2003_configuration = None

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.omni.plugins.migration.diamante.2003", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.omni.plugins.migration.diamante.2003", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.omni.plugins.migration.diamante.2003", "1.0.0")
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

        return self.diamante_2003_configuration.get_intermediate_entity_schemas()

    def get_attribute_mapping_output_entities(self):
        """
        Returns the attribute mapping output entity configurations
        provided by this configuration.

        @rtype: List
        @return: The attribute mapping output entity
        configurations provided by this configuration.
        """

        return self.diamante_2003_configuration.get_attribute_mapping_output_entities()

    def get_relation_mapping_entities(self):
        """
        Returns the relation mapping entity configurations
        provided by this configuration.

        @rtype: List
        @return: Relation mapping entity configurations
        provided by this configuration.
        """

        return self.diamante_2003_configuration.get_relation_mapping_entities()

    def get_post_attribute_mapping_handlers(self):
        """
        Returns the post attribute mapping handlers
        provided by this configuration.

        @rtype: List
        @return: List of post attribute mapping handlers
        provided by this configuration.
        """

        return self.diamante_2003_configuration.get_post_attribute_mapping_handlers()

    def get_post_conversion_handlers(self):
        """
        Returns the post processing handlers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        return self.diamante_2003_configuration.get_post_conversion_handlers()

    def get_input_entity_indexers(self):
        """
        Returns the input entity indexers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        return self.diamante_2003_configuration.get_input_entity_indexers()

    def get_output_entity_indexers(self):
        """
        Returns the output entity indexers
        provided by this configuration.

        @rtype: List
        @return: List of post processing handlers
        provided by this configuration.
        """

        return self.diamante_2003_configuration.get_output_entity_indexers()

    def get_input_io_adapters_options(self):
        """
        Returns the input output adapter configuration
        to load data into the intermediate structure with.

        @rtype: List
        @return: List with maps with the input output adapter configuration.
        """

        return self.diamante_2003_configuration.get_input_io_adapters_options()

    def get_output_io_adapters_options(self):
        """
        Returns the input output adapter configuration
        to save the intermediate structure with.

        @rtype: List
        @return: List with maps with the output output adapter configuration.
        """

        return self.diamante_2003_configuration.get_output_io_adapters_options()

    def get_omni_migration_plugin(self):
        return self.omni_migration_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.omni.plugins.migration")
    def set_omni_migration_plugin(self, omni_migration_plugin):
        self.omni_migration_plugin = omni_migration_plugin

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin

    def get_image_treatment_plugin(self):
        return self.image_treatment_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.image_treatment")
    def set_image_treatment_plugin(self, image_treatment_plugin):
        self.image_treatment_plugin = image_treatment_plugin
