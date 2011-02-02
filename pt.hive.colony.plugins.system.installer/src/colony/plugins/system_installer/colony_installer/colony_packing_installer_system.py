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

INSTALLER_TYPE = "colony_packing"
""" The installer type """

class ColonyPackingInstaller:
    """
    The colony packing installer class.
    """

    colony_packing_installer_plugin = None
    """ The colony packing installer plugin """

    def __init__(self, colony_packing_installer_plugin):
        """
        Constructor of the class.

        @type colony_packing_installer_plugin: ColonyPackingInstallerPlugin
        @param colony_packing_installer_plugin: The colony packing installer plugin.
        """

        self.colony_packing_installer_plugin = colony_packing_installer_plugin

    def load_installer(self):
        """
        Method called upon load of the installer.
        """

        self.colony_packing_installer_plugin.info("Loading colony packing installer")

    def get_installer_type(self):
        """
        Retrieves the type of deployer.

        @rtype: String
        @return: The type of deployer.
        """

        return INSTALLER_TYPE

    def deploy_bundle(self, file_path, properties):
        """
        Method called upon deployment of the bundle with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the bundle file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        pass

#        # retrieves the plugin manager
#        plugin_manager = self.colony_packing_deployer_plugin.manager
#
#        # retrieves the packing manager plugin
#        packing_manager_plugin = self.colony_packing_deployer_plugin.packing_manager_plugin
#
#        # retrieves the main plugin path as the plugin path
#        # for deployment
#        plugin_path = plugin_manager.get_main_plugin_path()
#
#        # creates the properties map for the file unpacking packing
#        properties = {TARGET_PATH_VALUE : plugin_path}
#
#        # unpacks the files using the colony service
#        packing_manager_plugin.unpack_files([contents_file.name], properties, COLONY_VALUE)

    def deploy_plugin(self, plugin_id, plugin_version, contents_file):
        """
        Method called upon deployment of the plugin with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the plugin file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        pass

#        # retrieves the plugin manager
#        plugin_manager = self.colony_packing_deployer_plugin.manager
#
#        # retrieves the packing manager plugin
#        packing_manager_plugin = self.colony_packing_deployer_plugin.packing_manager_plugin
#
#        # retrieves the main plugin path as the plugin path
#        # for deployment
#        plugin_path = plugin_manager.get_main_plugin_path()
#
#        # creates the properties map for the file unpacking packing
#        properties = {TARGET_PATH_VALUE : plugin_path}
#
#        # unpacks the files using the colony service
#        packing_manager_plugin.unpack_files([contents_file.name], properties, COLONY_VALUE)
