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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys
import datetime

DEFAULT_SMTP_HOSTNAME = "localhost"
""" The default smtp hostname """

DEFAULT_SMTP_PORT = 25
""" The default smtp port """

DEFAULT_SENDER_NAME = "Colony Integration"
""" The default sender name """

DEFAULT_SENDER_EMAIL = "integration@getcolony.com"
""" The default sender email """

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

USER_AGENT_IDENTIFIER = USER_AGENT_NAME + "/" + USER_AGENT_VERSION + " (Python/" + sys.platform + "/" + ENVIRONMENT_VERSION + ")"
""" The user agent identifier """

DATE_TIME_FORMAT = "%a, %d %b %Y %H:%M:%S +0000 (UTC)"
""" The format for the displayed date times """

class EmailBuildAutomationExtension:
    """
    The email build automation extension class.
    """

    email_build_automation_extension_plugin = None
    """ The email build automation extension plugin """

    def __init__(self, email_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type email_build_automation_extension_plugin: EmailBuildAutomationExtensionPlugin
        @param email_build_automation_extension_plugin: The email build automation extension plugin.
        """

        self.email_build_automation_extension_plugin = email_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # prints an info message
        logger.info("Running email build automation plugin")

        # retrieves the main client smtp plugin
        main_client_smtp_plugin = self.email_build_automation_extension_plugin.main_client_smtp_plugin

        # retrieves the format mime plugin
        format_mime_plugin = self.email_build_automation_extension_plugin.format_mime_plugin

        # retrieves the build automation structure associated plugin
        build_automation_structure_associated_plugin = build_automation_structure.associated_plugin

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # creates a new smtp client, using the main client smtp plugin
        smtp_client = main_client_smtp_plugin.create_client({})

        # opens the smtp client
        smtp_client.open({})

        # retrieves the sender parameters from the parameters map
        sender_name = parameters.get("sender_name", DEFAULT_SENDER_NAME)
        sender_email = parameters.get("sender_email", DEFAULT_SENDER_EMAIL)

        # retrieves the smtp parameters from the parameters map
        smtp_hostname = parameters.get("smtp_hostname", DEFAULT_SMTP_HOSTNAME)
        smtp_port = parameters.get("smtp_port", DEFAULT_SMTP_PORT)
        smtp_username = parameters.get("smtp_username", None)
        smtp_password = parameters.get("smtp_password", None)
        smtp_tls = parameters.get("smtp_tls", False)

        # creates the smtp parameters map
        smtp_parameters = {}

        # sets the authentication parameters
        smtp_parameters[USERNAME_VALUE] = smtp_username
        smtp_parameters[PASSWORD_VALUE] = smtp_password
        smtp_parameters[TLS_VALUE] = smtp_tls

        # creates the mime message
        mime_message = format_mime_plugin.create_message({})

        # creates the sender line
        sender_line = sender_name + " " + "<" + sender_email + ">"

        success_receivers = (("Jo�o Magalh�es", "joamag@hive.pt"),)
        failure_receivers = (("Jo�o Magalh�es", "joamag@hive.pt"), ("Tiago Silva", "tsilva@hive.pt"), ("Luis Martinho", "lmartinho@hive.pt"))

        # retrieves the build automation plugin id
        build_automation_plugin_id = build_automation_structure_associated_plugin.id

        # retrieves the build automation version (revision)
        build_automation_version = build_automation_structure_runtime.properties.get("version", -1)

        # writes the initial subject line
        subject = "[b%i] %s " % (build_automation_version, build_automation_plugin_id)

        # in case the build automation was successful
        if build_automation_structure_runtime.success:
            # adds the successful part to the subject
            subject += "was SUCCESSFUL"

            # sets the receivers as the success receivers
            receivers = success_receivers
        # otherwise
        else:
            # adds the failed part to the subject
            subject += "as FAILED"

            # sets the receivers as the failure receivers
            receivers = failure_receivers

        # creates the receiver line with the email
        receiver_line = ""

        # creates the list to hold the receiver emails
        receiver_emails = []

        # sets the is first flag
        is_first = True

        # iterates over all the receivers
        # to creates the receiver line
        for receiver in receivers:
            # in case it's the first iteration
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise
            else:
                # adds the separator to the receiver line
                receiver_line += ", "

            # retrieves the receiver name and email
            receiver_name, receiver_email = receiver

            # adds the receiver name and email to the receiver line
            receiver_line += receiver_name + " " + "<" + receiver_email + ">"

            # adds the receiver email to the list of receiver emails
            receiver_emails.append(receiver_email)

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

        # retrieves the logging buffer
        logging_buffer = build_automation_structure_runtime.logging_buffer

        # retrieves the logging contents from the logging buffer
        logging_contents = logging_buffer.get_value()

        # writes the contents to the mime message
        mime_message.write(logging_contents)

        # retrieves the mime message value
        mime_message_value = mime_message.get_value()

        # send the email using the defined values
        smtp_client.send_mail(smtp_hostname, smtp_port, sender_email, receiver_emails, mime_message_value, parameters)

        # closes the smtp client
        smtp_client.close({})

        # returns true (success)
        return True
