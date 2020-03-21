#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import base64
import hashlib
import datetime

import xml.dom.minidom

import colony

from . import exceptions

INVOICE_BASE_URL = "https://servicos.portaldasfinancas.gov.pt:400/fews"
""" The base URL to be used for invoice
submission, this is a secure HTTPS based URL"""

INVOICE_BASE_TEST_URL = "https://servicos.portaldasfinancas.gov.pt:700/fews"
""" The base test URL to be used for invoice
submission, this is a secure HTTPS based URL
but still only for testing purposes """

TRANSPORT_BASE_URL = "https://servicos.portaldasfinancas.gov.pt:401/sgdtws"
""" The base URL to be used for transport document
submission, this is a secure HTTPS based URL"""

TRANSPORT_BASE_TEST_URL = "https://servicos.portaldasfinancas.gov.pt:701/sgdtws"
""" The base test URL to be used for transport document
submission, this is a secure HTTPS based URL
but still only for testing purposes """

class APIAT(colony.System):
    """
    The API AT class.
    """

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :type open_client: bool
        :param open_client: If the client should be opened.
        :rtype: OpenIDClient
        :return: The created client.
        """

        # retrieves the client HTTP plugin
        ssl_plugin = self.plugin.ssl_plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the AT structure and test mode (if available)
        at_structure = api_attributes.get("at_structure", None)
        test_mode = api_attributes.get("test_mode", False)
        key = api_attributes.get("key", False)
        certificate = api_attributes.get("certificate", False)

        # creates a new client with the given options, opens
        # it in case it's required and returns the generated
        # client to the caller method
        at_client = ATClient(
            self.plugin,
            ssl_plugin,
            client_http_plugin,
            at_structure,
            test_mode,
            key,
            certificate
        )
        open_client and at_client.open()
        return at_client

class ATClient(object):
    """
    The class that represents a AT client connection.
    Will be used to encapsulate the HTTP request
    around a locally usable API.
    """

    plugin = None
    """ The plugin associated with the AT client this
    plugin is considered the owner of the client """

    ssl_plugin = None
    """ The SSL plugin """

    client_http_plugin = None
    """ The client HTTP plugin """

    at_structure = None
    """ The AT structure """

    test_mode = None
    """ Flag indicating the client is supposed to
    run in test mode (uses different API urls) """

    key = None
    """ The path to the private key file to be used
    in the connection with the server """

    certificate = None
    """ The path to the certificate file to be used
    in the connection with the server """

    http_client = None
    """ The HTTP client for the connection """

    def __init__(
        self,
        plugin,
        ssl_plugin = None,
        client_http_plugin = None,
        at_structure = None,
        test_mode = False,
        key = None,
        certificate = None
    ):
        """
        Constructor of the class.

        :type plugin: Plugin
        :param plugin: The plugin associated with the AT client this
        plugin is considered the owner of the client.
        :type ssl_plugin: SSLPlugin
        :param ssl_plugin: The SSL plugin.
        :type client_http_plugin: ClientHTTPPlugin
        :param client_http_plugin: The client HTTP plugin.
        :type at_structure: ATStructure
        :param at_structure: The AT structure.
        :type test_mode: bool
        :param test_mode: Flag indicating if the client is to
        be run in test mode.
        :type key: String
        :param key: The path to the private key file to be used
        in the connection with the server.
        :type certificate: String
        :param certificate: The path to the certificate file to be used
        in the connection with the server.
        """

        self.plugin = plugin
        self.ssl_plugin = ssl_plugin
        self.client_http_plugin = client_http_plugin
        self.at_structure = at_structure
        self.test_mode = test_mode
        self.key = key
        self.certificate = certificate

    def open(self):
        """
        Opens the AT client.
        """

        pass

    def close(self):
        """
        Closes the AT client.
        """

        # in case an HTTP client is defined closes it
        # (flushing its internal structures
        if self.http_client: self.http_client.close({})

    def generate_at_structure(self, username, password, set_structure = True):
        """
        Generates the AT structure for the given arguments.

        :type username: String
        :param username: The username.
        :type password: String
        :param password: The password.
        :type set_structure: bool
        :param set_structure: If the structure should be
        set in the AT client.
        :rtype: ATStructure
        :return: The generated AT structure.
        """

        # creates a new AT structure
        at_structure = ATStructure(username, password)

        # in case the structure is meant to be set
        # sets it accordingly (in the current object)
        if set_structure: self.set_at_structure(at_structure)

        # returns the AT structure
        return at_structure

    def get_resource(self, path):
        # retrieves the current plugin manager associated
        # with the current context of execution
        plugin_manager = self.plugin.manager

        # retrieves the plugin path for the currently associated
        # (owner) plugin and uses it to retrieve the complete path
        # for the requested resource then returns that path
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)
        path = os.path.join(plugin_path, path)
        return path

    def submit_invoice(self, invoice_payload):
        # retrieves the proper based URL according to the current
        # test mode and uses it to create the complete action URL
        base_url = self.test_mode and INVOICE_BASE_TEST_URL or INVOICE_BASE_URL
        submit_invoice_url = base_url + "/faturas"

        # submits the invoice document and returns the result
        result = self._submit_document(submit_invoice_url, invoice_payload)
        return result

    def submit_transport(self, transport_payload):
        # retrieves the proper based URL according to the current
        # test mode and uses it to create the complete action URL
        base_url = self.test_mode and TRANSPORT_BASE_TEST_URL or TRANSPORT_BASE_URL
        submit_transport_url = base_url + "/documentosTransporte"

        # submits the transport document and returns the result
        data = self._submit_document(submit_transport_url, transport_payload)
        return data

    def validate_credentials(self):
        """
        Validates that the credentials are valid, returning a flag
        indicating the result.

        This operation is considered a mock for the AT client as
        it returns valid, provides API compatibility.

        :rtype: bool
        :return: Flag indicating if the credentials are valid.
        """

        # returns valid for every request for validation received
        # as no validation is currently possible
        return True

    def get_at_structure(self):
        """
        Retrieves the AT structure.

        :rtype: ATStructure
        :return: The AT structure.
        """

        return self.at_structure

    def set_at_structure(self, at_structure):
        """
        Sets the AT structure.

        :type at_structure: ATStructure
        :param at_structure: The AT structure.
        """

        self.at_structure = at_structure

    def _submit_document(self, submit_url, document_payload):
        # retrieves the proper username and password values
        # according to the current test mode flag value then
        # convert both values into string to make sure that
        # no unicode buffers are present (avoids conversion)
        username = self.test_mode and "599999993/0037" or str(self.at_structure.username)
        password = self.test_mode and "testes1234" or str(self.at_structure.password)
        username = str(username)
        password = str(password)
        password_b = colony.legacy.bytes(password)

        # creates a new aes cipher structure to be
        # able to encrypt the target fields and gets
        # its currently set key as the secret (this
        # key was generated according to the default
        # block size defined in the module)
        aes = colony.AesCipher()
        secret = aes.get_key()

        # retrieves the path to the AT public key to be used
        # in the encryption of the secret value (as nonce)
        public_key_path = self.get_resource("api_at/resources/at.pem")

        # runs the encryption on the secret value to create an
        # RSA encrypted representation of it and then encodes
        # that value in base 64 to create the nonce value
        ssl_structure = self.ssl_plugin.create_structure({})
        secret_encrypted = ssl_structure.encrypt(public_key_path, secret)
        nonce = base64.b64encode(secret_encrypted)
        nonce = colony.legacy.str(nonce)

        # encrypts the current password using the aes structure
        # created for the current context and then encodes it
        # into a base 64 structure
        password_encrypted = aes.encrypt(password_b)
        password_encrypted_b64 = base64.b64encode(password_encrypted)
        password_encrypted_b64 = colony.legacy.str(password_encrypted_b64)

        # retrieves the current utc date to be used for temporal
        # verification of the request on the server side
        current_date = datetime.datetime.utcnow()
        current_date_s = current_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        current_date_b = colony.legacy.bytes(current_date_s)

        # creates the base digest string from the secret, current
        # date and password values, and uses it to create the verification
        # digest responsible for the "signature of the message"
        digest = secret + current_date_b + password_b
        digest_sha1 = hashlib.sha1(digest)
        digest_hash = digest_sha1.digest()
        digest_hash_encrypted = aes.encrypt(digest_hash)
        digest_hash_encrypted_b64 = base64.b64encode(digest_hash_encrypted)
        digest_hash_encrypted_b64 = colony.legacy.str(digest_hash_encrypted_b64)

        # defines the format of the SOAP envelope to be submitted to AT
        # as a normal string template to be populated with global values
        envelope = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
            <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
                <S:Header>
                    <wss:Security xmlns:wss="http://schemas.xmlsoap.org/ws/2002/12/secext">
                        <wss:UsernameToken>
                            <wss:Username>%s</wss:Username>
                            <wss:Password Digest="%s">%s</wss:Password>
                            <wss:Nonce>%s</wss:Nonce>
                            <wss:Created>%s</wss:Created>
                        </wss:UsernameToken>
                    </wss:Security>
                </S:Header>
                <S:Body>
                    %s
                </S:Body>
            </S:Envelope>"""

        # applies the attributes to the SOAP envelope
        message = envelope % (
            username,
            digest_hash_encrypted_b64,
            password_encrypted_b64,
            nonce,
            current_date_s,
            document_payload
        )

        # "fetches" the submit invoice URL with the message contents
        # this should post the invoice and create it in the remote
        # data source
        data = self._fetch_url(submit_url, method = "POST", contents = message)
        self._check_at_errors(data)

        # returns the resulting data
        return data

    def _fetch_url(self, url, parameters = None, method = "GET", contents = None):
        """
        Fetches the given URL for the given parameters and using
        the given method.

        This method should block while the remote communication
        is on idle or receiving.

        :type url: String
        :param url: The URL to be fetched.
        :type parameters: Dictionary
        :param parameters: The parameters to be used the fetch.
        :type method: String
        :param method: The method to be used in the fetch.
        :type contents: String
        :param contents: The contents.
        :rtype: String
        :return: The fetched data.
        """

        # in case parameters is not defined creates a new parameters
        # map instance to be used
        if not parameters: parameters = {}

        # retrieves the HTTP client and uses it to fetch the provided
        # URL with the provided parameters retrieving the received
        # message and the contents and returning it to the caller method
        http_client = self._get_http_client()
        http_response = http_client.fetch_url(
            url,
            method,
            parameters,
            content_type_charset = "utf-8",
            contents = contents
        )
        contents = http_response.received_message
        return contents

    def get_at_document_id(self, data):
        """
        Parses the provided xml data, retrieving the
        document identifier containing it.

        The provided xml data should be compliant with
        the pre-defined AT SOAP response.

        :type data: String
        :param data: The string containing the xml data
        to be used for parsing and retrieval of the document
        identifier.
        :rtype: String
        :return: The AT document id.
        """

        # parses the xml data and retrieves the entry document
        # structure that will be uses in the parsing
        document = xml.dom.minidom.parseString(data)

        # retrieves the AT document id from the document,
        # and returns it, returning none in case it the
        # document id was not found in the document
        at_doc_code_ids = document.getElementsByTagName("ATDocCodeID")
        at_doc_code_id = self._text(at_doc_code_ids[0]) if at_doc_code_ids else None
        return at_doc_code_id

    def _check_at_errors(self, data):
        """
        Checks the given data for AT errors.

        This method raises an exception in case an error
        exists in the data to be verified.

        :type data: Dictionary
        :param data: The data to be checked for AT errors.
        """

        # parses the xml data and retrieves the entry document
        # structure that will be uses in the parsing
        document = xml.dom.minidom.parseString(data)

        # tries to retrieve the various elements from the xml data
        # that represent error information, an error may be either
        # a normal message based error or a fault
        fault_strings = document.getElementsByTagName("faultstring")
        return_codes = document.getElementsByTagName("ReturnCode")
        return_messages = document.getElementsByTagName("ReturnMessage")

        # in case no fault strings and no returns messages are
        # defined must return immediately because no error has
        # been discovered (or raised)
        if not fault_strings and not return_messages: return

        # tries to retrieve the return code defaulting to undefined
        # in case there's a fault string then retrieves the return
        # message either from the fault string or from the return messages
        return_code = None if fault_strings else self._text(return_codes[0])
        return_message = self._text(fault_strings[0]) if fault_strings else self._text(return_messages[0])

        # "casts" the return code as an integer, in order to convert
        # it from the "normal" string representation
        return_code = return_code and int(return_code)

        # in case the return code is zero no error is currently present
        # (this is a successful request) must return immediately
        if return_code == 0: return

        # raises the AT API error exception associated with the error
        # that has just been "parsed"
        raise exceptions.ATAPIError(return_message, return_code)

    def _get_http_client(self):
        """
        Retrieves the HTTP client currently in use (in case it's created)
        if not created creates the HTTP client.

        :rtype: HTTPClient
        :return: The retrieved HTTP client.
        """

        # in case no HTTP client exists one must be created
        # for the interaction with the API service
        if not self.http_client:
            # retrieves the base values for both the key and the
            # certificate files and retrieves the (final) key and
            # certificate paths according to the current test mode
            base_key_path = self.get_resource("api_at/resources/key.pem")
            base_certificate_path = self.get_resource("api_at/resources/certificate.crt")
            key_path = self.test_mode and base_key_path or self.key
            certificate_path = self.test_mode and base_certificate_path or self.certificate

            # defines the client parameters to be used in the
            # creation of the HTTP client
            client_parameters = dict(
                content_type_charset = "utf-8",
                key_file_path = key_path,
                certificate_file_path = certificate_path,
                ssl_version = "tls1"
            )

            # creates the HTTP client to be used for the API
            # operation and opens it with the default configuration
            self.http_client = self.client_http_plugin.create_client(client_parameters)
            self.http_client.open()

        # returns the created/existing HTTP client
        return self.http_client

    def _text(self, node):
        for _node in node.childNodes:
            if not _node.nodeType == xml.dom.Node.TEXT_NODE: continue
            return _node.data
        return None

class ATStructure(object):
    """
    The AT structure class used to store
    the various AT dependent attributes
    placed there over the course of a session.
    """

    username = None
    """ The username """

    password = None
    """ The password """

    def __init__(self, username, password):
        """
        Constructor of the class.

        :type username: String
        :param username: The username.
        :type password: String
        :param password: The password.
        """

        self.username = username
        self.password = password

    def get_username(self):
        """
        Retrieves the username.

        :rtype: String
        :return: The username.
        """

        return self.username

    def set_username(self, username):
        """
        Sets the username.

        :type username: String
        :param username: The username.
        """

        self.username = username

    def get_password(self):
        """
        Retrieves the password.

        :rtype: String
        :return: The password.
        """

        return self.password

    def set_password(self, password):
        """
        Sets the password.

        :type password: String
        :param password: The password.
        """

        self.password = password
