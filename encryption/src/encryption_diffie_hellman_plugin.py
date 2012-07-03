#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class EncryptionDiffieHellmanPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Diffie Hellman Encryption plugin.
    """

    id = "pt.hive.colony.plugins.encryption.diffie_hellman"
    name = "Diffie Hellman Encryption Plugin"
    short_name = "Diffie Hellman Encryption"
    description = "The plugin that offers the diffie hellman encryption support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/encryption/diffie_hellman/resources/baf.xml"
    }
    capabilities = [
        "encryption.diffie_hellman",
        "build_automation_item"
    ]
    main_modules = [
        "encryption.diffie_hellman.encryption_diffie_hellman_system"
    ]

    encryption_diffie_hellman = None
    """ The encryption diffie helman """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import encryption.diffie_hellman.encryption_diffie_hellman_system
        self.encryption_diffie_hellman = encryption.diffie_hellman.encryption_diffie_hellman_system.EncryptionDiffieHellman(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_structure(self, parameters):
        return self.encryption_diffie_hellman.create_structure(parameters)
