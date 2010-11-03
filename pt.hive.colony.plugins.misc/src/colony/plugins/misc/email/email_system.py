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

import sys
import datetime

import colony.libs.map_util

DEFAULT_SMTP_HOSTNAME = "example.com"
""" The default smtp hostname """

DEFAULT_SMTP_PORT = 25
""" The default smtp port """

USERNAME_VALUE = "username"
""" The username value """

PASSWORD_VALUE = "password"
""" The password value """

TLS_VALUE = "tls"
""" The tls value """

FROM_VALUE = "From"
""" The from value """

TO_VALUE = "To"
""" The to value """

SUBJECT_VALUE = "Subject"
""" The subject value """

DATE_VALUE = "Date"
""" The date value """

USER_AGENT_VALUE = "User-Agent"
""" The user agent value """

USER_AGENT_NAME = "Hive-Colony-Email-Client"
""" The user agent name """

USER_AGENT_VERSION = "1.0.0"
""" The user agent version """

ENVIRONMENT_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
""" The environment version """

USER_AGENT_IDENTIFIER = USER_AGENT_NAME + "/" + USER_AGENT_VERSION + " (python/" + sys.platform + "/" + ENVIRONMENT_VERSION + ")"
""" The user agent identifier """

DATE_TIME_FORMAT = "%a, %d %b %Y %H:%M:%S +0000 (UTC)"
""" The format for the displayed date times """

class Email:
    """
    The email class.
    """

    email_plugin = None
    """ The email plugin """

    email_configuration = {}
    """ The email configuration """

    def __init__(self, email_plugin):
        """
        Constructor of the class.

        @type email_plugin: EmailPlugin
        @param email_plugin: The email plugin.
        """

        self.email_plugin = email_plugin

        self.email_configuration = {}

    def set_configuration_property(self, configuration_property):
        # retrieves the configuration
        configuration = configuration_property.get_data()

        # cleans the email configuration
        colony.libs.map_util.map_clean(self.email_configuration)

        # copies the configuration to the email configuration
        colony.libs.map_util.map_copy(configuration, self.email_configuration)

    def unset_configuration_property(self):
        # cleans the email configuration
        colony.libs.map_util.map_clean(self.email_configuration)

    def send_email(self, email_sender = None, email_receiver = None, name_sender = None, name_receiver = None, subject = None, contents = None):
        """
        Sends an email for the given configuration.

        @type email_sender: String
        @param email_sender: The sender of the email.
        @type email_receiver: String
        @param email_receiver: The receiver of the email.
        @type name_sender: String
        @param name_sender: The name of the sender.
        @type name_receiver: String
        @param name_receiver: The name of the receiver.
        @type subject: String
        @param subject: The subject of the email.
        @type contents: String
        @param contents: The contents of the email.
        """

        # retrieves the main client smtp plugin
        main_client_smtp_plugin = self.email_plugin.main_client_smtp_plugin

        # retrieves the format mime plugin
        format_mime_plugin = self.email_plugin.format_mime_plugin

        # creates a new smtp client, using the main client smtp plugin
        smtp_client = main_client_smtp_plugin.create_client({})

        # opens the smtp client
        smtp_client.open({})

        # tries to retrieve the smtp hostnmae value
        smtp_hostname = self.email_configuration.get("hostname", DEFAULT_SMTP_HOSTNAME)

        # tries to retrieve the smtp port value
        smtp_port = self.email_configuration.get("port", DEFAULT_SMTP_PORT)

        # tries to retrieve the smtp username value
        smtp_username = self.email_configuration.get("username", None)

        # tries to retrieve the smtp password value
        smtp_password = self.email_configuration.get("password", None)

        # tries to retrieve the tls value
        smtp_tls = self.email_configuration.get("tls", False)

        # creates the parameters map
        parameters = {}

        # sets the authentication parameters
        parameters[USERNAME_VALUE] = smtp_username
        parameters[PASSWORD_VALUE] = smtp_password
        parameters[TLS_VALUE] = smtp_tls

        # creates the mime message
        mime_message = format_mime_plugin.create_message({})

        # in case the name of the sender is defined
        if name_sender:
            # creates the sender line with the name and email
            sender_line = name_sender + "<" + email_sender + ">"
        # otherwise
        else:
            # creates the sender line with the email
            sender_line = "<" + email_sender + ">"

        # in case the name of the receiver is defined
        if name_receiver:
            # creates the receiver line with the name and email
            receiver_line = name_receiver + "<" + email_receiver + ">"
        else:
            # creates the receiver line with the email
            receiver_line = "<" + email_receiver + ">"

        # retrieves the current date time, and formats
        # it according to the "standard" format
        current_date_time = datetime.datetime.utcnow()
        current_date_time_formated = current_date_time.strftime(DATE_TIME_FORMAT)

        # sets the basic mime message headers
        mime_message.set_header(FROM_VALUE, sender_line)
        mime_message.set_header(TO_VALUE, receiver_line)
        mime_message.set_header(SUBJECT_VALUE, subject)
        mime_message.set_header(DATE_VALUE, current_date_time_formated)
        mime_message.set_header(USER_AGENT_VALUE, USER_AGENT_IDENTIFIER)

        # writes the contents to the mime message
        mime_message.write(contents)

        # retrieves the mime message value
        mime_message_value = mime_message.get_value()

        # send the email using the defined values
        smtp_client.send_mail(smtp_hostname, smtp_port, email_sender, [email_receiver], mime_message_value, parameters)

        # closes the smtp client
        smtp_client.close({})
