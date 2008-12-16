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

import os

import web_deployment_parser

DEPLOYER_TYPE = "web"

class WebDeployer:

    web_deployer_plugin = None

    def __init__(self, web_deployer_plugin):
        self.web_deployer_plugin = web_deployer_plugin

    def load_deployer(self):
        self.web_deployer_plugin.logger.info("Loading web deployer")

        # adds the new resource to the resource manager
        self.web_deployer_plugin.resource_manager_plugin.register_resource(self.web_deployer_plugin.id, "web_configuration", "xml", "resources/web_deployer_configuration.xml")

    def deploy_package(self, zip_file, plugin_id, plugin_version):
        zip_file_name = zip_file.name
        self.web_deployer_plugin.logger.info("Deploying zip file: " + zip_file_name + " using web deployer")

        # retrieves the resource (web configuration resource)
        web_configuration_resource = self.web_deployer_plugin.resource_manager_plugin.get_resource(self.web_deployer_plugin.id)

        # retrieves the resource value (web configuration path)
        web_configuration_path = web_configuration_resource.get_resource_value()

        # creates the full web configuration path
        full_web_configuration_path = os.path.join(os.path.dirname(__file__), web_configuration_path)

        # creates a new parser for the web configuration file
        web_configuration_file_parser = web_deployment_parser.WebDeployerConfigurationFileParser(full_web_configuration_path)

        # parsers the web configuration file
        web_configuration_file_parser.parse()

        # retrieves the web deployer configuration
        web_deployer_configuration = web_configuration_file_parser.get_web_deployer_configuration()

        # constructs the web deployment path
        web_deployment_path = web_deployer_configuration.web_apps_path + "/" + web_deployer_configuration.project_path + "/" + web_deployer_configuration.plugins_path

        # uncompresses the zip file into the target plugins directory
        self.uncompress_zip_file(zip_file, web_deployment_path)

    def get_deployer_type(self):
        """
        Retrieves the type of deployer.
        
        @rtype: String
        @return: The type of deployer.
        """

        return DEPLOYER_TYPE

    def uncompress_zip_file(self, file, web_deployment_path):
        """
        Uncompresses a zip file into the plugins directory
        
        @type file: Stream
        @param file: The file to unzip into the plugins directory
        @type web_deployment_path: String
        @param web_deployment_path: The path to unzip the zip file
        """

        # retrieves the zip file name
        file_name = file.name

        # retrieves the zip plugin from the colony deployer plugin
        zip_plugin = self.web_deployer_plugin.zip_plugin

        # extracts the zip file
        zip_plugin.unzip(file_name, web_deployment_path)
