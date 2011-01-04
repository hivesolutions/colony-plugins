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

import base64

class EncryptionSsl:
    """
    The encryption ssl class.
    """

    encryption_ssl_plugin = None
    """ The encryption ssl plugin """

    def __init__(self, encryption_ssl_plugin):
        """
        Constructor of the class.

        @type encryption_ras_plugin: EncryptionSslPlugin
        @param encryption_ras_plugin: The encryption ssl plugin.
        """

        self.encryption_ssl_plugin = encryption_ssl_plugin

    def create_structure(self, parameters):
        # retrieves the keys (if available)
        keys = parameters.get("keys", None)

        # creates the ssl structure
        ssl_structure = SslStructure(keys)

        # returns the ssl structure
        return ssl_structure

class SslStructure:
    """
    Class representing the ssl,
    cryptographic protocol structure.
    """

    encryption_rsa_plugin = None
    """ The encryption rsa plugin """

    encryption_pkcs_1_plugin = None
    """ The encryption pkcs 1 plugin """

    def __init__(self, encryption_rsa_plugin, encryption_pkcs_1_plugin):
        """
        Constructor of the class.

        @type encryption_rsa_plugin: EncryptionRsaPlugin
        @param encryption_rsa_plugin: The encryption rsa plugin.
        @type encryption_pkcs_1_plugin: EncryptionPkcs1Plugin
        @param encryption_pkcs_1_plugin: The encryption pkkc 1 plugin.
        """

        self.encryption_rsa_plugin = encryption_rsa_plugin
        self.encryption_pkcs_1_plugin = encryption_pkcs_1_plugin

    def verify_test_base_64(self, public_key_path, verification_string_value_base_64, base_string_value):
        # decodes the verification string value base 64
        verification_string_value = base64.b64decode(verification_string_value_base_64)

        # verifies the verification string value against the base string value,
        # and returns the return value
        return_value = self.verify_test(public_key_path, verification_string_value, base_string_value)

        # returns the return value
        return return_value

    def verify_test(self, public_key_path, verification_string_value, base_string_value):
        # creates the rsa structure
        rsa_structure = self.encryption_rsa_plugin.create_structure({})

        # creates the pkcs 1 structure
        pkcs_1_structure = self.encryption_pkcs_1_plugin.create_structure({})

        # loads the public key, retrieving the keys map
        keys = pkcs_1_structure.load_read_public_key_pem(public_key_path)

        # sets the keys in the rsa structure
        rsa_structure.set_keys(keys)

        # verifies the verification string value (using the public key)
        # and retrieves the signature verified
        signature_verified = rsa_structure.verify(verification_string_value)

        # verifies the and tests the signature, retrieving the return value
        return_value = pkcs_1_structure.verify_test(signature_verified, base_string_value)

        # returns the return value
        return return_value
