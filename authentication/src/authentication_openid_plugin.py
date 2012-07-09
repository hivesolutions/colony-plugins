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

class AuthenticationOpenidPlugin(colony.base.system.Plugin):
    """
    The main class for the Authentication Openid plugin.
    """

    id = "pt.hive.colony.plugins.authentication.openid"
    name = "Authentication Openid"
    description = "Authentication Openid Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "authentication_handler"
    ]
    main_modules = [
        "authentication.openid.system"
    ]

    authentication_openid = None
    """ The authentication openid """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import authentication.openid.system
        self.authentication_openid = authentication.openid.system.AuthenticationOpenid(self)

    def get_handler_name(self):
        return self.authentication_openid.get_handler_name()

    def handle_request(self, request):
        return self.authentication_openid.handle_request(request)
