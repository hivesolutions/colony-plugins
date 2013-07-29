#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

class InfoUserPlugin(colony.base.system.Plugin):
    """
    The main class for the User Information plugin.
    """

    id = "pt.hive.colony.plugins.info.user"
    name = "User Info"
    description = "The plugin that offers the user information support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "info.user"
    ]
    main_modules = [
        "info_user.system"
    ]

    infor_user = None
    """ The reference user info object to be used
    in the access to the back-end system structures """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import info_user.system
        self.info_user = info_user.system.InfoUser(self)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.system.Plugin.unset_configuration_property(self, property_name)

    def get_user_info(self, user):
        return self.info_user.get_user_info(user)

    @colony.base.decorators.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.info_user.set_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.info_user.unset_configuration_property()
