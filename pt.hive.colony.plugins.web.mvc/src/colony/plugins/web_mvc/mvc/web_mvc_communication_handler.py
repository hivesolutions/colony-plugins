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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class WebMvcCommunicationHandler:
    """
    The web mvc communication handler class.
    """

    connection_name_connection_map = {}
    """ The map associating the connection name with the connection """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.connection_name_connection_map = {}

    def handle_request(self, request, data_handler_method, connection_changed_handler_method, connection_name):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @type data_handler_method: Method
        @param data_handler_method: The method for data handling.
        @type connection_changed_handler_method: Method
        @param connection_changed_handler_method: The method for connection changed handling.
        @type connection_name: String
        @param connection_name: The name of the connection.
        @rtype: bool
        @return: The result of the handling.
        """

        return True
