#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import hmac
import time
import random
import hashlib

import colony

from . import exceptions

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

HMAC_SHA1_VALUE = "HMAC-SHA1"
""" The HMAC SHA1 value """

RSA_SHA1_VALUE = "RSA-SHA1"
""" The RSA SHA1 value """

PLAINTEXT_VALUE = "PLAINTEXT"
""" The plaintext value """

OAUTH_AUTHENTICATION_TYPE = 1
""" The OAuth authentication type """

DEFAULT_OAUTH_SIGNATURE_METHOD = HMAC_SHA1_VALUE
""" The default OAuth signature method """

DEFAULT_OAUTH_VERSION = "1.0"
""" The default OAuth version """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

PUT_METHOD_VALUE = "PUT"
""" The put method value """

OUT_OF_BAND_CALLBACK_VALUE = "oob"
""" The out of band (default) callback value """

HMAC_HASH_MODULES_MAP = {HMAC_SHA1_VALUE: hashlib.sha1}
""" The map associating the HMAC values with the hashlib hash function modules """

BASE_REST_URL = "http://api.dropbox.com/1/"
""" The base REST URL to be used """

BASE_REST_SECURE_URL = "https://api.dropbox.com/1/"
""" The base REST secure URL to be used """

WWW_REST_SECURE_URL = "http://www.dropbox.com/1/"
""" The WWW REST URL to be used """

WWW_REST_SECURE_URL = "https://www.dropbox.com/1/"
""" The WWW REST secure URL to be used """

CONTENT_REST_SECURE_URL = "http://api-content.dropbox.com/1/"
""" The content REST URL to be used """

CONTENT_REST_SECURE_URL = "https://api-content.dropbox.com/1/"
""" The content REST secure URL to be used """


class APIDropbox(colony.System):
    """
    The API Dropbox class.
    """

    def create_client(self, api_attributes, open_client=True):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :type open_client: bool
        :param open_client: If the client should be opened.
        :rtype: DropboxClient
        :return: The created client.
        """

        # retrieves the client HTTP plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the JSON plugin
        json_plugin = self.plugin.json_plugin

        # retrieves the various attributes to be used
        # in the construction of the Dropbox client
        encoding = api_attributes.get("encoding", None)
        oauth_structure = api_attributes.get("oauth_structure", None)

        # creates a new client with the given options, opens
        # it in case it's required and returns the generated
        # client to the caller method
        dropbox_client = DropboxClient(
            json_plugin, client_http_plugin, encoding, oauth_structure
        )
        if open_client:
            dropbox_client.open()
        return dropbox_client


class DropboxClient(object):
    """
    The class that represents a Dropbox client connection.
    """

    json_plugin = None
    """ The JSON plugin """

    client_http_plugin = None
    """ The client HTTP plugin """

    encoding = None
    """ The encoding used """

    request_headers = {}
    """ The request headers """

    oauth_structure = None
    """ The OAuth structure """

    http_client = None
    """ The HTTP client for the connection """

    def __init__(
        self,
        json_plugin=None,
        client_http_plugin=None,
        encoding=None,
        oauth_structure=None,
    ):
        """
        Constructor of the class.

        :type json_plugin: JSONPlugin
        :param json_plugin: The JSON plugin.
        :type client_http_plugin: ClientHTTPPlugin
        :param client_http_plugin: The client HTTP plugin.
        :type encoding: String
        :param encoding: The encoding used.
        :type oauth_structure: OAuthStructure
        :param oauth_structure: The OAuth structure
        """

        self.json_plugin = json_plugin
        self.client_http_plugin = client_http_plugin
        self.encoding = encoding
        self.oauth_structure = oauth_structure

        self.request_header = {}

    def open(self):
        """
        Opens the Dropbox client.
        """

        pass

    def close(self):
        """
        Closes the Dropbox client.
        """

        # in case an HTTP client is defined
        if self.http_client:
            # closes the HTTP client
            self.http_client.close({})

    def generate_oauth_structure(
        self,
        oauth_consumer_key,
        oauth_consumer_secret,
        oauth_signature_method=DEFAULT_OAUTH_SIGNATURE_METHOD,
        oauth_signature=None,
        oauth_timestamp=None,
        oauth_nonce=None,
        oauth_version=DEFAULT_OAUTH_VERSION,
        oauth_callback=OUT_OF_BAND_CALLBACK_VALUE,
        set_structure=True,
    ):
        """
        Generates a new OAuth structure, for the given parameters.

        :type oauth_consumer_key: String
        :param oauth_consumer_key: The consumer key.
        :type oauth_consumer_secret: String
        :param oauth_consumer_secret: The consumer secret.
        :type oauth_signature_method: String
        :param oauth_signature_method: The signature method.
        :type oauth_signature: String
        :param oauth_signature: The signature.
        :type oauth_timestamp: float
        :param oauth_timestamp: The timestamp.
        :type oauth_nonce: int
        :param oauth_nonce: The nonce.
        :type oauth_version: String
        :param oauth_version: The version.
        :type oauth_callback: String
        :param oauth_callback: The callback.
        :type set_structure: bool
        :param set_structure: The set structure flag (if the structure should be set in the client).
        :rtype: OAuthStructure
        :return: The generated OAuth structure.
        """

        # constructs a new OAuth structure
        oauth_structure = OAuthStructure(
            oauth_consumer_key,
            oauth_consumer_secret,
            oauth_signature_method=oauth_signature_method,
            oauth_signature=oauth_signature,
            oauth_timestamp=oauth_timestamp,
            oauth_nonce=oauth_nonce,
            oauth_version=oauth_version,
            oauth_callback=oauth_callback,
        )

        # in case the structure is meant to be set
        # sets it in the current instance and returns
        # the structure that was "just" generated
        if set_structure:
            self.set_oauth_structure(oauth_structure)
        return oauth_structure

    def open_oauth_request_token(self):
        """
        Opens the OAuth request token.

        :rtype: OAuthStructure
        :return: The current OAuth structure.
        """

        # sets the retrieval URL
        retrieval_url = BASE_REST_SECURE_URL + "oauth/request_token"

        # retrieves the timestamp
        oauth_timestamp = self._get_oauth_timestamp()

        # retrieves the nonce
        oauth_nonce = self._get_oauth_nonce()

        # start the parameters map
        parameters = {}

        # sets the OAuth parameters
        parameters["oauth_consumer_key"] = self.oauth_structure.oauth_consumer_key
        parameters["oauth_signature_method"] = (
            self.oauth_structure.oauth_signature_method
        )
        parameters["oauth_timestamp"] = oauth_timestamp
        parameters["oauth_nonce"] = oauth_nonce
        parameters["oauth_version"] = self.oauth_structure.oauth_version

        # in case callback is defined
        if self.oauth_structure.oauth_callback:
            # sets the callback
            parameters["oauth_callback"] = self.oauth_structure.oauth_callback

        if self.oauth_structure.oauth_signature:
            # sets the signature
            parameters["oauth_signature"] = self.oauth_structure.oauth_signature
        else:
            # escapes the consumer secret
            oauth_consumer_secret_escaped = "%s&" % self._escape_url(
                self.oauth_structure.oauth_consumer_secret
            )

            # creates the parameters tuple
            parameters_tuple = [
                "%s=%s"
                % (
                    self._escape_url(key),
                    self._escape_url(
                        colony.legacy.UNICODE(parameters[key]).encode(DEFAULT_ENCODING)
                    ),
                )
                for key in sorted(parameters)
            ]

            # creates the message
            message = "&".join(
                map(
                    self._escape_url,
                    [GET_METHOD_VALUE, retrieval_url, "&".join(parameters_tuple)],
                )
            )

            # sets the signature
            parameters["oauth_signature"] = (
                hmac.new(oauth_consumer_secret_escaped, message, hashlib.sha1)
                .digest()
                .encode("base64")[:-1]
            )

        # fetches the retrieval URL with the given parameters retrieving the JSON
        result = self._fetch_url(retrieval_url, parameters)

        # splits the multiple parameters around the separator characters
        # and then build the list of tuples that is then converted into
        # a key to value dictionary
        values = result.split("&")
        values_list = [value.split("=", 1) for value in values]
        values_list = [
            tuple if len(tuple) == 2 else (tuple[0], None) for tuple in values_list
        ]
        values_map = dict(values_list)

        # retrieves both the OAuth token and the OAuth token secret to
        # be able to use them in further authenticated requests
        self.oauth_structure.oauth_token = values_map["oauth_token"]
        self.oauth_structure.oauth_token_secret = values_map["oauth_token_secret"]

        # returns the OAuth structure
        return self.oauth_structure

    def open_oauth_access_token(self):
        """
        Opens the OAuth access token.

        :rtype: OAuthStructure
        :return: The current OAuth structure.
        """

        # sets the retrieval URL
        retrieval_url = BASE_REST_SECURE_URL + "oauth/access_token"

        # retrieves the timestamp
        oauth_timestamp = self._get_oauth_timestamp()

        # retrieves the nonce
        oauth_nonce = self._get_oauth_nonce()

        # start the parameters map
        parameters = {}

        # sets the OAuth parameters
        parameters["oauth_token"] = self.oauth_structure.oauth_token
        parameters["oauth_consumer_key"] = self.oauth_structure.oauth_consumer_key
        parameters["oauth_signature_method"] = (
            self.oauth_structure.oauth_signature_method
        )
        parameters["oauth_timestamp"] = oauth_timestamp
        parameters["oauth_nonce"] = oauth_nonce
        parameters["oauth_version"] = self.oauth_structure.oauth_version

        # in case the verifier is defined
        if self.oauth_structure.oauth_verifier:
            # sets the verifier
            parameters["oauth_verifier"] = self.oauth_structure.oauth_verifier

        if self.oauth_structure.oauth_signature:
            # sets the signature
            parameters["oauth_signature"] = self.oauth_structure.oauth_signature
        else:
            # escapes the consumer secret
            oauth_consumer_secret_escaped = "%s&%s" % (
                self._escape_url(self.oauth_structure.oauth_consumer_secret),
                self._escape_url(self.oauth_structure.oauth_token_secret),
            )

            # creates the parameters tuple
            parameters_tuple = [
                "%s=%s"
                % (
                    self._escape_url(key),
                    self._escape_url(
                        colony.legacy.UNICODE(parameters[key]).encode(DEFAULT_ENCODING)
                    ),
                )
                for key in sorted(parameters)
            ]

            # creates the message
            message = "&".join(
                map(
                    self._escape_url,
                    [GET_METHOD_VALUE, retrieval_url, "&".join(parameters_tuple)],
                )
            )

            # sets the signature
            parameters["oauth_signature"] = (
                hmac.new(oauth_consumer_secret_escaped, message, hashlib.sha1)
                .digest()
                .encode("base64")[:-1]
            )

        # fetches the retrieval URL with the given parameters retrieving the JSON
        result = self._fetch_url(retrieval_url, parameters)

        # splits the multiple parameters around the separator characters
        # and then build the list of tuples that is then converted into
        # a key to value dictionary
        values = result.split("&")
        values_list = [value.split("=", 1) for value in values]
        values_list = [
            tuple if len(tuple) == 2 else (tuple[0], None) for tuple in values_list
        ]
        values_map = dict(values_list)

        # retrieves the OAuth values from the values map
        self.oauth_structure.oauth_access_token = values_map["oauth_token"]
        self.oauth_structure.oauth_token_secret = values_map["oauth_token_secret"]

        # returns the OAuth structure
        return self.oauth_structure

    def get_oauth_authorize_url(self):
        """
        Retrieves the OAuth authorize URL.

        :rtype: String
        :return: The OAuth authorize URL.
        """

        # sets the retrieval URL
        retrieval_url = WWW_REST_SECURE_URL + "oauth/authorize"

        # creates the authentication parameters
        authentication_parameters = {
            "oauth_token": self.oauth_structure.oauth_token,
            "oauth_callback": self.oauth_structure.oauth_callback,
        }

        # creates the authentication URL from the authentication token
        authentication_url = self._build_url(retrieval_url, authentication_parameters)

        # returns the authentication URL
        return authentication_url

    def get_oauth_authenticate_url(self):
        """
        Retrieves the OAuth authenticate URL.

        :rtype: String
        :return: The OAuth authenticate URL.
        """

        # sets the retrieval URL
        retrieval_url = WWW_REST_SECURE_URL + "oauth/authenticate"

        # creates the authentication parameters
        authentication_parameters = {"oauth_token": self.oauth_structure.oauth_token}

        # creates the authentication URL from the authentication token
        authentication_url = self._build_url(retrieval_url, authentication_parameters)

        # returns the authentication URL
        return authentication_url

    def get_account_info(self):
        """
        Retrieves the account information for the current user.

        :rtype: Dictionary
        :return: The account information for the current user.
        """

        # requires authentication
        self.require_authentication()

        # start the parameters map
        parameters = {}

        retrieval_url = BASE_REST_SECURE_URL + "account/info"

        # fetches the retrieval URL with the given parameters retrieving the JSON
        json = self._fetch_url(retrieval_url, parameters)

        # loads JSON retrieving the data
        data = self.json_plugin.loads(json)

        # checks for Dropbox errors
        self._check_dropbox_errors(data)

        # returns the data
        return data

    def files_put(self, file_path, target_path=None):
        """
        Uploads a file in the given file to the given target
        path, this is a very slow operation.
        In case no target path is provided the base name of the
        file path is used for the root directory.

        :type file_path: String
        :param file_path: The (local) file path of the file to
        be uploaded (the file must exist).
        :type target_path: String
        :param target_path: The target (remote) path for the
        uploading of the file.
        :rtype: Dictionary
        :return: The resulting metadata from the upload.
        """

        # requires authentication
        self.require_authentication()

        # opens the file
        file = open(file_path, "rb")

        # reads the complete file contents and then
        # closes the file at the end or error
        try:
            file_contents = file.read()
        finally:
            file.close()

        # retrieves the base name to be set for the file
        # (this is the default file name value to be used)
        base_name = os.path.basename(file_path)
        target_path = target_path or base_name

        # start the parameters map
        parameters = {}

        # creates the URL that will be used for the put of the
        # file on the remove data source
        retrieval_url = CONTENT_REST_SECURE_URL + "files_put/dropbox/" + target_path

        # fetches the retrieval URL with the given parameters retrieving the JSON
        json = self._fetch_url(
            retrieval_url, parameters, PUT_METHOD_VALUE, file_contents
        )

        # loads JSON retrieving the data
        data = self.json_plugin.loads(json)

        # checks for Dropbox errors
        self._check_dropbox_errors(data)

        # returns the data
        return data

    def require_authentication(self):
        """
        Tests if authentication is enabled.
        Raising an exception in case no authentication values
        are available.
        """

        # in case the OAuth access token is not available
        if not self.oauth_structure.oauth_access_token:
            # raises the invalid authentication exception
            raise exceptions.InvalidAuthentication("user not authenticated")

    def get_oauth_structure(self):
        """
        Retrieves the OAuth structure.

        :rtype: OAuthStructure
        :return: The OAuth structure.
        """

        return self.oauth_structure

    def set_oauth_structure(self, oauth_structure):
        """
        Sets the OAuth structure.

        :type oauth_structure: OAuthStructure
        :param oauth_structure: The OAuth structure.
        """

        self.oauth_structure = oauth_structure

    def _fetch_url(self, url, parameters=None, method=GET_METHOD_VALUE, contents=None):
        """
        Fetches the given URL for the given parameters and using the given method.

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

        # in case parameters is not defined
        if not parameters:
            # creates a new parameters map
            parameters = {}

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # retrieves the current authentication type
        authentication_type = self._get_authentication_type()

        # builds the OAuth arguments, for authentication in case the
        # OAuth authentication method is selected
        if authentication_type == OAUTH_AUTHENTICATION_TYPE:
            # builds the OAuth arguments for authentication
            self._build_oauth_arguments(url, parameters, method)

        # fetches the URL retrieving the HTTP response
        http_response = http_client.fetch_url(
            url,
            method,
            parameters,
            content_type_charset=DEFAULT_CHARSET,
            contents=contents,
        )

        # retrieves the contents from the HTTP response
        contents = http_response.received_message

        # returns the contents
        return contents

    def _build_url(self, base_url, parameters):
        """
        Builds the URL for the given URL and parameters.

        :type url: String
        :param url: The base URL to be used.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for URL construction.
        :rtype: String
        :return: The built URL for the given parameters.
        """

        # retrieves the HTTO client, build the URL from the base URL
        # and then returns the URL to the caller method
        http_client = self._get_http_client()
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)
        return url

    def _build_oauth_arguments(self, url, parameters, method=GET_METHOD_VALUE):
        """
        Builds the OAuth arguments encoding them into the OAuth message specification.

        :type url: String
        :param url: The URL to be used for the OAuth encoding.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for the OAuth encoding.
        :type method: String
        :param method: The method to be used for the OAuth encoding.
        :rtype: String
        :return: The OAuth arguments encoded in OAuth message specification.
        """

        # retrieves the timestamp
        oauth_timestamp = self._get_oauth_timestamp()

        # retrieves the nonce
        oauth_nonce = self._get_oauth_nonce()

        # sets the OAuth parameters
        parameters["oauth_token"] = self.oauth_structure.oauth_access_token
        parameters["oauth_consumer_key"] = self.oauth_structure.oauth_consumer_key
        parameters["oauth_signature_method"] = (
            self.oauth_structure.oauth_signature_method
        )
        parameters["oauth_timestamp"] = oauth_timestamp
        parameters["oauth_nonce"] = oauth_nonce
        parameters["oauth_version"] = self.oauth_structure.oauth_version

        if self.oauth_structure.oauth_signature:
            # sets the signature
            parameters["oauth_signature"] = self.oauth_structure.oauth_signature
        else:
            # escapes the consumer secret
            oauth_consumer_secret_escaped = "%s&%s" % (
                self._escape_url(self.oauth_structure.oauth_consumer_secret),
                self._escape_url(self.oauth_structure.oauth_token_secret),
            )

            # creates the parameters tuple
            parameters_tuple = [
                "%s=%s"
                % (
                    self._escape_url(key),
                    self._escape_url(
                        colony.legacy.UNICODE(parameters[key]).encode(DEFAULT_ENCODING)
                    ),
                )
                for key in sorted(parameters)
            ]

            # creates the message
            message = "&".join(
                map(self._escape_url, [method, url, "&".join(parameters_tuple)])
            )

            # sets the signature
            parameters["oauth_signature"] = (
                hmac.new(oauth_consumer_secret_escaped, message, hashlib.sha1)
                .digest()
                .encode("base64")[:-1]
            )

    def _escape_url(self, url_text):
        """
        Escapes the given URL text into a valid HTTP get request string.

        :rtype: String
        :return: the given URL text in a valid HTTP get request string.
        """

        # returns the quoted version of the URL text
        return colony.quote_plus(str(url_text), "")

    def _check_dropbox_errors(self, data):
        """
        Checks the given data for Dropbox errors.

        This method raises an exception in case an error
        exists in the data to be verified.

        :type data: Dictionary
        :param data: The data to be checked for Dropbox errors.
        """

        pass

    def _get_authentication_type(self):
        """
        Retrieves the current authentication type being used.

        :rtype: int
        :return: The current authentication type being used.
        """

        if self.oauth_structure and self.oauth_structure.oauth_access_token:
            return OAUTH_AUTHENTICATION_TYPE

        return None

    def _get_oauth_timestamp(self):
        """
        Retrieves the real value for the OAuth timestamp.

        :rtype: float
        :return: The real value for the OAuth timestamp.
        """

        if self.oauth_structure.oauth_timestamp:
            oauth_timestamp = self.oauth_structure.oauth_token
        else:
            oauth_timestamp = int(time.time())

        return oauth_timestamp

    def _get_oauth_nonce(self):
        """
        Retrieves the real value for the OAuth nonce.

        :rtype: int
        :return: the real value for the OAuth nonce.
        """

        if self.oauth_structure.oauth_nonce:
            oauth_nonce = self.oauth_structure.oauth_nonce
        else:
            oauth_nonce = random.getrandbits(64)

        return oauth_nonce

    def _get_http_client(self):
        """
        Retrieves the HTTP client currently in use (in case it's created)
        if not created creates the HTTP client.

        :rtype: HTTPClient
        :return: The retrieved HTTP client.
        """

        # in case no HTTP client exists
        if not self.http_client:
            # defines the client parameters
            client_parameters = {CONTENT_TYPE_CHARSET_VALUE: DEFAULT_CHARSET}

            # creates the HTTP client and opens the client
            # with empty options (default)
            self.http_client = self.client_http_plugin.create_client(client_parameters)
            self.http_client.open({})

        # returns the HTTP client
        return self.http_client


class OAuthStructure(object):
    """
    The OAuth structure class.
    """

    oauth_consumer_key = None
    """ The consumer key """

    oauth_consumer_secret = None
    """ The consumer secret """

    oauth_signature_method = DEFAULT_OAUTH_SIGNATURE_METHOD
    """ The signature method """

    oauth_signature = None
    """ The signature """

    oauth_timestamp = None
    """ The timestamp """

    oauth_nonce = None
    """ The nonce """

    oauth_version = DEFAULT_OAUTH_VERSION
    """ The version """

    oauth_callback = OUT_OF_BAND_CALLBACK_VALUE
    """ The callback """

    oauth_token = None
    """ The OAuth token """

    oauth_token_secret = None
    """ The token secret """

    oauth_verifier = None
    """ The verifier """

    oauth_access_token = None
    """ The OAuth access token """

    def __init__(
        self,
        oauth_consumer_key,
        oauth_consumer_secret,
        oauth_signature_method=DEFAULT_OAUTH_SIGNATURE_METHOD,
        oauth_signature=None,
        oauth_timestamp=None,
        oauth_nonce=None,
        oauth_version=DEFAULT_OAUTH_VERSION,
        oauth_callback=OUT_OF_BAND_CALLBACK_VALUE,
    ):
        """
        Constructor of the class.

        :type oauth_consumer_key: String
        :param oauth_consumer_key: The consumer key.
        :type oauth_consumer_secret: String
        :param oauth_consumer_secret: The consumer secret.
        :type oauth_signature_method: String
        :param oauth_signature_method: The signature method.
        :type oauth_signature: String
        :param oauth_signature: The signature.
        :type oauth_timestamp: float
        :param oauth_timestamp: The timestamp.
        :type oauth_nonce: int
        :param oauth_nonce: The nonce.
        :type oauth_version: String
        :param oauth_version: The version.
        :type oauth_callback: Method
        :param oauth_callback: The callback.
        """

        self.oauth_consumer_key = oauth_consumer_key
        self.oauth_consumer_secret = oauth_consumer_secret
        self.oauth_signature_method = oauth_signature_method
        self.oauth_signature = oauth_signature
        self.oauth_timestamp = oauth_timestamp
        self.oauth_nonce = oauth_nonce
        self.oauth_version = oauth_version
        self.oauth_callback = oauth_callback

    def get_oauth_consumer_key(self):
        """
        Retrieves the consumer key.

        :rtype: String
        :return: The consumer key.
        """

        return self.oauth_consumer_key

    def set_oauth_consumer_key(self, oauth_consumer_key):
        """
        Sets the consumer key.

        :type oauth_consumer_key: String
        :param oauth_consumer_key: The consumer key.
        """

        self.oauth_consumer_key = oauth_consumer_key

    def get_oauth_consumer_secret(self):
        """
        Retrieves the consumer secret.

        :rtype: String
        :return: The consumer secret.
        """

        return self.oauth_consumer_secret

    def set_consumer_secret(self, oauth_consumer_secret):
        """
        Sets the consumer secret.

        :type oauth_consumer_secret: String
        :param oauth_consumer_secret: The consumer secret.
        """

        self.oauth_consumer_secret = oauth_consumer_secret

    def get_oauth_signature_method(self):
        """
        Retrieves the signature method.

        :rtype: String
        :return: The signature method.
        """

        return self.oauth_signature_method

    def set_oauth_signature_method(self, oauth_signature_method):
        """
        Sets the signature method.

        :type oauth_signature_method: String
        :param oauth_signature_method: The signature method.
        """

        self.oauth_signature_method = oauth_signature_method

    def get_oauth_signature(self):
        """
        Retrieves the signature.

        :rtype: String
        :return: The signature.
        """

        return self.oauth_signature

    def set_oauth_signature(self, oauth_signature):
        """
        Sets the signature.

        :type oauth_signature: String
        :param oauth_signature: The signature.
        """

        self.oauth_signature = oauth_signature

    def get_oauth_timestamp(self):
        """
        Retrieves the timestamp.

        :rtype: float
        :return: The timestamp.
        """

        return self.oauth_timestamp

    def set_oauth_timestamp(self, oauth_timestamp):
        """
        Sets the timestamp.

        :type oauth_timestamp: float
        :param oauth_timestamp: The timestamp
        """

        self.oauth_timestamp = oauth_timestamp

    def get_oauth_nonce(self):
        """
        Retrieves the nonce.

        :rtype: int
        :return: The nonce.
        """

        return self.oauth_nonce

    def set_oauth_nonce(self, oauth_nonce):
        """
        Sets the nonce.

        :type oauth_nonce: int
        :param oauth_nonce: The nonce.
        """

        self.oauth_nonce = oauth_nonce

    def get_oauth_version(self):
        """
        Retrieves the version.

        :rtype: String
        :return: The version.
        """

        return self.oauth_version

    def set_oauth_version(self, oauth_version):
        """
        Sets the version.

        :type oauth_version: String
        :param oauth_version: The version.
        """

        self.oauth_version = oauth_version

    def get_oauth_callback(self):
        """
        Retrieves the callback.

        :rtype: String
        :return: The callback.
        """

        return self.oauth_callback

    def set_oauth_callback(self, oauth_callback):
        """
        Sets the callback.

        :type oauth_callback: String
        :param oauth_callback: The callback.
        """

        self.oauth_callback = oauth_callback

    def get_oauth_token(self):
        """
        Retrieves the token.

        :rtype: String
        :return: The token.
        """

        return self.oauth_token

    def set_oauth_token(self, oauth_token):
        """
        Sets the token.

        :type oauth_token: String
        :param oauth_token: The token.
        """

        self.oauth_token = oauth_token

    def get_oauth_token_secret(self):
        """
        Retrieves the token secret.

        :rtype: String
        :return: The token secret.
        """

        return self.oauth_token_secret

    def set_oauth_token_secret(self, oauth_token_secret):
        """
        Sets the token secret.

        :type oauth_token_secret: String
        :param oauth_token_secret: The token secret.
        """

        self.oauth_token_secret = oauth_token_secret

    def get_oauth_verifier(self):
        """
        Retrieves the verifier.

        :rtype: String
        :return: The verifier.
        """

        return self.oauth_verifier

    def set_oauth_verifier(self, oauth_verifier):
        """
        Sets the verifier.

        :type oauth_verifier: String
        :param oauth_verifier: The verifier.
        """

        self.oauth_verifier = oauth_verifier

    def get_oauth_access_token(self):
        """
        Retrieves the access token.

        :rtype: String
        :return: The access token.
        """

        return self.oauth_access_token

    def set_oauth_access_token(self, oauth_access_token):
        """
        Sets the access token.

        :type oauth_access_tokken: String
        :param oauth_access_token: The access token.
        """

        self.oauth_access_token = oauth_access_token
