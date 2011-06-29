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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import main_service_smtp_relay_message_handler_exceptions

HANDLER_NAME = "relay"
""" The handler name """

MX_VALUE = "MX"
""" The mx value """

IN_VALUE = "IN"
""" The in value """

SMTP_PORT = 25
""" The smtp port """

class MainServiceSmtpRelayMessageHandler:
    """
    The main service smtp relay message handler class.
    """

    main_service_smtp_relay_message_handler_plugin = None
    """ The main service smtp relay message handler plugin """

    def __init__(self, main_service_smtp_relay_message_handler_plugin):
        """
        Constructor of the class.

        @type main_service_smtp_relay_message_handler_plugin: MainServiceSmtpRelayMessageHandlerPlugin
        @param main_service_smtp_relay_message_handler_plugin: The main service smtp relay message handler plugin.
        """

        self.main_service_smtp_relay_message_handler_plugin = main_service_smtp_relay_message_handler_plugin

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_message(self, message, session, arguments):
        """
        Handles the given smtp message.

        @type message: SmtpMessage
        @param message: The smtp message to handled.
        @type session: SmtpSession
        @param session: The smtp session to be used.
        @type arguments: Dictionary
        @param arguments: The arguments to the message handling.
        """

        # retrieves the main client smtp plugin
        main_client_smtp_plugin = self.main_service_smtp_relay_message_handler_plugin.main_client_smtp_plugin

        # retrieves the main client dns plugin
        main_client_dns_plugin = self.main_service_smtp_relay_message_handler_plugin.main_client_dns_plugin

        # retrieves the format mime plugin
        format_mime_plugin = self.main_service_smtp_relay_message_handler_plugin.format_mime_plugin

        # creates a new smtp client, using the main client smtp plugin
        smtp_client = main_client_smtp_plugin.create_client({})

        # creates a new dns client, using the main client dns plugin
        dns_client = main_client_dns_plugin.create_client({})

        # retrieves the message contents
        message_contents = message.get_contents()

        # retrieves the message sender
        message_sender = message.get_sender()

        # retrieves the message list of recipients
        message_recipients_list = message.get_recipients_list()



        # TENHO DE OBTER DA SESSAO OS SEGUINTES VALORES
        # 1. tipo de sessao smtp vs esmtp
        # 2. ip do cliente
        # 3. hostname do cliente
        # 4. hostname do servidor
        # 5. id da mensagem (cofirmar que ja deve estar gerado)

        import datetime
        current_datetime = datetime.datetime.utcnow()
        current_datetime_string = current_datetime.strftime("%a, %d %b %Y %H:%M:%S +0000 (UTC)")

        # creates the mime message structure for message manipulation
        # and reads the current message contents
        message_mime = format_mime_plugin.create_message({})
        message_mime.read_simple(message_contents)
        message_mime.set_header("Message-ID", "<2f3501cc3680$1e5baca0$5b1305e0$@mail.sender.com>")
        message_mime.set_header("Received", "from 188.81.141.175 (bl16-141-175.dsl.telepac.pt [188.81.141.175])\r\n\
        by mail.sender.com with ESMTP id 2f3501cc3680$1e5baca0$5b1305e0$;\r\n" + current_datetime_string)





        # retrieves the re-parsed contents
        message_contents = message_mime.get_value()

        # creates the domain recipients map for the message
        # recipients list
        domain_recipients_map = self._get_domain_recipients_map(message_recipients_list)

        # opens the smtp client
        smtp_client.open({})

        # opens the dns client
        dns_client.open({})

        try:
            # iterates over all the domain in the domain
            # recipients map
            for domain, recipients_list in domain_recipients_map.items():
                # sends the email using the given clients, for the given domain
                # and using the given message information
                self._send_email(smtp_client, dns_client, domain, message_sender, recipients_list, message_contents)
        finally:
            # closes the dns client
            dns_client.close({})

            # closes the smtp client
            smtp_client.close({})

    def _get_domain_recipients_map(self, recipients_list):
        """
        Retrieves a map associating the domain to the
        list of recipients of the domain.

        @type recipients_list: List
        @param recipients_list: The list o recipients to be processed.
        @rtype: Dictionary
        @return: The map associating the domain to the
        list of recipients of the domain.
        """

        # creates the domain recipients map
        domain_recipients_map = {}

        # iterates over all the recipients in the recipients
        # list
        for recipient in recipients_list:
            # splits the recipient to retrieve the user
            # and the domain
            _user, domain = recipient.split("@")

            # in case the domain is not defined in
            # the domain recipients map
            if not domain in domain_recipients_map:
                # creates a list for the domain in the
                # domain recipients map
                domain_recipients_map[domain] = []

            # adds the recipient to the list of recipients
            # for the current domain
            domain_recipients_map[domain].append(recipient)

        # returns the domain recipients map
        return domain_recipients_map

    def _send_email(self, smtp_client, dns_client, domain, message_sender, recipients_list, message_contents):
        """
        Sends an email using the given system clients, for the given
        domain and using the given message information.

        @type smtp_client: SmtpClient
        @param smtp_client: The smtp client to be used for sending the email.
        @type dns_client: DnsClient
        @param dns_client: The dns client to be for mx resource resolution.
        @type domain: String
        @param domain: The domain server of the target smtp server.
        @type message_sender: String
        @param message_sender: The message sender field.
        @type recipients_list: List
        @param recipients_list: The list of recipient fields.
        @type message_contents: String
        @param message_contents: The contents of the message to be sent.
        """

        # creates the domain query
        domain_query = (domain, MX_VALUE, IN_VALUE)

        try:
            # resolves the queries and retrieves the result
            response = dns_client.resolve_queries("8.8.8.8", 53, (domain_query,))
        except:
            # raises the host resolution error
            raise main_service_smtp_relay_message_handler_exceptions.HostResolutionError("problem while resolving domain: " + domain)

        # in case no answers are retrieved
        if not response.answers:
            # raises the host resolution error
            raise main_service_smtp_relay_message_handler_exceptions.HostResolutionError("could not resolve domain mx value: " + domain)

        # retrieves the hostname
        hostname = response.answers[0][4][1]

        # send the email to the host
        smtp_client.send_mail(hostname, SMTP_PORT, message_sender, recipients_list, message_contents, {})
