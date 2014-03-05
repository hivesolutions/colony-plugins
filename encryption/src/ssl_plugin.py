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

import colony.base.system

class SslPlugin(colony.base.system.Plugin):
    """
    The main class for the Ssl plugin.
    """

    id = "pt.hive.colony.plugins.encryption.ssl"
    name = "Ssl"
    description = "The plugin that offers the ssl support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "encryption.ssl"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.encryption.rsa"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.encryption.pkcs_1")
    ]
    main_modules = [
        "encryption.ssl.system"
    ]

    ssl = None
    """ The ssl """

    rsa_plugin = None
    """ The rsa plugin """

    pkcs_1_plugin = None
    """ The pkcs 1 plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import encryption.ssl.system
        self.ssl = encryption.ssl.system.Ssl(self)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def create_structure(self, parameters):
        return self.ssl.create_structure(parameters)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.encryption.rsa")
    def set_rsa_plugin(self, rsa_plugin):
        self.rsa_plugin = rsa_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.encryption.pkcs_1")
    def set_pkcs_1_plugin(self, pkcs_1_plugin):
        self.pkcs_1_plugin = pkcs_1_plugin
