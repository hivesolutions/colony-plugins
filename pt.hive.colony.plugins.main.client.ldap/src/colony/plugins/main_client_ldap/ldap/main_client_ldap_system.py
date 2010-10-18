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

import threading

LDAP_REQUEST_TYPE_MAP = {"bind" : 0x60, "unbind" : 0x62,
                         "search" : 0x63, "modify" : 0x66,
                         "add" : 0x68, "delete" : 0x6a,
                         "modify_dn" : 0x00, "compare" : 0x00,
                         "abandon" : 0x00, "extended" : 0x00}
""" The map of ldap request types """

LDAP_RESPONSE_TYPE_MAP = {"bind" : 0x61, "search_result_enttry" : 0x64,
                          "search_result_reference" : 0x73, "search_result_done" : 0x65,
                          "modify" : 0x67, "add" : 0x69, "delete" : 0x6b}
""" The map of ldap response types """

PROTOCOL_VERSION_VALUE = "protocol_version"
""" The protocol version value """

class MainClientLdap:
    """
    The main client ldap class.
    """

    main_client_ldap_plugin = None
    """ The main client ldap plugin """

    def __init__(self, main_client_ldap_plugin):
        """
        Constructor of the class.

        @type main_client_ldap_plugin: MainClientLdapPlugin
        @param main_client_ldap_plugin: The main client ldap plugin.
        """

        self.main_client_ldap_plugin = main_client_ldap_plugin

    def create_client(self, parameters):
        # retrieves the protovol version
        protocol_version = parameters.get(PROTOCOL_VERSION_VALUE, None)

        # creates the ldap client
        ldap_client = LdapClient(self, protocol_version)

        # returns the ldap client
        return ldap_client

    def create_request(self, parameters):
        pass

class LdapClient:
    """
    The ldap client class, representing
    a client connection in the ldap protocol.
    """

    main_client_ldap = None
    """ The main client ldap object """

    protocol_version = "none"
    """ The version of the ldap protocol """

    _ldap_client = None
    """ The ldap client object used to provide connections """

    _ldap_client_lock = None
    """ Lock to control the fetching of the queries """

    def __init__(self, main_client_ldap, protocol_version):
        """
        Constructor of the class.

        @type main_client_ldap: MainClientLdap
        @param main_client_ldap: The main client ldap object.
        @type protocol_version: String
        @param protocol_version: The version of the ldap protocol to
        be used.
        @type content_type_charset: String
        @param content_type_charset: The charset to be used by the content.
        """

        self.main_client_ldap = main_client_ldap
        self.protocol_version = protocol_version

        self._ldap_client_lock = threading.RLock()

    def open(self, parameters):
        # generates the parameters
        client_parameters = self._generate_client_parameters(parameters)

        # creates the ldap client, generating the internal structures
        self._ldap_client = self.main_client_ldap.main_client_ldap_plugin.main_client_utils_plugin.generate_client(client_parameters)

        # starts the ldap client
        self._ldap_client.start_client()

    def close(self, parameters):
        # stops the ldap client
        self._ldap_client.stop_client()

    def bind(self):
        # retrieves the format ber plugin
        format_ber_plugin = self.main_client_ldap.main_client_ldap_plugin.format_ber_plugin

        # ---------------- ZONA DE REQUEST ---------------

        EOC_TYPE = 0x00
        """ The eoc (end of content) type """

        BOOLEAN_TYPE = 0x01
        """ The boolean type """

        INTEGER_TYPE = 0x02
        """ The integer type """

        BIT_STRING_TYPE = 0x03
        """ The bit string type """

        OCTET_STRING_TYPE = 0x04
        """ The octet string type """

        SEQUENCE_TYPE = 0x30
        """ The sequence type """

        APPLICATION_TYPE = 0x60
        """ The application (base) type """

        BIND_REQUEST_TYPE = 0x60

        TYPE_VALUE = "type"
        """ The type value """

        VALUE_VALUE = "value"
        """ The value value """

        EXTRA_TYPE_VALUE = "extra_type"
        """ The extra type value """

        version = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE : 3}

        name = {TYPE_VALUE: OCTET_STRING_TYPE, VALUE_VALUE : "cn=root,dc=hive"}

        authentication = {TYPE_VALUE: OCTET_STRING_TYPE, VALUE_VALUE : "123123123",
                          EXTRA_TYPE_VALUE : 0x80}

        protocol_operation_contents = [version, name, authentication]

        message_id = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE : 1}

        protocol_operation = {TYPE_VALUE: SEQUENCE_TYPE, VALUE_VALUE : protocol_operation_contents,
                              EXTRA_TYPE_VALUE : BIND_REQUEST_TYPE}

        ldap_message_contents = [message_id, protocol_operation]

        ldap_message = {TYPE_VALUE : SEQUENCE_TYPE, VALUE_VALUE : ldap_message_contents}

        # creates a "new" ber structure
        ber_structure = format_ber_plugin.create_structure({})

        # packs the ldap message
        packed_ldap_message = ber_structure.pack(ldap_message)

        # --- END ZONA DE REQUEST -------------

        # retrieves the corresponding (ldap) client connection
        self.client_connection = self._ldap_client.get_client_connection(("servidor1.hive", 389, "normal"))

        self.client_connection.send(packed_ldap_message)

        # --- ZONA DE RESPONSE -----------

        # retrieves the data
        data = self.client_connection.retrieve_data(120, 1024)

        # --- END ZONA DE RESPONSE

        print ber_structure.to_hex(data)

        print "---------------------"

    def _generate_client_parameters(self, parameters):
        """
        Retrieves the client parameters map from the base parameters
        map.

        @type parameters: Dictionary
        @param parameters: The base parameters map to be used to build
        the final client parameters map.
        @rtype: Dictionary
        @return: The client service parameters map.
        """

        # creates the parameters map
        parameters = {"client_plugin" : self.main_client_ldap.main_client_ldap_plugin}

        # returns the parameters
        return parameters

class LdapRequest:
    """
    The ldap request class.
    """

    pass
