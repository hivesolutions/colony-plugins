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

LDAP_REQUEST_TYPE_MAP = {"bind" : 0x60, "unbind" : 0x62,
                         "search" : 0x63, "modify" : 0x66,
                         "add" : 0x68, "delete" : 0x6a,
                         "modify_dn" : 0x00, "compare" : 0x00,
                         "abandon" : 0x00, "extended" : 0x00}

LDAP_RESPONSE_TYPE_MAP = {"bind" : 0x61, "search_result_enttry" : 0x64,
                          "search_result_reference" : 0x73, "search_result_done" : 0x65,
                          "modify" : 0x67, "add" : 0x69, "delete" : 0x6b}

import main_client_ldap_exceptions

class MainClientLdap:
    """
    The main client ldap class.
    """

    main_client_ldap_plugin = None
    """ The main client ldap plugin """

    def __init__(self, main_service_ldap_plugin):
        """
        Constructor of the class.

        @type main_service_ldap_plugin: MainClientLdap
        @param main_service_ldap_plugin: The main client ldap plugin.
        """

        self.main_service_ldap_plugin = main_service_ldap_plugin

    def create_client(self, parameters):
        pass

    def create_request(self, parameters):
        pass

class LdapClient:
    pass

class LdapRequest:
    """
    The ldap request class.
    """

    pass
