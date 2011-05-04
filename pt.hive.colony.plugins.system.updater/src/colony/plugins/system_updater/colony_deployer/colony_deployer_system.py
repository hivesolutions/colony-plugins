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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

import colony_deployer_exceptions

DEPLOYER_TYPE = "colony"
""" The deployer type """

PLUGINS_DIRECTORY = "colony/plugins"
""" The plugins directory """

class ColonyDeployer:
    """
    The colony deployer class.
    """

    colony_deployer_plugin = None
    """ The colony deployer plugin """

    def __init__(self, colony_deployer_plugin):
        """
        Constructor of the class.

        @type colony_deployer_plugin: ColonyDeployerPlugin
        @param colony_deployer_plugin: The colony deployer plugin.
        """

        self.colony_deployer_plugin = colony_deployer_plugin

    def load_deployer(self):
        """
        Method called upon load of the deployer.
        """

        self.colony_deployer_plugin.info("Loading colony deployer")

    def get_deployer_type(self):
        """
        Retrieves the type of deployer.

        @rtype: String
        @return: The type of deployer.
        """

        return DEPLOYER_TYPE

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

        # raises an operation not implemented exception
        raise colony_deployer_exceptions.OperationNotSupported("not possible to deploy colony bundles")

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

        # retrieves the plugin manager
        plugin_manager = self.colony_deployer_plugin.manager

        # in case the plugin already exist in the plugin manager
        if plugin_manager._get_plugin_by_id_and_version(plugin_id, plugin_version):
            # returns immediately
            return

        # retrieves the zip file name
        contents_file_name = contents_file.name

        # prints some logging information
        self.colony_deployer_plugin.info("Deploying contents file: " + contents_file_name + " using colony deployer")

        # uncompresses the zip file
        self._uncompress_zip_file(contents_file)

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

        pass

    def commit_transaction(self, transaction_properties):
        """
        Commits the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be commited.
        """

        pass

    def rollback_transaction(self, transaction_properties):
        """
        "Rollsback" the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be "rollbacked".
        """

        pass

    def _uncompress_zip_file(self, file):
        """
        Uncompresses a zip file into the plugins directory.

        @type file: Stream
        @param file: The file to unzip into the plugins directory.
        """

        # retrieves the zip file name
        file_name = file.name

        # retrieves the zip plugin from the colony deployer plugin
        zip_plugin = self.colony_deployer_plugin.zip_plugin

        # extracts the zip file
        zip_plugin.unzip(file_name, PLUGINS_DIRECTORY)
