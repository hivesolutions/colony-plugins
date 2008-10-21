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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

PLUGINS_DIRECTORY = "colony/plugins"

class colonyDeployer:

    colony_deployer_plugin = None

    def __init__(self, colony_deployer_plugin):
        self.colony_deployer_plugin = colony_deployer_plugin

    def load_deployer(self):
        self.colony_deployer_plugin.logger.info("Loading colony deployer")

    def deploy_package(self, zip_file, plugin_id, plugin_version):
        plugin_manager = self.colony_deployer_plugin.manager

        # in case the plugin already exist in the plugin manager
        if plugin_manager._get_plugin_by_id_and_version(plugin_id, plugin_version):
            return

        zip_file_name = zip_file.name
        self.colony_deployer_plugin.logger.info("Deploying zip file: " + zip_file_name + " using colony deployer")
        self.uncompress_zip_file(zip_file)

    def uncompress_zip_file(self, file):
        """
        Uncompresses a zip file into the plugins directory
        
        @type file: Stream
        @param file: The file to unzip into the plugins directory
        """

        # retrieves the zip file name
        file_name = file.name

        # retrieves the zip plugin from the colony deployer plugin
        zip_plugin = self.colony_deployer_plugin.zip_plugin

        # extracts the zip file
        zip_plugin.unzip(file_name, PLUGINS_DIRECTORY)
