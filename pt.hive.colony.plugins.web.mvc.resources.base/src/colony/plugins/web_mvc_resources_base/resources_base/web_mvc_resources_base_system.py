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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

WEB_MVC_RESOURCES_BASE_RESOURCES_PATH = "web_mvc_resources_base/resources_base/resources"
""" The web mvc resources base resources path """

EXTRAS_PATH = WEB_MVC_RESOURCES_BASE_RESOURCES_PATH + "/extras"
""" The extras path """

class WebMvcResourcesBase:
    """
    The web mvc resources base class.
    """

    web_mvc_resources_base_plugin = None
    """ The web mvc resources base plugin """

    def __init__(self, web_mvc_resources_base_plugin):
        """
        Constructor of the class.

        @type web_mvc_resources_base_plugin: WebMvcResourcesBasePlugin
        @param web_mvc_resources_base_plugin: The web mvc resources base plugin.
        """

        self.web_mvc_resources_base_plugin = web_mvc_resources_base_plugin

    def get_resources_path(self):
        """
        Retrieves the path to the resources.
        This path should be used as the base reference to the resources.

        @rtype: String
        @return: The path to the resources.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_resources_base_plugin.manager

        # retrieves the web mvc resources base plugin path
        web_mvc_resources_base_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_resources_base_plugin.id)

        # creates the extras path
        extras_path = web_mvc_resources_base_plugin_path + "/" + EXTRAS_PATH

        # returns the extras path
        return extras_path
