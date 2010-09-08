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

PLUGINS_DIRECTORY = "colony/plugins"
""" The plugins directory value """

class ColonyPackingDeployer:
    """
    The colony packing deployer class.
    """

    colony_packing_deployer_plugin = None
    """ The colony packing deployer plugin """

    def __init__(self, colony_packing_deployer_plugin):
        """
        Constructor of the class.

        @type colony_packing_deployer_plugin: ColonyPackingDeployerPlugin
        @param colony_packing_deployer_plugin: The colony packing deployer plugin.
        """

        self.colony_packing_deployer_plugin = colony_packing_deployer_plugin

    def load_deployer(self):
        self.colony_packing_deployer_plugin.info("Loading colony packing deployer")

    def deploy_package(self, contents_file, plugin_id, plugin_version):
        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_deployer_plugin.packing_manager_plugin

        # creates the properties map for the file unpacking packing
        properties = {"target_path" : PLUGINS_DIRECTORY}

        # unpacks the files using the colony service
        packing_manager_plugin.unpack_files([contents_file.name], properties, "colony")

    def get_deployer_type(self):
        """
        Retrieves the type of deployer.

        @rtype: String
        @return: The type of deployer.
        """

        return DEPLOYER_TYPE
