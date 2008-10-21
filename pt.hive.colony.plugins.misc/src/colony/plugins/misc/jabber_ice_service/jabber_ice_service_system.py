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

__revision__ = "$LastChangedRevision: 2096 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:02:08 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import jabber_ice_service_ice_server

class JabberIceService:

    jabber_ice_service_plugin = None

    def __init__(self, jabber_ice_service_plugin):
        """
        Constructor of the class
        
        @type jabber_ice_service_plugin: Plugin
        @param jabber_ice_service_plugin: The jabber ice service plugin
        """

        self.jabber_ice_service_plugin = jabber_ice_service_plugin

    def get_ice_service_descriptor(self, ice_service_descriptor_class):
        ice_service_descriptor = ice_service_descriptor_class()
        ice_service_descriptor.name = "jabber"
        ice_service_descriptor.description = "just one more jabber service"
        ice_service_descriptor.server_file_path = jabber_ice_service_ice_server.get_server_path()

        jabber_access_object = {"name" : "jabber_op_access",
                                "category" : None,
                                "type" : "::pt::hive::prototype::converter::plugins::misc::jabbericeservice::JabberOp"}

        ice_service_descriptor.access_objects_list = [jabber_access_object]

        return ice_service_descriptor
