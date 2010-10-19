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

import main_client_ldap_structures

TYPE_VALUE = "type"
""" The type value """

VALUE_VALUE = "value"
""" The value value """

EXTRA_TYPE_VALUE = "extra_type"
""" The extra type value """

PROTOCOL_VERSION_VALUE = "protocol_version"
""" The protocol version value """

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

ENUMERATED_TYPE = 0x0a
""" The enumerated type """

SEQUENCE_TYPE = 0x30
""" The sequence type """

APPLICATION_TYPE = 0x60
""" The application type """

PRIVATE_TYPE = 0x80
""" The private type """

LDAP_TYPE_ALIAS_MAP = {APPLICATION_TYPE + 0 : 0x30,
                       APPLICATION_TYPE + 1 : 0x30,
                       APPLICATION_TYPE + 2 : 0x30,
                       PRIVATE_TYPE + 0: 0x04,
                       PRIVATE_TYPE + 3: 0x30}
""" The map of ldap type alias """

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

        # creates a "new" ber structure
        ber_structure = format_ber_plugin.create_structure({})

        # sets the ldap type alias map in the ber structure
        ber_structure.set_type_alias_map(LDAP_TYPE_ALIAS_MAP)

        simple_authentication = main_client_ldap_structures.SimpleAuthentication("ek41Xuyw")

        bind_request = main_client_ldap_structures.BindRequest(3, "cn=root,dc=hive", simple_authentication)

        request = LdapRequest(1, bind_request)

        result = request.get_result(ber_structure)

        # retrieves the corresponding (ldap) client connection
        self.client_connection = self._ldap_client.get_client_connection(("servidor1.hive", 389, "normal"))

        self.client_connection.send(result)

        # retrieves the data
        data = self.client_connection.retrieve_data(120, 1024)

        response = LdapResponse(request)

        response.process_data(data, ber_structure)

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

    message_id = None
    """ The message id, identifying this unique request """

    protocol_operation = None
    """ The protocol operation of the request """

    controls = []
    """ The list of controls for the request """

    def __init__(self, message_id, protocol_operation, controls = []):
        """
        Constructor of the class.

        @type message_id: int
        @param message_id: The message id.
        @type protocol_operation: ProtocolOperation
        @param protocol_operation: The protocol operation.
        @type controls: List
        @param controls: The controls list
        """

        self.message_id = message_id
        self.protocol_operation = protocol_operation
        self.controls = controls

    def get_result(self, ber_structure):
        """
        Retrieves the result string (serialized) value of
        the request.

        @type ber_structure: BerStructure
        @param ber_structure: The ber structure to be used.
        @rtype: String
        @return: The result string (serialized) value of
        the request.
        """

        # creates the message id integer value
        message_id = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE : self.message_id}

        # retrieves the protocol operation value
        protocol_operation = self.protocol_operation.get_value()

        # creates the ldap message contents (list)
        ldap_message_contents = [message_id, protocol_operation]

        # creates the ldap message sequence value
        ldap_message = {TYPE_VALUE : SEQUENCE_TYPE, VALUE_VALUE : ldap_message_contents}

        # packs the ldap message
        packed_ldap_message = ber_structure.pack(ldap_message)

        # returns the packed ldap message as the result
        return packed_ldap_message

class LdapResponse:
    """
    The ldap response class.
    """

    request = None
    """ The request that originated the response """

    message_id = None
    """ The message id, identifying this unique request """

    protocol_operation = None
    """ The protocol operation of the request """

    controls = []
    """ The list of controls for the request """

    def __init__(self, request):
        """
        Constructor of the class.

        @type request: LdapRequest
        @param request: The request.
        """

        self.request = request

    def process_data(self, data, ber_structure):
        # unpacks the data
        ldap_message = ber_structure.unpack(data)

        # retrieves the ldap message value
        ldap_message_value = ldap_message[VALUE_VALUE]

        # retrieves the message id and the message id value
        message_id = ldap_message_value[0]
        message_id_value = message_id[VALUE_VALUE]

        # retrieve the protocol operation and the protocol operation
        # value
        protocol_operation = ldap_message_value[1]

        # creates the protocol operation structure
        protocol_operation_structure = main_client_ldap_structures.LdapResult()

        # processes the protocol operation
        protocol_operation_structure.process_value(protocol_operation)

        # sets the current values
        self.message_id = message_id_value
        self.protocol_operation = protocol_operation_structure
