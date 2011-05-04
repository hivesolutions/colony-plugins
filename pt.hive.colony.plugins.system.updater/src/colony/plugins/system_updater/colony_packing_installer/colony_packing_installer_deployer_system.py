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

__revision__ = "$LastChangedRevision: 2349 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:52:01 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

DEPLOYER_TYPE = "colony_packing"
""" The deployer type """

UPGRADE_VALUE = "upgrade"
""" The upgrade value """

class ColonyPackingInstallerDeployer:
    """
    The colony packing installer deployer class.
    """

    colony_packing_installer_deployer_plugin = None
    """ The colony packing installer deployer plugin """

    def __init__(self, colony_packing_installer_deployer_plugin):
        """
        Constructor of the class.

        @type colony_packing_installer_deployer_plugin: ColonyPackingInstallerDeployerPlugin
        @param colony_packing_installer_deployer_plugin: The colony packing installer deployer plugin.
        """

        self.colony_packing_installer_deployer_plugin = colony_packing_installer_deployer_plugin

    def load_deployer(self):
        """
        Method called upon load of the deployer.
        """

        self.colony_packing_installer_deployer_plugin.info("Loading colony packing installer deployer")

    def get_deployer_type(self):
        """
        Retrieves the type of deployer.

        @rtype: String
        @return: The type of deployer.
        """

        return DEPLOYER_TYPE

    def deploy_bundle(self, bundle_id, bundle_version, contents_file):
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
        """

        # retrieves the colony packing installer plugin
        colony_packing_installer_plugin = self.colony_packing_installer_deployer_plugin.colony_packing_installer_plugin

        # installation options
        installation_properties = {
            UPGRADE_VALUE : True
        }

        # installs the package (plugin)
        colony_packing_installer_plugin.install_package(contents_file.name, installation_properties)

    def deploy_plugin(self, plugin_id, plugin_version, contents_file):
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
        """

        # retrieves the colony packing installer plugin
        colony_packing_installer_plugin = self.colony_packing_installer_deployer_plugin.colony_packing_installer_plugin

        # installation options
        installation_properties = {
            UPGRADE_VALUE : True
        }

        # installs the package (plugin)
        colony_packing_installer_plugin.install_package(contents_file.name, installation_properties)
