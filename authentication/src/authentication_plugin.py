#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class AuthenticationPlugin(colony.Plugin):
    """
    The main class for the Authentication plugin.
    """

    id = "pt.hive.colony.plugins.authentication"
    name = "Authentication"
    description = "Plugin that provides the authentication front-end mechanisms"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "authentication"
    ]
    capabilities_allowed = [
        "authentication_handler"
    ]
    main_modules = [
        "authentication"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import authentication
        self.system = authentication.Authentication(self)

    def authenticate_user(self, username, password, authentication_handler, arguments):
        return self.system.authenticate_user(username, password, authentication_handler, arguments)

    def process_authentication_string(self, authentication_string):
        return self.system.process_authentication_string(authentication_string)
