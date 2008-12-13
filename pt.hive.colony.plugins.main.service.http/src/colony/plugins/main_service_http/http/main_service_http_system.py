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

class MainServiceHttp:
    """
    The main service http class.
    """

    main_service_http_plugin = None
    """ The main serice http plugin """

    def __init__(self, main_service_http_plugin):
        """
        Constructor of the class.
        
        @type main_service_http_plugin: MainServiceHttpPlugin
        @param main_service_http_plugin: The main service http plugin.
        """

        self.main_service_http_plugin = main_service_http_plugin

    def start_service(self, parameters):
        port = parameters["port"]

        self.start_server(port)

    def start_server(port):
        # @todo: think in how to link httpd with the thread pool plugin

        # creates the http socket
        http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # binds the http socket
        http_socket.bind((HOST, port))

        # start listening
        http_socket.listen(1)

        
        connection, address = http_socket.accept()

        print "'Connected by", address

        is_first = True

        while 1:
            # receives the data in chucks of 1024 bytes
            data = connection.recv(1024)
            lines = data.split("\n")
            print data
            if is_first:
                request = lines[0]

                # retrieves the operation and the request type
                operation, path, request_type = request.split(" ")

                print "received operation: " + operation + " and request of type: " + request_type

                if operation == "GET":
                    file = open("c:/test.html", "r")
                    file_contents = file.read()

                    result = "HTTP/1.1 200 OK"
                    content_type = "Content-Type: text/html"
                    content_length = "Content-Length: " + str(len(file_contents))
                    keep_alive = "Connection: Keep-Alive"
                    answer = result + "\n" + content_type +"\n" + content_length + "\n" + keep_alive + "\n\n" + file_contents

                    print "sent answer: " + answer

                    connection.send(answer)
                is_first = False
            else:
                break

        connection.close()
