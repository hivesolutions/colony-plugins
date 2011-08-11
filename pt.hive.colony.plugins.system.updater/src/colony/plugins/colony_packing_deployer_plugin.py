#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 7715 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-26 07:31:00 +0000 (sex, 26 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class ColonyPackingDeployerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Colony Packing Deployer plugin.
    """

    id = "pt.hive.colony.plugins.system.updater.colony_packing_deployer"
    name = "Colony Packing Deployer Plugin"
    short_name = "Colony Packing Deployer"
    description = "Colony Packing Deployer Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/system_updater/colony_packing/resources/baf.xml"
    }
    capabilities = [
        "deployer",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.packing.manager", "1.0.0")
    ]
    main_modules = [
        "system_updater.colony_packing.colony_packing_deployer_exceptions",
        "system_updater.colony_packing.colony_packing_deployer_system"
    ]

    colony_packing_deployer = None
    """ The colony packing deployer """

    packing_manager_plugin = None
    """ Plugin for packing of files """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import system_updater.colony_packing.colony_packing_deployer_system
        self.colony_packing_deployer = system_updater.colony_packing.colony_packing_deployer_system.ColonyPackingDeployer(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.colony_packing_deployer.load_deployer()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_deployer_type(self):
        return self.colony_packing_deployer.get_deployer_type()

    def deploy_bundle(self, bundle_id, bundle_version, contents_file, transaction_properties):
        """
        Method called upon deployment of the bundle with
        the given id, version and contents file.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to be deployed.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to be deployed.
        @type contents_file: ContentsFile
        @param contents_file: The contents file of the bundle to
        be deployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        return self.colony_packing_deployer.deploy_bundle(bundle_id, bundle_version, contents_file, transaction_properties)

    def deploy_plugin(self, plugin_id, plugin_version, contents_file, transaction_properties):
        """
        Method called upon deployment of the plugin with
        the given id, version and contents file.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be deployed.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be deployed.
        @type contents_file: ContentsFile
        @param contents_file: The contents file of the plugin to
        be deployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        return self.colony_packing_deployer.deploy_plugin(plugin_id, plugin_version, contents_file, transaction_properties)

    def deploy_container(self, container_id, container_version, contents_file, transaction_properties):
        """
        Method called upon deployment of the container with
        the given id, version and contents file.

        @type container_id: String
        @param container_id: The id of the container to be deployed.
        @type container_version: String
        @param container_version: The version of the container to be deployed.
        @type contents_file: ContentsFile
        @param contents_file: The contents file of the container to
        be deployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        return self.colony_packing_deployer.deploy_container(container_id, container_version, contents_file, transaction_properties)

    def undeploy_bundle(self, bundle_id, bundle_version, transaction_properties):
        """
        Method called upon undeployment of the bundle with
        the given id and version.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to be undeployed.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to be undeployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        return self.colony_packing_deployer.undeploy_bundle(bundle_id, bundle_version, transaction_properties)

    def undeploy_plugin(self, plugin_id, plugin_version, transaction_properties):
        """
        Method called upon undeployment of the plugin with
        the given id and version.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be undeployed.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be undeployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        return self.colony_packing_deployer.undeploy_plugin(plugin_id, plugin_version, transaction_properties)

    def undeploy_container(self, container_id, container_version, transaction_properties):
        """
        Method called upon undeployment of the container with
        the given id and version.

        @type container_id: String
        @param container_id: The id of the container to be undeployed.
        @type container_version: String
        @param container_version: The version of the container to be undeployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        return self.colony_packing_deployer.undeploy_container(container_id, container_version, transaction_properties)

    def open_transaction(self, transaction_properties):
        """
        Opens a new transaction and retrieves the transaction
        properties map.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the current transaction.
        @rtype: Dictionary
        @return: The map describing the transaction.
        """

        return self.colony_packing_deployer.open_transaction(transaction_properties)

    def commit_transaction(self, transaction_properties):
        """
        Commits the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be commited.
        """

        return self.colony_packing_deployer.commit_transaction(transaction_properties)

    def rollback_transaction(self, transaction_properties):
        """
        "Rollsback" the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be "rollbacked".
        """

        return self.colony_packing_deployer.rollback_transaction(transaction_properties)

    def get_packing_manager_plugin(self):
        return self.packing_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.packing.manager")
    def set_packing_manager_plugin(self, packing_manager_plugin):
        self.packing_manager_plugin = packing_manager_plugin
