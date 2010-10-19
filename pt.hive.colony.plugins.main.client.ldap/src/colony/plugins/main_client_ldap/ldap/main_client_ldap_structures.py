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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

TYPE_VALUE = "type"
""" The type value """

VALUE_VALUE = "value"
""" The value value """

EXTRA_TYPE_VALUE = "extra_type"
""" The extra type value """

BIND_VALUE = "bind"
""" The bind value """

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

LDAP_REQUEST_TYPE_MAP = {BIND_VALUE : 0x00, "unbind" : 0x02,
                         "search" : 0x63, "modify" : 0x66,
                         "add" : 0x68, "delete" : 0x6a,
                         "modify_dn" : 0x00, "compare" : 0x00,
                         "abandon" : 0x00, "extended" : 0x00}
""" The map of ldap request types """

LDAP_RESPONSE_TYPE_MAP = {"bind" : 0x61, "search_result_enttry" : 0x64,
                          "search_result_reference" : 0x73, "search_result_done" : 0x65,
                          "modify" : 0x67, "add" : 0x69, "delete" : 0x6b}
""" The map of ldap response types """

class ProtocolOperation:
    pass

class BindOperation(ProtocolOperation):

    version = None

    name = None

    authentication = None

    def __init__(self, version, name, authentication):
        self.version = version
        self.name = name
        self.authentication = authentication

    def get_value(self):
        # retrieves the bind request type
        bind_request_type = APPLICATION_TYPE + LDAP_REQUEST_TYPE_MAP[BIND_VALUE]

        # creates the version integer value
        version = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE : self.version}

        # creates the name octet string value
        name = {TYPE_VALUE: OCTET_STRING_TYPE, VALUE_VALUE : self.name}

        # retrieves the authentication value
        authentication = self.authentication.get_value()

        # creates the protocol operation contents (list)
        protocol_operation_contents = [version, name, authentication]

        # creates the bind operation sequence value
        bind_operation = {TYPE_VALUE: SEQUENCE_TYPE, VALUE_VALUE : protocol_operation_contents,
                          EXTRA_TYPE_VALUE : bind_request_type}

        # returns the bind operation (value)
        return bind_operation

class Authentication:
    pass

class SimpleAuthentication(Authentication):

    value = None

    def __init__(self, value):
        self.value = value

    def get_value(self):
        # creates the authentication octet string value
        authentication = {TYPE_VALUE: OCTET_STRING_TYPE, VALUE_VALUE : self.value,
                          EXTRA_TYPE_VALUE : 0x80}

        # returns the authentication (value)
        return authentication
