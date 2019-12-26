#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class SSLSocketUpgraderPlugin(colony.Plugin):
    """
    The main class for the SSL Socket Upgrader plugin.
    """

    id = "pt.hive.colony.plugins.service.ssl_socket_upgrader"
    name = "SSL Socket Upgrader"
    description = "The plugin that offers the SSL socket upgrader"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "socket_upgrader"
    ]
    dependencies = [
        colony.PackageDependency("Python 2.6", "ssl")
    ]
    main_modules = [
        "ssl_socket_upgrader"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import ssl_socket_upgrader
        self.system = ssl_socket_upgrader.SSLSocketUpgrader(self)

    def get_upgrader_name(self):
        """
        Retrieves the socket upgrader name.

        :rtype: String
        :return: The socket upgrader name.
        """

        return self.system.get_upgrader_name()

    def upgrade_socket(self, socket):
        """
        Upgrades the given socket, configured with
        the default parameters.

        :type socket: Socket
        :param socket: The socket to be upgraded.
        :rtype: Socket
        :return: The upgraded socket.
        """

        return self.system.upgrade_socket(socket)

    def upgrade_socket_parameters(self, socket, parameters):
        """
        Upgrades the given socket, configured with
        the given parameters.

        :type socket: Socket
        :param socket: The socket to be upgraded.
        :type parameters: Dictionary
        :param parameters: The parameters for socket configuration.
        :rtype: Socket
        :return: The upgraded socket.
        """

        return self.system.upgrade_socket_parameters(socket, parameters)

    def process_exception(self, socket, exception):
        """
        Processes the exception taking into account the severity of it,
        as for some exception a graceful handling is imposed.

        The provided socket object should comply with typical python
        interface for it.

        :type socket: Socket
        :param socket: The socket to be used in the exception processing.
        :type exception: Exception
        :param exception: The exception that is going to be handled/processed.
        :rtype: bool
        :return: The result of the processing, in case it's false a normal
        exception handling should be performed otherwise a graceful one is used.
        """

        return self.system.process_exception(socket, exception)
