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

import os
import sys
import copy
import time
import select
import threading

import bonjour

import bonjour_exceptions

WINDOWS_OS = "windows"
""" The windows os value """

MAC_OS = "mac"
""" The mac os value """

UNIX_OS = "unix"
""" The unix os value """

OTHER_OS = "other"
""" The other os value """

BROWSING_TIMEOUT = 0.5
""" The browsing timeout, used in the selection of the browse service """

ADDED_VALUE = "added"
""" The added value """

REMOVED_VALUE = "removed"
""" The removed value """

class Bonjour:
    """
    The bonjour class.
    """

    bonjour_plugin = None
    """ The bonjour plugin """

    browsing_flag = False
    """ The browsing flag """

    registration_type_domain_service_map = {}
    """ The map relating the registration type and the domain with the service """

    browsing_service_registration_type_map = {}
    """ The map relating the browsing service with the registration type """

    browsing_services = []
    """ The browsing services list """

    browsing_service_file_descriptor_map = {}
    """ The map relating the browsing service and the file descriptor """

    file_descriptor_browsing_service_reference_map = {}
    """ The map relating the file descriptor and the browsing service reference """

    events_map = {}
    """ The events map """

    values_map = {}
    """ The values map """

    def __init__(self, bonjour_plugin):
        """
        Constructor of the class

        @type bonjour_plugin: BonjourPlugin
        @param bonjour_plugin: The bonjour plugin.
        """

        self.bonjour_plugin = bonjour_plugin

        self.registration_type_domain_service_map = {}
        self.browsing_service_registration_type_map = {}
        self.browsing_services = []
        self.browsing_service_file_descriptor_map = {}
        self.file_descriptor_browsing_service_reference_map = {}
        self.events_map = {}
        self.values_map = {}

    def start_browsing_loop(self):
        """
        Starts the browsing loop, enabling browsing.
        """

        # sets the browsing flag as true
        self.browsing_flag = True

        # creates the empty registration type domain service map
        self.registration_type_domain_service_map = {}

        # creates the empty browsing service registration type map
        self.browsing_service_registration_type_map = {}

        # iterates while the browsing flag is active
        while self.browsing_flag :
            # retrieves the file descriptors
            file_descriptors = self.browsing_service_file_descriptor_map.values()

            if file_descriptors:
                # retrieves the current return value
                return_value = select.select(file_descriptors, [], [], BROWSING_TIMEOUT)

                available_file_descriptors = return_value[0]

                for available_file_descriptor in available_file_descriptors:
                    service_reference = self.file_descriptor_browsing_service_reference_map[available_file_descriptor]

                    bonjour.DNSServiceProcessResult(service_reference)
            else:
                time.sleep(BROWSING_TIMEOUT)

    def stop_browsing_loop(self):
        """
        Stops the browsing loop, disabling the current browsing.
        """

        # sets the browsing flag as true
        self.browsing_flag = False

    def create_browsing_service_file_descriptor(self, browsing_service):
        """
        Creates a file descriptor for the given browsing service.

        @type browsing_service: Tuple
        @param browsing_service: The browsing service tuple to create the file descriptor.
        @rtype: Tuple
        @return: The file descriptor tuple, containing both the file descriptor and the service reference.
        """

        # retrieves the registration type and the domain from the browsing service
        registration_type, domain = browsing_service

        # the service flags for zeroconf discovery
        flags = 0

        # the network interface index for zeroconf discovery
        interface_index = 0

        # the user data for zeroconf discovery
        user_data = None

        # creates a service reference
        service_reference = bonjour.AllocateDNSServiceRef()

        # browsers for services of the defined registration type in the defined domain
        return_value = bonjour.pyDNSServiceBrowse(service_reference, flags, interface_index, registration_type, domain, self.browse_service_bonjour_callback, user_data)

        # in case the search was not successful
        if not return_value == bonjour.kDNSServiceErr_NoError:
            raise bonjour_exceptions.BonjourBrowsingFailed("service browsing not successful")

        # retrieves the socket and loops
        file_descriptor = bonjour.DNSServiceRefSockFD(service_reference)

        return (
            file_descriptor,
            service_reference
        )

    def browse_service_bonjour_callback(self, service_reference, flags, interface_index, error_code, service_name, registration_type, domain, user_data):
        """
        The callback method for the bonjour service browsing, called upon service retrieval.

        @type service_reference: Tuple
        @param service_reference: The service reference.
        @type flags: int
        @param flags: The callback flags.
        @type interface_index: int
        @param interface_index: The callback interface index.
        @type error_code: int
        @param error_code: The callback error code.
        @type service_name: String
        @param service_name: The service name.
        @type registration_type: String
        @param registration_type: The registration type.
        @type domain: String
        @param domain: The domain.
        @type user_data: String
        @param usar_data: The user data.
        """

        # in case it's a notification of type service removed
        if flags & bonjour.kDNSServiceFlagsAdd:
            # the user data for zeroconf resolution
            user_data = (
                ADDED_VALUE,
                registration_type,
                domain
            )
        else:
            # the user data for zeroconf resolution
            user_data = (
                REMOVED_VALUE,
                registration_type,
                domain
            )

        # the service flags for zeroconf resolution
        flags = 0

        # the network interface index for zeroconf resolution
        interface_index = 0

        # creates a service reference
        service_reference = bonjour.AllocateDNSServiceRef()

        # resolves the service in zeroconf (bonjour)
        return_value = bonjour.pyDNSServiceResolve(service_reference, flags, interface_index, service_name, registration_type, domain, self.resolve_service_bonjour_callback, user_data)

        # processes the zeroconf resolution
        bonjour.DNSServiceProcessResult(service_reference)

    def resolve_service_bonjour_callback(self, service_reference, flags, interface_index, error_code, service_full_name, host, port, txt_record_length, txt_record, user_data):
        """
        The callback method for the bonjour service resolution, called upon service resolution.

        @type service_reference: String
        @param service_reference: The service reference.
        @type flags: int
        @param flags: The callback flags.
        @type interface_index: int
        @param interface_index: The callback interface index.
        @type error_code: int
        @param error_code: The callback error code.
        @type service_full_name: String
        @param service_full_name: The service full name.
        @type host: String
        @param host: The host.
        @type port: int
        @param The port.
        @type txt_record_length: int
        @param txt_record_length: The text record length.
        @type txt_record: String
        @param txt_record: The text record.
        @type user_data: String
        @param user_data: The user data.
        """

        # in case the operative system is mac
        if self.get_operative_system() == MAC_OS:
            # converts port from to the target code
            port = self.big_endian_to_little_endian(port)

        # retrieves the operation type, registration type and domain from the user data
        operation_type, registration_type, domain = user_data

        # strips the host from dots
        host_striped = host.strip(".")

        # creates the service value
        service_value = (
            service_full_name,
            host_striped,
            port
        )

        if operation_type == ADDED_VALUE:
            # adds the service value
            self.add_service_value(service_value, registration_type, domain)
        elif operation_type == REMOVED_VALUE:
            # removes the service value
            self.remove_service_value(service_value, registration_type, domain)

    def add_service_value(self, service_value, registration_type, domain):
        """
        Adds a service value to map of services for the give registration type and domain.

        @type service_value: Tuple
        @param service_value: The tuple containing the service values to be added.
        @type registration_type: String
        @param registration_type: The registration type.
        @type domain: String
        @param domain: The domain.
        """

        # creates the browsing service
        browsing_service = (
            registration_type,
            domain
        )

        # retrieves the service full name, the host and the port
        service_full_name, host, port = service_value

        # retrieves the service full name length
        service_full_name_length = len(service_full_name)

        # creates the service full name list splitting the string using the dot character
        service_full_name_list = service_full_name.split(".")

        # iterates in the range of the service full name length
        for index in range(service_full_name_length):
            # retrieves the sub list for the service full name
            service_full_name_sub_list = service_full_name_list[index:]

            # joins the sublist using the dot character as separator, creating the substring
            value = ".".join(service_full_name_sub_list)

            # in case the value is not contained in the registration type domain service map
            if not value in self.registration_type_domain_service_map:
                # creates an empty list for the value in the registration type domain service map
                self.registration_type_domain_service_map[value] = []

            # retrieves the registration type domain service map reference
            registration_type_domain_service_map_reference = self.registration_type_domain_service_map[value]

            if not service_value in registration_type_domain_service_map_reference:
                registration_type_domain_service_map_reference.append(service_value)

            if not browsing_service in self.browsing_service_registration_type_map:
                self.browsing_service_registration_type_map[browsing_service] = []

            browsing_service_services = self.browsing_service_registration_type_map[browsing_service]

            if not value in browsing_service_services:
                browsing_service_services.append(value)

    def remove_service_value(self, service_value, registration_type, domain):
        """
        Removes a service value to map of services.

        @type service_value: Tuple
        @param service_value: The tuple containing the service values to be removed.
        @type registration_type: String
        @param registration_type: The registration type.
        @type domain: String
        @param domain: The domain.
        """

        # creates the browsing service
        browsing_service = (
            registration_type,
            domain
        )

        # retrieves the service full name, the host and the port
        service_full_name, host, port = service_value

        # retrieves the service full name length
        service_full_name_length = len(service_full_name)

        # creates the service full name list splitting the string using the dot character
        service_full_name_list = service_full_name.split(".")

        # iterates in the range of the service full name length
        for index in range(service_full_name_length):
            # retrieves the sub list for the service full name
            service_full_name_sub_list = service_full_name_list[index:]

            # joins the sublist using the dot character as separator, creating the substring
            value = ".".join(service_full_name_sub_list)

            # in case the value is contained in the registration type domain service map
            if value in self.registration_type_domain_service_map:

                # retrieves the registration type domain service map reference
                registration_type_domain_service_map_reference = self.registration_type_domain_service_map[value]

                if service_value in registration_type_domain_service_map_reference:
                    registration_type_domain_service_map_reference.remove(service_value)

            if browsing_service in self.browsing_service_registration_type_map:
                browsing_service_services = self.browsing_service_registration_type_map[browsing_service]

                if value in browsing_service_services:
                    self.browsing_service_registration_type_map[browsing_service].remove(value)

    def add_service_for_browsing(self, registration_type, domain):
        """
        Adds the service with the given registration type for browsing in the given domain.

        @type registration_type: String
        @param registration_type: The registration type of browsing.
        @type domain: String
        @param domain: The domain type of browsing.
        """

        # converts the registration type
        registration_type = self.convert_type(registration_type)

        # creates the browsing service tuple
        browsing_service = (
            registration_type,
            domain
        )

        # in case the browsing service does not exists in the list of browsing services
        if not browsing_service in self.browsing_services:
            # creates the browsing service file descriptor and the browsing service reference for the given browsing service
            browsing_service_file_descriptor, browsing_service_reference = self.create_browsing_service_file_descriptor(browsing_service)

            # adds the browsing service tuple to the list of browsing services
            self.browsing_services.append(browsing_service)

            # sets the browsing service file descriptor for the browsing service
            self.browsing_service_file_descriptor_map[browsing_service] = browsing_service_file_descriptor

            # sets the browsing service reference for the browsing service file descriptor
            self.file_descriptor_browsing_service_reference_map[browsing_service_file_descriptor] = browsing_service_reference

    def remove_service_for_browsing(self, registration_type, domain):
        """
        Removes the service with the given registration type for browsing in the given domain.

        @type registration_type: String
        @param registration_type: The registration type of browsing.
        @type domain: String
        @param domain: The domain type of browsing.
        """

        # converts the registration type
        registration_type = self.convert_type(registration_type)

        # creates the browsing service tuple
        browsing_service = (
            registration_type,
            domain
        )

        # in case the browsing service exists in the list of browsing services
        if browsing_service in self.browsing_services:
            # removes the browsing service tuple to the list of browsing services
            self.browsing_services.remove(browsing_service)

            # retrieves the browsing service file descriptor for the given browsing service
            browsing_service_file_descriptor = self.browsing_service_file_descriptor_map[browsing_service]

            # deletes the browsing service file descriptor for the browsing service
            del self.browsing_service_file_descriptor_map[browsing_service]

            # deletes the browsing service reference for the browsing service file descriptor
            del self.file_descriptor_browsing_service_reference_map[browsing_service_file_descriptor]

        if browsing_service in self.browsing_service_registration_type_map:
            browsing_service_services = self.browsing_service_registration_type_map[browsing_service]

            for service_value in browsing_service_services:
                del self.registration_type_domain_service_map[service_value]

            del self.browsing_service_registration_type_map[browsing_service]

    def register_bonjour_service(self, service_name, registration_type, domain, host, port):
        """
        Registers a bonjour service to the subnetwork.

        @type service_name: String
        @param service_name: The service name.
        @type registration_type: String
        @param registration_type: The registration type.
        @type domain: String
        @param domain: The domain.
        @type host: String
        @param host: The host.
        @type port: int
        @param port: The port.
        """

        # in case the operative system is mac
        if self.get_operative_system() == MAC_OS:
            # converts port from to the target code
            port = self.big_endian_to_little_endian(port)

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

        # prints a log message about the service registration
        self.bonjour_plugin.info("Service '%s' registered in domain: '%s', host: '%s', port: '%s' for bonjour" % (service_name, domain, host, port))

    def browse_bonjour_services(self, registration_type, domain, timeout):
        """
        Browses bonjour services during the given timeout time.

        @type registration_type: String
        @param registration_type: The registration type to search.
        @type domain: String
        @param domain: The domain to search.
        @type timeout: int
        @param timeout: The timeout for the search (in seconds).
        @rtype: List
        @return: The list of browsed bonjour services.
        """

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

        # continuous loop
        while True:
            # retrieves the current time
            current_time = time.time()

            # in case the tiomeout is completed (current difference greater than timeout)
            if (current_time - initial_time) > timeout:
                # deletes the values map value (temporary) for the current guid
                del self.values_map[guid_value]

                # returns the values list
                return values_list

            # retrieves the current return value
            return_value = select.select([file_descriptor], [], [], timeout)

            # in case the return value is null
            if not return_value == ([], [], []):
                # continues processing the result
                bonjour.DNSServiceProcessResult(service_reference)

    def browse_bonjour_services_fast(self, registration_type, domain):
        """
        Browses bonjour services (the fast way).

        @type registration_type: String
        @param registration_type: The registration type to search.
        @type domain: String
        @param domain: The domain to search.
        @rtype: List
        @return: The list of browsed bonjour services.
        """

        # creates the key value using the registration type and the domain
        key_value = registration_type + "." + domain

        if key_value in self.registration_type_domain_service_map:
            return self.registration_type_domain_service_map[key_value]
        else:
            return []

    def register_bonjour_callback(self, service_reference, flags, error_code, service_name, registration_type, domain, user_data):
        """
        The callback method for the bonjour service registration, called upon registration completion.

        @type service_reference: Tuple
        @param service_reference: The service reference tuple.
        @type flags: int
        @param flags: The callback flags.
        @type error_code: int
        @param error_code: The callback error code.
        @type service_name: String
        @param service_name: The service name.
        @type registration_type: String
        @param registration_type: The registration type.
        @type domain: String
        @param domain: The domain.
        @type user_data: String
        @param user_data: The user data.
        """

        # creates the service full name
        service_full_name = service_name + registration_type

        # strips the service full name, finding for dots
        service_full_name = service_full_name.strip(".")

        # retrieves the event form the map of events
        event = self.events_map[service_full_name]

        # notifies the event, unblocks it
        event.set()

    def browse_bonjour_callback(self, service_reference, flags, interface_index, error_code, service_name, registration_type, domain, user_data):
        """
        The callback method for the bonjour service browsing, called upon service retrieval.

        @type service_reference: Tuple
        @param service_reference: The service reference.
        @type flags: int
        @param flags: The callback flags.
        @type interface_index: int
        @param interface_index: The callback interface index.
        @type error_code: int
        @param error_code: The callback error code.
        @type service_name: String
        @param service_name: The service name.
        @type registration_type: String
        @param registration_type: The registration type.
        @type domain: String
        @param domain: The domain.
        @type user_data: String
        @param usar_data: The user data.
        """

        # in case it's a notification of type service removed
        if not flags & bonjour.kDNSServiceFlagsAdd:
            return

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
        return_value = bonjour.pyDNSServiceResolve(service_reference, flags, interface_index, service_name, registration_type, domain, self.resolve_bonjour_callback, user_data)

        # processes the zeroconf resolution
        bonjour.DNSServiceProcessResult(service_reference)

    def resolve_bonjour_callback(self, service_reference, flags, interface_index, error_code, service_full_name, host, port, txt_record_length, txt_record, user_data):
        """
        The callback method for the bonjour service resolution, called upon service resolution.

        @type service_reference: String
        @param service_reference: The service reference.
        @type flags: int
        @param flags: The callback flags.
        @type interface_index: int
        @param interface_index: The callback interface index.
        @type error_code: int
        @param error_code: The callback error code.
        @type service_full_name: String
        @param service_full_name: The service full name.
        @type host: String
        @param host: The host.
        @type port: int
        @param The port.
        @type txt_record_length: int
        @param txt_record_length: The text record length.
        @type txt_record: String
        @param txt_record: The text record.
        @type user_data: String
        @param user_data: The user data.
        """

        # in case the operative system is mac
        if self.get_operative_system() == MAC_OS:
            # converts port from to the target code
            port = self.big_endian_to_little_endian(port)

        # retrieves the guid value from the user data
        guid_value = user_data

        # retrieves the list of values
        values_list = self.values_map[user_data]

        # strips the host from dots
        host_striped = host.strip(".")

        # creates the value
        value = (
            service_full_name,
            host_striped,
            port
        )

        # in case the value is not in values list
        if not value in values_list:
            # appends an element to the list of values
            values_list.append(value)

    def big_endian_to_little_endian(self, value):
        """
        Converts a big endian value to little endian.

        @type value: int
        @param value: The value to be converted.
        @rtype: int
        @return: The converted value.
        """

        # creates the final values+
        final_value = 0

        # creates the integer value list
        integer_value = []

        while value > 0:
            # retrieves the less significant byte value
            byte_value = value & 0xFF

            # adds the byte value to the integer value list
            integer_value.append(byte_value)

            # right shifts the value by one byte (8 bits)
            value = value >> 8

        # creates the is first flag
        is_first = True

        # iterates over all the values in integer value list
        for value in integer_value:
            # in case it is the first value visit
            if is_first:
                is_first = False
            else:
                # left shifts the final value by one byte (8 bits)
                final_value = final_value << 8

            # increments the final value name with the current value
            final_value += value

        # returns the final value
        return final_value

    def get_operative_system(self):
        """
        Retrieves the current operative system.

        @rtype: String
        @return: The type of the current operative system.
        """

        # retrieves the current os name
        os_name = os.name

        # retrieves the current system platform
        sys_platform = sys.platform

        if os_name == "nt" or os_name == "dos" or sys_platform == "win32":
            return WINDOWS_OS
        elif os_name == "mac" or sys_platform == "darwin":
            return MAC_OS
        elif os_name == "posix":
            return UNIX_OS

        return OTHER_OS

    def convert_type(self, type):
        """
        Converts the given type.

        @type type: String
        @param type: The type to be converted.
        @rtype: String
        @return: The converted type.
        """

        # creates a copy of type
        value = copy.copy(type)

        # in case the last character in the string is no a dot
        if not type[-1] == ".":
            # adds the dot to the end of the string
            value += "."

        # returns the value
        return value
