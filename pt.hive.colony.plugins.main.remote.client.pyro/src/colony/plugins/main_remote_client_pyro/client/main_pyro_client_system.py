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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import Pyro.core

SERVICE_NAME = "pyro"

class MainPyroClient:
    """
    The main pyro client class.
    """

    main_pyro_client_plugin = None
    """ The main pyro client plugin """

    def __init__(self, main_pyro_client_plugin):
        """
        Constructor of the class.
        
        @type main_pyro_client_plugin: MainPyroClientPlugin
        @param main_pyro_client_plugin: The main pyro client plugin.
        """

        self.main_pyro_client_plugin = main_pyro_client_plugin

    def get_service_name(self):
        return SERVICE_NAME

    def create_remote_client(self, service_attributes):
        # creates a new pyro client instance
        pyro_client = PyroClient()

        # retrieves the pyro main uri
        pyro_main_uri = service_attributes["pyro_main_uri"]

        # sets the pyro main uri value
        pyro_client.pyro_main_uri = pyro_main_uri

        return pyro_client

class PyroClient:
    """
    The pyro client class.
    """

    pyro_main_uri = "none"
    """ The pyro main uri """

    pyro_main_proxy = None
    """ The pyro main proxy """

    def __init__(self, pyro_main_uri = "none", pyro_main_proxy = None):
        """
        Constructor of the class.
        
        @type pyro_main_uri: String
        @param pyro_main_uri: The pyro main uri.
        @type pyro_main_proxy: Proxy
        @param pyro_main_proxy: The pyro main proxy.
        """

        self.pyro_main_uri = pyro_main_uri
        self.pyro_main_proxy = pyro_main_proxy

    def get_pyro_main_proxy(self):
        """
        Retrieves the pyro main proxy.
        
        @rtype: Proxy
        @return: The pyro main proxy.
        """

        if not self.pyro_main_proxy:
            self.pyro_main_proxy = Pyro.core.getProxyForURI(self.pyro_main_uri)

        return self.pyro_main_proxy

    def __nonzero__(self):
        return True

    def __getattr__(self, name):
        # retrieves the pyro main proxy
        main_proxy = self.get_pyro_main_proxy()

        # retrieves the name uri (remote call)
        name_uri = main_proxy.get_proxy_uri(name)

        # retrieves the pyro name proxy
        pyro_name_proxy = Pyro.core.getProxyForURI(name_uri)

        # sets the attribute
        setattr(self, name, pyro_name_proxy)

        return pyro_name_proxy
