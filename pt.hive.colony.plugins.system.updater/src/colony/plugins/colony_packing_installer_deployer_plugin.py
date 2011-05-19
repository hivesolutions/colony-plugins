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

class ColonyPackingInstallerDeployerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Colony Packing Installer Deployer plugin.
    """

    id = "pt.hive.colony.plugins.system.updater.colony_packing_installer_deployer"
    name = "Colony Packing Installer Deployer Plugin"
    short_name = "Colony Packing Installer Deployer"
    description = "Colony Packing Installer Deployer Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/system_updater/colony_packing_installer/resources/baf.xml"
    }
    capabilities = [
        "deployer",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.system.installer.colony_packing_installer", "1.0.0")
    ]
    main_modules = [
        "system_updater.colony_packing_installer.colony_packing_installer_deployer_exceptions",
        "system_updater.colony_packing_installer.colony_packing_installer_deployer_system"
    ]

    colony_packing_installer_deployer = None
    """ The colony packing installer deployer """

    colony_packing_installer_plugin = None
    """ The colony packing installer plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import system_updater.colony_packing_installer.colony_packing_installer_deployer_system
        self.colony_packing_installer_deployer = system_updater.colony_packing_installer.colony_packing_installer_deployer_system.ColonyPackingInstallerDeployer(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.colony_packing_installer_deployer.load_deployer()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.system.updater.colony_packing_installer_deployer", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_deployer_type(self):
        return self.colony_packing_installer_deployer.get_deployer_type()

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

        return self.colony_packing_installer_deployer.deploy_bundle(bundle_id, bundle_version, contents_file, transaction_properties)

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

        return self.colony_packing_installer_deployer.deploy_plugin(plugin_id, plugin_version, contents_file, transaction_properties)

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

        return self.colony_packing_installer_deployer.open_transaction(transaction_properties)

    def commit_transaction(self, transaction_properties):
        """
        Commits the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be commited.
        """

        return self.colony_packing_installer_deployer.commit_transaction(transaction_properties)

    def rollback_transaction(self, transaction_properties):
        """
        "Rollsback" the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be "rollbacked".
        """

        return self.colony_packing_installer_deployer.rollback_transaction(transaction_properties)

    def get_colony_packing_installer_plugin(self):
        return self.colony_packing_installer_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.system.installer.colony_packing_installer")
    def set_colony_packing_installer_plugin(self, colony_packing_installer_plugin):
        self.colony_packing_installer_plugin = colony_packing_installer_plugin
