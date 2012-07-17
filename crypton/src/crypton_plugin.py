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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class CryptonPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Crypton plugin.
    """

    id = "pt.hive.colony.plugins.crypton"
    name = "Crypton"
    description = "The plugin that offers the crypton base infrastructure"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "mvc_service",
        "controller_access"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.mvc.utils", "1.x.x"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.random", "1.x.x"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.encryption.ssl", "1.x.x")
    ]
    main_modules = [
        "crypton.exceptions",
        "crypton.system"
    ]

    crypton = None
    """ The crypton """

    mvc_utils_plugin = None
    """ The mvc utils plugin """

    random_plugin = None
    """ The random plugin """

    encryption_ssl_plugin = None
    """ The encryption ssl plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import crypton.encryption.crypton_system
        self.crypton = crypton.encryption.crypton_system.Crypton(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.crypton.load_components()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.crypton.unload_components()

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.plugin_system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.plugin_system.Plugin.unset_configuration_property(self, property_name)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return self.crypton.get_patterns()

    def get_communication_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as communication patterns,
        to the web mvc service. The tuple should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as communication patterns,
        to the web mvc service.
        """

        return self.crypton.get_communication_patterns()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        return self.crypton.get_resource_patterns()

    def get_controller(self, controller_name):
        """
        Retrieves the specified controller.

        @type controller_name: String
        @param controller_name: The controller's name.
        @rtype: Object
        @return The controller with the specified name.
        """

        return self.crypton.get_controller(controller_name)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.mvc.utils")
    def set_mvc_utils_plugin(self, mvc_utils_plugin):
        self.mvc_utils_plugin = mvc_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.encryption.ssl")
    def set_encryption_ssl_plugin(self, encryption_ssl_plugin):
        self.encryption_ssl_plugin = encryption_ssl_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.random")
    def set_random_plugin(self, random_plugin):
        self.random_plugin = random_plugin

    @colony.base.decorators.set_configuration_property_method("configuration")
    def service_configuration_set_configuration_property(self, property_name, property):
        self.crypton.set_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("configuration")
    def service_configuration_unset_configuration_property(self, property_name):
        self.crypton.unset_configuration_property()
