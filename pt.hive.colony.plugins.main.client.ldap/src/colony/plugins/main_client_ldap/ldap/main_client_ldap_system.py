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

import colony.libs.string_buffer_util

import main_client_ldap_structures
import main_client_ldap_exceptions

DEFAULT_PORT = 389
""" The default port """

DEFAULT_SOCKET_NAME = "normal"
""" The default socket name """

DEFAULT_SOCKET_PARAMETERS = {}
""" The default socket parameters """

DEFAULT_PROTOCOL_VERSION = 3
""" The default protocol version """

REQUEST_TIMEOUT = 10
""" The request timeout """

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

TYPE_NUMBER_VALUE = "type_number"
""" The type number value """

TYPE_CONSTRUCTED_VALUE = "type_constructed"
""" The type constructed value """

TYPE_CLASS_VALUE = "type_class"
""" The type class value """

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

SEQUENCE_TYPE = 0x10
""" The sequence type """

SET_TYPE = 0x11
""" The set type """

PRIMITIVE_MODE = 0x00
""" The primitive mode """

CONSTRUCTED_MODE = 0x01
""" The constructed mode """

UNIVERSAL_CLASS = 0x00
""" The universal class """

APPLICATION_CLASS = 0x01
""" The application class """

CONTEXT_SPECIFIC_CLASS = 0x02
""" The context specific class """

PRIVATE_CLASS = 0x03
""" The private class """

LDAP_TYPE_ALIAS_MAP = {UNIVERSAL_CLASS : {},
                       APPLICATION_CLASS : {0x00 : 0x10,
                                            0x01 : 0x10,
                                            0x02 : 0x10,
                                            0x03 : 0x10,
                                            0x04 : 0x10,
                                            0x05 : 0x10},
                       CONTEXT_SPECIFIC_CLASS : {},
                       PRIVATE_CLASS: {0x00 : 0x04,
                                       0x03 : 0x10}}
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

    client_connection = None
    """ The current client connection """

    ber_structure = None
    """ The structure to ber encoding """

    current_message_id = 0
    """ The current message id """

    _ldap_client = None
    """ The ldap client object used to provide connections """

    _ldap_client_lock = None
    """ Lock to control the fetching of the queries """

    _extra_messages_buffer = []
    """ The extra messages buffer """

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
        self._extra_messages_buffer = []

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

    def connect(self, host, port = DEFAULT_PORT, socket_name = DEFAULT_SOCKET_NAME, socket_parameters = DEFAULT_SOCKET_PARAMETERS, name = "", password = ""):
        # retrieves the corresponding (ldap) client connection
        self.client_connection = self._ldap_client.get_client_connection((host, port, socket_name, socket_parameters))

        # acquires the ldap client lock
        self._ldap_client_lock.acquire()

        try:
            # binds the connection
            self.bind(name, password)
        finally:
            # releases the ldap client lock
            self._ldap_client_lock.release()

    def disconnect(self):
        # acquires the ldap client lock
        self._ldap_client_lock.acquire()

        try:
            # unbinds the connection
            self.unbind()
        finally:
            # releases the ldap client lock
            self._ldap_client_lock.release()

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

    def retrieve_response(self, request, response_timeout = None):
        """
        Retrieves the response from the sent request.

        @type: LdapRequest
        @return: The request that originated the response.
        @type response_timeout: int
        @param response_timeout: The timeout for the response retrieval.
        @rtype: LdapResponse
        @return: The response from the sent request.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a response object
        response = LdapResponse(request)

        # creates the message size object
        message_size = None

        # creates the received data size (counter)
        received_data_size = 0

        # continuous loop
        while True:
            # in case the extra messages buffer is valid (not empty)
            if self._extra_messages_buffer:
                # pops the last value of the extra messages buffer
                # as the data
                data = self._extra_messages_buffer.pop()
            else:
                # receives the data
                data = self.client_connection.receive(response_timeout, CHUNK_SIZE)

            # in case no valid data was received
            if data == "":
                raise main_client_ldap_exceptions.LdapInvalidDataException("empty data received")

            # retrieves the data length
            data_length = len(data)

            # increments the received data size (counter)
            received_data_size += data_length

            # writes the data to the string buffer
            message.write(data)

            # in case the message size is not set
            if not message_size:
                # retrieves the message value from the string buffer
                message_value = message.get_value()

                # retrieves the message value length
                message_value_length = len(message_value)

                # in case the message length is greater
                # than one
                if message_value_length > 1:
                    try:
                        # tries to retrieve the message size unpacking the message value
                        message_size, message_size_length = self.ber_structure._get_packed_length(message_value)
                    except:
                        # continues the loop, because it is
                        # not possible to "decode" the message size
                        continue
                else:
                    # continues the loop, because there's not enough
                    # bytes available
                    continue

            # in case the message data size is the same
            # as the message size plus the message size length
            # plus the identification byte
            if received_data_size >= message_size + message_size_length + 1:
                # retrieves the total message size value
                total_message_size = message_size + message_size_length + 1

                # retrieves the message value from the string buffer
                message_value = message.get_value()

                # retrieves the extra message value
                extra_message_value = message_value[total_message_size:]

                # retrieves the "real" message value
                message_value = message_value[:total_message_size]

                # adds the extra message value to the extra messages buffer
                extra_message_value and self._extra_messages_buffer.insert(0, extra_message_value)

                # process the message value data in the response
                response.process_data(message_value, self.ber_structure)

                # returns the response
                return response

    def bind(self, name, password):
        """
        Executes the bind operation with the given name
        and password.

        @type name: String
        @param name: The name to be used in the bind operation.
        @type password: String
        @param password: The password to be used in the bind operation.
        """

        # retrieves the protocol version
        protocol_version = self.protocol_version or DEFAULT_PROTOCOL_VERSION

        # creates the simple authentication
        simple_authentication = main_client_ldap_structures.SimpleAuthentication(password)

        # creates the bind request
        bind_request = main_client_ldap_structures.BindRequest(protocol_version, name, simple_authentication)

        # sends the request for the bind and controls
        request = self.send_request(bind_request, [])

        # retrieves the response
        response = self.retrieve_response(request)

        # validates the response
        self._validate_response(response)

    def unbind(self):
        """
        Executes the unbind operation.
        """

        # creates the unbind request
        unbind_request = main_client_ldap_structures.UnbindRequest()

        # sends the request for the unbind and controls
        self.send_request(unbind_request, [])

    def search(self):
        # creates the attribute value assertion
        attribute_value_assertion = main_client_ldap_structures.AttributeValueAssertion("uid", "joamag")

        # creates the present filter
        present_filter = main_client_ldap_structures.PresentFilter("objectclass")

        # creates the equality match filter
        equality_match_filter = main_client_ldap_structures.EqualityMatchFilter(attribute_value_assertion)

        # creates the and filter
        and_filter = main_client_ldap_structures.AndFilter([present_filter, equality_match_filter])

        # creates the attributes
        attributes = main_client_ldap_structures.Attributes(["+", "*"])

        # creates the search request
        search_request = main_client_ldap_structures.SearchRequest("dc=hive", 2, 0, 0, 180, False, and_filter, attributes)

        # sends the request for the search and controls
        request = self.send_request(search_request, [])

        # retrieves the response
        response = self.retrieve_response(request)

        # retrieves the response
        #response = self.retrieve_response(request)

        print response

    def _validate_response(self, response):
        """
        Validates the given ldap response according
        to the ldap specification.

        @type response: LdapResponse
        @param response: The ldap response to be validated.
        """

        # retrieves the request for the response
        request = response.request

        # retrieves the response message id
        response_message_id = response.message_id

        # retrieves the request message id
        request_message_id = request.message_id

        # in case the request and response message id's do not match
        if not request_message_id == response_message_id:
            # raises a ldap validation exception
            raise main_client_ldap_exceptions.LdapValidationException("invalid response message id '%i' for request message id '%i'" % (response_message_id, request_message_id))

        # retrieves the response protocol operation
        response_protocol_operation = response.protocol_operation

        # retrieves the response result code
        response_result_code = response_protocol_operation.result_code

        # in case the response result code is not valid
        if not response_result_code == 0:
            # raises a ldap validation exception
            raise main_client_ldap_exceptions.LdapValidationException("invalid response code: " + str(response_result_code))

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
        parameters = {"client_plugin" : self.main_client_ldap.main_client_ldap_plugin,
                      "request_timeout" : REQUEST_TIMEOUT,
                      "response_timeout" : RESPONSE_TIMEOUT}

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
