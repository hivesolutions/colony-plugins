#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import struct
import socket
import hashlib

import colony.libs.map_util

import main_service_bittorrent_parser

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

class MainServiceBittorrent:
    """
    The main service bittorrent class.
    """

    main_service_bittorrent_plugin = None
    """ The main service bittorrent plugin """

    bittorrent_service_handler_plugins_map = {}
    """ The bittorrent service handler plugins map """

    bittorrent_socket = None
    """ The bittorrent socket """

    bittorrent_connection_active = False
    """ The bittorrent connection active flag """

    bittorrent_service_configuration = {}
    """ The bittorrent service configuration """

    http_client = None
    """ The http client to be used """

    def __init__(self, main_service_bittorrent_plugin):
        """
        Constructor of the class.

        @type main_service_bittorrent_plugin: MainServiceBittorrentPlugin
        @param main_service_bittorrent_plugin: The main service bittorrent plugin.
        """

        self.main_service_bittorrent_plugin = main_service_bittorrent_plugin

        self.bittorrent_service_handler_plugin_map = {}
        self.bittorrent_service_configuration = {}

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        pass

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        self.stop_server()

    def set_service_configuration_property(self, service_configuration_property):
        # retrieves the service configuration
        service_configuration = service_configuration_property.get_data()

        # cleans the bittorrent service configuration
        colony.libs.map_util.map_clean(self.bittorrent_service_configuration)

        # copies the service configuration to the bittorrent service configuration
        colony.libs.map_util.map_copy(service_configuration, self.bittorrent_service_configuration)

    def unset_service_configuration_property(self):
        # cleans the bittorrent service configuration
        colony.libs.map_util.map_clean(self.bittorrent_service_configuration)

    def _get_service_configuration(self):
        """
        Retrieves the service configuration map.

        @rtype: Dictionary
        @return: The service configuration map.
        """

        return self.bittorrent_service_configuration

    def start_torrent(self, parameters):
        # interpreto o ficheri vejo se tem erros
        # se nao tiver estableco a conexao com o tracker e vejo o que existe
        # de bom para ele

        # retrieves the bencode plugin
        bencode_plugin = self.main_service_bittorrent_plugin.bencode_plugin

        # retrieves the metafile file path
        metafile_file_path = parameters.get("file_path", None)

        # opens the metafile for reading
        metafile = open(metafile_file_path, "rb")

        # reads the file contents
        metafile_contents = metafile.read()

        # closes the file
        metafile.close()

        # creates the metafile map from the metafile contents
        metafile_map = bencode_plugin.loads(metafile_contents)

        # creates a new torrent parser for the created metafile map
        torrent_parser = main_service_bittorrent_parser.TorrentParser(metafile_map)

        # runs the parser
        torrent_parser.parse()

        # retrieves the "parsed" torrent structure from
        # the torrent parser
        torrent_structure = torrent_parser.get_value()

        info_map_encoded = bencode_plugin.dumps(torrent_structure.info_map)

        parameters = {}

        parameters["info_hash"] = hashlib.sha1(info_map_encoded).digest()
        parameters["peer_id"] = "-CO1000-111111111111"
        parameters["port"] = str(6881)
        parameters["uploaded"] = str(0)
        parameters["downloaded"] = str(0)
        parameters["left"] = str(1000000)
        parameters["compact"] = str(0)
        parameters["event"] = "started"

        # fetches the retrieval url with the given parameters retrieving the data
        data = self._fetch_url(torrent_structure.main_tracker_url, parameters)

        data_decoded = bencode_plugin.loads(data)

        peers_data = data_decoded["peers"]

        # calculates the number of peers sent
        number_peers = len(peers_data) / 6

        for index in range(number_peers):
            address_integer, port = struct.unpack_from("!4sH", peers_data, index * 6)

            # converts the address to the "normalized" string value
            address = socket.inet_ntoa(str(address_integer))

            print address + ": " + str(port)

            try:
                # creates the socket
                socket_value = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # sets the socket's timeout
                socket_value.settimeout(1.0)

                # defines the connect parameters
                connect_parameters = (
                    address,
                    port
                )

                # connects the socket
                socket_value.connect(connect_parameters)
            except:
                print "problema"
            else:
                print "conectado"

        print "ola"

    def stop_torrent(self, parameters):
        pass

    def start_server(self, socket_provider, port, encoding, service_configuration):
        """
        Starts the server in the given port.

        @type socket_provider: String
        @param socket_provider: The name of the socket provider to be used.
        @type port: int
        @param port: The port to start the server.
        @type encoding: String
        @param encoding: The encoding to be used in the connection.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration map.
        """

        pass

    def stop_server(self):
        """
        Stops the server.
        """

        pass

    def _fetch_url(self, url, parameters = None, method = GET_METHOD_VALUE, headers = False):
        """
        Fetches the given url for the given parameters and using the given method.

        @type url: String
        @param url: The url to be fetched.
        @type parameters: Dictionary
        @param parameters: The parameters to be used the fetch.
        @type method: String
        @param method: The method to be used in the fetch.
        @type headers: bool
        @param headers: If the headers should be returned.
        @rtype: String
        @return: The fetched data.
        """

        # in case parameters is not defined
        if not parameters:
            # creates a new parameters map
            parameters = {}

        # retrieves the http client
        http_client = self._get_http_client()

        # fetches the url retrieving the http response
        http_response = http_client.fetch_url(url, method, parameters)

        # closes the http client
        http_client.close({})

        # retrieves the contents from the http response
        contents = http_response.received_message

        # retrieves the headers map from the http response
        headers_map = http_response.headers_map

        # in case the headers flag is set
        if headers:
            # returns the contents and the headers map
            return contents, headers_map
        else:
            # returns the contents
            return contents

    def _get_http_client(self):
        """
        Retrieves the http client currently in use (in case it's created)
        if not created creates the http client.

        @rtype: HttpClient
        @return: The retrieved http client.
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.main_service_bittorrent_plugin.main_client_http_plugin

        # creates the http client
        http_client = main_client_http_plugin.create_client({})

        # opens the http client
        http_client.open({})

        # returns the http client
        return http_client
