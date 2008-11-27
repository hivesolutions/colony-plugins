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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import select
import threading
import time

import bonjour

import bonjour_exceptions

class Bonjour:

    bonjour_plugin = None

    events_map = {}
    
    values_map = {}

    def __init__(self, bonjour_plugin):
        self.bonjour_plugin = bonjour_plugin

        self.events_map = {}
        self.values_map = {}

    def register_bonjour_service(self, service_name, registration_type, domain, host, port):
        # the service flags for zeroconf registration
        flags = 0

        # the network interface index for zeroconf registration
        interface_index = 0

        # the text record length for zeroconf registration
        txt_record_length = 0

        # the text record for zeroconf registration
        txt_record = ""

        # the user data for zeroconf registration
        user_data = None

        # creates the service full name
        service_full_name = service_name + registration_type

        # strips the service full name, finding for dots
        service_full_name = service_full_name.strip(".")

        # creates the waiting event to wait for the bonjour service registration
        event = threading.Event()

        # adds the event to the map of events
        self.events_map[service_full_name] = event

        # creates a service reference
        service_reference = bonjour.AllocateDNSServiceRef()

        # registers the service in zeroconf (bonjour)
        return_value = bonjour.pyDNSServiceRegister(service_reference, flags, interface_index, service_name, registration_type, domain, host, port, txt_record_length, txt_record, self.register_bonjour_callback, user_data)

        # in case the registration is not successful
        if not return_value == bonjour.kDNSServiceErr_NoError:
            raise bonjour_exceptions.BonjourServiceNotRegistrable("service registration not successful")

        # retrieves the socket and loops
        file_descriptor = bonjour.DNSServiceRefSockFD(service_reference)

        # iterates while the event is not set
        while not event.isSet():
            select.select([file_descriptor], [], [])
            bonjour.DNSServiceProcessResult(service_reference)

    def browse_bonjour_services(self, registration_type, domain, timeout):
        # retrieves the guid plugin
        guid_plugin = self.bonjour_plugin.guid_plugin

        # the guid value for the search
        guid_value = guid_plugin.generate_guid()

        # the service flags for zeroconf discovery
        flags = 0

        # the network interface index for zeroconf discovery
        interface_index = 0

        # the user data for zeroconf discovery
        user_data = guid_value

        # creates the a list of values to return
        values_list = []

        # adds the values list to the map of values
        self.values_map[guid_value] = values_list

        # creates a service reference
        service_reference = bonjour.AllocateDNSServiceRef()

        # browsers for services of the defined registration type in the defined domain
        return_value = bonjour.pyDNSServiceBrowse(service_reference, flags, interface_index, registration_type, domain, self.browse_bonjour_callback, user_data) 

        # in case the search was not successful
        if not return_value == bonjour.kDNSServiceErr_NoError:
            raise bonjour_exceptions.BonjourBrowsingFailed("service browsing not successful")

        # retrieves the socket and loops
        file_descriptor = bonjour.DNSServiceRefSockFD(service_reference)

        # retrieves the current time (start time)
        initial_time = time.time()

        while True:
            current_time = time.time()

            if (current_time - initial_time) > timeout:
                del self.values_map[guid_value]
                return values_list

            return_value = select.select([file_descriptor], [], [], timeout)
            if not return_value == ([], [], []):
                bonjour.DNSServiceProcessResult(service_reference)

    def register_bonjour_callback(self, service_reference, flags, error_code, service_name, registration_type, domain, user_data):
        # creates the service full name
        service_full_name = service_name + registration_type

        # strips the service full name, finding for dots
        service_full_name = service_full_name.strip(".")

        # retrieves the event form the map of events
        event = self.events_map[service_full_name]

        # notifies the event, unblocks it
        event.set()

    def browse_bonjour_callback(self, service_reference, flags, interface_index, error_code, service_name, registration_type, domain, user_data):
        # retrieves the guid value from the user data
        guid_value = user_data

        # the service flags for zeroconf resolution
        flags = 0

        # the network interface index for zeroconf resolution
        interface_index = 0

        # the user data for zeroconf resolution
        user_data = guid_value

        # creates a service reference
        service_reference = bonjour.AllocateDNSServiceRef()

        # resolves the service in zeroconf (bonjour)
        return_value = bonjour.pyDNSServiceResolve(service_reference, flags, interface_index, service_name, registration_type, domain, self.resolve_bonjour_callback, user_data);

        bonjour.DNSServiceProcessResult(service_reference)

    def resolve_bonjour_callback(self, service_reference, flags, interface_index, error_code, service_full_name, host, port, txt_record_length, txt_record, user_data):
        # retrieves the guid value from the user data
        guid_value = user_data

        # retrieves the list of values
        values_list = self.values_map[user_data]

        # creates the value
        value = (service_full_name, host, port)

        # in case the value is not in values list
        if not value in values_list:
            # appends an element to the list of values
            values_list.append(value)
