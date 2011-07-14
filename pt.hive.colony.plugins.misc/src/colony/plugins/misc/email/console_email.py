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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 12939 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-02-01 17:54:16 +0000 (Tue, 01 Feb 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "email"
""" The console extension name """

TEST_SUBJECT = "Colony Framework [getcolony.com] ping message"
""" The test subject contents """

TEST_MESSAGE = "You've just been pinged by Colony Framework [getcolony.com]"
""" The test message contents """

#TEST_EMAIL_SENDER = "no-reply@getcolony.com"
TEST_EMAIL_SENDER = "joamag@hive.pt"
""" The test email sender """

class ConsoleEmail:
    """
    The console email class.
    """

    email_plugin = None
    """ The email plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, email_plugin):
        """
        Constructor of the class.

        @type email_plugin: DownloaderPlugin
        @param email_plugin: The email plugin.
        """

        self.email_plugin = email_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_send_email(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the send email command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        pass

    def process_send_test_email(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the send test email command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the email instance
        email = self.email_plugin.email

        # retrieves the file path from the arguments
        destiny_address = arguments_map["destiny_address"]

        # sends the test email to the destiny address
        email.send_email(TEST_EMAIL_SENDER, destiny_address, None, None, TEST_SUBJECT, TEST_MESSAGE)

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "send_email" : {
                "handler" : self.process_send_email,
                "description" : "sends an email with the given contains to the defined destiny address",
                "arguments" : [
                    {
                        "name" : "destiny_address",
                        "description" : "the address where to send the email to",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            },
            "send_test_email" : {
                "handler" : self.process_send_test_email,
                "description" : "sends a test email to the defined destiny address",
                "arguments" : [
                    {
                        "name" : "destiny_address",
                        "description" : "the address where to send the email to",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
