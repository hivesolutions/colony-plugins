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

import re
import base64
import hashlib

import colony

from . import exceptions

HANDLER_NAME = "ldap"
""" The handler name """

USERNAME_VALUE = "username"
""" The username value """

VALID_VALUE = "valid"
""" The valid value """

ROOT_DN_VALUE = "root_dn"
""" The root dn value """

ROOT_PASSWORD_VALUE = "root_password"
""" The root password value """

HOST_VALUE = "host"
""" The host value """

SEARCH_DN_VALUE = "search_dn"
""" The search dn value """

HASH_VALUE = "hash"
""" The hash value """

VALUE_VALUE = "value"
""" The value value """

MD5_CRYPT_VALUE = "crypt"
""" The MD5 crypt value """

SSHA_VALUE = "ssha"
""" The SSHA value """

PASSWORD_VALUE_REGEX_VALUE = r"\{(?P<hash>\w+)\}(?P<value>.+)"
""" The password value regex value """

MD5_CRYPT_SALT_VALUE_REGEX_VALUE = r"\$1\$(?P<salt>.+)\$.+"
""" The MD5 crypt salt value regex value """

PASSWORD_VALUE_REGEX = re.compile(PASSWORD_VALUE_REGEX_VALUE)
""" The password value regex """

MD5_CRYPT_SALT_VALUE_REGEX = re.compile(MD5_CRYPT_SALT_VALUE_REGEX_VALUE)
""" The MD5 crypt salt value regex """


class AuthenticationLDAP(colony.System):
    """
    The authentication LDAP class.
    """

    def get_handler_name(self):
        """
        Retrieves the handler name.

        :rtype: String
        :return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Authenticates a user in the general service.

        :type request: AuthenticationRequest
        :param request: The authentication request to be handled.
        """

        # retrieves the client LDAP plugin
        client_ldap_plugin = self.plugin.client_ldap_plugin

        # retrieves the request username
        username = request.get_username()

        # retrieves the request password
        password = request.get_password()

        # retrieves the request arguments
        arguments = request.get_arguments()

        # retrieves the root dn
        root_dn = arguments[ROOT_DN_VALUE]

        # retrieves the root password
        root_password = arguments[ROOT_PASSWORD_VALUE]

        # retrieves the host
        host = arguments[HOST_VALUE]

        # retrieves the search dn
        search_dn = arguments[SEARCH_DN_VALUE]

        # in case the username or password are not defined
        if not username or not password:
            # raises an authentication error
            raise exceptions.AuthenticationError(
                "an username and a password must be provided"
            )

        # creates a new LDAP client
        ldap_client = client_ldap_plugin.create_client({})

        # opens the LDAP client
        ldap_client.open({})

        try:
            # connects the LDAP client
            ldap_client.connect(host, name=root_dn, password=root_password)

            # retrieves the user password searching in the LDAP client
            user_password = ldap_client.search(search_dn, username, password)

            # tries to match the user password
            user_password_match = PASSWORD_VALUE_REGEX.match(user_password)

            # retrieves the user password hash and value
            user_password_hash = user_password_match.group(HASH_VALUE)
            user_password_value = user_password_match.group(VALUE_VALUE)

            # converts the user password hash to lower case
            user_password_hash_lower = user_password_hash.lower()

            # in case the user password hash is of type MD5 crypt
            if user_password_hash_lower == MD5_CRYPT_VALUE:
                # processes the password using MD5 crypt
                processed_password_value = self._process_password_md5_crypt(
                    password, user_password_value
                )
            # in case the user password hash is of type SSHA
            elif user_password_hash_lower == SSHA_VALUE:
                # processes the password using SSHA
                processed_password_value = self._process_password_ssha(
                    password, user_password_value
                )
            # otherwise it must be a "normal" hash
            else:
                # processes the password using hash
                processed_password_value = self._process_password_hash(
                    password, user_password_hash_lower
                )

            # in case the processed password value and
            # the user password value are equal
            if processed_password_value == user_password_value:
                # creates the return value
                return_value = {VALID_VALUE: True, USERNAME_VALUE: username}
            # otherwise there is an error in authentication
            else:
                # raises the authentication error
                raise exceptions.AuthenticationError("password mismatch")

            # disconnects from the LDAP client
            ldap_client.disconnect()
        finally:
            # closes the LDAP client
            ldap_client.close({})

        # returns the return value
        return return_value

    def _process_password_md5_crypt(self, password, user_password_value):
        # matches the user password value against the
        # MD5 crypt salt value regex
        user_password_value_match = MD5_CRYPT_SALT_VALUE_REGEX.match(
            user_password_value
        )

        # retrieves the salt from the user password value match
        salt = user_password_value_match.group("salt")

        # encrypts the password and the salt with the
        # MD5 crypt algorithm
        processed_password_value = colony.md5_crypt(password, salt)

        # returns the processed password value
        return processed_password_value

    def _process_password_ssha(self, password, user_password_value):
        # decodes the user password value, retrieving
        # the reference value
        reference = base64.b64decode(user_password_value)

        # retrieves the salt from the reference
        salt = reference[20:]

        # calculates the password hash value
        password_hash = hashlib.sha1(password + salt)

        # retrieves the password hash digest
        password_hash_digest = password_hash.digest()

        # creates the processes password value encoding
        # the password hash digest and the salt into
        # base64
        processed_password_value = base64.b64encode(password_hash_digest + salt)

        # returns the processed password value
        return processed_password_value

    def _process_password_hash(self, password, user_password_hash_lower):
        # creates the password hash value from the user password
        # hash value in lower
        password_hash = hashlib.new(user_password_hash_lower)

        # updates the password hash with the password
        password_hash.update(password)

        # retrieves the password hash digest
        password_hash_digest = password_hash.digest()

        # creates the processed password value encoding
        # the password hash digest into base64
        processed_password_value = base64.b64encode(password_hash_digest)

        # returns the processed password value
        return processed_password_value
