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


HANDLER_NAME = "proxy"
""" The handler name """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

class MainServiceHttpProxyHandler:
    """
    The main service http proxy handler class.
    """

    main_service_http_proxy_handler_plugin = None
    """ The main service http proxy handler plugin """

    def __init__(self, main_service_http_proxy_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_proxy_handler_plugin: MainServiceHttpProxyHandlerPlugin
        @param main_service_http_proxy_handler_plugin: The main service http proxy handler plugin.
        """

        self.main_service_http_proxy_handler_plugin = main_service_http_proxy_handler_plugin

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        # retrieves the proxy target
        proxy_target = request.properties.get("proxy_target", "http://www.google.com")

        # retrieves the main client http plugin
        main_client_http_plugin = self.main_service_http_proxy_handler_plugin.main_client_http_plugin

        # creates the http client
        http_client = main_client_http_plugin.create_client({})

        # opens the http client
        http_client.open({})

        #PARA OBTER O DIFF DE PATH
        #base_path - handler_path
        # original:
#        # in case there is a valid handler path
#        if request_handler_path:
#            request_path = request_resource_path.replace(request_handler_path, "", 1)
#        else:
#            request_path = request_resource_path

        #http_client.fetch_url("http://www.sapo.pt", method = GET_METHOD_VALUE, parameters = {}, protocol_version = HTTP_1_1_VERSION, content_type = DEFAULT_CONTENT_TYPE, content_type_charset = DEFAULT_CHARSET, contents = None)

        # fetches the contents from the url
        http_response = http_client.fetch_url(proxy_target)

        # retrieves the data from the http response
        data = http_response.received_message

        # writes the (received) data to the request
        request.write(data)

        # TENHO TB DE ESCREVER OS HEADERS CERTOS

        # closes the http client
        http_client.close({})

# tenho de receber o request e encaminhar o mesmo por um cliente
# depois tenho de receber a resposta do cliente e por no send

#
#<VirtualHost www.hive.pt:80>
#ServerAdmin root@hive.pt
#DocumentRoot /var/www/html/hive-welcome
#ServerName www.hive.pt
#ServerAlias hive.pt
##Alias /roundcubemail "/var/www/html/roundcubemail"
#Alias /trac "/var/www/html/trac"
##Alias /maven2 "/var/www/html/maven2"
#Alias /phpldapadmin "/var/www/html/phpldapadmin"
#Alias /phpMyAdmin "/var/www/html/phpMyAdmin "
#
#ProxyRequests On
#ProxyVia On
#
#<Proxy *>
#Order deny,allow
#Allow from all
#</Proxy>
#
#ProxyPass / http://hive.pt:8080/
#</VirtualHost>


#        # retrieves the format mime plugin
#        format_mime_plugin = self.main_service_http_file_handler_plugin.format_mime_plugin
#
#        # retrieves the resource manager plugin
#        resource_manager_plugin = self.main_service_http_file_handler_plugin.resource_manager_plugin
#
#        # retrieves the default path
#        default_path = self.handler_configuration.get("default_path", "/")
#
#        # retrieves the default page
#        default_page = self.handler_configuration.get("default_page", "index.html")
#
#        # retrieves the default relative paths
#        relative_paths = self.handler_configuration.get("relative_paths", False)
#
#        # retrieves the base directory for file search
#        base_directory = request.properties.get("base_path", default_path)
#
#        # retrieves the default page
#        default_page = request.properties.get("default_page", default_page)
#
#        # retrieves the relative paths
#        relative_paths = request.properties.get("relative_paths", relative_paths)
#
#        # retrieves the requested resource path
#        resource_path = request.get_resource_path_decoded()
#
#        # retrieves the handler path
#        handler_path = request.get_handler_path()
#
#        # retrieves the real base directory
#        real_base_directory = resource_manager_plugin.get_real_string_value(base_directory)
#
#        # in case the relative paths are disabled
#        if not relative_paths:
#            # escapes the resource path in the relatives paths
#            resource_path = self._escape_relative_paths(resource_path)
#
#        # in case there is a valid handler path
#        if handler_path:
#            path = resource_path.replace(handler_path, "", 1)
#        else:
#            path = resource_path
#
#        # in case the path is the base one
#        if path == "/" or path == "":
#            path = "/" + default_page
#
#        # retrieves the mime type for the path
#        mime_type = format_mime_plugin.get_mime_type_file_name(path)
#
#        # strips the path value from the initial and final slash
#        path = path.strip("/")
#
#        # creates the complete path
#        complete_path = real_base_directory + "/" + path
#
#        # in case the paths does not exist
#        if not os.path.exists(complete_path):
#            # raises file not found exception with 404 http error code
#            raise main_service_http_file_handler_exceptions.FileNotFoundException(resource_path, 404)
#
#        # retrieves the file stat
#        file_stat = os.stat(complete_path)
#
#        # retrieves the modified timestamp
#        modified_timestamp = file_stat[stat.ST_MTIME]
#
#        # computes the etag value base in the file stat and
#        # modified timestamp
#        etag_value = self._compute_etag(file_stat, modified_timestamp)
#
#        # verifies the resource to validate any modification
#        if not request.verify_resource_modification(modified_timestamp, etag_value):
#            # sets the request mime type
#            request.content_type = mime_type
#
#            # sets the request status code
#            request.status_code = 304
#
#            # returns immediately
#            return
#
#        # calculates the expiration timestamp from the modified timestamp
#        # incrementing the delta timestamp for expiration
#        expiration_timestamp = modified_timestamp + EXPIRATION_DELTA_TIMESTAMP
#
#        # sets the request mime type
#        request.content_type = mime_type
#
#        # sets the request status code
#        request.status_code = 200
#
#        # sets the last modified timestamp
#        request.set_last_modified_timestamp(modified_timestamp)
#
#        # sets the expiration timestamp in the request
#        request.set_expiration_timestamp(expiration_timestamp)
#
#        # sets the etag in the request
#        request.set_etag(etag_value)
#
#        # in case the complete path is a directory
#        if os.path.isdir(complete_path):
#            # processes the path as a directory
#            self._process_directory(request, complete_path)
#        # otherwise
#        else:
#            # processes the path as a file
#            self._process_file(request, complete_path)
