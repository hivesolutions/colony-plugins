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

import colony.libs.string_buffer_util

DEFAULT_PORT = 389
""" The default port """

DEFAULT_SOCKET_NAME = "normal"
""" The default socket name """

RESPONSE_TIMEOUT = 10
""" The response timeout """

CHUNK_SIZE = 4096
""" The chunk size """

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

    ber_structure = None
    """ The structure to ber encoding """

    current_message_id = 0
    """ The current message id """

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

        # generates the ber structure
        ber_structure = self._generate_ber_structure()

        # sets the ber structure
        self.ber_structure = ber_structure

        # starts the ldap client
        self._ldap_client.start_client()

    def close(self, parameters):
        # stops the ldap client
        self._ldap_client.stop_client()

    def send_request(self, protocol_operation, controls = []):
        """
        Sends the request for the given parameters.

        @type protocol_operation: ProtocolOperation
        @param protocol_operation: The protocol operation.
        @type session: controls
        @param session: The controls list.
        @rtype: LdapRequest
        @return: The sent request for the given parameters.
        """

        # generates and retrieves a new message id
        message_id = self._get_message_id()

        # creates the ldap request
        request = LdapRequest(message_id, protocol_operation, controls)

        # retrieves the result value from the request
        result_value = request.get_result(self.ber_structure)

        # sends the result value
        self.client_connection.send(result_value)

        # returns the request
        return request

    def retrieve_response(self, request, response_timeout = RESPONSE_TIMEOUT):
        """
        Retrieves the response from the sent request.

        @rtype: LdapRequest
        @return: The request that originated the response.
        @type response_timeout: int
        @param response_timeout: The timeout for the response retrieval.
        @rtype: LdapResponse
        @return: The response from the sent request.
        """

        pass

        # TENHO DE IR RECEBENDO O MATERIAL QUANDO NAO DER UMA EXCEPCAO
        # a SACAR O TAMANHO DO CENAS JA TENHO O TAMANHO PARA PODER
        # ir sacando o resto

        # TENHO DE IR APANHANDO AS EXCEPCOES


#        # creates the string buffer for the message
#        message = colony.libs.string_buffer_util.StringBuffer()
#
#        # creates a response object
#        response = LdapResponse(request)
#
#        message_size = None
#
#        # continuous loop
#        while True:
#            # retrieves the data
#            data = self.client_connection.retrieve_data(response_timeout, CHUNK_SIZE)
#
#            # in case no valid data was received
#            if data == "":
#                raise main_client_smtp_exceptions.SmtpInvalidDataException("empty data received")
#
#            # writes the data to the string buffer
#            message.write(data)
#
#            # retrieves the message value from the string buffer
#            message_value = message.get_value()
#
#            # in case the message size is not set
#            if not message_size:
#                if len(message_value) >= 2:
#
#
#            # retrieves the message value length
#            message_value_length = len(message_value)
#
#            # finds the first end token value
#            end_token_index = message_value.rfind(END_TOKEN_VALUE)

            # calculates the last end token index, using the message
#            # value length as reference
#            last_end_token_index = message_value_length - 2
#
#            # in case the end token is found in the last position
#            # of the message
#            if end_token_index == last_end_token_index:
#                # tries to find a previous value of the newline
#                # in order to check if it is the "last newline"
#                value = message_value.rfind(END_TOKEN_VALUE, 0, last_end_token_index)
#
#                # in case no previous newline is found
#                if value == -1:
#                    # sets the base value as zero (string initial)
#                    base_value = 0
#                else:
#                    # sets the base value as the index of the find
#                    # plus two indexes (the length of the end token value)
#                    base_value = value + 2
#
#                # retrieves the comparison character (the character that
#                # indicates if it is the final line)
#                comparison_character = message_value[base_value + 3]
#
#                # in case the comparison character is a dash (not the final line)
#                if comparison_character == "-":
#                    continue
#                elif not comparison_character == " ":
#                    raise main_client_smtp_exceptions.SmtpInvalidDataException("invalid comparison character")
#
#                # retrieves the smtp message
#                smtp_message = message_value[:end_token_index]
#
#                # splits the smtp message in lines
#                smtp_message_lines = smtp_message.split("\r\n")
#
#                # retrieves the number of smtp message lines
#                smtp_message_lines_length = len(smtp_message_lines)
#
#                # starts the index counter
#                index = 1
#
#                # iterates over all the smtp message lines
#                for smtp_message_line in smtp_message_lines:
#                    # in case it's the last line
#                    if index == smtp_message_lines_length:
#                        # splits the smtp message line
#                        smtp_message_line_splitted = smtp_message_line.split(" ", 1)
#
#                        # retrieves the smtp code
#                        smtp_code = int(smtp_message_line_splitted[0])
#
#                        # retrieves the smtp message
#                        smtp_message = smtp_message_line_splitted[1]
#
#                        # sets the smtp code in the response
#                        response.set_code(smtp_code)
#
#                        # sets the smtp message in the response
#                        response.set_message(smtp_message)
#
#                        # adds the smtp message to the list of
#                        # messages in response
#                        response.add_message(smtp_message)
#                    # in case it's not the last line
#                    else:
#                        # splits the smtp message line
#                        smtp_message_line_splitted = smtp_message_line.split("-", 1)
#
#                        # retrieves the smtp message
#                        smtp_message = smtp_message_line_splitted[1]
#
#                        # adds the smtp message to the list of
#                        # messages in response
#                        response.add_message(smtp_message)
#
#                    # increments the index counter
#                    index += 1
#
#                # sets the session object in the response
#                response.set_session(session)
#
#                # returns the response
#                return response

    def bind(self):

        # TENHO DE RETIRAR ISTO


        # retrieves the corresponding (ldap) client connection
        self.client_connection = self._ldap_client.get_client_connection(("servidor1.hive", DEFAULT_PORT, DEFAULT_SOCKET_NAME))

        # END RETIRAR


        # creates the simple authentication
        simple_authentication = main_client_ldap_structures.SimpleAuthentication("ek41Xuyw")

        # creates the bind request
        bind_request = main_client_ldap_structures.BindRequest(3, "cn=root,dc=hive", simple_authentication)

        # sends the request
        request = self.send_request(bind_request, [])


        # ----- a mudar para response

        # retrieves the data
        data = self.client_connection.retrieve_data(120, 1024)

        response = LdapResponse(request)

        response.process_data(data, self.ber_structure)

        # -----

    def _get_message_id(self):
        """
        Retrieves the message id, incrementing the
        current message id counter.

        @rtype: int
        @return: The newly generated message id.
        """

        # increments the current message id
        self.current_message_id += 1

        # returns the current message id
        return self.current_message_id

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

    def _generate_ber_structure(self):
        """
        Generates a ber structure for the current instance.
        The generates ber structure is set with the
        ldap type alias map.

        @rtype: BerStructure
        @return: The generated ber structure.
        """

        # retrieves the format ber plugin
        format_ber_plugin = self.main_client_ldap.main_client_ldap_plugin.format_ber_plugin

        # creates a "new" ber structure
        ber_structure = format_ber_plugin.create_structure({})

        # sets the ldap type alias map in the ber structure
        ber_structure.set_type_alias_map(LDAP_TYPE_ALIAS_MAP)

        # returns the generated ber structure
        return ber_structure

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
        protocol_operation_structure = main_client_ldap_structures.ProtocolOperation()

        # processes the value using the protocol operation, retrieving
        # the protocol operation value
        protocol_operation_value = protocol_operation_structure.process_value(protocol_operation)

        # sets the current values
        self.message_id = message_id_value
        self.protocol_operation = protocol_operation_value
