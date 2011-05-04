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

__revision__ = "$LastChangedRevision: 11875 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-11-11 01:33:21 +0000 (Qui, 11 Nov 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import system_installer_exceptions

class SystemInstaller:
    """
    The system installer class.
    """

    system_installer_plugin = None
    """ The system installer plugin """

    installer_plugins_map = {}
    """ The installer plugins map """

    def __init__(self, system_installer_plugin):
        """
        Constructor of the class.

        @type system_installer_plugin: SystemInstallerPlugin
        @param system_installer_plugin: The system installer plugin.
        """

        self.system_installer_plugin = system_installer_plugin

        self.installer_plugins_map = {}

    def install_package(self, file_path, properties, installer_type):
        # retrieves the installer plugin for the installer type
        installer_plugin = self._get_installer_plugin_by_installer_type(installer_type)

        # installs the package with the installer plugin
        installer_plugin.install_package(file_path, properties)

    def install_bundle(self, file_path, properties, installer_type):
        # retrieves the installer plugin for the installer type
        installer_plugin = self._get_installer_plugin_by_installer_type(installer_type)

        # installs the bundle with the installer plugin
        installer_plugin.install_bundle(file_path, properties)

    def install_plugin(self, file_path, properties, installer_type):
        # retrieves the installer plugin for the installer type
        installer_plugin = self._get_installer_plugin_by_installer_type(installer_type)

        # installs the plugin with the installer plugin
        installer_plugin.install_plugin(file_path, properties)

    def uninstall_plugin(self, plugin_id, plugin_version, properties, installer_type):
        # retrieves the installer plugin for the installer type
        installer_plugin = self._get_installer_plugin_by_installer_type(installer_type)

        # uninstalls the plugin with the installer plugin
        installer_plugin.uninstall_plugin(plugin_id, plugin_version, properties)

    def installer_load(self, installer_plugin):
        # retrieves the plugin installer type
        installer_type = installer_plugin.get_installer_type()

        # adds the installer plugin to the installer
        # plugins map
        self.installer_plugins_map[installer_type] = installer_plugin

    def installer_unload(self, installer_plugin):
        # retrieves the plugin installer type
        installer_type = installer_plugin.get_installer_type()

        # removes the installer plugin from the installer
        # plugins map
        del self.installer_plugins_map[installer_type]

    def _get_installer_plugin_by_installer_type(self, installer_type):
        """
        Retrieves a installer plugin for the given installer type.

        @type installer_type : String
        @param installer_type: The type of the installer to retrieve.
        @rtype: Plugin
        @return: The installer plugin for the given installer type.
        """

        # in case the installer type does not exist in the installer
        # plugins map
        if not installer_type in self.installer_plugins_map:
            # raises the missing installer exception
            raise system_installer_exceptions.MissingInstaller(installer_type)

        # retrieves the installer plugin from the installer plugins map
        installer_plugin = self.installer_plugins_map[installer_type]

        # returns the installer plugin
        return installer_plugin
