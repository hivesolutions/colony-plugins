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

HEADER_TEMPLATE = "From: (%s) %s\n\
To: (%s) %s\n\
Subject: %s\n"

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

    def send_email(self, email_sender = "none", email_receiver = "none", name_sender = "none", name_receiver = "none", subject = "none", containts = "none", smtp_server = "none", smtp_login = "none", smtp_password = "none"):
        # establishes the connection with the smtp server
        server = smtplib.SMTP("hive.pt")

        # in case there is a login and a password defined
        if not smtp_login == "none" and not smtp_password == "none":
            # creates the passphrase using the given login and the password
            passphrase = "\0%s\0%s" % (smtp_login, smtp_password)

            # encodes the passphrase into base 64
            base64_passphrase = base64.b64encode(passphrase)

            server.docmd("AUTH PLAIN")
            server.docmd(base64_passphrase)

        header = HEADER_TEMPLATE % (name_sender, email_sender, name_receiver, email_receiver, subject)

        final_containts = header + containts

        server.sendmail(email_sender, email_receiver, final_containts)
        server.quit()
