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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import build_automation_parser

class BuildAutomation:
    """
    The build automation class.
    """

    build_automation_plugin = None
    """ The build automation plugin """

    stages = ["compile", "test", "package", "install", "deploy", "clean", "site", "site-deploy"]
    """ The build automation stages """

    def __init__(self, build_automation_plugin):
        """
        Constructor of the class.
        
        @type build_automation_plugin: BuildAutomationPlugin
        @param build_automation_plugin: The build automation plugin.
        """

        self.build_automation_plugin = build_automation_plugin

    def run_automation_plugin_id(self, plugin_id):
        """
        Runs all the automation plugins for the given plugin id.
        
        @type plugin_id: String
        @param plugin_id: The id of the plugin to run all the automation plugins.
        """

        # retrieves the build automation plugin path
        build_automation_plugin_path = self.build_automation_plugin.manager.get_plugin_path_by_id(self.build_automation_plugin.id)

        # creates the base baf xml path
        base_baf_xml_path = build_automation_plugin_path + "/build_automation/automation/resources/base_baf.xml"

        # creates the build automation file parser
        build_automation_file_parser = build_automation_parser.BuildAutomationFileParser(base_baf_xml_path)

        # parses the baf xml file
        build_automation_file_parser.parse()

        # retrieves the build automation value
        build_automation = build_automation_file_parser.get_value()
