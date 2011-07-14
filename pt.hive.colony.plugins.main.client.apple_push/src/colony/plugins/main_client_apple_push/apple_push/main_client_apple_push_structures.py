#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import struct
import binascii

DEVICE_TOKEN_LENGTH = 32
""" The device token length """

SIMPLE_NOTIFICATION_FORMAT_COMMAND = 0
""" The simple notification format command """

ENHANCED_NOTIFICATION_FORMAT_COMMAND = 1
""" The enhanced notification format command """

SIMPLE_NOTIFICATION_FORMAT_TEMPLATE = "!BH32sH%ds"
""" The simple notification format template """

ENHANCED_NOTIFICATION_FORMAT_TEMPLATE = "!BiiH32sH%ds"
""" The enhanced notification format template """

ERROR_RESPONSE_FORMAT_TEMPLATE = "!BBi"
""" The error response format template """

FEEDBACK_RESPONSE_FORMAT_TEMPLATE = "!IH32s"
""" The feedback response format template """

class NotificationMessage:
    """
    The notification message class.
    """

    command = None
    """ The command """

    device_token = None
    """ The device token """

    payload = None
    """ The payload """

    def __init__(self, command, device_token, payload):
        """
        Constructor of the class.

        @type command: int
        @param command: The command.
        @type device_token: String
        @param device_token: The device token.
        @type payload: String
        @param payload: The payload.
        """

        self.command = command
        self.device_token = device_token
        self.payload = payload

class SimpleNotificationMessage(NotificationMessage):
    """
    The simple notification message class.
    """

    def __init__(self, device_token, payload):
        """
        Constructor of the class.

        @type device_token: String
        @param device_token: The device token.
        @type payload: String
        @param payload: The payload.
        """

        NotificationMessage.__init__(self, SIMPLE_NOTIFICATION_FORMAT_COMMAND, device_token, payload)

    def get_value(self):
        """
        Retrieves the value representing the structure
        in the target protocol.

        @rtype: String
        @return: The value representing the structure in
        the target protocol.
        """

        # retrieves the payload length
        payload_length = len(self.payload)

        # converts the device token to hexadecimal value
        device_token = binascii.unhexlify(self.device_token)

        # creates the format for the message using the payload simple format template
        simple_notification_format = SIMPLE_NOTIFICATION_FORMAT_TEMPLATE % payload_length

        # creates the simple format message
        simple_format_message = struct.pack(simple_notification_format, self.command, DEVICE_TOKEN_LENGTH, device_token, payload_length, self.payload)

        # returns the simple format message
        return simple_format_message

class EnhancedNotificationMessage(NotificationMessage):
    """
    The enhanced notification message class.
    """

    identifier = None
    """ The identifier """

    expiry = None
    """ The expiry """

    def __init__(self, device_token, payload, identifier, expiry):
        """
        Constructor of the class.

        @type device_token: String
        @param device_token: The device token.
        @type payload: String
        @param payload: The payload.
        @type identifier: int
        @param identifier: The identifier.
        @type expiry: int
        @param expiry: The expirty.
        """

        NotificationMessage.__init__(self, ENHANCED_NOTIFICATION_FORMAT_COMMAND, device_token, payload)
        self.identifier = identifier
        self.expiry = expiry

    def get_value(self):
        """
        Retrieves the value representing the structure
        in the target protocol.

        @rtype: String
        @return: The value representing the structure in
        the target protocol.
        """

        # retrieves the payload length
        payload_length = len(self.payload)

        # converts the device token to hexadecimal value
        device_token = binascii.unhexlify(self.device_token)

        # creates the format for the message using the payload enhanced format template
        enhanced_notification_format = ENHANCED_NOTIFICATION_FORMAT_TEMPLATE % payload_length

        # creates the enhanced format message
        enhanced_format_message = struct.pack(enhanced_notification_format, self.command, self.identifier, self.expiry, DEVICE_TOKEN_LENGTH, device_token, payload_length, self.payload)

        # returns the enhanced format message
        return enhanced_format_message

class NotificationResponse:
    """
    The notification response class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

class ErrorNotificationResponse(NotificationResponse):
    """
    The error notification response class.
    """

    command = None
    """ The command """

    status = None
    """ The status """

    identifier = None
    """ The identifier """

    def __init__(self):
        """
        Constructor of the class.
        """

        NotificationResponse.__init__(self)

    def process_value(self, value):
        """
        Processes the value in the target protocol, converting it
        and populating the current structure.

        @type value: String
        @param value: The value in the target protocol to be converted.
        """

        # creates the error response format
        error_response_format = ERROR_RESPONSE_FORMAT_TEMPLATE

        # retrieves the error data
        command, status, identifier = struct.unpack(error_response_format, value)

        # sets the current values
        self.command = command
        self.status = status
        self.identifier = identifier

        # returns the self value
        return self

class FeedbackNotificationResponse(NotificationResponse):
    """
    The feedback notification response class.
    """

    feedback_tuples = []
    """ The feedback tuples """

    def __init__(self):
        """
        Constructor of the class.
        """

        NotificationResponse.__init__(self)

        self.feedback_tuples = []

    def process_value(self, value):
        """
        Processes the value in the target protocol, converting it
        and populating the current structure.

        @type value: String
        @param value: The value in the target protocol to be converted.
        """

        # creates the feedback response format
        feedback_response_format = FEEDBACK_RESPONSE_FORMAT_TEMPLATE

        # retrieves the value length
        value_length = len(value)

        # sets the initial start and end indexes
        start_index = 0
        end_index = 38

        # iterates continuously
        while True:
            # in case the end index is bigger
            # than the value length
            if end_index > value_length:
                # breaks the cycle
                break

            # retrieves the tuple value from the
            tuple_value = value[start_index:end_index]

            # retrieves the feedback data
            timestamp, _token_length, device_token = struct.unpack(feedback_response_format, tuple_value)

            # converts the device token into string value
            device_token = binascii.hexlify(device_token)

            # sets the current value in the feedback tuple
            feedback_tuple = (
                timestamp,
                device_token
            )

            # adds the feedback tuple to the feedback tuples
            self.feedback_tuples.append(feedback_tuple)

        # returns the self value
        return self
