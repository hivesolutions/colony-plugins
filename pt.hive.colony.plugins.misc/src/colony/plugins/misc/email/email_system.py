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

import base64
import smtplib

DEFAULT_SMTP_SERVER = "smtp_server"
""" The default smtp server """

HEADER_TEMPLATE = "From: (%s) %s\n\
To: (%s) %s\n\
Subject: %s\n"
""" The header template to be used in email messages """

class Email:
    """
    The email class.
    """

    email_plugin = None
    """ The email plugin """

    def __init__(self, email_plugin):
        """
        Constructor of the class.

        @type email_plugin: EmailPlugin
        @param email_plugin: The email plugin.
        """

        self.email_plugin = email_plugin

    def send_email(self, email_sender = "none", email_receiver = "none", name_sender = "none", name_receiver = "none", subject = "none", contents = "none", smtp_server = "none", smtp_login = "none", smtp_password = "none"):
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
        @type smtp_server: String
        @param smtp_server: The smtp server to be used when sending the email.
        @type smtp_login: String
        @param smtp_login: The login to be used in the server authentication.
        @type smtp_password: String
        @param smtp_password: The password to be used in the server authentication.
        """

        # retrieves the service configuration
        service_configuration = self.email_plugin.get_configuration_property("server_configuration").get_data()

        # in case the smtp server is not defined
        if not smtp_server:
            # retrieves the smtp server from configuration
            smtp_server = service_configuration.get("smtp_server", DEFAULT_SMTP_SERVER)

        # establishes the connection with the smtp server
        server = smtplib.SMTP(smtp_server)

        # in case there is a login and a password defined
        if not smtp_login == "none" and not smtp_password == "none":
            # creates the passphrase using the given login and the password
            passphrase = "\0%s\0%s" % (smtp_login, smtp_password)

            # encodes the passphrase into base 64
            base64_passphrase = base64.b64encode(passphrase)

            # sets the authentication method
            server.docmd("AUTH PLAIN")

            # sets the passphrase
            server.docmd(base64_passphrase)

        # creates the header from the header template
        header = HEADER_TEMPLATE % (name_sender, email_sender, name_receiver, email_receiver, subject)

        # creates the final contents
        final_contents = header + contents

        # sends the mail
        server.sendmail(email_sender, email_receiver, final_contents)

        # quits the server
        server.quit()
