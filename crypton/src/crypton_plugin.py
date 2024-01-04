#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony


class CryptonPlugin(colony.Plugin):
    """
    The main class for the Crypton plugin.
    """

    id = "pt.hive.colony.plugins.crypton"
    name = "Crypton"
    description = "The plugin that offers the Crypton base infrastructure"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["mvc_service", "controller_access"]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.mvc.utils"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.random"),
        colony.PluginDependency("pt.hive.colony.plugins.encryption.ssl"),
    ]
    main_modules = ["crypton"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import crypton

        self.system = crypton.Crypton(self)

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)
        self.system.load_components()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.unload_components()

    @colony.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.Plugin.set_configuration_property(self, property_name, property)

    @colony.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.Plugin.unset_configuration_property(self, property_name)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the MVC service. The tuple should relate the route with the handler
        method/function.

        :rtype: Tuple
        :return: The tuple of regular expressions to be used as patterns,
        to the MVC service.
        """

        return self.system.get_patterns()

    def get_controller(self, name):
        return self.system.get_controller(name)

    @colony.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.system.set_configuration_property(property)

    @colony.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.system.unset_configuration_property()
