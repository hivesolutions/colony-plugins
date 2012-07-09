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

class AuthenticationPythonPlugin(colony.base.system.Plugin):
    """
    The main class for the Authentication Python plugin.
    """

    id = "pt.hive.colony.plugins.authentication.python"
    name = "Authentication Python"
    description = "Authentication Python Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "configuration_models_bundle" : {
            "authentication.py" : {
                "path" : "authentication/python/configuration/authentication_configuration.py",
                "global" : False,
                "replace" : False
            }
        }
    }
    capabilities = [
        "authentication_handler",
        "configuration_model_provider"
    ]
    main_modules = [
        "authentication.python.configuration.authentication_configuration",
        "authentication.python.exceptions",
        "authentication.python.system"
    ]

    authentication_python = None
    """ The authentication python """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import authentication.python.system
        self.authentication_python = authentication.python.system.AuthenticationPython(self)

    def get_handler_name(self):
        return self.authentication_python.get_handler_name()

    def handle_request(self, request):
        return self.authentication_python.handle_request(request)
