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


class InfoUserPlugin(colony.Plugin):
    """
    The main class for the User Information plugin.
    """

    id = "pt.hive.colony.plugins.info.user"
    name = "User Info"
    description = "The plugin that offers the user information support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT, colony.JYTHON_ENVIRONMENT]
    capabilities = ["info.user"]
    main_modules = ["info_user"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import info_user

        self.system = info_user.InfoUser(self)

    @colony.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.Plugin.set_configuration_property(self, property_name, property)

    @colony.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.Plugin.unset_configuration_property(self, property_name)

    def get_user_info(self, user):
        return self.system.get_user_info(user)

    @colony.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.system.set_configuration_property(property)

    @colony.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.system.unset_configuration_property()
