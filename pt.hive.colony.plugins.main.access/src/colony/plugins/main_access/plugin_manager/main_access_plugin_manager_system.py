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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class MainAccessPluginManager:

    main_access_plugin_manager_plugin = None
    """ The main access plugin manager plugin """

    manager = None
    """ The manager """

    def __init__(self, main_access_plugin_manager_plugin):
        self.main_access_plugin_manager_plugin = main_access_plugin_manager_plugin
        self.manager = main_access_plugin_manager_plugin.manager

    def get_plugin_by_id(self, plugin_id):
        return self.manager._get_plugin_by_id(plugin_id)

    def get_plugin_by_id_and_version(self, plugin_id, plugin_version):
        return self.manager._get_plugin_by_id_and_version(plugin_id, plugin_version)

    def get_plugins_by_capability(self, capability):
        return self.manager._get_plugins_by_capability(capability)

    def get_plugins_by_capability_allowed(self, capability_allowed):
        return self.manager._get_plugins_by_capability_allowed(capability_allowed)
