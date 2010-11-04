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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "email"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### EMAIL HELP ###\n\
send_email <destiny-address>      - sends an email with the given contains to the defined destiny address\n\
send_test_email <destiny-address> - sends a test email to the defined destiny address"
""" The help text """

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

    commands = ["send_email", "send_test_email"]
    """ The commands list """

    def __init__(self, email_plugin):
        """
        Constructor of the class.

        @type email_plugin: EmailPlugin
        @param email_plugin: The email plugin.
        """

        self.email_plugin = email_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_send_email(self, args, output_method):
        pass

    def process_send_test_email(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the destiny address
        destiny_address = args[0]

        # sends the test email to the destiny address
        self.email_plugin.email.send_email(TEST_EMAIL_SENDER, destiny_address, None, None, TEST_SUBJECT, TEST_MESSAGE)
