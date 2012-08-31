#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system
import colony.libs.quote_util

import exceptions

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

REQUEST_TIMEOUT_VALUE = "request_timeout"
""" The request timeout value """

DEFAULT_API_VERSION = "64.0"
""" The default paypal api version """

BASE_REST_URL = "http://api-3t.paypal.com/nvp"
""" The base rest url to be used """

BASE_REST_SECURE_URL = "https://api-3t.paypal.com/nvp"
""" The base rest secure url to be used """

BASE_SANDBOX_REST_URL = "http://api-3t.sandbox.paypal.com/nvp"
""" The base sandbox rest url to be used """

BASE_SANDBOX_REST_SECURE_URL = "https://api-3t.sandbox.paypal.com/nvp"
""" The base sandbox rest secure url to be used """

BASE_WEB_URL = "http://www.paypal.com/webscr"
""" The base web url to be used """

BASE_WEB_SECURE_URL = "https://www.paypal.com/webscr"
""" The base web secure url to be used """

BASE_SANDBOX_WEB_URL = "http://www.sandbox.paypal.com/webscr"
""" The base sandbox web url to be used """

BASE_SANDBOX_WEB_SECURE_URL = "https://www.sandbox.paypal.com/webscr"
""" The base sandbox web secure url to be used """

DEFAULT_REQUEST_TIMEOUT = 60
""" The default request timeout """

class ApiPaypal(colony.base.system.System):
    """
    The api paypal class.
    """

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given api attributes.

        @type api_attributes: Dictionary
        @param api_attributes: The api attributes to be used.
        @type open_client: bool
        @param open_client: If the client should be opened.
        @rtype: OpenidClient
        @return: The created client.
        """

        # retrieves the client http plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the paypal structure (if available)
        paypal_structure = api_attributes.get("paypal_structure", None)

        # creates a new paypal client with the given options
        paypal_client = PaypalClient(client_http_plugin, paypal_structure)

        # returns the paypal client
        return paypal_client

class PaypalClient:
    """
    The class that represents a paypal client connection.
    """

    REFUND_TYPE_FULL = "Full"
    """ The full refund type """

    REFUND_TYPE_PARTIAL = "Partial"
    """ The partial refund type """

    REFUND_TYPE_EXTERNAL_DISPUTE = "ExternalDispute"
    """ The external dispute refund type """

    REFUND_TYPE_OTHER = "Other"
    """ The other refund type """

    REFUND_SOURCE_ANY = "any"
    """ The any refund source """

    REFUND_SOURCE_DEFAULT = "default"
    """ The default refund source """

    REFUND_SOURCE_INSTANT = "instant"
    """ The instant refund source """

    REFUND_SOURCE_ECHECK = "echeck"
    """ The echeck refund source """

    client_http_plugin = None
    """ The client http plugin """

    paypal_structure = None
    """ The paypal structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, client_http_plugin = None, paypal_structure = None):
        """
        Constructor of the class.

        @type client_http_plugin: MainClientHttpPlugin
        @param client_http_plugin: The client http plugin.
        @type paypal_structure: PaypalStructure
        @param paypal_structure: The paypal structure.
        """

        self.client_http_plugin = client_http_plugin
        self.paypal_structure = paypal_structure

    def open(self):
        """
        Opens the paypal client.
        """

        pass

    def close(self):
        """
        Closes the paypal client.
        """

        # in case an http client is defined closes it
        # (flushing its internal structures
        if self.http_client: self.http_client.close({})

    def generate_paypal_structure(self, username, password, signature, api_version = DEFAULT_API_VERSION, set_structure = True):
        """
        Generates the paypal structure for the given arguments.

        @type username: String
        @param username: The username.
        @type password: String
        @param passwird: The password.
        @type country: String
        @param country: The signature value unique by client.
        @type api_version: String
        @param api_version: The version of the api being used.
        @type set_structure: bool
        @param set_structure: If the structure should be
        set in the paypal client.
        @rtype: PaypalStructure
        @return: The generated paypal structure.
        """

        # creates a new paypal structure
        paypal_structure = PaypalStructure(username, password, signature, api_version)

        # in case the structure is meant to be set
        # sets it accordingly (in the current object)
        if set_structure: self.set_paypal_structure(paypal_structure)

        # returns the paypal structure
        return paypal_structure

    def do_direct_payment(self, ip_address, amount, card, payer, address, order = {}, shipping_address = {}):
        """
        Directly performs payment by issuing a request to paypal with the specified information.

        This method is synchronous, and paypal will directly reply with the information stating
        if the payment was processed correctly or not (an exception will be raised in case it
        isn't).

        @type ip_address: String
        @param ip_address: The ip address from where the customer performed the payment.
        @type amount: float
        @param amount: The amount being paid.
        @type card: Dictionary
        @param card: The card to be used to pay for the order.
        @type payer: Dictionary
        @param payer: The payer that is to pay the order.
        @type order: Dictionary
        @param order: Map with details about the order being paid (lines and totals).
        @type shipping_address: Dictionary
        @param shipping_address: The address details of where the order is to be shipped.
        @rtype: Dictionary
        @return: The paypal response data.
        """

        # sets the retrieval url, this is always the same
        # value the command control is on the parameters
        retrieval_url = BASE_SANDBOX_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the base parameters, required for the authentication
        # of the request to be executed
        self._set_base_parameters(parameters)

        # unpacks the provided structures
        order_lines = order.get("lines", [])

        # sets the global wide parameters for the current request
        # they don't depend on any sequence
        parameters["METHOD"] = "DoDirectPayment"
        parameters["PAYMENTACTION"] = "Sale"
        parameters["IPADDRESS"] = ip_address
        parameters["RETURNFMFDETAILS"] = "1"

        # sets the payment details in the parameters map
        parameters["AMT"] = "%.2f" % amount
        if "currency" in order: parameters["CURRENCYCODE"] = order["currency"]
        if "item" in order: parameters["ITEMAMT"] = "%.2f" % order["item"]
        if "shipping" in order: parameters["SHIPPINGAMT"] = "%.2f" % order["shipping"]
        if "tax" in order: parameters["TAXAMT"] = "%.2f" % order["tax"]
        if "invoice_number" in order: parameters["INVNUM"] = order["invoice_number"]

        # calculates the number of order lines
        number_order_lines = len(order_lines)

        # sets the order line structure values in the parameters map
        for order_line_index in range(number_order_lines):
            # retrieves the order line
            order_line = order_lines[order_line_index]

            # sets the order line attributes in the parameters
            if "name" in order_line: parameters["L_NAME%d" % order_line_index] = order_line["name"]
            if "description" in order_line: parameters["L_DESC%d" % order_line_index] = order_line["description"]
            if "amount" in order_line: parameters["L_AMT%d" % order_line_index] = "%.2f" % order_line["amount"]
            if "code" in order_line: parameters["L_NUMBER%d" % order_line_index] = order_line["code"]
            if "quantity" in order_line: parameters["L_QTY%d" % order_line_index] = order_line["quantity"]
            if "tax" in order_line: parameters["L_TAXAMT%d" % order_line_index] = "%.2f" % order_line["tax"]

        # sets the card structure values in the parameters map
        parameters["ACCT"] = card["number"]
        parameters["EXPDATE"] = card["expiration"]
        if "type" in card: parameters["CREDITCARDTYPE"] = card["type"]
        if "cvv2" in card: parameters["CVV2"] = card["cvv2"]
        if "start_date" in card: parameters["STARTDATE"] = card["start_date"]
        if "issue_number" in card: parameters["ISSUENUMBER"] = card["issue_number"]

        # sets the buyer structure values in the parameters map
        parameters["FIRSTNAME"] = payer["first_name"]
        parameters["LASTNAME"] = payer["last_name"]
        if "email" in payer: parameters["EMAIL"] = payer["email"]

        # sets the address structure values in the parameters map
        parameters["STREET"] = address["street"]
        parameters["CITY"] = address["city"]
        parameters["STATE"] = address["state"]
        parameters["COUNTRYCODE"] = address["country"]
        parameters["ZIP"] = address["zip_code"]
        if "phone_number" in address: parameters["SHIPTOPHONENUM"] = address["phone_number"]

        # sets the shipping address structure values in the parameters map
        if shipping_address:
            parameters["SHIPTONAME"] = shipping_address["name"]
            parameters["SHIPTOSTREET"] = shipping_address["street_name"]
            parameters["SHIPTOCITY"] = shipping_address["city"]
            parameters["SHIPTOSTATE"] = shipping_address["state"]
            parameters["SHIPTOZIP"] = shipping_address["zip_code"]
            parameters["SHIPTOCOUNTRY"] = shipping_address["country"]
            if "phone_number" in shipping_address: parameters["SHIPTOPHONENUM"] = shipping_address["phone_number"]

        # fetches the retrieval url with the given parameters retrieving
        # the resulting key value pairs to be decoded and then parses
        # them as a "normal" query string
        response_text = self._fetch_url(retrieval_url, parameters)
        data = self._parse_query_string(response_text)

        # checks the current data map for error in the previously
        # defined attribute names
        self._check_paypal_errors(data)

        # retrieves the various attributes from the data to be used
        # to update the current paypal structure
        transaction_id = data["TRANSACTIONID"]

        # updates the current paypal structure according to the attributes
        # that have just been retrieved from the data structure
        self.paypal_structure.transaction_id = transaction_id

        # returns the response data
        return data

    def refund_transaction(self, transaction_id, refund_type = REFUND_TYPE_FULL, refund_source = REFUND_SOURCE_INSTANT, amount = None, currency_code = None, refund_item_details = None, note = None):
        """
        Refunds the specified transaction, with the specified amount and refund source.

        This method is synchronous, and paypal will directly reply with the information stating
        if the payment was processed correctly or not (an exception will be raised in case it
        isn't).

        @type transaction_id: String
        @param transaction_id: The unique identifier of the paypal transaction that is to be
        refunded.
        @type refund_type: String
        @param refund_type: The type of refund to be performed: Full, Partial, ExternalDispute,
        Other).
        @type refund_source: String
        @param refund_source: The source used to refund the transaction: any, default (source
        will be retrieved from merchant configuration), instant (balance will be used), echeck.
        @type amount: float
        @param amount: The amount to be refunded in case this is a partial refund (otherwise
        the amount should not be specified).
        @type currency_code: String
        @param currency_code: The code of the currency in which to perform the refund.
        @type refund_item_details: String
        @param refund_item_details: Details about the item being refunded.
        @type note: String
        @param note: Optional notes about the refund.
        @rtype: Dictionary
        @return: The paypal response data.
        """

        # sets the retrieval url, this is always the same
        # value the command control is on the parameters
        retrieval_url = BASE_SANDBOX_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the base parameters, required for the authentication
        # of the request to be executed
        self._set_base_parameters(parameters)

        # sets the refund details in the parameters map
        parameters["METHOD"] = "RefundTransaction"
        parameters["TRANSACTIONID"] = transaction_id
        parameters["REFUNDTYPE"] = refund_type
        parameters["REFUNDSOURCE"] = refund_source
        if amount: parameters["AMT"] = "%.2f" % amount
        if currency_code: parameters["CURRENCYCODE"] = currency_code
        if refund_item_details: parameters["REFUNDITEMDETAILS"] = refund_item_details
        if note: parameters["NOTE"] = note

        # fetches the retrieval url with the given parameters retrieving
        # the resulting key value pairs to be decoded and then parses
        # them as a "normal" query string
        response_text = self._fetch_url(retrieval_url, parameters)
        data = self._parse_query_string(response_text)

        # checks the current data map for error in the previously
        # defined attribute names
        self._check_paypal_errors(data)

        # returns the data
        return data

    def set_express_checkout(self, amount, return_url, cancel_url, currency = "EUR", payment_action = "Sale", items = []):
        # sets the retrieval url, this is always the same
        # value the command control is on the parameters
        retrieval_url = BASE_SANDBOX_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the base parameters, required for the authentication
        # of the request to be executed
        self._set_base_parameters(parameters)

        # sets the global wide parameters for the current request
        # they don't depend on any sequence
        parameters["METHOD"] = "SetExpressCheckout"
        parameters["PAYMENTREQUEST_0_AMT"] = "%.2f" % amount
        parameters["RETURNURL"] = return_url
        parameters["CANCELURL"] = cancel_url
        parameters["PAYMENTREQUEST_0_CURRENCYCODE"] = currency
        parameters["PAYMENTREQUEST_0_PAYMENTACTION"] = payment_action

        # resets the index counter value to the start value
        # and then iterates over all the items to set the appropriate
        # value into the parameters map
        index = 0
        for item in items:
            # sets the item parameters in the map and then increments
            # the counter by one position
            parameters["L_PAYMENTREQUEST_0_NAME%d" % index] = item["name"]
            parameters["L_PAYMENTREQUEST_0_DESC%d" % index] = item["description"]
            parameters["L_PAYMENTREQUEST_0_AMT%d" % index] = item["cost"]
            index += 1

        # fetches the retrieval url with the given parameters retrieving
        # the resulting key value pairs to be decoded and then parses
        # them as a "normal" query string
        response_text = self._fetch_url(retrieval_url, parameters)
        data = self._parse_query_string(response_text)

        # checks the current data map for error in the previously
        # defined attribute names
        self._check_paypal_errors(data)

        # retrieves the various attributes from the data to be used
        # to update the current paypal structure
        token = data["TOKEN"]

        # updates the current paypal structure according to the attributes
        # that have just been retrieved from the data structure
        self.paypal_structure.token = token

    def get_express_checkout_url(self):
        """
        Retrieves the url used to redirect the user to the payment page
        in the paypal api in the express checkout mode.

        @rtype: String
        @return: the url used to redirect the user to the payment page
        in the paypal api in the express checkout mode.
        """

        # sets the retrieval url, this is always the same
        # value the command control is on the parameters
        retrieval_url = BASE_SANDBOX_WEB_SECURE_URL

        # start the parameters map
        parameters = {}

        # populates the parameters map with the required parameters
        # for the generation of the url
        parameters["cmd"] = "_express-checkout"
        parameters["token"] = self.paypal_structure.token

        # creates the express checkout url from the parameters
        express_checkout_url = self._build_url(retrieval_url, parameters)

        # returns the express checkout url
        return express_checkout_url

    def get_paypal_structure(self):
        """
        Retrieves the paypal structure.

        @rtype: PaypalStructure
        @return: The paypal structure.
        """

        return self.paypal_structure

    def set_paypal_structure(self, paypal_structure):
        """
        Sets the paypal structure.

        @type paypal_structure: PaypalStructure
        @param paypal_structure: The paypal structure.
        """

        self.paypal_structure = paypal_structure

    def _set_base_parameters(self, parameters):
        """
        Sets the base paypal rest request parameters
        in the parameters map.

        These are considered to be the base values used for the
        authentication of the request.

        @type parameters: Dictionary
        @param parameters: The parameters map to be used in setting
        the base parameters.
        """

        # sets the user the password and the signature values
        # these are considered to be the base values and are
        # used to authenticate the request
        parameters["USER"] = self.paypal_structure.username
        parameters["PWD"] = self.paypal_structure.password
        parameters["SIGNATURE"] = self.paypal_structure.signature
        parameters["VERSION"] = self.paypal_structure.api_version

    def _fetch_url(self, url, parameters = None, method = GET_METHOD_VALUE):
        """
        Fetches the given url for the given parameters and using the given method.

        @type url: String
        @param url: The url to be fetched.
        @type parameters: Dictionary
        @param parameters: The parameters to be used the fetch.
        @type method: String
        @param method: The method to be used in the fetch.
        @rtype: String
        @return: The fetched data.
        """

        # in case parameters is not defined
        # creates a new parameters map
        if not parameters: parameters = {}

        # retrieves the http client
        http_client = self._get_http_client()

        # fetches the url retrieving the http response
        http_response = http_client.fetch_url(url, method, parameters, content_type_charset = DEFAULT_CHARSET)

        # retrieves the contents from the http response
        contents = http_response.received_message

        # returns the contents
        return contents

    def _build_url(self, base_url, parameters):
        """
        Builds the url for the given url and parameters.

        @type url: String
        @param url: The base url to be used.
        @type parameters: Dictionary
        @param parameters: The parameters to be used for url construction.
        @rtype: String
        @return: The built url for the given parameters.
        """

        # retrieves the http client
        http_client = self._get_http_client()

        # build the url from the base urtl
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the url
        return url

    def _check_paypal_errors(self, data):
        """
        Checks the given data for paypal errors.

        @type data: String
        @param data: The data to be checked for paypal errors.
        @rtype: bool
        @return: The result of the data error check.
        """

        # retrieves the message value and returns immediately
        # in case it's not defined (no error in request)
        message = data.get("L_SHORTMESSAGE0", None)
        if not message: return

        # tries to retrieve the long message to be used for more
        # in depth diagnostics of the problem
        long_message = data.get("L_LONGMESSAGE0", None)

        # raises the paypal api error
        raise exceptions.PaypalApiError("error in request: " + message, long_message)

    def _parse_query_string(self, query_string):
        """
        Parses the query string value, creating a map
        containing the various key value pair associations.

        @type query_string: String
        @param query_string: The query string value to be
        decoded and parsed into the key values map.
        @rtype: Dictionary
        @return: The map resulting from the parsing of the
        provided query string value.
        """

        # creates the response map
        fields_map = {}

        # splits the field value pairs
        field_value_pairs = query_string.split("&")

        # iterates over each of the field value pairs
        # to create the proper map associations
        for field_value_pair in field_value_pairs:
            # retrieves the field and value from the pair
            field, value = field_value_pair.split("=")

            # sets the field and value in the map
            fields_map[field] = colony.libs.quote_util.unquote(value)

        # returns the fields map
        return fields_map

    def _get_http_client(self):
        """
        Retrieves the http client currently in use (in case it's created)
        if not created creates the http client.

        @rtype: HttpClient
        @return: The retrieved http client.
        """

        # in case no http client exists
        if not self.http_client:
            # defines the client parameters
            client_parameters = {
                CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET
            }

            # creates the http client
            self.http_client = self.client_http_plugin.create_client(client_parameters)

            # defines the open parameters
            open_parameters = {
                REQUEST_TIMEOUT_VALUE : DEFAULT_REQUEST_TIMEOUT
            }

            # opens the http client
            self.http_client.open(open_parameters)

        # returns the http client
        return self.http_client

class PaypalStructure:
    """
    The paypal structure class used to store
    the various paypal dependent attributes
    placed there over the course of a session.
    """

    username = None
    """ The username """

    password = None
    """ The password """

    signature = None
    """ The signature value unique by client """

    api_version = None
    """ The version of the api being used """

    token = None
    """ The current token id value used in the session """

    transaction_id = None
    """ The current transaction id value used in the session """

    def __init__(self, username, password, signature, api_version = DEFAULT_API_VERSION):
        """
        Constructor of the class.

        @type username: String
        @param username: The username.
        @type password: String
        @param password: The password.
        @type signature: String
        @param signature: The signature value unique by client.
        @type api_version: String
        @param api_version: The version of the api being used.
        """

        self.username = username
        self.password = password
        self.signature = signature
        self.api_version = api_version

    def get_username(self):
        """
        Retrieves the username.

        @rtype: String
        @return: The username.
        """

        return self.username

    def set_username(self, username):
        """
        Sets the username.

        @type username: String
        @param username: The username.
        """

        self.username = username

    def get_password(self):
        """
        Retrieves the password.

        @rtype: String
        @return: The password.
        """

        return self.password

    def set_password(self, password):
        """
        Sets the password.

        @type password: String
        @param password: The password.
        """

        self.password = password

    def get_signature(self):
        """
        Retrieves the signature.

        @rtype: String
        @return: The signature.
        """

        return self.signature

    def set_signature(self, signature):
        """
        Sets the signature.

        @type signature: String
        @param signature: The signature.
        """

        self.signature = signature

    def get_api_version(self):
        """
        Retrieves the api version.

        @rtype: String
        @return: The api version.
        """

        return self.api_version

    def set_api_version(self, api_version):
        """
        Sets the api version.

        @type api_version: String
        @param api_version: The api version.
        """

        self.api_version = api_version

    def get_token(self):
        """
        Retrieves the token.

        @rtype: String
        @return: The token.
        """

        return self.token

    def set_token(self, token):
        """
        Sets the token.

        @type token: String
        @param token: The token.
        """

        self.token = token

    def get_transaction_id(self):
        """
        Retrieves the transaction id.

        @rtype: String
        @return: The transaction id.
        """

        return self.transaction_id

    def set_transaction_id(self, transaction_id):
        """
        Sets the transaction id.

        @type transaction_id: String
        @param transaction_id: The transaction id.
        """

        self.transaction_id = transaction_id
